# QA — DilsAI Estudos MVP Readiness V1

## 1. Objetivo

Registrar o QA final de readiness do MVP inicial do DilsAI Estudos após o ciclo de OCR Robustness V1.

Este QA não cria nova funcionalidade. Ele consolida o estado atual para fechamento seguro do MVP.

## 2. Escopo validado

Foram considerados como parte do MVP inicial:

- backend FastAPI;
- frontend estático;
- tela cheia de estudos;
- taxonomia acadêmica;
- base interna simples;
- resposta com fonte;
- upload de material;
- extração de PDF textual;
- OCR de imagem;
- OCR de PDF escaneado;
- fallback seguro;
- labels amigáveis de fonte;
- documentação por ciclo.

## 3. Critérios de aprovação

O MVP é considerado pronto para demonstração e piloto controlado se:

- o backend compila;
- o frontend permanece funcional;
- a documentação principal existe;
- o QA histórico foi preservado;
- o produto não promete mais do que entrega;
- os limites de OCR e IA externa estão documentados;
- não há chave sensível no repositório;
- o próximo ciclo pesado ficou separado do fechamento do MVP.

## 4. Checklist técnico

### Git

Esperado:

- branch criada a partir da `main`;
- histórico preservado;
- tags anteriores preservadas;
- nenhum arquivo sensível incluído.

### Documentação

Esperado:

- `docs/DILSAI_ESTUDOS_MVP_READINESS_V1.md`;
- `docs/QA_MVP_READINESS_V1.md`.

### Segurança

Esperado:

- `.env` não versionado;
- nenhuma chave OpenAI exposta;
- nenhuma promessa de OCR perfeito;
- nenhuma promessa de RAG já entregue;
- nenhuma promessa de armazenamento permanente de material do aluno.

## 5. Resultado

Status:

`QA_MVP_READINESS_V1_OK`

O DilsAI Estudos fica oficialmente fechado como MVP inicial em readiness, preparado para demonstração e piloto controlado.

## 6. Próxima tag sugerida

`v0.1.20-dilsai-estudos-mvp-readiness-v1`
