# QA — DilsAI Estudos Academic Taxonomy V1

## Status

QA_ACADEMIC_TAXONOMY_V1_OK

## Branch

feat/dilsai-estudos-academic-taxonomy-v1

## Objetivo

Validar a primeira taxonomia acadêmica oficial do DilsAI Estudos, alinhando frontend, backend e prompt base para níveis, matérias e modos de estudo.

## Entregas validadas

- Adicionado StudyLevel no backend.
- Expandido StudyTopic no backend.
- Adicionado modo resumo no backend.
- Prompt base passou a receber o nível do aluno.
- Tela cheia passou a enviar level no payload.
- Frontend passou a normalizar nível, matéria e modo antes de enviar para a API.
- Selects da tela cheia passaram a ser populados pela taxonomia oficial do JavaScript.
- Documento oficial docs/DILSAI_ESTUDOS_ACADEMIC_TAXONOMY_V1.md criado.

## Validações executadas

JavaScript:

node --check script.js

Resultado: OK.

Backend Python:

find app -name "*.py" -print0 | xargs -0 python -m py_compile

Resultado: OK.

Diff check:

git diff --check

Resultado: OK.

Contrato API:

O endpoint /api/v1/chat aceitou level=ensino_medio, topic=biologia e mode=resumo sem erro 422.

Resposta validada:

status: success
mode: resumo
topic: biologia
used_context: true
confidence: context_assisted

## Observação sobre IA real

A resposta continua usando fallback porque a conta/projeto/chave da OpenAI está bloqueada por quota externa 429 insufficient_quota, já diagnosticado no ciclo anterior.

Isso não invalida este QA, porque o objetivo deste PR é validar contrato de taxonomia e evitar erro 422 entre frontend e backend.

## Resultado final

Taxonomia Acadêmica V1 validada.

O backend aceitou nova matéria biologia e novo modo resumo sem erro 422.

## Próximo passo recomendado

Após merge e tag deste PR, iniciar Base de Conhecimento Simples V1, com arquivos internos por nível/matéria e busca determinística simples, ainda sem embeddings.
