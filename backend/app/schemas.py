from enum import Enum

from pydantic import BaseModel, Field


class StudyLevel(str, Enum):
    geral = "geral"
    fundamental_1 = "fundamental_1"
    fundamental_2 = "fundamental_2"
    ensino_medio = "ensino_medio"
    tecnico = "tecnico"
    concurso = "concurso"
    universidade = "universidade"


class StudyMode(str, Enum):
    direto = "direto"
    professor = "professor"
    resumo = "resumo"
    passo_a_passo = "passo_a_passo"
    revisao = "revisao"
    simulado = "simulado"
    fonte_segura = "fonte_segura"


class StudyTopic(str, Enum):
    geral = "geral"
    matematica_logica = "matematica_logica"
    portugues = "portugues"
    redacao = "redacao"
    programacao = "programacao"
    informatica = "informatica"
    direito = "direito"
    administracao = "administracao"
    fisica = "fisica"
    quimica = "quimica"
    biologia = "biologia"
    historia = "historia"
    geografia = "geografia"
    ingles = "ingles"
    filosofia = "filosofia"
    sociologia = "sociologia"
    engenharia = "engenharia"
    saude = "saude"
    humanas = "humanas"
    negocios = "negocios"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=4000)
    user_name: str = Field(default="Aluno", max_length=80)
    level: StudyLevel = StudyLevel.geral
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
