from app.schemas import ChatRequest, StudyLevel, StudyMode, StudyTopic
from app.services.academic_accuracy import build_basic_unit_conversion_answer
from app.services.llm import _fallback_response


def test_basic_unit_conversion_solves_cubic_meters_to_liters():
    answer = build_basic_unit_conversion_answer("quanto é 3 metros cubicos")

    assert answer is not None
    assert "Resposta final" in answer
    assert "3 m³ = 3000 litros" in answer


def test_professor_mode_fallback_solves_cubic_meters_without_context():
    payload = ChatRequest(
        user_name="Dilson",
        message="quanto é 3 metros cubicos",
        level=StudyLevel.ensino_medio,
        topic=StudyTopic.matematica_logica,
        mode=StudyMode.professor,
    )

    answer = _fallback_response(payload=payload, has_api_key=True)

    assert "Resposta final" in answer
    assert "3000 litros" in answer
    assert "Preciso de mais contexto" not in answer
