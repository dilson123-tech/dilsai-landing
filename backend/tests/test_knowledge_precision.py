from app.schemas import ChatRequest, StudyLevel, StudyMode, StudyTopic
from app.services.knowledge import find_knowledge_context


def test_knowledge_does_not_match_biology_only_by_high_school_level_for_math():
    payload = ChatRequest(
        user_name="Dilson",
        message="quanto e 30*3",
        level=StudyLevel.ensino_medio,
        topic=StudyTopic.matematica_logica,
        mode=StudyMode.fonte_segura,
    )

    knowledge = find_knowledge_context(payload)

    assert knowledge.found is False
    assert knowledge.title is None
    assert knowledge.source_path is None
    assert knowledge.score == 0
