from app.config import Settings
from app.schemas import ChatRequest
from app.services.prompts import build_system_prompt


def _fallback_response(payload: ChatRequest, has_api_key: bool) -> str:
    setup_notice = (
        "A IA real ainda não está configurada neste ambiente porque falta OPENAI_API_KEY. "
        if not has_api_key
        else ""
    )

    return (
        f"{setup_notice}"
        f"Recebi sua pergunta, {payload.user_name}. "
        "Este backend já está no padrão DilsAI Estudos: tema, modo de resposta e política contra resposta inventada. "
        "No próximo ciclo, com a chave configurada, a resposta será gerada pelo modelo de IA respeitando essas regras.\n\n"
        f"Pergunta recebida: {payload.message}"
    )


async def generate_study_answer(payload: ChatRequest, settings: Settings) -> str:
    has_context = bool(payload.context and payload.context.strip())
    has_api_key = bool(settings.openai_api_key.strip())

    if payload.mode == "fonte_segura" and not has_context:
        return (
            "Não encontrei informação suficiente na base atual para responder com segurança. "
            "Para usar o Modo Fonte Segura, envie o material, apostila, PDF ou contexto da aula."
        )

    if not has_api_key:
        return _fallback_response(payload, has_api_key=False)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        system_prompt = build_system_prompt(
            topic=payload.topic,
            mode=payload.mode,
            has_context=has_context,
        )

        user_content = payload.message
        if has_context:
            user_content = (
                "Contexto/material fornecido pelo aluno:\n"
                f"{payload.context}\n\n"
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
            return (
                "Não consegui gerar uma resposta útil agora. "
                "Tente reformular a pergunta ou enviar mais contexto."
            )

        return content

    except Exception:
        return (
            "Não consegui acionar o provedor de IA neste momento. "
            "A configuração do backend precisa ser revisada antes de usar em produção."
        )
