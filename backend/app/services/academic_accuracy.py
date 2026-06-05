from app.schemas import ChatRequest, StudyLevel, StudyMode, StudyTopic


LEVEL_ACCURACY_RULES = {
    StudyLevel.geral: "Use linguagem clara, sem presumir conhecimento prévio.",
    StudyLevel.fundamental_1: "Use explicação simples, exemplos básicos e frases curtas.",
    StudyLevel.fundamental_2: "Explique com base escolar, exemplos e revisão dos conceitos.",
    StudyLevel.ensino_medio: "Foque em compreensão, prova, interpretação e pegadinhas comuns.",
    StudyLevel.tecnico: "Foque em aplicação prática, procedimento e uso profissional.",
    StudyLevel.concurso: "Seja objetivo, destaque pegadinhas, termos-chave e raciocínio de prova.",
    StudyLevel.universidade: "Use precisão conceitual, termos técnicos e aprofundamento responsável.",
}


TOPIC_ACCURACY_RULES = {
    StudyTopic.geral: "Adapte a resposta ao conteúdo enviado e ao objetivo do aluno.",
    StudyTopic.matematica_logica: "Mostre passos, fórmulas usadas, conferência e erro comum.",
    StudyTopic.portugues: "Priorize interpretação, gramática, sentido do texto e justificativa.",
    StudyTopic.redacao: "Aponte estrutura, tese, argumentos, coesão e melhoria prática.",
    StudyTopic.programacao: "Explique lógica, código, erro provável, solução e boas práticas.",
    StudyTopic.informatica: "Explique conceito, uso prático, diferença entre termos e aplicação.",
    StudyTopic.direito: "Separe conceito, regra, aplicação e ressalva; não invente artigo ou lei.",
    StudyTopic.administracao: "Explique conceito, aplicação gerencial e exemplo prático.",
    StudyTopic.fisica: "Identifique grandezas, fórmula, unidades, substituição e interpretação.",
    StudyTopic.quimica: "Explique conceitos, reação/processo e cuidado com nomenclatura.",
    StudyTopic.biologia: "Explique processos, funções, relações e termos científicos.",
    StudyTopic.historia: "Contextualize período, causa, consequência e comparação.",
    StudyTopic.geografia: "Explique conceito, localização/processo e impacto socioambiental.",
    StudyTopic.ingles: "Explique vocabulário, estrutura, tradução e uso no contexto.",
    StudyTopic.filosofia: "Explique ideia, autor/conceito quando houver base e comparação.",
    StudyTopic.sociologia: "Explique conceito social, contexto, exemplo e relação crítica.",
    StudyTopic.engenharia: "Use precisão técnica, cálculo quando necessário e aplicação prática.",
    StudyTopic.saude: "Use linguagem responsável, cautelosa e não substitua profissional de saúde.",
    StudyTopic.humanas: "Contextualize, compare e explique causas/consequências.",
    StudyTopic.negocios: "Explique aplicação prática, decisão, risco e exemplo empresarial.",
}


MODE_ACCURACY_RULES = {
    StudyMode.direto: "Responda curto, mas preserve precisão e resposta final.",
    StudyMode.professor: "Ensine com didática, exemplo e fechamento claro.",
    StudyMode.resumo: "Organize em tópicos, pontos-chave e conclusão.",
    StudyMode.passo_a_passo: "Resolva em etapas numeradas e explique cada decisão.",
    StudyMode.revisao: "Crie revisão com tópicos, pontos que caem em prova e perguntas de fixação.",
    StudyMode.simulado: "Crie questões, gabarito e comentário da resposta correta.",
    StudyMode.fonte_segura: "Priorize estritamente o contexto. Se faltar base, avise e peça material.",
}


