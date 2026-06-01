# QA — DilsAI Estudos Context Textarea Metadata Leak V1

## Status

QA_CONTEXT_TEXTAREA_METADATA_LEAK_V1_OK

## Branch

fix/dilsai-estudos-context-textarea-metadata-leak-v1

## Objetivo

Corrigir e blindar possível vazamento visual de metadados da resposta dentro do campo Material/contexto opcional.

## Problema observado

Durante validação visual do Source Display Frontend V1, foi observado que uma linha de metadados como Tema, Modo e Usou contexto poderia aparecer dentro do textarea de contexto.

## Causa provável

Não foi identificado código escrevendo diretamente no textarea de contexto.

A causa mais provável é restauração/autofill/cache do navegador ou estado visual antigo preservado.

## Correções aplicadas

- Adicionado autocomplete=off no textarea de contexto da tela cheia.
- Adicionados atributos data-lpignore e data-form-type para reduzir interferência de autofill.
- Adicionado autocomplete=off no textarea de contexto do chat rápido.
- Criada função defensiva para limpar somente conteúdo curto que pareça metadado vazado.
- A limpeza preserva material real do usuário e só remove linhas curtas com padrão de metadado.

## Validações executadas

- node --check script.js: OK.
- git diff --check: OK.
- Validação visual recomendada: campo Material/contexto opcional deve iniciar vazio.
- Resposta deve continuar exibindo Fonte: Fotossíntese no meta da mensagem.

## Resultado

Blindagem inicial do textarea/contexto concluída.

## Próximo passo recomendado

Depois do merge e tag, avançar para upload explícito de material simples.
