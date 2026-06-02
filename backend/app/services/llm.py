from app.config import Settings
from app.schemas import ChatRequest
from app.services.knowledge import find_knowledge_context
from app.services.prompts import build_system_prompt


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
    lines = _normalize_context_lines(user_context)
    excerpt = _context_excerpt(user_context)

    points = "\n".join(f"- {line}" for line in lines)

    if not points:
        points = "- O material foi enviado, mas não consegui extrair linhas claras para resumir."

    return (
        "A IA externa não pôde ser acionada neste momento, mas encontrei material enviado pelo aluno. "
        "Abaixo está um apoio de estudo gerado de forma determinística a partir do contexto recebido, sem fingir consulta ao modelo externo.\n\n"
        f"Pergunta do aluno: {payload.message}\n\n"
        "Resumo preliminar do material:\n"
        f"{points}\n\n"
        "Trecho-base usado:\n"
        f"{excerpt}\n\n"
        "Observação: este é um fallback seguro. Quando a cota/chave da IA externa estiver disponível, "
        "a resposta poderá ser reescrita de forma mais didática pelo modelo."
    )


def _fallback_response(
    payload: ChatRequest,
    has_api_key: bool,
    knowledge_context: str = "",
    user_context: str = "",
) -> str:
    setup_notice = (
        "A IA real ainda não está configurada neste ambiente porque falta OPENAI_API_KEY. "
        if not has_api_key
        else ""
    )

    if user_context:
        return _uploaded_context_fallback(payload, user_context)

    if knowledge_context:
        return (
            f"{setup_notice}"
            "Encontrei uma base interna DilsAI Estudos relacionada à sua pergunta. "
            "Como o provedor externo de IA não pôde ser acionado neste momento, "
            "segue o material interno localizado para estudo:\n\n"
            f"{knowledge_context}"
        )

    return (
        f"{setup_notice}"
        f"Recebi sua pergunta, {payload.user_name}. "
        "Este backend já está no padrão DilsAI Estudos: tema, modo de resposta e política contra resposta inventada. "
        "No próximo ciclo, com a chave/cota configurada, a resposta será gerada pelo modelo de IA respeitando essas regras.\n\n"
        f"Pergunta recebida: {payload.message}"
    )


async def generate_study_answer(payload: ChatRequest, settings: Settings) -> str:
    knowledge = find_knowledge_context(payload)
    knowledge_context = knowledge.prompt_context

    user_context = payload.context.strip() if payload.context and payload.context.strip() else ""
    combined_context = "\n\n".join(
        item for item in [knowledge_context, user_context] if item
    )

    has_context = bool(combined_context)
    has_api_key = bool(settings.openai_api_key.strip())

    if payload.mode == "fonte_segura" and not has_context:
        return (
            "Não encontrei informação suficiente na base atual para responder com segurança. "
            "Para usar o Modo Fonte Segura, envie o material, apostila, PDF ou contexto da aula."
        )

    if not has_api_key:
        return _fallback_response(
            payload,
            has_api_key=False,
            knowledge_context=knowledge_context,
            user_context=user_context,
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key.strip())
        system_prompt = build_system_prompt(
            topic=payload.topic,
            mode=payload.mode,
            has_context=has_context,
            level=payload.level,
        )

        user_content = payload.message
        if has_context:
            user_content = (
                "Contexto/material disponível para resposta:\n"
                f"{combined_context}\n\n"
                "Pergunta do aluno:\n"
                f"{payload.message}"
            )

        response = client.chat.completions.create(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )

        content = response.choices[0].message.content
        if not content:
            return _fallback_response(
                payload,
                has_api_key=True,
                knowledge_context=knowledge_context,
                user_context=user_context,
            )

        return content

    except Exception:
        return _fallback_response(
            payload,
            has_api_key=True,
            knowledge_context=knowledge_context,
            user_context=user_context,
        )
