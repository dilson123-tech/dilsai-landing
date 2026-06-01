# DilsAI Estudos — Source Response V1

## Status

DILSAI_ESTUDOS_SOURCE_RESPONSE_V1

## Objetivo

Adicionar metadados formais de fonte na resposta da API do DilsAI Estudos.

Este marco transforma a base interna simples em uma resposta mais confiável, permitindo que frontend, aluno, professor ou parceiro saibam qual material interno foi usado para apoiar a resposta.

## Campos adicionados ao ChatResponse

- source_title
- source_path
- source_type
- source_score

## Fonte interna inicial

Quando a base interna Markdown for encontrada, a API retorna:

- source_title: título extraído do arquivo Markdown.
- source_path: caminho relativo dentro de backend/app/knowledge.
- source_type: internal_markdown.
- source_score: pontuação determinística da busca simples.

## Regra de produto

O DilsAI Estudos não deve fingir fonte.

Se nenhuma fonte interna for encontrada, os campos de fonte devem permanecer nulos.

## Próximo passo recomendado

Depois deste marco, evoluir para exibir fonte com mais destaque no frontend e preparar o contrato para upload explícito de material.
