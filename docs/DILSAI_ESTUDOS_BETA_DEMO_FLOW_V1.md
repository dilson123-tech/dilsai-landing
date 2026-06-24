# DilsAI Estudos — Beta Demo Flow V1

## Objetivo

Definir um roteiro simples para demonstrar o DilsAI Estudos no beta.

A demonstração deve mostrar que o usuário pode digitar uma dúvida, colar uma questão, enviar ou colar um print/imagem e receber uma explicação passo a passo.

## Base técnica

Este fluxo parte da tag:

v0.1.35-dilsai-estudos-beta-friendly-errors-v1

Estado confirmado:

- Chat V3 aprovado.
- OCR real testado.
- API OpenAI paga testada.
- Onboarding beta aplicado na interface.
- Mensagens amigáveis de erro aplicadas.
- Backend preservado.
- OCR preservado.
- Fluxo de envio preservado.

## Demonstração 1 — pergunta digitada

Ação do usuário:

Explique de forma simples o que é uma API em programação.

Resultado esperado:

O DilsAI responde de forma educacional, com linguagem simples.

## Demonstração 2 — questão colada em texto

Ação do usuário:

Resolva esta questão e explique passo a passo:

Uma escola tem 240 alunos. Em uma pesquisa, 35% dos alunos disseram que participam de atividades esportivas.

Quantos alunos participam de atividades esportivas?

Resultado esperado:

O DilsAI calcula 35% de 240 = 84 e explica o raciocínio passo a passo.

## Demonstração 3 — print/imagem da questão

Ação do usuário:

Enviar uma imagem ou colar com Ctrl+V um print contendo uma questão legível.

Resultado esperado:

O DilsAI detecta a imagem, tenta usar OCR, carrega o conteúdo como contexto e responde com explicação passo a passo.

## Demonstração 4 — arquivo ruim ou grande

Ação do usuário:

Enviar arquivo inválido, grande demais ou imagem muito ruim.

Resultado esperado:

O DilsAI mostra mensagem amigável, sem erro técnico para o usuário.

## Frase curta para apresentar o produto

O DilsAI Estudos é uma IA educacional para tirar dúvidas, resolver questões passo a passo e usar materiais próprios como texto, PDF ou print, sempre como apoio de estudo.

## O que não demonstrar neste beta

Evitar demonstrar:

- uso para cola;
- captura escondida de tela;
- promessa de resposta perfeita;
- envio de arquivos enormes;
- uso como substituto de professor, escola ou curso;
- exposição de chave de API;
- logs técnicos para usuário final.

## Checklist antes da demonstração

Antes de apresentar:

- Confirmar que o backend está rodando, se for teste local.
- Confirmar que a API está ativa.
- Usar questão simples e legível.
- Usar print nítido.
- Não mostrar chave de API.
- Não prometer acerto absoluto.
- Explicar que IA e OCR podem errar.

## Status

BETA_DEMO_FLOW_DEFINED_V1
