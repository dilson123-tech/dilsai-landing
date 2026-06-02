# QA — DilsAI Estudos Simple Material Upload V1

## Status

QA_SIMPLE_MATERIAL_UPLOAD_V1_OK

## Branch

feat/dilsai-estudos-simple-material-upload-v1

## Objetivo

Validar o upload explícito de material simples na tela cheia do DilsAI Estudos.

Este ciclo permite selecionar arquivo .txt ou .md, ler o conteúdo localmente no navegador e carregar o texto no campo Material/contexto opcional antes de enviar a pergunta.

## Entregas validadas

- Campo Enviar material simples adicionado na tela cheia.
- Input de arquivo aceitando .txt e .md.
- Leitura local do arquivo no navegador.
- Conteúdo do arquivo carregado automaticamente no textarea de contexto.
- Status visual exibindo arquivo carregado e tamanho.
- Limite simples de tamanho aplicado.
- Sem upload para servidor neste ciclo.
- Sem PDF, OCR ou RAG neste ciclo.

## Validação visual executada

Arquivo usado:

dilsai-material-teste.txt

Resultado visual confirmado:

- O arquivo foi selecionado pelo botão Escolher arquivo.
- O status exibiu Material carregado.
- O conteúdo foi inserido no campo Material/contexto opcional.
- A pergunta foi enviada com Nível Ensino Médio, Matéria Biologia e Modo Resumo.
- A resposta retornou Usou contexto.
- A resposta exibiu Fonte: Fotossíntese.

## Observação

Como a OpenAI segue bloqueada por quota externa, a resposta usou fallback honesto e base interna quando encontrada.

Isso não invalida o QA, porque o objetivo deste PR é validar a leitura local do arquivo e o envio do conteúdo como contexto.

## Resultado final

Simple Material Upload V1 validado.

O DilsAI Estudos agora permite carregar material simples .txt/.md no campo de contexto da tela cheia.

## Próximo passo recomendado

Após merge e tag, evoluir para uma destas opções:

1. melhorar destaque visual do material carregado;
2. adicionar botão para limpar material carregado;
3. iniciar upload PDF simples em ciclo separado.
