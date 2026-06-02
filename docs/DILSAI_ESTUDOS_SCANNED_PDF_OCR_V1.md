# DilsAI Estudos — Scanned PDF OCR V1

## Status

DILSAI_ESTUDOS_SCANNED_PDF_OCR_V1

## Objetivo

Adicionar fallback OCR inicial para PDF escaneado/imagem.

Quando um PDF não possui texto digital extraível via pypdf, o backend converte as primeiras páginas em imagem usando pdf2image/Poppler e executa OCR com Tesseract via pytesseract.

## Escopo

Incluído:

- dependência `pdf2image==1.17.0`;
- uso de Poppler/pdftoppm do sistema;
- fallback OCR para PDF sem texto digital;
- limite inicial de 3 páginas para evitar custo alto;
- retorno `source_type=pdf_ocr` no endpoint de extração;
- contexto com tipo `PDF escaneado convertido para imagem e processado por OCR`;
- fonte amigável `PDF escaneado via OCR enviado pelo aluno`.

Fora do escopo:

- OCR avançado com pré-processamento;
- múltiplas estratégias de contraste/rotação;
- RAG/embeddings;
- armazenamento de arquivo;
- OCR completo ilimitado em PDFs longos.

## Regra de produto

OCR pode errar. O sistema deve avisar que o conteúdo foi obtido por OCR inicial e pode conter erros.

## Próximo passo recomendado

Após validar este ciclo, melhorar pré-processamento de OCR ou iniciar RAG/embeddings em ciclo separado.
