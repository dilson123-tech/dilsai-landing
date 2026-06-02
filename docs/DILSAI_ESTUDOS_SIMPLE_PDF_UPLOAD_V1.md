# DilsAI Estudos — Simple PDF Upload V1

## Status

DILSAI_ESTUDOS_SIMPLE_PDF_UPLOAD_V1

## Objetivo

Adicionar suporte inicial a PDF textual/digital no upload de material da tela cheia do DilsAI Estudos.

## Escopo

Incluído:

- input da tela cheia passa a aceitar `.pdf`;
- frontend detecta PDF e envia o arquivo ao backend;
- backend adiciona endpoint `POST /api/v1/materials/extract-text`;
- backend extrai texto de PDF digital/textual usando `pypdf`;
- texto extraído é carregado no campo `Material/contexto opcional`;
- PDF sem texto extraível retorna aviso honesto;
- arquivo não é salvo no servidor.

Fora do escopo:

- OCR;
- PDF escaneado/imagem;
- armazenamento de arquivos;
- RAG com embeddings;
- múltiplos arquivos simultâneos.

## Regra de produto

O DilsAI Estudos não deve fingir que leu PDF escaneado.

Se o PDF não tiver texto extraível, o sistema deve avisar que OCR será necessário em ciclo futuro.

## Próximo passo recomendado

Após validar PDF textual, evoluir para OCR de imagens/PDF escaneado em ciclo separado.
