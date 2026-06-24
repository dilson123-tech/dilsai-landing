# DilsAI Estudos — Beta Launch Notes V1

## Objetivo

Registrar as notas oficiais de lançamento do beta do DilsAI Estudos.

Este documento prepara a comunicação do produto para a fase de beta público controlado, deixando claro o que já está disponível, o que pode ser testado, quais limites continuam existindo e o que ainda não deve ser prometido.

Este documento parte da tag:

v0.1.38-dilsai-estudos-beta-public-readiness-v1

## Nome do marco

DilsAI Estudos Beta Público Controlado

## Status do lançamento

O DilsAI Estudos está em fase de preparação para beta público controlado.

Isso significa:

- produto real;
- fluxo principal funcionando;
- uso com usuários reais em ambiente controlado;
- limites claros;
- comunicação responsável;
- evolução gradual para SaaS.

Isso não significa:

- produto final;
- SaaS completo;
- uso ilimitado;
- cobrança pronta;
- login pronto;
- histórico pronto;
- painel administrativo pronto.

## Frase curta oficial

O DilsAI Estudos é uma IA educacional para tirar dúvidas, resolver questões passo a passo e estudar com textos, PDFs, imagens e prints de forma responsável.

## Descrição oficial do beta

O DilsAI Estudos Beta Público Controlado permite que estudantes testem uma IA educacional capaz de responder dúvidas, explicar questões passo a passo e usar materiais enviados pelo próprio aluno como apoio de estudo.

O produto aceita pergunta digitada, questão colada em texto, imagem ou print com OCR e materiais simples como contexto.

A proposta do beta é validar a experiência real de estudo com IA, mantendo limites de uso, comunicação honesta e posicionamento responsável.

## Para quem é este beta

Este beta é indicado para:

- estudantes que querem entender questões;
- pessoas que precisam de explicação passo a passo;
- alunos que estudam por textos, PDFs, imagens ou prints;
- usuários que querem testar uma IA como apoio de aprendizado;
- parceiros que querem avaliar o potencial educacional do produto.

## Para quem este beta não é

Este beta não é indicado para:

- uso como cola;
- captura escondida de tela;
- fraude em provas;
- promessa de aprovação;
- substituição de professor;
- substituição de escola, curso ou material oficial;
- uso profissional crítico sem revisão humana;
- uso ilimitado ou sem controle.

## O que já está disponível no beta

### Pergunta digitada

O usuário pode digitar uma dúvida e receber uma explicação educacional.

Exemplo:

Explique de forma simples o que é uma API em programação.

### Questão colada em texto

O usuário pode colar uma questão no campo principal e pedir explicação passo a passo.

Exemplo:

Uma escola tem 240 alunos. Em uma pesquisa, 35% dos alunos disseram que participam de atividades esportivas.

Resultado esperado:

O DilsAI explica que 35% de 240 é 84.

### Imagem ou print com OCR

O usuário pode enviar ou colar uma imagem/print legível contendo uma questão.

Resultado esperado:

O DilsAI tenta ler o conteúdo com OCR, usa o texto extraído como contexto e responde de forma educacional.

### Material próprio como contexto

O usuário pode usar textos, PDFs ou imagens como apoio para estudar.

Resultado esperado:

O DilsAI considera o material enviado e evita inventar quando não houver base suficiente.

### Resposta educacional

A resposta deve priorizar:

- explicação simples;
- passo a passo;
- clareza;
- aprendizado;
- honestidade quando faltar contexto.

### Mensagens amigáveis

O produto já possui mensagens mais amigáveis para situações como:

- erro de conexão;
- API indisponível;
- arquivo inválido;
- arquivo grande;
- arquivo vazio;
- leitura ruim;
- OCR insuficiente;
- resposta indisponível.

## O que foi validado antes deste lançamento

Antes das notas de lançamento, o projeto já validou:

- Chat V3 aprovado.
- Campo principal de pergunta funcionando.
- Campo de contexto funcionando.
- Upload de material simples funcionando.
- PDF textual suportado.
- Imagem/print com OCR suportado.
- PDF escaneado via OCR suportado.
- API OpenAI paga testada.
- OCR real testado.
- Resposta educacional passo a passo.
- Onboarding beta aplicado.
- Mensagens amigáveis aplicadas.
- Roteiro de demonstração beta documentado.
- Landing page com apresentação mais comercial.
- Checklist final de beta público controlado documentado.

Marco técnico principal:

DILSAI_CHAT_V3_REAL_OCR_TEST_OK

## Como apresentar o beta

Apresentação curta recomendada:

O DilsAI Estudos é uma IA educacional em beta controlado. Ele ajuda o aluno a tirar dúvidas, entender questões passo a passo e estudar usando texto, PDF, imagem ou print. A proposta é apoiar o aprendizado de forma responsável, não substituir professor nem servir para cola.

