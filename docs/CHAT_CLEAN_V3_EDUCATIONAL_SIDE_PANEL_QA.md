# DilsAI Estudos — Chat Seco V3 Educational Side Panel QA

## Status

Painel lateral educacional aprovado visualmente no `chat-clean-v3.html`.

O projeto DilsAI Estudos é produto real para estudo, provas, cursos, ensino básico, ensino médio, ENEM, cursos técnicos, superior/faculdade, concursos e estudos profissionais.

## Arquivo

- `chat-clean-v3.html`

## O que foi validado

- Chat principal preservado.
- Campo de conversa aprovado não foi alterado.
- Ctrl+V de print continua sendo tratado no composer.
- Anexo de imagem permanece no campo antes do envio.
- OCR segue como camada interna do Chat Seco V3.
- Lateral foi transformada em painel educacional compacto.
- Cada campo abre nele mesmo, usando estrutura tipo accordion.
- Ao selecionar opções, o campo resume o valor escolhido.

## Abas/campos educacionais

- Nível
- Matéria
- Cursos/Profissões
- Modo
- Material
- OCR

## Diretriz preservada

Não mexer mais no miolo do campo de conversa aprovado. Evoluções futuras devem acontecer nas camadas laterais ou na integração controlada com API/OCR, sem quebrar a UX do composer.

## Checkpoints

- CHAT_CLEAN_V3_EDUCATIONAL_SIDE_PANEL_OK
- CHAT_CLEAN_V3_COMPOSER_PRESERVED_OK
- CHAT_CLEAN_V3_JS_CHECK_OK
