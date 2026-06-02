# QA — DilsAI Estudos Scanned PDF OCR V1

## Status

QA_SCANNED_PDF_OCR_V1_OK

## Branch

feat/dilsai-estudos-scanned-pdf-ocr-v1

## Objetivo

Validar OCR inicial para PDF escaneado/imagem no DilsAI Estudos.

## Entregas validadas

- Backend mantém extração textual de PDF digital com pypdf.
- Quando o PDF não possui texto digital extraível, o backend converte páginas em imagem usando pdf2image/Poppler.
- Backend executa OCR nas imagens com Tesseract via pytesseract.
- OCR inicial é limitado às primeiras páginas para evitar custo alto.
- Endpoint retorna source_type=pdf_ocr quando usa OCR em PDF escaneado.
- Resposta inclui warning honesto avisando que OCR pode conter erros.
- Frontend diferencia PDF textual de PDF escaneado processado por OCR.
- Fonte amigável passa a exibir PDF escaneado via OCR enviado pelo aluno.

## Validação técnica

Arquivo usado:

/tmp/dilsai-pdf-escaneado-teste.pdf

Resultado do endpoint:

status=success
file_name=dilsai-pdf-escaneado-teste.pdf
source_type=pdf_ocr
page_count=1
char_count=200
warning=PDF sem texto digital extraível. O conteúdo foi obtido por OCR inicial nas primeiras 1 página(s). OCR pode conter erros.

Trecho extraído:

DilsAl Estudos PDF escaneado teste
Esta pagina virou imagem dentro do PDF.
O backend deve converter o PDF em imagem e executar O
Fotossintese usa luz solar para produzir glicose.

## Observação

O OCR confundiu DilsAI com DilsAl e cortou parte de uma palavra, comportamento aceitável neste ciclo inicial.

## Validação visual

Fluxo validado na tela cheia:

1. Selecionar dilsai-pdf-escaneado-teste.pdf.
2. Confirmar status PDF escaneado processado por OCR.
3. Confirmar preenchimento do campo Material/contexto opcional.
4. Enviar pergunta usando contexto.
5. Confirmar fonte amigável como PDF escaneado via OCR enviado pelo aluno.

Resultado visual confirmado:

PDF escaneado processado por OCR: dilsai-pdf-escaneado-teste.pdf (200 caracteres)

## Resultado final

Scanned PDF OCR V1 validado para PDF escaneado simples de uma página.

## Próximo passo recomendado

Após merge e tag, melhorar pré-processamento OCR ou iniciar RAG/embeddings em ciclo separado.
