# QA — DilsAI Estudos Simple PDF Upload V1

## Status

QA_SIMPLE_PDF_UPLOAD_V1_OK

## Branch

feat/dilsai-estudos-simple-pdf-upload-v1

## Objetivo

Validar upload e extração de PDF textual/digital no DilsAI Estudos.

## Entregas validadas

- Input da tela cheia aceita .pdf.
- Frontend detecta PDF e envia ao backend.
- Backend adiciona endpoint POST /api/v1/materials/extract-text.
- Backend extrai texto com pypdf.
- Texto extraído é carregado no campo Material/contexto opcional.
- PDF textual retorna page_count, char_count, source_type=pdf_text e warning=null.
- Arquivo não é salvo no servidor.
- OCR permanece fora do escopo.

## Validação técnica

Arquivo usado:

/tmp/dilsai-pdf-teste.pdf

Resultado do endpoint:

status=success
file_name=dilsai-pdf-teste.pdf
source_type=pdf_text
page_count=1
char_count=183
warning=null

Texto extraído confirmou conteúdo do PDF textual.

## Observação

PDF escaneado ou imagem não faz parte deste ciclo. Se o PDF não tiver texto extraível, o sistema deve avisar que OCR será necessário em ciclo futuro.

## Resultado final

Simple PDF Upload V1 validado para PDF textual/digital.

## Próximo passo recomendado

Após merge e tag, evoluir para OCR de imagem/PDF escaneado em ciclo separado.
