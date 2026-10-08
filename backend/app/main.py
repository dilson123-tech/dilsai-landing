import re
from io import BytesIO

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.schemas import ChatRequest, ChatResponse, StudyLevel, StudyTopic
from app.services.knowledge import find_knowledge_context
from app.services.llm import ImageAnswerUnavailable, generate_image_study_answer, generate_study_answer
from app.services.rate_limit import InMemoryRateLimiter, get_client_identifier


def extract_user_material_source(context: str | None) -> tuple[str | None, str | None]:
    if not context or not context.strip():
        return None, None

    title = "Material enviado pelo aluno"
    source_type = "user_uploaded_text"

    for raw_line in context.splitlines():
        line = raw_line.strip()
        lower = line.lower()

        if lower.startswith("arquivo enviado pelo aluno:"):
            candidate = line.split(":", 1)[1].strip()
            if candidate:
                title = candidate
            break

    context_lower = context.lower()
    title_lower = title.lower()

    if (
        "pdf escaneado" in context_lower
        or "ocr de pdf" in context_lower
        or "pdf convertido para imagem" in context_lower
    ):
        source_type = "user_uploaded_pdf_ocr"
    elif (
        title_lower.endswith(".pdf")
        or "pdf textual extraído" in context_lower
        or "pdf textual extraido" in context_lower
    ):
        source_type = "user_uploaded_pdf_text"
    elif (
        title_lower.endswith(".png")
        or title_lower.endswith(".jpg")
        or title_lower.endswith(".jpeg")
        or title_lower.endswith(".webp")
        or "ocr de imagem" in context_lower
    ):
        source_type = "user_uploaded_image_ocr"
    elif title_lower.endswith(".md"):
        source_type = "user_uploaded_markdown"
    elif title_lower.endswith(".txt"):
        source_type = "user_uploaded_text"

    return title, source_type


settings = get_settings()
rate_limiter = InMemoryRateLimiter()

SCANNED_PDF_OCR_MAX_PAGES = 3

IMAGE_OCR_MAX_SIDE = 800
# Imagem para a IA de visão: mais legível que a do OCR, mas com payload controlado.
# Com detail "high" a OpenAI reduz a imagem para lado menor 768 px, então 1280 px já entrega
# a mesma resolução final que 1600 px, com upload e compressão mais rápidos.
IMAGE_VISION_MAX_SIDE = 1280
IMAGE_VISION_FALLBACK_SIDE = 1024
# OCR de apoio não pode segurar a resposta: a IA de visão lê a foto mesmo sem ele.
IMAGE_VISION_OCR_TIMEOUT_SECONDS = 6
IMAGE_VISION_MAX_ENCODED_BYTES = 1_500_000
# Aceita "Confiança: alta", "**Confiança:** média", "Confiança - baixa" etc.; vale a primeira ocorrência.
IMAGE_CONFIDENCE_PATTERN = re.compile(r"confian[çc]a\W{0,6}(alta|m[ée]dia|baixa)", re.IGNORECASE)
IMAGE_CONFIDENCE_NOTICES = {
    "alta": "Resposta gerada pela foto. Confira se corresponde à sua questão.",
    "media": "Resposta provável gerada pela foto. Confira antes de usar.",
    "baixa": "Não consegui ler a foto com segurança. Tire outra foto mais perto.",
}
IMAGE_CONFIDENCE_MISSING_LINE = (
    "Confiança: média — confira o enunciado e as alternativas na foto antes de usar esta resposta."
)
IMAGE_UPLOAD_MAX_BYTES = 5_000_000
IMAGE_MAX_PIXELS = 40_000_000
IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}
SCANNED_PDF_OCR_DPI = 220

app = FastAPI(
    title=settings.app_name,
    description="API do DilsAI Estudos — IA de estudos com precisão, modos e resposta segura.",
    version=settings.app_version,
)



def _expensive_route_limit(path: str) -> tuple[str | None, int | None]:
    if path == "/api/v1/chat":
        return "chat", settings.rate_limit_chat_per_minute

    if path in ("/api/v1/materials/extract-text", "/api/v1/materials/solve-image"):
        return "materials", settings.rate_limit_material_per_minute

    return None, None


