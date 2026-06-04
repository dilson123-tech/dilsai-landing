from app.schemas import ChatRequest, StudyLevel, StudyMode, StudyTopic
from app.services.academic_accuracy import build_deterministic_context_answer
from app.services.prompts import build_system_prompt


def test_system_prompt_contains_academic_accuracy_contract():
    prompt = build_system_prompt(
        topic=StudyTopic.matematica_logica,
        mode=StudyMode.passo_a_passo,
        has_context=True,
        level=StudyLevel.ensino_medio,
    )

    assert "Motor de precisão acadêmica V1" in prompt
    assert "Resposta final" in prompt
    assert "OCR" in prompt
    assert "Não invente resposta final" in prompt


def test_deterministic_context_answer_is_structured_and_cautious():
    payload = ChatRequest(
        message="Resolva a questão do print.",
        level=StudyLevel.ensino_medio,
        topic=StudyTopic.matematica_logica,
        mode=StudyMode.professor,
        context="2 + 2 = ?",
    )

    answer = build_deterministic_context_answer(
        payload=payload,
        context="Arquivo original: image.png\\n2 + 2 = ?\\nA) 3\\nB) 4",
        source_label="print enviado pelo aluno",
        has_api_key=False,
    )

    assert "Resposta baseada no material enviado" in answer
    assert "Não vou fingir certeza" in answer
    assert "Resposta final" in answer
    assert "Arquivo original" not in answer.split("Leitura inicial do material:", 1)[1].split("Apoio de estudo:", 1)[0]
