# QA — DilsAI Estudos Source Response V1

## Status

QA_SOURCE_RESPONSE_V1_OK

## Branch

feat/dilsai-estudos-source-response-v1

## Objetivo

Validar que a API do DilsAI Estudos retorna metadados formais de fonte quando usa a Base de Conhecimento Simples V1.

## Entregas validadas

- ChatResponse expandido com source_title.
- ChatResponse expandido com source_path.
- ChatResponse expandido com source_type.
- ChatResponse expandido com source_score.
- Endpoint /api/v1/chat retorna metadados de fonte quando find_knowledge_context encontra base interna.
- Mantida compatibilidade com used_context e confidence.
- Fonte interna continua marcada como internal_markdown.

## Validações executadas

### Backend Python

Comando:

find app -name "*.py" -print0 | xargs -0 python -m py_compile

Resultado:

OK.

### Diff check

Comando:

git diff --check

Resultado:

OK.

### Teste fonte — Fotossíntese

Payload:

level=ensino_medio
topic=biologia
mode=resumo
message=Faça um resumo curto sobre fotossíntese.

Resultado validado:

status=success
used_context=true
confidence=context_assisted
source_title=Fotossíntese
source_path=ensino_medio/biologia/fotossintese.md
source_type=internal_markdown
source_score=18

### Teste fonte — API

Payload:

level=geral
topic=programacao
mode=professor
message=Explique o que é uma API para iniciante.

Resultado validado:

status=success
used_context=true
confidence=context_assisted
source_title=API
source_path=geral/programacao/api.md
source_type=internal_markdown
source_score=16

## Observação sobre IA real

A OpenAI continua bloqueada por quota externa 429 insufficient_quota, já diagnosticado em ciclos anteriores.

Este QA permanece válido porque o objetivo deste PR é validar metadados formais de fonte usando a base interna local.

## Resultado final

Source Response V1 validado.

O DilsAI Estudos agora informa formalmente qual fonte interna foi usada para apoiar a resposta.
