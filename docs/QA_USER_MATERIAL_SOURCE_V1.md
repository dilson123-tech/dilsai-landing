# QA — DilsAI Estudos User Material Source V1

## Status

QA_USER_MATERIAL_SOURCE_V1_OK

## Branch

feat/dilsai-estudos-user-material-source-v1

## Objetivo

Validar metadados formais de fonte para material enviado pelo aluno.

Este ciclo complementa o Context Aware Fallback V1, permitindo que respostas baseadas em contexto enviado pelo usuário retornem source_title e source_type de forma honesta.

## Entregas validadas

- Criado helper extract_user_material_source.
- API identifica nome do arquivo a partir de Arquivo enviado pelo aluno.
- API identifica PDF textual extraído como user_uploaded_pdf_text.
- source_path permanece null porque o arquivo não é salvo no servidor.
- source_score permanece null porque não há ranking de base interna.
- Material enviado pelo aluno continua tendo prioridade sobre base interna no fallback.
- Fonte interna não é usada indevidamente quando a resposta vem do material enviado.

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
source_title=dilsai-pdf-teste.pdf
source_path=null
source_type=user_uploaded_pdf_text
source_score=null

A resposta retornou fallback seguro baseado no material enviado pelo aluno.

## Resultado final

User Material Source V1 validado.

O DilsAI Estudos agora informa fonte formal também para material temporário enviado pelo aluno.

## Próximo passo recomendado

Após merge e tag, exibir labels mais amigáveis no frontend para:

- user_uploaded_pdf_text
- user_uploaded_text
- user_uploaded_markdown
