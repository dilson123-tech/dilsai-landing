# DilsAI Estudos — Chat Seco V3 OCR Layer QA

## Status

Camada OCR adicionada ao `chat-clean-v3.html` com sucesso.

O Chat Seco V3 preserva a UX aprovada do composer: o aluno cola print com Ctrl+V, arrasta imagem ou usa o botão `+`; a imagem fica anexada no campo antes do envio.

## Arquivo

- `chat-clean-v3.html`

## O que foi adicionado

- OCR_URL usando `http://127.0.0.1:8091/api/v1/materials/extract-text`.
- Status visual no anexo:
  - `Lendo...`
  - `OCR pronto`
  - `OCR falhou`
- Preparação de imagem para OCR sem destruir excessivamente a nitidez.
- Limpeza básica de textos da interface no OCR.
- OCR armazenado internamente para futura integração com API.

## Regras preservadas

- Não mexer no campo principal aprovado.
- Não enviar resposta fake.
- Não ligar API de chat neste checkpoint.
- Não alterar o fluxo visual do print no composer.
- Não reintroduzir lateral antiga nem upload antigo.

## Validação

- JS extraído do HTML passou em `node --check`.
- OCR aparece como camada interna do anexo.
- Envio visual do print permanece limpo.
- A conversa continua isolada no `chat-clean-v3.html`.

## Checkpoints

- CHAT_CLEAN_V3_OCR_LAYER_OK
- CHAT_CLEAN_V3_OCR_JS_CHECK_OK
- CHAT_CLEAN_V3_COMPOSER_PRESERVED_OK
