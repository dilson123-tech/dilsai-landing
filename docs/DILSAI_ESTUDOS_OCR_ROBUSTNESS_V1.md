# DilsAI Estudos — OCR Robustness V1

## Status

DILSAI_ESTUDOS_OCR_ROBUSTNESS_V1

## Objetivo

Blindar o OCR inicial do DilsAI Estudos antes de avançar para RAG/embeddings.

Este ciclo não adiciona um novo tipo de leitura. Ele melhora o contrato técnico e visual dos fluxos já existentes de OCR de imagem e PDF escaneado.

## Entregas

- Constantes explícitas para OCR de PDF escaneado:
  - `SCANNED_PDF_OCR_MAX_PAGES = 3`
  - `SCANNED_PDF_OCR_DPI = 220`
- Endpoint passa a retornar metadados de OCR:
  - `ocr_engine`
  - `ocr_languages`
  - `ocr_processed_pages`
  - `ocr_page_limit`
- Warning de PDF OCR passa a mencionar limite operacional de páginas.
- Frontend inclui aviso de extração no contexto carregado quando o backend retorna `warning`.
- Frontend informa que OCR pode conter erros quando PDF escaneado é processado por OCR.

## Requisitos de sistema

Para OCR funcionar no ambiente local/produção:

- `tesseract-ocr`
- `tesseract-ocr-por`
- `tesseract-ocr-eng`
- `poppler-utils`
- Python:
  - `pillow`
  - `pytesseract`
  - `pdf2image`

## Fora do escopo

- RAG/embeddings.
- Pré-processamento avançado de imagem.
- Rotação automática.
- Detecção de baixa qualidade por score.
- OCR ilimitado em PDFs longos.

## Regra de produto

OCR deve ser tratado como apoio inicial. O sistema deve avisar que pode haver erro de leitura, especialmente em PDF escaneado ou imagem de baixa qualidade.

## Próximo passo recomendado

Após validar este ciclo, iniciar RAG/embeddings ou um ciclo específico de pré-processamento OCR.
