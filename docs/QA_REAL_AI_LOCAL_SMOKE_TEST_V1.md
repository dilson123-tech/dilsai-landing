# QA — DilsAI Estudos Real AI Local Smoke Test V1

## 1. Objetivo

Registrar a primeira validação local da IA real no backend do DilsAI Estudos.

Este documento registra apenas o resultado técnico do smoke test. Nenhuma chave, segredo, token ou valor sensível deve ser incluído neste relatório.

## 2. Contexto

O DilsAI Estudos já tinha os seguintes marcos concluídos:

- v0.1.0-dilsai-estudos-product-plan
- v0.1.1-dilsai-estudos-backend-foundation
- v0.1.2-dilsai-estudos-frontend-chat-v1

Após a criação da chave da OpenAI pelo responsável do projeto, a chave foi configurada localmente apenas no arquivo backend/.env.

O arquivo backend/.env não deve ser versionado.

## 3. Ambiente de teste

Repositório:

- dilsai-landing

Backend local:

- FastAPI
- Porta: 8091
- Endpoint de saúde: /health
- Endpoint de chat: /api/v1/chat

Frontend local usado no ciclo anterior:

- Porta: 5500
- Chat oficial DilsAI Estudos conectado ao endpoint /api/v1/chat

## 4. Segurança da chave

A chave real foi configurada apenas localmente em:

- backend/.env

Regras mantidas:

- não colar chave no chat;
- não commitar backend/.env;
- não colocar chave no frontend;
- não colocar chave em index.html, script.js ou config.js;
- a comunicação com OpenAI deve passar pelo backend.

## 5. Teste executado

Foi executado um POST local para:

- http://127.0.0.1:8091/api/v1/chat

Payload usado:

- user_name: Dilson
- message: Explique o que é uma API em programação com exemplo simples.
- topic: programacao
- mode: professor

## 6. Resultado observado

O endpoint respondeu com:

- status: success
- mode: professor
- topic: programacao
- used_context: false
- confidence: general
- safety_notice: null

A resposta retornada foi gerada pela IA real, explicando o conceito de API em programação com exemplo simples.

## 7. Validação funcional

Resultado:

- Backend recebeu a requisição.
- Backend acionou o provedor de IA.
- IA retornou resposta real.
- Endpoint /api/v1/chat retornou JSON válido.
- O modo professor funcionou.
- O tema programacao foi aceito.
- O fallback sem chave deixou de ser usado quando OPENAI_API_KEY estava configurada localmente.

Status:

REAL_AI_LOCAL_SMOKE_TEST_OK

## 8. Observações

No terminal, alguns acentos podem aparecer escapados em formato Unicode, como \u00e9 e \u00e3. Isso é comportamento esperado de saída JSON no terminal e não indica erro funcional.

## 9. Próximo passo recomendado

Após este smoke test, o próximo ciclo técnico recomendado é iniciar a base de conhecimento/RAG.

Objetivo do próximo ciclo:

- criar estrutura inicial de materiais de estudo;
- permitir contexto/base por tema;
- responder com mais precisão;
- preparar citação/fonte de material;
- reforçar a regra de não inventar resposta quando faltar base.

