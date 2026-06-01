# QA — DilsAI Estudos Source Display Frontend V1

## Status

QA_SOURCE_DISPLAY_FRONTEND_V1_OK

## Branch

feat/dilsai-estudos-source-display-frontend-v1

## Objetivo

Validar que o frontend do DilsAI Estudos exibe a fonte usada quando a API retorna metadados formais de fonte.

## Entregas validadas

- Chat rápido passou a incluir source_title no meta da resposta.
- Tela cheia passou a incluir source_title no meta da resposta.
- A resposta exibe visualmente a fonte usada quando a base interna Markdown é encontrada.
- Mantida compatibilidade com Tema, Modo, Confiança e Usou contexto.
- Sem alteração no contrato da API neste PR.

## Validação visual executada

Teste realizado na tela cheia:

Nível: Ensino Médio
Matéria: Biologia
Modo: Resumo
Pergunta: Faça um resumo curto sobre fotossíntese.

Resultado visual confirmado:

Tema: biologia • Modo: resumo • Usou contexto • Fonte: Fotossíntese

A resposta retornou conteúdo da base interna:

backend/app/knowledge/ensino_medio/biologia/fotossintese.md

## Resultado

Source Display Frontend V1 validado.

O usuário agora consegue ver no frontend qual fonte interna foi usada para apoiar a resposta.

## Observação técnica

Foi observado que texto de metadados pode aparecer dentro do campo Material/contexto opcional em algum fluxo visual. Isso não bloqueia este PR, mas deve ser corrigido no próximo ciclo com um PR específico.

Sugestão de próximo PR:

fix: prevent chat metadata from leaking into context textarea

## Próximo passo recomendado

Após merge e tag, iniciar correção do textarea/contexto antes de avançar para upload explícito de material.