def build_academic_accuracy_rules(
    *,
    topic: StudyTopic,
    mode: StudyMode,
    has_context: bool,
    level: StudyLevel,
) -> str:
    context_rule = (
        "Há material/contexto do aluno. Use esse material como fonte principal; conhecimento geral só pode complementar com aviso."
        if has_context
        else "Não há material do aluno. Responda apenas se for seguro; quando depender de enunciado, alternativa, PDF, print ou aula específica, peça o material."
    )

    return f"""
Motor de precisão acadêmica V1:
- Produto real: responda para ajudar o estudante a entender e acertar, não para parecer bonito.
- {context_rule}
- Regra do nível: {LEVEL_ACCURACY_RULES.get(level, LEVEL_ACCURACY_RULES[StudyLevel.geral])}
- Regra da matéria: {TOPIC_ACCURACY_RULES.get(topic, TOPIC_ACCURACY_RULES[StudyTopic.geral])}
- Regra do modo: {MODE_ACCURACY_RULES.get(mode, MODE_ACCURACY_RULES[StudyMode.professor])}
- Se o OCR estiver confuso, cortado ou ilegível, avise antes de concluir.
- Se faltar alternativa, enunciado ou dado essencial, peça complemento.
- Não invente resposta final quando a base for insuficiente.
- Em questões, use uma seção explícita chamada "Resposta final" quando houver base suficiente.
- Estrutura recomendada: leitura do enunciado, o que se pede, resolução, Resposta final, por que está certo e erro comum.
- Quando houver incerteza, diga exatamente qual é a limitação.
""".strip()


def _clean_context_lines(context: str, max_lines: int = 8) -> list[str]:
    lines: list[str] = []

    blocked_prefixes = (
        "arquivo enviado pelo aluno:",
        "arquivo original:",
        "arquivo otimizado:",
        "tamanho:",
        "tipo:",
        "aviso:",
        "--- página",
        "print da questão",
        "digite aqui",
        "enviar",
        "limpar",
    )

    for raw_line in context.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        lower = line.lower()
        if any(lower.startswith(prefix) for prefix in blocked_prefixes):
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


def build_deterministic_context_answer(
    *,
    payload: ChatRequest,
    context: str,
    source_label: str,
    has_api_key: bool,
) -> str:
    lines = _clean_context_lines(context)
    excerpt = _context_excerpt(context)

    points = "\n".join(f"- {line}" for line in lines)
    if not points:
        points = "- O material foi enviado, mas o texto extraído não ficou claro o bastante."

    engine_status = (
        "Motor local seguro acionado porque a IA externa não está configurada neste ambiente."
        if not has_api_key
        else "Motor local seguro acionado porque a IA externa não respondeu neste momento."
    )

    return (
        "Resposta baseada no material enviado\n\n"
        f"{engine_status}\n"
        "Não vou fingir certeza além do que o material permite.\n\n"
        f"Pergunta do aluno:\n{payload.message}\n\n"
        f"Fonte usada: {source_label}\n\n"
        "Leitura inicial do material:\n"
        f"{points}\n\n"
        "Apoio de estudo:\n"
        "Use os pontos acima como base para revisar o conteúdo. Se isso for uma questão, confira se o print trouxe o enunciado completo, alternativas e dados necessários.\n\n"
        "Resposta final:\n"
        "Ainda preciso do motor de IA completo ou de um enunciado mais claro para resolver com precisão total. Com o material atual, a leitura segura é a síntese acima.\n\n"
        "Ponto de atenção:\n"
        "Se o OCR cortou texto, misturou letras ou pegou partes da tela, recorte apenas a questão e envie novamente.\n\n"
        "Trecho-base usado:\n"
        f"{excerpt}"
    )


def build_internal_knowledge_answer(
    *,
    payload: ChatRequest,
    knowledge_context: str,
    has_api_key: bool,
) -> str:
    engine_status = (
        "Motor local seguro acionado porque a IA externa não está configurada neste ambiente."
        if not has_api_key
        else "Motor local seguro acionado porque a IA externa não respondeu neste momento."
    )

    return (
        "Resposta baseada na base interna DilsAI Estudos\n\n"
        f"{engine_status}\n"
        "Usei a base interna encontrada como apoio, sem inventar fonte externa.\n\n"
        f"Pergunta do aluno:\n{payload.message}\n\n"
        "Material interno localizado:\n"
        f"{knowledge_context}\n\n"
        "Ponto de atenção:\n"
        "Para resposta mais precisa sobre aula, prova ou apostila específica, envie o material do aluno."
    )


def build_no_context_answer(*, payload: ChatRequest, has_api_key: bool) -> str:
    engine_status = (
        "A IA externa ainda não está configurada neste ambiente."
        if not has_api_key
        else "A IA externa não respondeu neste momento."
    )

    return (
        "Preciso de mais contexto para responder com precisão\n\n"
        f"{engine_status}\n\n"
        f"Pergunta recebida:\n{payload.message}\n\n"
        "Para aumentar a chance de acerto real, envie uma destas opções:\n"
        "- print completo da questão;\n"
        "- alternativas da prova;\n"
        "- trecho da apostila;\n"
        "- PDF/material da aula;\n"
        "- sua tentativa de resposta.\n\n"
        "Ponto de atenção:\n"
        "Como produto de estudos, o DilsAI deve evitar chute quando faltar base."
    )