## O que demonstrar

Durante uma demonstração, mostrar:

- uma pergunta simples digitada;
- uma questão colada em texto;
- uma imagem ou print legível;
- uma mensagem amigável quando algo falhar;
- o posicionamento de apoio ao estudo.

## O que evitar na demonstração

Evitar demonstrar:

- uso em prova real;
- promessa de acerto absoluto;
- arquivos grandes;
- imagens ruins de propósito como caso principal;
- captura escondida;
- discurso de cola;
- qualquer fluxo que pareça fraude;
- cobrança ou login como se já estivessem prontos.

## Limites oficiais do beta

### Limite educacional

O DilsAI Estudos ajuda a estudar.

Ele não substitui professor, escola, curso, livro ou revisão humana.

### Limite de precisão

A IA pode errar.

O OCR pode ler errado.

O usuário deve revisar a resposta, principalmente em questões importantes.

### Limite de imagem

Imagens ruins, tortas, escuras, cortadas ou com texto pequeno podem prejudicar a leitura.

Orientação oficial:

Enviar imagem nítida, bem cortada e com a questão legível.

### Limite de material

Materiais longos devem ser enviados por partes.

Orientação oficial:

Mandar uma questão por vez para melhorar a qualidade da resposta.

### Limite de uso

O beta deve ser controlado.

Limite recomendado inicial:

- até 10 perguntas por dia por usuário beta;
- até 3 imagens/prints por dia por usuário beta;
- até 1 PDF/material maior por dia por usuário beta, quando aplicável.

### Limite operacional

A resposta depende de API configurada, crédito disponível e ambiente técnico funcionando.

Se a IA estiver indisponível, o produto deve orientar o usuário a tentar novamente mais tarde ou acionar suporte.

## O que ainda não está pronto

O beta ainda não possui:

- login de usuário;
- histórico de perguntas;
- controle real de uso por usuário;
- controle real de custo por usuário;
- planos grátis e pagos;
- cobrança;
- painel administrativo;
- monitoramento completo;
- suporte formal estruturado;
- deploy público final documentado como produção estável.

## Riscos conhecidos

### Expectativa exagerada

Risco:

Usuário acreditar que a IA sempre acerta.

Mitigação:

Comunicar que o DilsAI é apoio de estudo e pode errar.

### OCR ruim

Risco:

Imagem ruim gerar resposta imprecisa.

Mitigação:

Orientar envio de imagem nítida ou texto colado.

### Custo de API

Risco:

Uso excessivo gerar custo inesperado.

Mitigação:

Manter beta controlado e implementar limites reais nas próximas versões.

### Uso indevido

Risco:

Usuário tentar usar para cola ou fraude.

Mitigação:

Reforçar uso responsável e não posicionar o produto como ferramenta de burlar avaliações.

### Produto incompleto

Risco:

Usuário esperar SaaS completo.

Mitigação:

Comunicar claramente que é beta público controlado, não produto final.

## Mensagem pública recomendada

O DilsAI Estudos está entrando em fase beta controlada.

Nesta fase, o produto já permite tirar dúvidas, colar questões, enviar prints/imagens e usar materiais próprios como apoio para receber explicações passo a passo.

Ainda é uma versão beta: a IA pode errar, o OCR pode falhar e alguns recursos como login, histórico, planos e cobrança ainda serão implementados em fases futuras.

Use como apoio de estudo, não como substituto de professor nem como forma de burlar avaliações.

## Checklist antes de anunciar o beta

Antes de anunciar o beta publicamente, confirmar:

- [ ] main limpa;
- [ ] sem PRs abertos;
- [ ] tag v0.1.39 criada;
- [ ] smoke test final planejado;
- [ ] demonstração simples funcionando;
- [ ] pergunta digitada validada;
- [ ] questão colada validada;
- [ ] imagem/print com OCR validado;
- [ ] mensagem de erro amigável validada;
- [ ] limites comunicados;
- [ ] uso responsável comunicado.

## Próximo marco recomendado

Após este documento, o próximo marco recomendado é:

v0.1.40-dilsai-estudos-beta-final-smoke-test-v1

Objetivo:

Executar e documentar o smoke test final antes do marco v0.2.0.

## Caminho para v0.2.0

Sequência recomendada:

v0.1.39-dilsai-estudos-beta-launch-notes-v1

v0.1.40-dilsai-estudos-beta-final-smoke-test-v1

v0.2.0-dilsai-estudos-beta-publico-controlado

## Decisão estratégica

O DilsAI Estudos já tem base suficiente para ser apresentado como beta público controlado.

A prioridade agora é validar o fluxo principal, comunicar limites com honestidade e evitar prometer SaaS completo antes da hora.

## Status

BETA_LAUNCH_NOTES_DEFINED_V1
