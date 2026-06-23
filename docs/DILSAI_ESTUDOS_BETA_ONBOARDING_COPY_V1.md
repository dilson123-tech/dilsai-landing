# DilsAI Estudos — Beta Onboarding Copy V1

## Objetivo

Definir os textos iniciais de orientação para a fase beta controlada do DilsAI Estudos.

Este documento parte da tag:

v0.1.32-dilsai-estudos-beta-usage-limits-v1

A intenção é preparar uma comunicação clara para o usuário antes de implementar esses textos no frontend.

Este PR não altera o Chat V3, OCR, backend ou comportamento da aplicação.

## Princípio de comunicação

O usuário deve entender rapidamente:

- o que o DilsAI faz;
- como enviar uma questão;
- como colar um print;
- como pedir explicação;
- o que fazer quando a imagem estiver ruim;
- que o produto é apoio de estudo, não ferramenta de cola.

## Texto principal de boas-vindas

Texto recomendado:

Bem-vindo ao DilsAI Estudos.

Envie uma pergunta, cole o texto de uma questão ou mande um print/imagem para eu explicar passo a passo.

Eu vou ajudar você a entender o conteúdo, encontrar o raciocínio e estudar com mais clareza.

## Texto curto para o topo do chat

Texto recomendado:

Envie sua dúvida, texto ou print da questão. O DilsAI explica passo a passo.

## Texto para campo principal

Placeholder recomendado:

Cole sua pergunta, texto da questão ou envie um print aqui...

## Texto para envio de imagem/print

Texto recomendado:

Você pode enviar um print da questão. Para melhorar a leitura, recorte apenas a questão e use uma imagem nítida.

## Texto após imagem enviada

Texto recomendado:

Imagem recebida. Vou tentar ler o conteúdo e usar como contexto para explicar a questão.

## Texto quando OCR funcionar

Texto recomendado:

Consegui usar o conteúdo da imagem como contexto. Agora vou explicar a questão passo a passo.

## Texto quando OCR estiver ruim

Texto recomendado:

Não consegui ler a imagem com segurança. Tente enviar um print mais nítido ou cole o texto da questão.

## Texto quando faltar contexto

Texto recomendado:

Preciso ver a questão ou o material para responder com precisão. Envie o texto, um print ou uma imagem da questão.

## Texto quando o usuário pedir só a resposta

Texto recomendado:

Posso te ajudar com a resposta, mas vou explicar o raciocínio também para você aprender o passo a passo.

## Texto ético curto

Texto recomendado:

Use o DilsAI como apoio de estudo. Ele ajuda a entender questões e conteúdos, não a burlar avaliações.

## Texto ético completo

Texto recomendado:

O DilsAI Estudos é uma ferramenta de aprendizado. Ele ajuda você a revisar conteúdos, entender questões, estudar para provas e praticar raciocínio.

Use de forma responsável. Não use para fraudar avaliações, colar em provas ou burlar regras da sua escola, curso ou instituição.

## Texto para API/crédito indisponível

Texto recomendado:

No momento a IA está temporariamente indisponível. Tente novamente em alguns minutos. Se o problema continuar, o suporte precisa verificar a configuração ou o crédito da API.

## Texto para limite de uso

Texto recomendado:

Você atingiu o limite de uso do beta por hoje. Volte mais tarde ou aguarde a liberação de novas tentativas.

## Texto para arquivo grande

Texto recomendado:

Esse arquivo parece grande demais para o beta atual. Tente enviar uma imagem menor, de preferência um print recortado apenas da questão.

## Texto para material longo

Texto recomendado:

Esse material parece longo. Para uma resposta melhor, envie uma questão por vez ou divida o conteúdo em partes menores.

## Texto para resposta com fonte do aluno

Texto recomendado:

Fonte usada: material enviado pelo aluno.

## Texto para resposta com base interna

Texto recomendado:

Fonte usada: base de estudos do DilsAI.

## Texto para falta de fonte segura

Texto recomendado:

Não encontrei uma fonte segura suficiente para afirmar isso com precisão. Envie mais material ou reformule a pergunta.

## Microcopy dos botões

### Botão enviar

Enviar

### Botão limpar

Limpar

### Botão nova conversa

Nova conversa

### Botão anexar imagem

Enviar imagem

### Botão tentar novamente

Tentar novamente

## Primeira experiência recomendada

Ao abrir o beta, o usuário deve ver uma mensagem simples:

Olá! Eu sou o DilsAI Estudos.

Você pode:
1. Digitar uma dúvida.
2. Colar o texto de uma questão.
3. Enviar um print ou imagem da questão.

Eu vou explicar passo a passo, como professor.

## Exemplo de pergunta sugerida

Resolva essa questão e explique passo a passo.

## Exemplo de orientação para print

Tire um print claro da questão, cole aqui no chat e escreva:

Resolva essa questão e explique passo a passo.

## Tom de voz

O tom do DilsAI deve ser:

- claro;
- educativo;
- paciente;
- direto;
- amigável;
- honesto quando faltar informação.

O tom não deve ser:

- arrogante;
- técnico demais;
- frio;
- vendedor exagerado;
- permissivo com cola ou fraude;
- confiante quando o material estiver incompleto.

## Regras para implementação futura

Quando estes textos forem implementados:

- não reconstruir o Chat V3;
- não mexer no OCR aprovado sem necessidade;
- manter o composer principal aprovado;
- implementar por partes pequenas;
- validar com node --check script.js;
- validar backend com pytest quando houver mudança de backend;
- manter mensagens simples no frontend.

## Próximo passo recomendado

Criar PR técnico pequeno para implementar apenas os textos de onboarding mais importantes no frontend, sem alterar o fluxo aprovado.

Sugestão de próximo marco:

v0.1.34-dilsai-estudos-beta-onboarding-ui-v1

## Status

BETA_ONBOARDING_COPY_DEFINED_V1
