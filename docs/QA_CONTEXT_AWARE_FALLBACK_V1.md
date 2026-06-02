# QA — DilsAI Estudos Context Aware Fallback V1

## Status

QA_CONTEXT_AWARE_FALLBACK_V1_OK

## Branch

feat/dilsai-estudos-context-aware-fallback-v1

## Objetivo

Validar que o fallback do DilsAI Estudos usa o contexto enviado pelo aluno quando o provedor externo de IA não pode ser acionado.

## Entregas validadas

- Criada função de fallback determinístico para contexto enviado.
- Fallback passa a resumir linhas úteis do material enviado.
- Cabeçalhos técnicos de upload são filtrados do resumo preliminar.
- Material enviado pelo aluno tem prioridade sobre base interna no fallback.
- Quando usa material enviado, source_title/source_path/source_type/source_score permanecem nulos.
- Fallback deixa claro que não consultou o modelo externo.

## Validação técnica

Payload testado:

message=Resuma esse material em linguagem simples.
level=ensino_medio
topic=geral
mode=resumo
context=conteúdo extraído de PDF textual de teste

Resultado validado:

status=success
used_context=true
confidence=context_assisted
source_title=null
source_path=null
source_type=null
source_score=null

A resposta retornou:

- aviso de que a IA externa não pôde ser acionada;
- confirmação de material enviado pelo aluno;
- resumo preliminar do material;
- trecho-base usado;
- observação de fallback seguro.

## Resultado final

Context Aware Fallback V1 validado.

O DilsAI Estudos agora continua útil com material enviado pelo aluno mesmo quando a OpenAI está bloqueada por quota externa.

## Próximo passo recomendado

Após merge e tag, avaliar OCR em ciclo separado ou criar metadados formais para fonte de material enviado pelo usuário.
