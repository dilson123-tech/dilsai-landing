# DilsAI Estudos — User Material Source V1

## Status

DILSAI_ESTUDOS_USER_MATERIAL_SOURCE_V1

## Objetivo

Adicionar metadados formais de fonte quando a resposta usa material enviado pelo aluno.

Este ciclo complementa o Context Aware Fallback V1. Antes, quando a resposta usava contexto enviado pelo aluno, os campos `source_title`, `source_path`, `source_type` e `source_score` permaneciam nulos. Agora, o sistema informa a origem do material enviado de forma honesta.

## Campos esperados

Para PDF textual extraído:

- `source_title`: nome do arquivo enviado.
- `source_type`: `user_uploaded_pdf_text`.
- `source_path`: `null`, pois o arquivo não é salvo no servidor.
- `source_score`: `null`, pois não vem de ranking da base interna.

Para `.txt`:

- `source_type`: `user_uploaded_text`.

Para `.md`:

- `source_type`: `user_uploaded_markdown`.

## Regra de produto

O DilsAI Estudos não deve fingir que o material enviado virou base interna permanente.

Material enviado pelo aluno é fonte temporária da resposta atual.

## Próximo passo recomendado

Após validar este ciclo, exibir no frontend uma legenda mais amigável para `user_uploaded_pdf_text`, `user_uploaded_text` e `user_uploaded_markdown`.
