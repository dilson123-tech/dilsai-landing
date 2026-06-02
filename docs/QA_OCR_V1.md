# QA — DilsAI Estudos OCR V1

## Status

QA_OCR_V1_OK

## Branch

feat/dilsai-estudos-ocr-v1

## Objetivo

Validar OCR inicial para imagens enviadas pelo aluno no DilsAI Estudos.

## Entregas validadas

- Input da tela cheia aceita PNG/JPG/JPEG/WEBP.
- Frontend detecta imagem e envia ao backend.
- Backend aceita image/png, image/jpeg e image/webp no endpoint de extração.
- Backend executa OCR com Pillow + pytesseract.
- OCR usa Tesseract com idiomas por+eng.
- Texto extraído é carregado no campo Material/contexto opcional.
- source_type técnico retornado como image_ocr no endpoint de extração.
- Fonte formal da resposta usa user_uploaded_image_ocr.
- Frontend exibe fonte amigável como Imagem enviada pelo aluno.
- O sistema avisa honestamente quando OCR não encontra texto.
- PDF escaneado convertido para imagem ficou fora do escopo.

## Validação técnica

Arquivo usado:

/tmp/dilsai-ocr-teste.png

Resultado do endpoint:

status=success
file_name=dilsai-ocr-teste.png
source_type=image_ocr
page_count=null
char_count=118
warning=null

Texto extraído:

DilsAl Estudos OCR teste
Fotossintese usa luz solar, agua e gas carbonico.
A planta produz glicose e libera oxigenio.

## Observação

O OCR confundiu DilsAI com DilsAl, o que é aceitável neste ciclo inicial. OCR pode errar caracteres visualmente parecidos.

## Validação visual

Fluxo validado na tela cheia:

1. Selecionar /tmp/dilsai-ocr-teste.png.
2. Confirmar status OCR concluído.
3. Confirmar preenchimento do campo Material/contexto opcional.
4. Enviar pergunta usando contexto.
5. Confirmar fonte amigável exibida como Imagem enviada pelo aluno.

Resultado visual confirmado:

Fonte: Imagem enviada pelo aluno: dilsai-ocr-teste.png

## Resultado final

OCR V1 validado para imagem simples com texto legível.

## Próximo passo recomendado

Após merge e tag, evoluir em ciclo separado para PDF escaneado convertido para imagem ou melhorar pré-processamento de OCR.
