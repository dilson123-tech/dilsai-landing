from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import ChatRequest, ChatResponse
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


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    answer = await generate_study_answer(payload=payload, settings=settings)
    used_context = bool(payload.context and payload.context.strip())

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
    )


@app.post("/chat", response_model=ChatResponse)
async def legacy_chat(payload: ChatRequest) -> ChatResponse:
    return await chat(payload)
