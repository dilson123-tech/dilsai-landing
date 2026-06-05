from app.schemas import ChatRequest, StudyLevel, StudyMode, StudyTopic
from app.services.academic_accuracy import build_basic_arithmetic_answer
from app.services.llm import _fallback_response


def test_basic_arithmetic_answer_solves_simple_multiplication():
    answer = build_basic_arithmetic_answer("quanto e 30*3")

    assert answer is not None
    assert "Resposta final" in answer
    assert "90" in answer


def test_professor_mode_fallback_solves_arithmetic_without_context():
    payload = ChatRequest(
        user_name="Dilson",
        message="quanto e 30*3",
        level=StudyLevel.ensino_medio,
        topic=StudyTopic.matematica_logica,
        mode=StudyMode.professor,
    )

    answer = _fallback_response(payload=payload, has_api_key=True)

    assert "Resposta final" in answer
    assert "90" in answer
    assert "Preciso de mais contexto" not in answer

def test_basic_arithmetic_answer_solves_square_root():
    answer = build_basic_arithmetic_answer("raiz quadrada de 144")

    assert answer is not None
    assert "Resposta final" in answer
    assert "12" in answer
    assert "√144" in answer


def test_professor_mode_fallback_solves_square_root_without_context():
    payload = ChatRequest(
        user_name="Dilson",
        message="raiz quadrada de 144",
        level=StudyLevel.ensino_medio,
        topic=StudyTopic.matematica_logica,
        mode=StudyMode.professor,
    )

    answer = _fallback_response(payload=payload, has_api_key=True)

    assert "Resposta final" in answer
    assert "12" in answer
    assert "Preciso de mais contexto" not in answer

