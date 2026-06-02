# DilsAI Estudos — Simple Material Upload V1

## Status

DILSAI_ESTUDOS_SIMPLE_MATERIAL_UPLOAD_V1

## Objetivo

Adicionar upload explícito de material simples na tela cheia do DilsAI Estudos.

Este ciclo permite que o aluno selecione um arquivo `.txt` ou `.md`, lido localmente pelo navegador, e carregue o conteúdo no campo de contexto antes de enviar a pergunta.

## Escopo

Incluído:

- input de arquivo na tela cheia;
- suporte a `.txt` e `.md`;
- leitura local via navegador;
- preenchimento automático do campo `Material/contexto opcional`;
- exibição de nome e tamanho do arquivo carregado;
- limite simples de tamanho;
- sem upload para servidor neste ciclo.

Fora do escopo:

- PDF;
- OCR;
- imagem;
- armazenamento de arquivo;
- envio multipart para backend;
- RAG com embeddings.

## Regra de segurança

O arquivo é lido no navegador e o conteúdo é enviado como contexto somente quando o aluno envia a pergunta.

## Próximo passo recomendado

Após validar este ciclo, evoluir para upload PDF simples ou melhorar o card visual de fonte/material.
