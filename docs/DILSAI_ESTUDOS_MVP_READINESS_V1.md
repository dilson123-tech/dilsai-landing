# DilsAI Estudos — MVP Readiness V1

## 1. Natureza do produto

O DilsAI Estudos é um produto real, com objetivo de virar uma plataforma educacional vendável.

Não é projeto de estudo, teste visual, protótipo descartável ou tela bonita sem função.

Este documento fecha o ciclo de MVP inicial após a tag `v0.1.19-dilsai-estudos-ocr-robustness-v1`.

A regra desta fase é simples: não refazer backend, não refazer frontend, não trocar arquitetura, não iniciar RAG/embeddings sem planejamento próprio e não quebrar upload, OCR, fallback, fonte ou rastreabilidade.

## 2. Estado do MVP

Régua atual: **MVP educacional inicial ~99% pronto**.

Entregas já consolidadas:

- backend FastAPI funcional;
- frontend estático funcional;
- tela cheia de estudos;
- seleção de nível, matéria e modo;
- base interna simples;
- resposta com fonte;
- exibição amigável de fonte no frontend;
- upload de `.txt` e `.md`;
- limpeza de material carregado;
- extração de PDF textual;
- OCR de imagem;
- OCR de PDF escaneado;
- fallback honesto quando OpenAI está indisponível;
- fonte formal para material enviado pelo aluno;
- labels amigáveis de fonte;
- documentação e QA por ciclo.

## 3. O que está fechado no MVP atual

### Produto e escopo

Status: **100% no MVP inicial**.

O produto ajuda estudantes a estudar com IA usando nível, matéria, modo de resposta e material próprio.

### Backend

Status: **100% no MVP inicial**.

Arquivos principais:

- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/schemas.py`
- `backend/app/services/llm.py`
- `backend/app/services/knowledge.py`
- `backend/app/services/prompts.py`
- `backend/app/knowledge/`

Endpoints principais:

- `GET /health`
- `POST /api/v1/chat`
- `POST /chat`
- `POST /api/v1/materials/extract-text`

### Frontend

Status: **100% no MVP inicial**.

Arquivos principais:

- `index.html`
- `script.js`
- `styles.css`

O fluxo de tela cheia já está validado para uso local, apresentação e piloto controlado.

### Base interna simples

Status: **100% no MVP inicial**.

Base atual:

- `backend/app/knowledge/ensino_medio/biologia/fotossintese.md`
- `backend/app/knowledge/geral/programacao/api.md`

### Upload e extração de material

Status: **100% no MVP inicial**.

Tipos aceitos:

- `.txt`
- `.md`
- `.pdf`
- `.png`
- `.jpg`
- `.jpeg`
- `.webp`

### OCR

Status: **100% no MVP inicial**.

OCR atual cobre:

- imagem enviada pelo aluno;
- PDF escaneado;
- aviso honesto de possível erro;
- limite operacional inicial para PDF escaneado.

### Fallback seguro

Status: **100% no MVP inicial**.

Quando a IA externa falha, o sistema não inventa resposta. Ele usa o contexto enviado pelo aluno e informa claramente que é um apoio determinístico preliminar.

## 4. Limites honestos do MVP

Este MVP ainda não promete:

- RAG com embeddings;
- memória persistente do aluno;
- login;
- plano pago;
- dashboard administrativo;
- correção automática perfeita;
- OCR perfeito;
- leitura perfeita de documento ruim, torto, borrado ou manuscrito;
- armazenamento permanente de arquivos enviados pelo aluno.

Esses pontos são evolução futura, não falha do MVP atual.

## 5. Requisitos locais

Dependências Python principais:

- FastAPI;
- Uvicorn;
- OpenAI SDK;
- pypdf;
- Pillow;
- pytesseract;
- pdf2image;
- pydantic;
- pydantic-settings;
- python-dotenv.

Dependências de sistema para OCR:

```bash
sudo apt-get install -y tesseract-ocr tesseract-ocr-por tesseract-ocr-eng poppler-utils
```

Validação recomendada:

```bash
which tesseract
tesseract --version
tesseract --list-langs
which pdftoppm
pdftoppm -v
```

## 6. Como rodar localmente

Backend:

```bash
cd ~/projetos/dilsai-landing/backend
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8091 --reload
```

Health:

```bash
curl -s http://127.0.0.1:8091/health | python -m json.tool
```

Frontend:

```bash
cd ~/projetos/dilsai-landing
python3 -m http.server 5500
```

URL local:

```text
http://127.0.0.1:5500
```

## 7. Checklist de validação manual

Antes de apresentar o MVP, validar:

- backend sobe sem erro;
- `/health` responde;
- frontend abre;
- botão “Estudar em tela cheia” funciona;
- nível, matéria e modo aparecem corretamente;
- pergunta simples retorna resposta;
- base interna mostra fonte;
- upload `.txt` ou `.md` preenche contexto;
- PDF textual é extraído;
- imagem gera OCR;
- PDF escaneado gera OCR;
- fonte aparece de forma amigável;
- botão limpar material funciona;
- fallback com contexto funciona se OpenAI estiver indisponível;
- nenhum `.env` é commitado;
- nenhuma chave externa aparece em código ou documentação.

## 8. Regras de segurança e qualidade

O DilsAI Estudos deve continuar seguindo estas regras:

- não fingir que leu material quando não leu;
- não fingir que OCR é perfeito;
- não esconder falha da IA externa;
- não expor chave OpenAI;
- não commitar `.env`;
- não salvar arquivo do aluno sem contrato explícito;
- não misturar material temporário do aluno com base interna permanente;
- manter fonte e rastreabilidade sempre que possível;
- separar o próximo ciclo de RAG/embeddings em PR próprio.

## 9. Próximos blocos pós-MVP

Depois deste fechamento, os próximos caminhos são:

### Opção 1 — RAG/embeddings planejado

Antes de codar:

- definir armazenamento;
- definir indexação;
- definir limpeza;
- separar base interna de material do aluno;
- garantir citação de fonte;
- evitar resposta inventada.

### Opção 2 — OCR V2

Melhorias possíveis:

- pré-processamento de imagem;
- contraste;
- orientação;
- limite configurável;
- melhor mensagem visual para OCR parcial.

### Opção 3 — Piloto comercial

Preparar:

- roteiro de demonstração;
- landing melhorada;
- termos simples;
- plano inicial;
- público-alvo;
- checklist de implantação.

## 10. Conclusão

O MVP inicial do DilsAI Estudos está tecnicamente fechado para demonstração e piloto controlado.

O próximo avanço pesado deve ser feito em ciclo próprio, principalmente se envolver RAG/embeddings.

Checkpoint:

`DILSAI_ESTUDOS_MVP_READINESS_V1_OK`
