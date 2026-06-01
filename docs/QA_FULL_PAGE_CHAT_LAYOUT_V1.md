# QA — DilsAI Estudos Full Page Chat Layout V1

## Status

QA_FULL_PAGE_CHAT_LAYOUT_V1_PARTIAL_OK

## Branch

feat/dilsai-estudos-full-page-chat-layout-v1

## Objetivo

Criar a primeira versão da experiência principal do DilsAI Estudos em tela grande, estilo plataforma de estudos com IA, preservando a landing e mantendo o chat rápido/flutuante existente.

## Entregas implementadas

- Botão principal "Estudar em tela cheia" no topo da landing.
- Botão secundário "Chat rápido" preservando a experiência anterior.
- Nova seção `#dilsai-study-app`.
- Layout em tela grande com seleção de nível, matéria, modo, campo de material/contexto opcional, área grande de mensagens, botão limpar conversa e formulário de pergunta.
- Integração da tela grande reaproveitando a função existente `askDilsAI()`.
- Correção de contrato frontend/backend para tópico:
  - frontend agora usa `matematica_logica`;
  - normalizador defensivo converte `matematica` para `matematica_logica`.

## Validações executadas

### JavaScript

Comando executado:

`node --check script.js`

Resultado:

OK.

### Segurança de segredo

Verificações:

- `backend/.env` existe localmente.
- `OPENAI_API_KEY` está presente localmente.
- `backend/.env` não está rastreado pelo Git.

Resultado:

OK.

### Backend

Endpoint `/health` respondeu com status OK.

Resultado:

OK.

### Contrato frontend/backend

O backend rejeitava `topic=matematica` com HTTP 422 porque o schema aceita apenas:

- `programacao`
- `portugues`
- `matematica_logica`
- `geral`

Foi aplicada correção no frontend para usar `matematica_logica`.

Teste posterior com `topic=matematica_logica` retornou `status=success`.

Resultado:

OK.

## Observação sobre IA real

A chave OpenAI foi carregada corretamente:

- provider: `openai`
- model: `gpt-4o-mini`
- key prefix detectado localmente: `sk-proj...`

Porém, o teste direto com a OpenAI retornou:

`RateLimitError 429 — insufficient_quota`

Interpretação:

A integração técnica está chegando na OpenAI, mas a conta/projeto/chave está sem cota/crédito/billing disponível para concluir a geração real neste momento.

Isso não bloqueia o PR visual/técnico da tela cheia, mas deve ser resolvido antes de validar novamente o uso real da IA em produção.

## Resultado

- Layout tela cheia: OK.
- Integração frontend/backend: OK.
- Contrato de tópico: OK.
- Segurança do `.env`: OK.
- IA real: bloqueada temporariamente por quota externa da conta OpenAI.

## Próximo passo recomendado

1. Liberar billing/crédito/cota no painel da OpenAI.
2. Repetir teste direto da OpenAI.
3. Repetir teste pela tela cheia.
4. Se OK, atualizar este QA para `QA_FULL_PAGE_CHAT_LAYOUT_V1_OK`.

## Nota de produto

Este PR mantém a direção oficial: DilsAI Estudos é produto real de IA para estudos, não ferramenta de cola, não captura escondida e não resposta inventada.
