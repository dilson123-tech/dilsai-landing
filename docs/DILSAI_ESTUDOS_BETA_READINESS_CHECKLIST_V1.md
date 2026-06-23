# DilsAI Estudos — Beta Readiness Checklist V1

## Objetivo

Registrar a régua de prontidão do DilsAI Estudos para uma primeira fase beta controlada, após a confirmação do fluxo real de imagem/print com OCR, contexto e API OpenAI paga.

Este documento parte da tag:

v0.1.30-dilsai-estudos-real-ocr-api-smoke-test-v1

## Estado atual confirmado

O DilsAI Estudos já possui uma base funcional validada:

- Chat V3 aprovado.
- Campo principal aceitando texto.
- Campo principal aceitando imagem/print enviado pelo usuário.
- OCR/contexto funcionando.
- Backend FastAPI funcionando localmente.
- Integração com API OpenAI paga funcionando.
- Resposta educacional explicada funcionando.
- Fonte exibida como Material enviado pelo aluno quando o contexto vem do usuário.
- Testes automatizados do backend passando.
- script.js validado com node --check.
- Documentação técnica dos marcos principais registrada.

Marco técnico mais importante confirmado:

DILSAI_CHAT_V3_REAL_OCR_TEST_OK

## O que já pode ser considerado pronto para beta controlado

### Núcleo de estudo

- [x] Usuário consegue enviar pergunta em texto.
- [x] Usuário consegue colar texto de questão.
- [x] Usuário consegue enviar imagem/print.
- [x] Sistema usa contexto do material enviado.
- [x] IA responde em modo professor.
- [x] IA explica passo a passo.
- [x] Sistema identifica fonte como material enviado pelo aluno.
- [x] Sistema evita depender apenas de resposta bonita sem contexto.

### Backend

- [x] FastAPI estruturado.
- [x] Endpoint /health existente.
- [x] Endpoint /api/v1/chat existente.
- [x] Integração com OpenAI API funcionando.
- [x] OPENAI_API_KEY mantida fora do Git.
- [x] pytest configurado com backend/pytest.ini.
- [x] Testes automatizados passando.

### Frontend

- [x] Chat V3 preservado.
- [x] Painel visual funcional.
- [x] Fluxo de imagem enviado no painel validado.
- [x] Resposta exibida com tema, modo, confiança e fonte.
- [x] Validação JS com node --check funcionando.

### Segurança e ética

- [x] Sem captura escondida.
- [x] Sem modo stealth.
- [x] Sem ferramenta de cola automática.
- [x] Envio de imagem/material feito de forma voluntária pelo usuário.
- [x] API key não exposta.
- [x] Produto posicionado como ferramenta de aprendizado.

## O que ainda falta antes de beta público

### Produto

- [ ] Definir público inicial do beta.
- [ ] Definir limite de uso por usuário.
- [ ] Definir plano gratuito ou demonstração.
- [ ] Definir mensagem clara de que o DilsAI ajuda a estudar, mas não substitui professor.
- [ ] Definir tela simples de boas-vindas para explicar como enviar questão.
- [ ] Definir política de uso aceitável para provas, concursos e avaliações.

### Técnico

- [ ] Definir ambiente de deploy.
- [ ] Configurar variáveis de ambiente em produção.
- [ ] Criar controle básico de erro quando faltar crédito na API.
- [ ] Criar aviso amigável quando OCR falhar ou vier texto ruim.
- [ ] Criar limite de tamanho para imagem/material.
- [ ] Criar proteção contra envio excessivo de requisições.
- [ ] Criar logs mínimos sem armazenar conteúdo sensível desnecessário.

### Comercial

- [ ] Definir nome final público.
- [ ] Definir promessa principal do produto.
- [ ] Definir preço inicial.
- [ ] Definir página de planos.
- [ ] Definir chamada para teste beta.
- [ ] Definir canal de suporte inicial.
- [ ] Preparar roteiro de demonstração.

## Regras para próximos PRs

Não mexer no OCR aprovado sem motivo forte.

Não reconstruir o Chat V3.

Não trocar a experiência principal sem antes documentar o motivo.

Não adicionar grande refatoração junto com ajuste comercial.

Priorizar PRs pequenos, testáveis e fáceis de reverter.

## Próximos PRs recomendados

### PR #34 — Beta usage limits V1

Objetivo:

Criar uma primeira camada simples de limites e mensagens para uso controlado.

Exemplos:

- limite operacional documentado;
- aviso quando arquivo for grande;
- mensagem amigável para erro de API;
- orientação para o usuário tentar novamente.

### PR #35 — Beta onboarding copy V1

Objetivo:

Melhorar a primeira experiência do usuário com textos claros:

- como enviar uma questão;
- como colar print;
- como pedir explicação;
- o que o DilsAI pode e não pode fazer.

### PR #36 — Beta demo script V1

Objetivo:

Criar um roteiro de demonstração para mostrar o produto a alunos, pais, professores ou parceiros.

## Decisão estratégica

O DilsAI Estudos já passou do ponto de protótipo técnico simples.

A próxima fase não deve ser inventar módulos grandes.

A próxima fase deve transformar o que já funciona em uma experiência confiável de beta controlado.

## Conclusão

O produto está tecnicamente pronto para uma fase beta interna/controlada, desde que o uso seja limitado, monitorado e apresentado como ferramenta de aprendizado.

Status:

BETA_CONTROLADA_TECNICAMENTE_VIAVEL

