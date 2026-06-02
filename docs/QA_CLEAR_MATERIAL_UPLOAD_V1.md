# QA — DilsAI Estudos Clear Material Upload V1

## Status

QA_CLEAR_MATERIAL_UPLOAD_V1_OK

## Branch

feat/dilsai-estudos-clear-material-upload-v1

## Objetivo

Validar o botão Limpar material na tela cheia do DilsAI Estudos.

Este ciclo complementa o Simple Material Upload V1, permitindo remover o material carregado sem recarregar a página e sem apagar o chat.

## Entregas validadas

- Botão Limpar material adicionado abaixo do upload simples.
- O botão limpa o input de arquivo.
- O botão limpa o campo Material/contexto opcional quando o conteúdo veio de arquivo carregado.
- O botão remove os metadados locais loadedFileName e loadedFileSize.
- O botão atualiza o status visual para Material carregado removido.
- O chat permanece intacto.

## Validações executadas

### JavaScript

Comando:

node --check script.js

Resultado:

OK.

### Diff check

Comando:

git diff --check

Resultado:

OK.

### Validação visual

Fluxo validado:

1. Carregar arquivo .txt no campo Enviar material simples.
2. Confirmar preenchimento automático do campo Material/contexto opcional.
3. Clicar em Limpar material.
4. Confirmar que o campo de contexto foi limpo.
5. Confirmar que o arquivo selecionado foi removido.
6. Confirmar que o chat não foi apagado.

Resultado:

OK.

## Resultado final

Clear Material Upload V1 validado.

O DilsAI Estudos agora permite carregar e remover material simples sem recarregar a página.

## Próximo passo recomendado

Após merge e tag, avançar para upload PDF simples em ciclo separado.
