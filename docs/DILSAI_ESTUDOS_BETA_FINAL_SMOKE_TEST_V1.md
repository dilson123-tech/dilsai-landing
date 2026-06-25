# DilsAI Estudos — Beta Final Smoke Test V1

## Objetivo

Registrar o plano e a régua final de smoke test do DilsAI Estudos antes do marco v0.2.0.

Este documento define as validações mínimas que precisam estar conferidas antes de apresentar o produto como Beta Público Controlado.

Este documento parte da tag:

v0.1.39-dilsai-estudos-beta-launch-notes-v1

## Nome do marco

DilsAI Estudos Beta Final Smoke Test V1

## Decisão principal

O DilsAI Estudos já possui base técnica e documental suficiente para chegar ao Beta Público Controlado.

Antes da v0.2.0, a decisão correta é validar o fluxo principal ponta a ponta, sem reconstruir interface, sem mexer no OCR aprovado e sem iniciar módulos grandes.

## Escopo deste smoke test

Este smoke test cobre:

- estado do repositório;
- validação estática do frontend;
- validação automatizada do backend;
- pergunta digitada;
- questão colada em texto;
- imagem ou print com OCR;
- PDF ou material próprio;
- mensagens amigáveis de erro;
- comunicação de limites;
- uso responsável.

## Fora do escopo deste smoke test

Este smoke test não cobre:

- login de usuário;
- histórico de perguntas;
- cobrança;
- planos pagos;
- painel administrativo;
- analytics;
- monitoramento completo;
- deploy definitivo de produção;
- reconstrução de interface;
- alteração do OCR;
- alteração do Chat V3;
- troca de arquitetura.

## Estado esperado antes dos testes

Antes de executar os testes finais, o projeto deve estar assim:

- main limpa;
- main alinhada com origin/main;
- sem PRs abertos;
- última tag publicada: v0.1.39-dilsai-estudos-beta-launch-notes-v1;
- branch de smoke test criada a partir da main;
- sem alterações locais fora do documento de smoke test.

## Validações técnicas obrigatórias

### Validação de JavaScript

Comando:

```bash
node --check script.js
```

Resultado esperado:

- comando sem erro;
- nenhuma quebra de sintaxe no frontend.

### Validação automatizada do backend

Comando:

```bash
cd backend
source .venv/bin/activate
pytest -q
cd ..
```

Resultado esperado:

- testes automatizados passando;
- nenhuma regressão básica no backend;
- nenhuma alteração necessária no OCR ou Chat V3.

### Validação de estado Git

Comando:

```bash
git status -sb
git log --oneline -5
git tag --list "v0.1.*" | sort -V | tail -10
gh pr list --state open
```

Resultado esperado:

- branch correta;
- alterações controladas;
- histórico recente correto;
- tags recentes corretas;
- sem PRs abertos antes da abertura do PR atual.

## Smoke test funcional recomendado

### Teste 1 — pergunta digitada

Entrada recomendada:

Explique de forma simples o que é uma API em programação.

Resultado esperado:

- DilsAI responde em tom educacional;
- explica de forma simples;
- não inventa contexto externo desnecessário;
- resposta serve como apoio de estudo.

Status:

- [ ] Pendente de execução final antes da v0.2.0.

### Teste 2 — questão colada em texto

Entrada recomendada:

Uma escola tem 240 alunos. Em uma pesquisa, 35% dos alunos disseram que participam de atividades esportivas.

Quantos alunos participam de atividades esportivas?

Resultado esperado:

- DilsAI calcula 35% de 240;
- resposta esperada: 84 alunos;
- explica o raciocínio passo a passo;
- linguagem acessível para estudante.

Status:

- [ ] Pendente de execução final antes da v0.2.0.

### Teste 3 — imagem ou print com OCR

Entrada recomendada:

Enviar ou colar um print legível contendo uma questão simples.

Resultado esperado:

- DilsAI reconhece que existe imagem/print;
- tenta executar OCR;
- usa o texto extraído como contexto;
- responde com explicação passo a passo;
- não promete leitura perfeita.

Status:

- [ ] Pendente de execução final antes da v0.2.0.

