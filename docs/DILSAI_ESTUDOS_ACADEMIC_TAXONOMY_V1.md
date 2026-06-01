# DilsAI Estudos — Academic Taxonomy V1

## Status

DILSAI_ESTUDOS_ACADEMIC_TAXONOMY_V1

## Objetivo

Oficializar a primeira taxonomia acadêmica do DilsAI Estudos para alinhar frontend, backend e prompt base.

Este marco transforma a seleção de nível, matéria e modo em contrato técnico explícito, reduzindo risco de erro 422 e preparando o caminho para base de conhecimento, resposta com fonte, upload explícito de material, OCR e RAG.

## Níveis oficiais

- Geral
- Ensino Fundamental I
- Ensino Fundamental II
- Ensino Médio
- Curso Técnico
- Concurso
- Universidade

## Matérias/áreas oficiais

- Geral
- Matemática e lógica
- Português
- Redação
- Programação
- Informática
- Direito
- Administração
- Física
- Química
- Biologia
- História
- Geografia
- Inglês
- Filosofia
- Sociologia
- Engenharia
- Saúde
- Humanas
- Negócios

## Modos oficiais

- Professor
- Direto
- Resumo
- Passo a passo
- Revisão
- Simulado
- Fonte segura

## Mudanças técnicas

- Adicionado `StudyLevel` no backend.
- Expandido `StudyTopic` no backend.
- Adicionado modo `resumo` no backend.
- Prompt base passou a receber nível do aluno.
- Frontend passou a normalizar nível, matéria e modo antes de enviar para a API.
- Tela cheia passou a enviar `level` no payload.
- Selects da tela cheia passaram a ser populados pela taxonomia oficial do JavaScript.
- Mantida compatibilidade com valores antigos como `matematica`, convertendo para `matematica_logica`.

## Regra de produto

O DilsAI Estudos continua sendo uma ferramenta de aprendizado e preparação.

Não é ferramenta de cola.
Não usa captura escondida.
Não finge fonte.
Não promete aprovação.
Não inventa base quando o material não foi enviado.

## Próximo passo recomendado

Depois deste marco, o próximo ciclo recomendado é Base de Conhecimento Simples V1, ainda sem embeddings, usando arquivos internos por nível/matéria e busca determinística simples.
