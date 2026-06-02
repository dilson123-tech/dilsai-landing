# QA — DilsAI Estudos OCR Robustness V1

## Status

QA_OCR_ROBUSTNESS_V1_OK

## Branch

feat/dilsai-estudos-ocr-robustness-v1

## Objetivo

Validar melhorias de robustez e contrato técnico do OCR antes de avançar para RAG/embeddings.

## Entregas validadas

- Constantes explícitas para OCR de PDF escaneado:
  - SCANNED_PDF_OCR_MAX_PAGES = 3
  - SCANNED_PDF_OCR_DPI = 220
- Endpoint retorna metadados formais de OCR:
  - ocr_engine
  - ocr_languages
  - ocr_processed_pages
  - ocr_page_limit
- Warning de PDF OCR informa limite operacional de páginas.
- Frontend passa a incluir aviso de extração no contexto carregado quando existe warning.
- Frontend informa que OCR pode conter erros em PDF escaneado.
- Nenhum RAG/embedding foi incluído neste ciclo.

## Validação técnica

Arquivo usado:

/tmp/dilsai-pdf-escaneado-teste.pdf

Resultado do endpoint:

status=success
file_name=dilsai-pdf-escaneado-teste.pdf
source_type=pdf_ocr
page_count=1
char_count=200
ocr_engine=tesseract
ocr_languages=por+eng
ocr_processed_pages=1
ocr_page_limit=3

Warning validado:

PDF sem texto digital extraível. O conteúdo foi obtido por OCR inicial em 1 página(s), com limite operacional de 3 página(s). OCR pode conter erros.

## Observação

O texto OCR manteve pequenas imperfeições esperadas, como DilsAI virar DilsAl e corte parcial de palavra. Isso é aceitável neste ciclo porque o sistema avisa que OCR pode conter erros.

## Resultado final

OCR Robustness V1 validado.

O DilsAI Estudos agora expõe metadados técnicos claros de OCR e comunica melhor os limites do processamento.

## Próximo passo recomendado

Após merge e tag, decidir entre:

1. pré-processamento OCR V2;
2. início de RAG/embeddings;
3. handoff completo do projeto antes de trocar de chat.
