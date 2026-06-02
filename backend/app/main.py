from io import BytesIO

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import ChatRequest, ChatResponse
from app.services.knowledge import find_knowledge_context
from app.services.llm import generate_study_answer

settings = get_settings()

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


@app.post("/api/v1/materials/extract-text")
async def extract_material_text(request: Request) -> dict:
    content_type = request.headers.get("content-type", "")
    file_name = request.headers.get("x-file-name", "material.pdf")

    if "application/pdf" not in content_type:
        raise HTTPException(status_code=415, detail="Apenas PDF é aceito neste endpoint.")

    data = await request.body()
    max_bytes = 2_500_000

    if not data:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    if len(data) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail="PDF muito grande para o upload simples V1. Use um arquivo menor.",
        )

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
        if not extracted_text:
            warning = (
                "Não foi possível extrair texto deste PDF. "
                "Ele pode ser escaneado/imagem e exigir OCR em ciclo futuro."
            )

        return {
            "status": "success",
            "file_name": file_name,
            "source_type": "pdf_text",
            "page_count": len(reader.pages),
            "char_count": len(extracted_text),
            "text": extracted_text,
            "warning": warning,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível extrair texto do PDF: {str(exc)[:180]}",
        ) from exc


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    knowledge = find_knowledge_context(payload)
    answer = await generate_study_answer(payload=payload, settings=settings)
    used_context = bool(payload.context and payload.context.strip()) or knowledge.found

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
        source_title=knowledge.title if knowledge.found else None,
        source_path=knowledge.source_path if knowledge.found else None,
        source_type="internal_markdown" if knowledge.found else None,
        source_score=knowledge.score if knowledge.found else None,
    )


@app.post("/chat", response_model=ChatResponse)
async def legacy_chat(payload: ChatRequest) -> ChatResponse:
    return await chat(payload)
