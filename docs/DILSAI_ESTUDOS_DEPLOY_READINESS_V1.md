# DilsAI Estudos — Deploy Readiness V1

Status: DILSAI_ESTUDOS_DEPLOY_READINESS_DEFINED_V1
Marco: v0.2.4-dilsai-estudos-deploy-readiness-v1

## Objetivo

Preparar o DilsAI Estudos para beta real em ambiente publicado, conferindo frontend, backend, variáveis de ambiente, rotas oficiais, limites de uso e riscos antes de liberar para usuários reais.

## Estado confirmado

- Frontend principal: index.html
- Script oficial ativo: script.js
- Backend FastAPI: backend/app/main.py
- Rotas oficiais:
  - GET /health
  - POST /api/v1/chat
  - POST /api/v1/materials/extract-text
- Frontend publicado previsto:
  - https://dilson123-tech.github.io/dilsai-landing/
- Backend de produção previsto:
  - https://dilsai-api.onrender.com

## Correção aplicada neste marco

Foi removido do index.html o carregamento legado de:

- config.js
- boot.js
- boot.js duplicado
- chatbox legado
- launcher legado

Motivo: o fluxo legado apontava para 127.0.0.1:8000 e /ask, o que poderia quebrar o chat no GitHub Pages.

Após a correção, a página carrega somente o script oficial:

- script.js

## Configuração esperada do frontend

O script.js define automaticamente:

- Local: http://127.0.0.1:8091
- Produção: https://dilsai-api.onrender.com

Rotas usadas pelo frontend:

- Chat: /api/v1/chat
- Extração de material: /api/v1/materials/extract-text

## Variáveis de ambiente do backend

Arquivo de referência:

- backend/.env.example

Variáveis obrigatórias para beta:

- APP_NAME
- APP_ENV
- APP_VERSION
- CORS_ALLOW_ORIGINS
- LLM_PROVIDER
- LLM_MODEL
- LLM_TEMPERATURE
- LLM_MAX_TOKENS
- OPENAI_API_KEY
- RATE_LIMIT_ENABLED
- RATE_LIMIT_WINDOW_SECONDS
- RATE_LIMIT_CHAT_PER_MINUTE
- RATE_LIMIT_MATERIAL_PER_MINUTE

## Atenção com chave OpenAI

Nunca commitar nem colar a chave real no chat, issue, PR ou documentação.

Se uma chave for exposta em terminal, print, chat ou log, ela deve ser tratada como comprometida:

1. Excluir ou rotacionar a chave antiga no painel da OpenAI.
2. Criar uma chave nova.
3. Atualizar apenas no .env local e nas variáveis secretas do provedor.
4. Testar novamente a API.

## Bloqueio atual conhecido

A integração OpenAI já foi testada com chave presente, mas retornou ausência de créditos disponíveis.

Antes do beta real, é obrigatório confirmar:

- chave ativa;
- crédito ou saldo ativo;
- chamada real ao modelo funcionando;
- fallback seguro funcionando quando a OpenAI falhar.

## Checklist de deploy

### Frontend

- [x] index.html não carrega mais scripts legados.
- [x] script.js é o único script principal do DilsAI Estudos.
- [x] Links de termos e privacidade apontam para seções reais.
- [ ] Publicação do GitHub Pages conferida no navegador.
- [ ] Chat testado no domínio publicado.

### Backend

- [x] /health existe.
- [x] /api/v1/chat existe.
- [x] /api/v1/materials/extract-text existe.
- [x] Rate limit ativo para rotas caras.
- [ ] Backend publicado confirmado.
- [ ] Variáveis de ambiente configuradas no provedor.
- [ ] CORS de produção conferido.
- [ ] OpenAI com crédito ativo confirmada.

## Testes mínimos antes de liberar usuário real

- node --check script.js
- cd backend && source .venv/bin/activate && pytest -q
- curl http://127.0.0.1:8091/health
- curl https://dilsai-api.onrender.com/health

## Decisão

O DilsAI Estudos pode avançar para beta real somente após:

1. confirmar backend publicado;
2. confirmar frontend chamando o backend correto;
3. confirmar chave OpenAI nova e segura;
4. confirmar saldo ou crédito OpenAI ativo;
5. testar chat real no domínio publicado.