@app.middleware("http")
async def apply_expensive_route_rate_limit(request: Request, call_next):
    if not settings.rate_limit_enabled or request.method == "OPTIONS":
        return await call_next(request)

    bucket, limit = _expensive_route_limit(request.url.path)

    if bucket and limit is not None:
        client_id = get_client_identifier(request)
        result = rate_limiter.check(
            identifier=client_id,
            bucket=bucket,
            limit=limit,
            window_seconds=settings.rate_limit_window_seconds,
        )

        if not result.allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Limite de uso atingido. Aguarde um pouco antes de tentar novamente.",
                    "rate_limit": {
                        "bucket": bucket,
                        "limit": result.limit,
                        "remaining": result.remaining,
                        "retry_after_seconds": result.retry_after,
                    },
                },
                headers={"Retry-After": str(result.retry_after)},
            )

    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "message": "DilsAI Estudos API está funcionando.",
    }


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }



def _prepare_image_for_ocr(image):
    from PIL import ImageOps

    image = ImageOps.exif_transpose(image)
    original_size = image.size

    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    image.thumbnail((IMAGE_OCR_MAX_SIDE, IMAGE_OCR_MAX_SIDE))

    processed_size = image.size
    return image, original_size, processed_size



def _ocr_scanned_pdf_bytes(data: bytes, max_pages: int = SCANNED_PDF_OCR_MAX_PAGES) -> tuple[str, int]:
    from pdf2image import convert_from_bytes
    import pytesseract

    images = convert_from_bytes(
        data,
        dpi=SCANNED_PDF_OCR_DPI,
        first_page=1,
        last_page=max_pages,
        fmt="png",
    )

    page_texts: list[str] = []

    for index, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image, lang="por+eng")
        clean_text = (text or "").strip()

        if clean_text:
            page_texts.append(f"--- Página {index} OCR ---\n{clean_text}")

    return "\n\n".join(page_texts).strip(), len(images)


@app.post("/api/v1/materials/extract-text")
async def extract_material_text(request: Request) -> dict:
    raw_content_type = request.headers.get("content-type", "")
    content_type = raw_content_type.split(";", 1)[0].strip().lower()
    file_name = request.headers.get("x-file-name", "material")
    data = await request.body()

    max_bytes = 5_000_000

    if not data:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    if len(data) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail="Arquivo muito grande para o upload OCR/PDF simples V1. Use um arquivo menor.",
        )

    text_types = {"text/plain", "text/markdown"}
    image_types = {"image/png", "image/jpeg", "image/jpg", "image/webp"}

    if (
        content_type in text_types
        or file_name.lower().endswith(".txt")
        or file_name.lower().endswith(".md")
    ):
        try:
            extracted_text = data.decode("utf-8").strip()
        except UnicodeDecodeError:
            extracted_text = data.decode("latin-1", errors="replace").strip()

        if not extracted_text:
            raise HTTPException(status_code=400, detail="Não foi possível ler texto do arquivo enviado.")

        return {
            "ok": True,
            "source_type": "text",
            "file_name": file_name,
            "char_count": len(extracted_text),
            "text": extracted_text,
            "notice": "Texto extraído do arquivo enviado pelo aluno.",
            "ocr_page_limit": None,
        }

    if content_type == "application/pdf":
        if not data.startswith(b"%PDF"):
            raise HTTPException(status_code=400, detail="Arquivo não parece ser um PDF válido.")

        try:
            from pypdf import PdfReader

            reader = PdfReader(BytesIO(data))
            page_texts: list[str] = []

            for index, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                clean_text = text.strip()
                if clean_text:
                    page_texts.append(f"--- Página {index} ---\n{clean_text}")

            extracted_text = "\n\n".join(page_texts).strip()

            warning = None
            source_type = "pdf_text"

            if not extracted_text:
                ocr_text, ocr_page_count = _ocr_scanned_pdf_bytes(data)
                extracted_text = ocr_text
                source_type = "pdf_ocr"

                if not extracted_text:
                    warning = (
                        "Não foi possível extrair texto deste PDF nem via OCR inicial. "
                        "O arquivo pode ter baixa qualidade, estar ilegível ou exigir pré-processamento."
                    )
                else:
                    warning = (
                        "PDF sem texto digital extraível. O conteúdo foi obtido por OCR inicial "
                        f"em {ocr_page_count} página(s), com limite operacional de "
                        f"{SCANNED_PDF_OCR_MAX_PAGES} página(s). OCR pode conter erros."
                    )

            return {
                "status": "success",
                "file_name": file_name,
                "source_type": source_type,
                "page_count": len(reader.pages),
                "char_count": len(extracted_text),
                "text": extracted_text,
                "warning": warning,
                "ocr_engine": "tesseract" if source_type == "pdf_ocr" else None,
                "ocr_languages": "por+eng" if source_type == "pdf_ocr" else None,
                "ocr_processed_pages": ocr_page_count if source_type == "pdf_ocr" else None,
                "ocr_page_limit": SCANNED_PDF_OCR_MAX_PAGES if source_type == "pdf_ocr" else None,
            }

        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Não foi possível extrair texto do PDF: {str(exc)[:180]}",
            ) from exc

    if content_type in image_types:
        try:
            from PIL import Image
            import pytesseract
            from pytesseract import TesseractNotFoundError

            image = Image.open(BytesIO(data))
            image, original_size, processed_size = _prepare_image_for_ocr(image)
            text = pytesseract.image_to_string(image, lang="por+eng")
            extracted_text = (text or "").strip()

            warning = None
            if not extracted_text:
                warning = (
                    "Não foi possível extrair texto legível desta imagem. "
                    "A qualidade pode estar baixa, sem contraste ou sem texto."
                )

            return {
                "status": "success",
                "file_name": file_name,
                "source_type": "image_ocr",
                "page_count": None,
                "char_count": len(extracted_text),
                "text": extracted_text,
                "warning": warning,
                "ocr_engine": "tesseract",
                "ocr_languages": "por+eng",
                "ocr_processed_pages": 1,
                "ocr_page_limit": None,
                "image_original_size": list(original_size),
                "image_processed_size": list(processed_size),
            }

        except TesseractNotFoundError as exc:
            raise HTTPException(
                status_code=503,
                detail="OCR indisponível: Tesseract não está instalado no sistema.",
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Não foi possível executar OCR na imagem: {str(exc)[:180]}",
            ) from exc

    raise HTTPException(
        status_code=415,
        detail="Tipo de arquivo não suportado. Use TXT, MD, PDF textual ou imagem PNG/JPG/JPEG/WEBP.",
    )


