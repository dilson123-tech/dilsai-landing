from app.config import Settings
from app.schemas import ChatRequest
from app.services.knowledge import find_knowledge_context
from app.services.prompts import build_system_prompt
from app.services.academic_accuracy import build_deterministic_context_answer, build_internal_knowledge_answer, build_no_context_answer


def _normalize_context_lines(context: str, max_lines: int = 8) -> list[str]:
    lines: list[str] = []

    for raw_line in context.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        lower = line.lower()

        # Remove cabeçalhos técnicos do upload para o fallback ficar mais limpo.
        if lower.startswith("arquivo enviado pelo aluno:"):
            continue
        if lower.startswith("tamanho:"):
            continue
        if lower.startswith("tipo:"):
            continue
        if lower.startswith("--- página"):
            continue

        lines.append(line)

        if len(lines) >= max_lines:
            break

    return lines


def _context_excerpt(context: str, max_chars: int = 1400) -> str:
    clean = context.strip()

    if len(clean) <= max_chars:
        return clean

    return clean[:max_chars].rstrip() + "\n..."


def _uploaded_context_fallback(payload: ChatRequest, user_context: str) -> str:
    return build_deterministic_context_answer(
        payload=payload,
        context=user_context,
        source_label="material enviado pelo aluno",
        has_api_key=False,
    )


def _fallback_response(
    payload: ChatRequest,
    has_api_key: bool,
    knowledge_context: str = "",
    user_context: str = "",
) -> str:
    if user_context:
        return build_deterministic_context_answer(
            payload=payload,
            context=user_context,
            source_label="material enviado pelo aluno",
            has_api_key=has_api_key,
        )

    if knowledge_context:
        return build_internal_knowledge_answer(
            payload=payload,
            knowledge_context=knowledge_context,
            has_api_key=has_api_key,
        )

    return build_no_context_answer(payload=payload, has_api_key=has_api_key)

