# DilsAI Estudos — OCR V1

## Status

DILSAI_ESTUDOS_OCR_V1

## Objetivo

Adicionar OCR inicial para imagens enviadas pelo aluno.

Este ciclo permite enviar imagem PNG/JPG/JPEG/WEBP, executar OCR no backend usando Tesseract e carregar o texto extraído no campo Material/contexto opcional.

## Escopo

Incluído:

- suporte a upload de imagem no input da tela cheia;
- endpoint existente de extração passa a aceitar image/png, image/jpeg e image/webp;
- OCR com Pillow + pytesseract;
- idioma por/eng;
- mensagem honesta quando OCR não encontra texto;
- mensagem honesta quando Tesseract não está instalado;
- fonte formal user_uploaded_image_ocr.

Fora do escopo:

- PDF escaneado convertido para imagem;
- múltiplas páginas/imagens;
- OCR avançado com pré-processamento;
- RAG/embeddings.

## Regra de produto

OCR pode errar. O DilsAI Estudos deve tratar OCR como apoio inicial, não leitura perfeita.

## Próximo passo recomendado

Depois deste ciclo, evoluir para PDF escaneado usando conversão PDF para imagem em ciclo separado.
