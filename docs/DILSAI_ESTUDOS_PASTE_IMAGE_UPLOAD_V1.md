# DilsAI Estudos — Paste Image Upload V1

## 1. Objetivo

Adicionar suporte inicial para colar print/imagem diretamente na tela cheia de estudos do DilsAI Estudos.

Este ciclo atende um uso real de alunos: copiar um print de questão, apostila, prova, exercício ou tela e colar direto no chat, sem precisar salvar arquivo manualmente.

## 2. Escopo

O recurso permite:

- colar imagem/print com Ctrl+V dentro da área de estudos;
- detectar imagem no clipboard;
- transformar a imagem colada em arquivo interno;
- enviar a imagem para o mesmo endpoint de OCR já existente;
- preencher o campo de contexto com o texto extraído;
- mostrar status de OCR;
- avisar que OCR pode conter erros;
- preservar upload normal por seletor de arquivo.

## 3. Limites

Este ciclo não altera:

- backend;
- endpoint de OCR;
- PDF textual;
- PDF escaneado;
- fallback seguro;
- resposta com fonte;
- RAG/embeddings;
- login;
- cobrança;
- deploy.

## 4. Segurança e UX

O recurso não promete leitura perfeita.

Prints ruins, borrados, cortados, escuros ou manuscritos podem gerar OCR incompleto ou incorreto.

O aluno deve conferir o texto extraído antes de confiar totalmente na resposta.

## 5. Checkpoint

`DILSAI_ESTUDOS_PASTE_IMAGE_UPLOAD_V1_OK`
