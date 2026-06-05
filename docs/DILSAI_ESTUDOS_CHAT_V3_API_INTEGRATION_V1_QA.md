# DilsAI Estudos — Chat V3 API Integration V1 QA

## Status

Integração inicial do Chat Seco V3 com a API real do DilsAI Estudos validada.

O DilsAI Estudos é produto real e vendável para estudantes, cursos, provas, concursos e estudos profissionais. Esta entrega conecta o painel aprovado ao backend com o Motor de Precisão Acadêmica V1, preservando o composer aprovado.

## O que foi entregue

- Chat Seco V3 chamando `/api/v1/chat`.
- Leitura das configurações laterais:
  - Nível
  - Matéria
  - Curso/profissão
  - Modo
  - Material extra
- OCR do print enviado como contexto real.
- Material extra enviado como contexto real.
- Configuração lateral não entra mais como fonte/material.
- Resposta renderizada no chat.
- Estado visual de envio com “Analisando...”.
- Composer aprovado preservado.

## Correções críticas

### 1. Configuração lateral não contamina contexto

As opções de nível, matéria, curso/profissão e modo são enviadas como configuração pedagógica, não como material de estudo.

Fonte real agora é apenas:

- OCR do print;
- material extra;
- base interna forte quando aplicável;
- material enviado pelo aluno.

### 2. Fonte Segura não usa fonte fraca

Modo Fonte Segura sem material confiável pede contexto e não puxa base interna fraca.

Validação aprovada:

- Pergunta: `quanto é 30*3`
- Modo: `fonte_segura`
- Sem print/material
- Resultado: pediu material/contexto
- Não puxou Fotossíntese nem fonte interna indevida.

### 3. Modo Professor responde básico conhecido

Modo Professor não deve pedir PDF para perguntas simples.

Validações aprovadas:

- `quanto e 30*3` -> `Resposta final: 90`
- `raiz quadrada de 144` -> `Resposta final: 12`
- `quanto e 3 metros cubicos` -> `3 m³ = 3000 litros`
- `quem descobriu brasil` -> `Pedro Álvares Cabral, em 1500`

## Fallbacks determinísticos adicionados

- Aritmética básica.
- Raiz quadrada simples.
- Conversão básica de volume:
  - m³ para litros
  - m³ para cm³
- Fato escolar básico:
  - chegada de Pedro Álvares Cabral ao Brasil em 1500.

## Limitação conhecida

Sem crédito ativo na OpenAI API, o DilsAI cai no fallback offline. O fallback ajuda em perguntas básicas, mas não substitui o motor real de IA.

Erro diagnosticado:

- `RateLimitError`
- `insufficient_quota`
- saldo OpenAI API em `$0.00`

Para o produto responder perguntas gerais de todas as matérias, é obrigatório validar crédito/billing da OpenAI API.

## Regras preservadas

- Não mexer no composer aprovado.
- Não quebrar Ctrl+V de print.
- Não quebrar anexo no campo.
- Não quebrar OCR visual.
- Não transformar configuração lateral em fonte.
- Não responder Fonte Segura sem base confiável.

## Checkpoints

- CHAT_V3_API_INTEGRATION_V1_OK
- CHAT_V3_COMPOSER_PRESERVED_OK
- STUDY_SETTINGS_NOT_CONTEXT_OK
- SAFE_SOURCE_REQUIRES_RELIABLE_CONTEXT_OK
- BASIC_ARITHMETIC_FALLBACK_OK
- BASIC_SQUARE_ROOT_FALLBACK_OK
- BASIC_UNIT_CONVERSION_FALLBACK_OK
- BASIC_SCHOOL_FACT_FALLBACK_OK
- OPENAI_API_CREDIT_REQUIRED_FOR_GENERAL_ENGINE