### Teste 4 — material próprio como contexto

Entrada recomendada:

Enviar um texto curto, PDF textual simples ou material próprio permitido pelo beta.

Resultado esperado:

- DilsAI usa o material enviado como apoio;
- identifica que a resposta depende do contexto;
- evita inventar se faltar informação suficiente;
- mantém tom educacional.

Status:

- [ ] Pendente de execução final antes da v0.2.0.

### Teste 5 — erro amigável

Entrada recomendada:

Simular arquivo inválido, arquivo grande, arquivo vazio ou falha de leitura.

Resultado esperado:

- produto não mostra erro técnico bruto;
- mensagem orienta o usuário;
- não expõe chave, stack trace ou detalhe interno;
- mantém experiência amigável.

Status:

- [ ] Pendente de execução final antes da v0.2.0.

## Checklist de comunicação do beta

Antes da v0.2.0, confirmar:

- [ ] produto apresentado como apoio de estudo;
- [ ] sem promessa de resposta perfeita;
- [ ] sem promessa de aprovação;
- [ ] sem discurso de cola;
- [ ] sem captura escondida;
- [ ] sem modo stealth;
- [ ] OCR comunicado como sujeito a falhas;
- [ ] IA comunicada como sujeita a erro;
- [ ] limites de uso comunicados;
- [ ] falta de login, histórico e cobrança comunicada como limitação atual.

## Checklist de produto

Antes da v0.2.0, confirmar:

- [ ] pergunta digitada validada;
- [ ] questão colada validada;
- [ ] imagem/print com OCR validado;
- [ ] material próprio validado;
- [ ] erro amigável validado;
- [ ] landing revisada;
- [ ] frase curta comercial mantida;
- [ ] roteiro de demonstração mantido;
- [ ] notas de lançamento mantidas;
- [ ] checklist de prontidão mantido.

## Checklist de engenharia

Antes da v0.2.0, confirmar:

- [ ] node --check script.js passando;
- [ ] pytest -q passando no backend;
- [ ] main limpa;
- [ ] sem PRs abertos;
- [ ] tag v0.1.40 criada após merge;
- [ ] sem alterações em backend neste marco;
- [ ] sem alterações em OCR neste marco;
- [ ] sem alterações no Chat V3 neste marco;
- [ ] sem alterações de arquitetura neste marco.

## Riscos observados

### OCR pode falhar

Imagens ruins, cortadas, tortas ou escuras podem prejudicar a leitura.

Mitigação:

Orientar o usuário a enviar print nítido ou colar o texto da questão.

### IA pode errar

A resposta pode conter erro de interpretação ou cálculo.

Mitigação:

Manter comunicação de apoio de estudo e revisão humana.

### API pode ficar indisponível

A resposta depende de crédito, chave e disponibilidade da API.

Mitigação:

Mostrar mensagem amigável e não expor erro técnico.

### Usuário pode esperar SaaS completo

O produto ainda não tem login, histórico, cobrança e painel admin.

Mitigação:

Comunicar claramente que é beta público controlado, não versão final SaaS.

### Usuário pode tentar uso indevido

Existe risco de tentativa de cola ou fraude.

Mitigação:

Reforçar uso responsável e não posicionar o produto como ferramenta para burlar avaliações.

## Critério para avançar para v0.2.0

O projeto pode avançar para v0.2.0 quando:

- smoke test funcional principal estiver conferido;
- documentação beta estiver completa;
- comunicação pública estiver honesta;
- limites estiverem claros;
- main estiver limpa;
- tags estiverem publicadas;
- não houver PRs abertos;
- não houver regressão básica identificada.

## Próximo marco recomendado

Após este documento, o próximo marco recomendado é:

v0.2.0-dilsai-estudos-beta-publico-controlado

Objetivo:

Marcar oficialmente o DilsAI Estudos como Beta Público Controlado.

## Decisão estratégica

A v0.1.40 deve ser a última checagem antes da v0.2.0.

O foco não é adicionar recurso novo.

O foco é provar que o que já existe pode ser apresentado com segurança, limite e honestidade.

## Status

BETA_FINAL_SMOKE_TEST_DEFINED_V1
