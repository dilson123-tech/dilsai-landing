# DilsAI Estudos — Friendly Source Labels V1

## Status

DILSAI_ESTUDOS_FRIENDLY_SOURCE_LABELS_V1

## Objetivo

Exibir fontes no frontend com rótulos amigáveis para aluno, professor e parceiro.

## Antes

A tela exibia apenas o título bruto da fonte, por exemplo:

- Fonte: Fotossíntese
- Fonte: dilsai-pdf-teste.pdf

## Depois

A tela passa a exibir a origem de forma mais clara:

- Fonte: Base interna DilsAI: Fotossíntese
- Fonte: PDF enviado pelo aluno: dilsai-pdf-teste.pdf
- Fonte: Texto enviado pelo aluno: material.txt
- Fonte: Markdown enviado pelo aluno: apostila.md

## Tipos tratados

- internal_markdown
- user_uploaded_pdf_text
- user_uploaded_text
- user_uploaded_markdown

## Regra de produto

O frontend deve deixar claro se a resposta veio da base interna do DilsAI ou de material temporário enviado pelo aluno.

## Próximo passo recomendado

Após este ciclo, iniciar OCR de imagem/PDF escaneado em ciclo separado.
