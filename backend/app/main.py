from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Criar a aplicação FastAPI
app = FastAPI(
    title="DilsAI API",
    description="API da sua IA pessoal e profissional",
    version="1.0.0"
)

# Configurar CORS para permitir o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar OpenAI (vamos usar uma chave de teste por enquanto)
openai.api_key = "sua_chave_aqui"

# Modelo para receber mensagens
class ChatMessage(BaseModel):
    message: str
    user_name: str = "Usuário"

# Endpoint principal da IA
@app.post("/chat")
async def chat_with_ai(chat: ChatMessage):
    try:
        # Resposta básica por enquanto
        response_text = f"Olá {chat.user_name}! Recebi sua mensagem: '{chat.message}'. Esta é uma resposta de teste da DilsAI!"
        
        return {
            "response": response_text,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint de teste
@app.get("/")
async def root():
    return {"message": "DilsAI API está funcionando!"}

# Endpoint de saúde
@app.get("/health")
async def health():
    return {"status": "ok", "message": "API funcionando perfeitamente!"}
