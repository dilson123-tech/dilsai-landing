from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="DilsAI API")

class AskRequest(BaseModel):
    question: str

@app.get("/status")
def status():
    return {"ok": True, "app": "DilsAI API"}

@app.post("/ask")
def ask(req: AskRequest):
    return {"answer": f"Pergunta recebida: {req.question}", "source": "mock"}
