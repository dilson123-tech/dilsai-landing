# DilsAI Estudos — Chat Seco V3 Visual QA

## Status

Checkpoint visual aprovado para o novo painel de conversa isolado do DilsAI Estudos.

Este projeto é produto real para estudos e futura comercialização. Este painel não substitui ainda a tela principal; ele é uma base limpa e isolada para validar a UX correta antes de integrar OCR/API e depois substituir o painel antigo.

## Arquivo

- `chat-clean-v3.html`

## Objetivo do Chat Seco V3

Criar um painel de conversa limpo, sem lateral e sem herdar o fluxo antigo quebrado de upload, com comportamento parecido com ChatGPT:

- campo único para digitar;
- colar print com Ctrl+V no campo;
- arrastar imagem;
- escolher imagem pelo botão `+`;
- imagem fica anexada no composer antes do envio;
- nada é enviado antes de clicar em `Enviar`;
- ao enviar, a imagem aparece na conversa;
- se houver texto digitado, o texto aparece junto como pergunta;
- sem OCR/API neste checkpoint.

## Resultado visual validado

Validação manual aprovada:

- print colado no campo aparece como anexo pendente;
- botão Enviar mantém comportamento correto;
- print só aparece na conversa depois de clicar Enviar;
- mensagem temporária/fake foi removida;
- painel antigo/lateral não participa deste fluxo;
- arquivo JS interno do HTML passou em `node --check`.

## Limites deste checkpoint

Este checkpoint ainda não faz OCR nem chama API.

Próxima fase correta:

1. ligar OCR ao Chat Seco V3;
2. guardar texto OCR como contexto interno;
3. manter o print visual no composer;
4. enviar pergunta + OCR para API somente ao clicar Enviar;
5. só depois integrar/substituir o painel antigo da tela principal.

## Checkpoints

- CHAT_CLEAN_V3_VISUAL_OK
- CHAT_CLEAN_V3_JS_CHECK_OK
