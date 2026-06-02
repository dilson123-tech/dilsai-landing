from io import BytesIO

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import ChatRequest, ChatResponse
from app.services.knowledge import find_knowledge_context
from app.services.llm import generate_study_answer


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

SCANNED_PDF_OCR_MAX_PAGES = 3
SCANNED_PDF_OCR_DPI = 220

app = FastAPI(
    title=settings.app_name,
    description="API do DilsAI Estudos — IA de estudos com precisão, modos e resposta segura.",
    version=settings.app_version,
)

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

    image_types = {"image/png", "image/jpeg", "image/jpg", "image/webp"}

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
        detail="Tipo de arquivo não suportado. Use PDF textual ou imagem PNG/JPG/JPEG/WEBP.",
    )


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    knowledge = find_knowledge_context(payload)
    answer = await generate_study_answer(payload=payload, settings=settings)
    has_user_context = bool(payload.context and payload.context.strip())
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