class InvalidImageError(ValueError):
    pass


def _prepare_image_for_vision(data: bytes) -> dict:
    from PIL import Image, ImageOps

    try:
        with Image.open(BytesIO(data)) as probe:
            width, height = probe.size
            probe.verify()
    except Exception as exc:
        raise InvalidImageError("Arquivo não parece ser uma imagem válida.") from exc

    if width * height > IMAGE_MAX_PIXELS:
        raise InvalidImageError("Imagem com resolução grande demais. Tire a foto com resolução menor.")

    try:
        image = Image.open(BytesIO(data))
        image = ImageOps.exif_transpose(image)
        original_size = image.size

        if image.mode != "RGB":
            image = image.convert("RGB")

        encoded = b""
        for max_side, quality in (
            (IMAGE_VISION_MAX_SIDE, 82),
            (IMAGE_VISION_MAX_SIDE, 72),
            (IMAGE_VISION_FALLBACK_SIDE, 70),
        ):
            candidate = image.copy()
            candidate.thumbnail((max_side, max_side))
            buffer = BytesIO()
            candidate.save(buffer, format="JPEG", quality=quality, optimize=True)
            encoded = buffer.getvalue()
            if len(encoded) <= IMAGE_VISION_MAX_ENCODED_BYTES:
                break
    except Exception as exc:
        raise InvalidImageError("Não foi possível processar a imagem enviada.") from exc

    return {
        "image": candidate,
        "jpeg": encoded,
        "original_size": original_size,
        "processed_size": candidate.size,
    }


def _ocr_hint_for_vision(image) -> str:
    """OCR rápido só como apoio para a IA de visão. Falhas são ignoradas."""
    try:
        import pytesseract

        ocr_image = image.copy()
        ocr_image.thumbnail((IMAGE_OCR_MAX_SIDE, IMAGE_OCR_MAX_SIDE))
        return (pytesseract.image_to_string(ocr_image, lang="por+eng", timeout=IMAGE_VISION_OCR_TIMEOUT_SECONDS) or "").strip()
    except Exception:
        return ""


def _image_answer_confidence(answer: str) -> str | None:
    match = IMAGE_CONFIDENCE_PATTERN.search(answer or "")
    if not match:
        return None
    value = match.group(1).lower()
    return "media" if value in {"média", "media"} else value


def _enum_header(request: Request, name: str, enum_cls, default):
    value = (request.headers.get(name) or "").strip()
    try:
        return enum_cls(value) if value else default
    except ValueError:
        return default


