import asyncio

from app.main import chat
from app.schemas import ChatRequest, StudyLevel, StudyMode, StudyTopic


def test_safe_source_without_user_context_rejects_weak_internal_source():
    payload = ChatRequest(
        user_name="Dilson",
        message="Qual é a resposta da questão?",
        level=StudyLevel.ensino_medio,
        topic=StudyTopic.matematica_logica,
        mode=StudyMode.fonte_segura,
    )

    response = asyncio.run(chat(payload))

    assert response.used_context is False
    assert response.confidence == "context_required"
    assert response.source_title is None
    assert response.source_path is None
    assert response.source_type is None
    assert response.source_score is None
    assert "Fonte Segura" in response.response
    assert "envie o print completo" in response.response
