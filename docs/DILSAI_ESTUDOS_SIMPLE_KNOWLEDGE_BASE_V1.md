# DilsAI Estudos — Simple Knowledge Base V1

## Status

DILSAI_ESTUDOS_SIMPLE_KNOWLEDGE_BASE_V1

## Objetivo

Criar a primeira base de conhecimento simples do DilsAI Estudos, sem embeddings e sem RAG vetorial.

Este ciclo adiciona arquivos internos em Markdown e uma busca determinística inicial por nível, matéria e palavras-chave.

## Escopo

Incluído:

- serviço `app.services.knowledge`;
- busca local em arquivos `.md`;
- base inicial de Biologia sobre fotossíntese;
- base inicial de Programação sobre API;
- injeção de base interna no contexto do prompt;
- `used_context=true` quando base interna for encontrada;
- fallback honesto usando base interna quando o provedor externo de IA estiver indisponível.

Fora do escopo:

- embeddings;
- banco vetorial;
- upload de arquivo;
- OCR;
- ranking semântico avançado;
- resposta com campo formal de fonte no schema.

## Regra de produto

A base interna deve ajudar o aluno com precisão, mas não deve fingir fonte externa.

Quando o material interno for usado, ele deve ser tratado como base interna DilsAI Estudos.

## Próximo passo recomendado

Após este marco, implementar Resposta com Fonte V1, adicionando metadados de fonte no schema de resposta.