@app.post("/api/v1/materials/solve-image")
async def solve_image_question(request: Request) -> dict:
    raw_content_type = request.headers.get("content-type", "")
    content_type = raw_content_type.split(";", 1)[0].strip().lower()
    data = await request.body()

    if not data:
        raise HTTPException(status_code=400, detail="Imagem vazia. Tire outra foto e tente novamente.")

    if len(data) > IMAGE_UPLOAD_MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Imagem muito grande. Envie uma foto de até 5 MB.",
        )

    if content_type not in IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Tipo de imagem não suportado. Use JPEG, PNG ou WEBP.",
        )

    try:
        prepared = await run_in_threadpool(_prepare_image_for_vision, data)
    except InvalidImageError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    topic = _enum_header(request, "x-study-topic", StudyTopic, StudyTopic.geral)
    level = _enum_header(request, "x-study-level", StudyLevel, StudyLevel.geral)
    ocr_hint = await run_in_threadpool(_ocr_hint_for_vision, prepared["image"])

    try:
        answer = await run_in_threadpool(
            generate_image_study_answer,
            prepared["jpeg"],
            settings,
            topic,
            level,
            ocr_hint,
        )
    except ImageAnswerUnavailable as exc:
        detail = (
            "Resolver pela foto está indisponível no momento: a IA de visão não está configurada."
            if exc.reason == "missing_api_key"
            else "Não consegui analisar a foto agora. Tente novamente em instantes ou use \"Ler texto desta foto\"."
        )
        raise HTTPException(status_code=503, detail=detail) from exc

    confidence = _image_answer_confidence(answer)
    if confidence is None:
        # A IA esqueceu a linha de confiança: não tratar a resposta como garantida.
        confidence = "media"
        answer = f"{answer.rstrip()}\n\n{IMAGE_CONFIDENCE_MISSING_LINE}"

    return {
        "ok": True,
        "status": "success",
        "source_type": "image_vision",
        "response": answer,
        "answer": answer,
        "notice": IMAGE_CONFIDENCE_NOTICES[confidence],
        # "alta" | "media" | "baixa". Com baixa a IA não marca alternativa e pede nova foto.
        "confidence": confidence,
        "can_answer": confidence != "baixa",
        "needs_better_photo": confidence == "baixa",
        # OCR fraco não é erro aqui: a IA de visão leu a foto diretamente.
        "warning": None,
        "ocr_weak": len(ocr_hint) < 20,
        "model": settings.vision_model,
        "topic": topic.value,
        "level": level.value,
        "ocr_char_count": len(ocr_hint),
        "image_original_size": list(prepared["original_size"]),
        "image_processed_size": list(prepared["processed_size"]),
        "image_bytes": len(prepared["jpeg"]),
    }


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    knowledge = find_knowledge_context(payload)
    has_user_context = bool(payload.context and payload.context.strip())

    # Academic Accuracy V1:
    # Em Fonte Segura, sem material do aluno, não aceitar base interna fraca.
    # Produto real precisa preferir pedir contexto a responder com fonte errada.
    weak_internal_source = (
        payload.mode == "fonte_segura"
        and not has_user_context
    )

    if weak_internal_source:
        return ChatResponse(
            response=(
                "Não encontrei material suficiente para responder com segurança no Modo Fonte Segura.\n\n"
                "Para evitar resposta inventada ou fonte fraca, envie o print completo da questão, "
                "as alternativas, o trecho da apostila, PDF ou contexto da aula.\n\n"
                "Ponto de atenção:\n"
                "Fonte Segura só deve responder quando houver base confiável."
            ),
            mode=payload.mode,
            topic=payload.topic,
            used_context=False,
            confidence="context_required",
            safety_notice="Modo Fonte Segura exige material confiável do aluno ou base interna forte.",
            source_title=None,
            source_path=None,
            source_type=None,
            source_score=None,
        )

    answer = await generate_study_answer(payload=payload, settings=settings)
    user_source_title, user_source_type = extract_user_material_source(payload.context)
    used_context = has_user_context or knowledge.found
    use_user_source = has_user_context and bool(user_source_title)
    use_internal_source = knowledge.found and not has_user_context

    safety_notice = None
    confidence = "general"

    if payload.mode == "fonte_segura":
        confidence = "context_required"
        if not used_context:
            safety_notice = "Modo Fonte Segura exige contexto/material para resposta precisa."
    elif used_context:
        confidence = "context_assisted"

    return ChatResponse(
        response=answer,
        mode=payload.mode,
        topic=payload.topic,
        used_context=used_context,
        confidence=confidence,
        safety_notice=safety_notice,
        source_title=user_source_title if use_user_source else knowledge.title if use_internal_source else None,
        source_path=None if use_user_source else knowledge.source_path if use_internal_source else None,
        source_type=user_source_type if use_user_source else "internal_markdown" if use_internal_source else None,
        source_score=None if use_user_source else knowledge.score if use_internal_source else None,
    )


@app.post("/chat", response_model=ChatResponse)
async def legacy_chat(payload: ChatRequest) -> ChatResponse:
    return await chat(payload)
