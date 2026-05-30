# DilsAI Estudos — Backend

Backend FastAPI do DilsAI Estudos.

## Objetivo

Fornecer uma API para uma IA de estudos com respostas didáticas, modos de estudo, temas organizados, política contra resposta inventada e configuração segura por variável de ambiente.

## Rodar localmente

1. Entrar na pasta backend:

cd backend

2. Criar ambiente virtual local:

python3 -m venv .venv

3. Ativar ambiente:

source .venv/bin/activate

4. Instalar dependências:

pip install -r requirements.txt

5. Criar arquivo de ambiente:

cp .env.example .env

6. Rodar API:

uvicorn app.main:app --reload --host 127.0.0.1 --port 8091

## Endpoints

Health:

curl http://127.0.0.1:8091/health

Chat:

curl -s -X POST http://127.0.0.1:8091/api/v1/chat -H "Content-Type: application/json" -d '{"user_name":"Dilson","message":"Explique o que é uma API em programação.","topic":"programacao","mode":"professor"}'

Modo Fonte Segura:

curl -s -X POST http://127.0.0.1:8091/api/v1/chat -H "Content-Type: application/json" -d '{"user_name":"Dilson","message":"Resuma o conteúdo enviado.","topic":"geral","mode":"fonte_segura","context":"Uma API permite que sistemas diferentes conversem usando regras definidas."}'

## Variáveis de ambiente

Copie backend/.env.example para backend/.env.

Nunca commitar backend/.env com chave real.

## Segurança

- Não usar chave fixa no código.
- Não commitar venv.
- Não commitar __pycache__.
- Restringir CORS por ambiente.
- Usar resposta segura quando faltar contexto.