def _safe_eval_arithmetic_expression(expression: str) -> float | int | None:
    import ast
    import operator

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](eval_node(node.operand))

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = eval_node(node.left)
            right = eval_node(node.right)

            if isinstance(node.op, ast.Div) and right == 0:
                raise ZeroDivisionError("divisão por zero")

            return operators[type(node.op)](left, right)

        raise ValueError("expressão não permitida")

    try:
        tree = ast.parse(expression, mode="eval")
        return eval_node(tree)
    except Exception:
        return None


def _format_arithmetic_result(value: float | int) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    if isinstance(value, float):
        formatted = f"{value:.10f}".rstrip("0").rstrip(".")
        return formatted

    return str(value)


def extract_basic_arithmetic_expression(message: str) -> str | None:
    import re

    normalized = (
        message.lower()
        .replace("quanto é", "")
        .replace("quanto e", "")
        .replace("calcule", "")
        .replace("resolver", "")
        .replace("resolva", "")
        .replace("vezes", "*")
        .replace("x", "*")
        .replace("×", "*")
        .replace("÷", "/")
        .replace(",", ".")
    )

    # Mantém apenas expressão aritmética básica.
    candidate = "".join(ch for ch in normalized if ch in "0123456789+-*/(). ")

    candidate = re.sub(r"\s+", "", candidate)

    if not candidate:
        return None

    if not re.search(r"\d", candidate):
        return None

    if not re.search(r"[+\-*/]", candidate):
        return None

    return candidate




def extract_basic_square_root_value(message: str) -> float | int | None:
    import re
    import math

    normalized = (
        message.lower()
        .replace(",", ".")
        .replace("√", " raiz quadrada de ")
        .replace("sqrt", " raiz quadrada de ")
    )

    patterns = [
        r"raiz\s+quadrada\s+(?:de|do|da)?\s*(-?\d+(?:\.\d+)?)",
        r"raiz\s+(?:de|do|da)?\s*(-?\d+(?:\.\d+)?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, normalized)
        if not match:
            continue

        value = float(match.group(1))

        if value < 0:
            return None

        result = math.sqrt(value)

        if result.is_integer():
            return int(result)

        return result

    return None


def build_basic_square_root_answer(message: str) -> str | None:
    value = extract_basic_square_root_value(message)

    if value is None:
        return None

    import re

    normalized = message.lower().replace(",", ".")
    match = re.search(r"(-?\d+(?:\.\d+)?)", normalized)
    original_number = match.group(1) if match else "o número informado"

    result_text = _format_arithmetic_result(value)

    return (
        "Resolvi como raiz quadrada básica.\n\n"
        f"Conta:\n√{original_number}\n\n"
        "Resolução:\n"
        f"√{original_number} = {result_text}, porque {result_text} × {result_text} = {original_number}.\n\n"
        "Resposta final:\n"
        f"{result_text}\n\n"
        "Ponto de atenção:\n"
        "Para questões maiores com enunciado, alternativas ou fórmula aplicada, envie o print ou o material completo."
    )

def build_basic_arithmetic_answer(message: str) -> str | None:
    square_root_answer = build_basic_square_root_answer(message)
    if square_root_answer:
        return square_root_answer

    expression = extract_basic_arithmetic_expression(message)

    if not expression:
        return None

    result = _safe_eval_arithmetic_expression(expression)

    if result is None:
        return None

    result_text = _format_arithmetic_result(result)
    readable_expression = expression.replace("*", " × ").replace("/", " ÷ ").replace("+", " + ").replace("-", " - ")

    return (
        "Resolvi como aritmética básica.\n\n"
        f"Conta:\n{readable_expression}\n\n"
        "Resolução:\n"
        f"{readable_expression} = {result_text}\n\n"
        "Resposta final:\n"
        f"{result_text}\n\n"
        "Ponto de atenção:\n"
        "Para questões maiores de prova, com enunciado ou alternativas, envie o print ou o material completo."
    )
