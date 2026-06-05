from app.schemas import ChatRequest, StudyLevel, StudyMode, StudyTopic
from app.services.academic_accuracy import build_basic_school_fact_answer
from app.services.llm import _fallback_response


def test_basic_school_fact_answers_discovery_of_brazil():
    answer = build_basic_school_fact_answer("quem descobriu o brasil")

    assert answer is not None
    assert "Pedro Álvares Cabral" in answer
    assert "1500" in answer
    assert "Resposta final" in answer
    assert "povos indígenas" in answer


def test_professor_mode_fallback_answers_basic_history_without_context():
    payload = ChatRequest(
        user_name="Dilson",
        message="quem descobriu o brasil",
        level=StudyLevel.ensino_medio,
        topic=StudyTopic.historia,
        mode=StudyMode.professor,
    )

    answer = _fallback_response(payload=payload, has_api_key=True)

    assert "Pedro Álvares Cabral" in answer
    assert "1500" in answer
    assert "Preciso de mais contexto" not in answer
