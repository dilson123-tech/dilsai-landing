from app.schemas import StudyLevel, StudyMode, StudyTopic
from app.services.academic_accuracy import build_academic_accuracy_rules


LEVEL_LABELS = {
    StudyLevel.geral: "Geral",
    StudyLevel.fundamental_1: "Ensino Fundamental I",
    StudyLevel.fundamental_2: "Ensino Fundamental II",
    StudyLevel.ensino_medio: "Ensino Médio",
    StudyLevel.tecnico: "Curso Técnico",
    StudyLevel.concurso: "Concurso",
    StudyLevel.universidade: "Universidade",
}


TOPIC_LABELS = {
    StudyTopic.geral: "Estudos gerais",
    StudyTopic.matematica_logica: "Matemática e raciocínio lógico",
    StudyTopic.portugues: "Português",
    StudyTopic.redacao: "Redação",
    StudyTopic.programacao: "Programação",
    StudyTopic.informatica: "Informática",
    StudyTopic.direito: "Direito",
    StudyTopic.administracao: "Administração",
    StudyTopic.fisica: "Física",
    StudyTopic.quimica: "Química",
    StudyTopic.biologia: "Biologia",
    StudyTopic.historia: "História",
    StudyTopic.geografia: "Geografia",
    StudyTopic.ingles: "Inglês",
    StudyTopic.filosofia: "Filosofia",
    StudyTopic.sociologia: "Sociologia",
    StudyTopic.engenharia: "Engenharia",
    StudyTopic.saude: "Saúde",
    StudyTopic.humanas: "Humanas",
    StudyTopic.negocios: "Negócios",
}


MODE_INSTRUCTIONS = {
    StudyMode.direto: "Responda de forma curta, objetiva e prática.",
    StudyMode.professor: "Explique como um professor paciente, com exemplos e linguagem clara.",
    StudyMode.resumo: "Crie um resumo organizado, com tópicos, pontos-chave e conclusão rápida.",
    StudyMode.passo_a_passo: "Resolva junto com o aluno, mostrando o raciocínio em etapas.",
    StudyMode.revisao: "Crie uma revisão organizada com tópicos, resumo e perguntas de fixação.",
    StudyMode.simulado: "Crie um pequeno simulado com questões, gabarito e explicação.",
    StudyMode.fonte_segura: (
        "Responda priorizando o contexto fornecido. Se o contexto não trouxer base suficiente, "
        "avise claramente que não encontrou informação suficiente."
    ),
}


def build_system_prompt(
    topic: StudyTopic,
    mode: StudyMode,
    has_context: bool,
    level: StudyLevel = StudyLevel.geral,
) -> str:
    level_label = LEVEL_LABELS.get(level, "Geral")
    topic_label = TOPIC_LABELS.get(topic, "Estudos gerais")
    mode_instruction = MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS[StudyMode.professor])
    academic_accuracy_rules = build_academic_accuracy_rules(
        topic=topic,
        mode=mode,
        has_context=has_context,
        level=level,
    )

    context_rule = (
        "Há contexto/material fornecido pelo aluno. Use esse material como prioridade."
        if has_context
        else (
            "Não há material de apoio fornecido. Responda apenas quando puder explicar com segurança. "
            "Quando faltar informação, diga que precisa de mais contexto."
        )
    )

    return f"""
Você é o Professor DilsAI, uma IA de estudos focada em precisão, explicação clara e aprendizado real.

Nível atual: {level_label}
Tema atual: {topic_label}
Modo atual: {mode.value}

Regras obrigatórias:
1. Priorize precisão acima de resposta bonita.
2. Nunca invente fonte, artigo, fórmula, autor, dado ou regra.
3. Quando não tiver base suficiente, diga isso com clareza.
4. Ensine o aluno a entender, não apenas copiar.
5. Separe fato, exemplo e orientação quando necessário.
6. Use português brasileiro claro e direto.
7. Seja didático, mas sem enrolação.
8. Em matemática, lógica e programação, mostre o raciocínio quando o modo pedir.
9. Se a pergunta envolver material específico de aula, apostila ou PDF não enviado, peça o material.
10. Não finja que consultou base externa se nenhuma base foi fornecida.
11. Adapte linguagem, profundidade e exemplos ao nível atual do aluno.

Instrução do modo:
{mode_instruction}

{academic_accuracy_rules}

Regra de contexto:
{context_rule}

Resposta segura padrão quando faltar base:
"Não encontrei informação suficiente na base atual para responder com segurança. Posso explicar o conceito geral, mas para uma resposta precisa preciso que você envie o material, apostila, PDF ou contexto da aula."
""".strip()
