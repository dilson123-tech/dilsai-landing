# QA — DilsAI Estudos Paste Image Upload V1

## 1. Objetivo

Validar o suporte inicial para colar print/imagem com Ctrl+V na tela cheia de estudos.

## 2. Base de referência

- `v0.1.20-dilsai-estudos-mvp-readiness-v1`
- `v0.1.21-dilsai-estudos-commercial-readiness-roadmap-v1`
- `v0.1.22-dilsai-estudos-terms-privacy-v1`
- `v0.1.23-dilsai-estudos-commercial-landing-v1`

## 3. Escopo validado

Este QA valida:

- criação de listener de paste;
- detecção de imagem no clipboard;
- envio da imagem para OCR existente;
- preenchimento do contexto;
- status visual para print colado;
- preservação do upload normal;
- preservação do backend.

## 4. Critérios de aprovação

O ciclo é aprovado se:

- `script.js` compilar com `node --check`;
- backend continuar compilando;
- `index.html` orientar o usuário sobre Ctrl+V;
- o listener `paste` existir;
- o fluxo usar o OCR já existente;
- o fluxo de upload por arquivo continuar existindo;
- não houver RAG, login ou cobrança neste PR.

## 5. Resultado esperado

`QA_PASTE_IMAGE_UPLOAD_V1_OK`

## 6. Próxima tag sugerida

`v0.1.24-dilsai-estudos-paste-image-upload-v1`
