from enum import Enum

from pydantic import BaseModel, Field


class StudyMode(str, Enum):
    direto = "direto"
    professor = "professor"
    passo_a_passo = "passo_a_passo"
    revisao = "revisao"
    simulado = "simulado"
    fonte_segura = "fonte_segura"


class StudyTopic(str, Enum):
    programacao = "programacao"
    portugues = "portugues"
    matematica_logica = "matematica_logica"
    geral = "geral"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=4000)
    user_name: str = Field(default="Aluno", max_length=80)
    topic: StudyTopic = StudyTopic.geral
    mode: StudyMode = StudyMode.professor
    context: str | None = Field(
        default=None,
        max_length=8000,
        description="Material, apostila, trecho de aula ou contexto fornecido pelo aluno.",
    )


class ChatResponse(BaseModel):
    response: str
    status: str = "success"
    mode: StudyMode
    topic: StudyTopic
    used_context: bool
    confidence: str
    safety_notice: str | None = None
