# DilsAI Estudos — Context Aware Fallback V1

## Status

DILSAI_ESTUDOS_CONTEXT_AWARE_FALLBACK_V1

## Objetivo

Melhorar o fallback do DilsAI Estudos quando o provedor externo de IA não puder ser acionado.

Quando o aluno envia material via contexto, .txt, .md ou PDF extraído, o fallback passa a usar esse material para gerar apoio preliminar de estudo de forma determinística, sem fingir consulta ao modelo externo.

## Escopo

Incluído:

- fallback determinístico usando contexto enviado pelo aluno;
- prioridade do material do aluno sobre base interna no fallback;
- resumo preliminar com linhas relevantes do contexto;
- trecho-base usado na resposta;
- aviso claro de que é fallback seguro;
- campos de fonte interna permanecem nulos quando a resposta usa material enviado pelo aluno.

Fora do escopo:

- IA generativa local;
- OCR;
- RAG com embeddings;
- resumo semântico avançado;
- substituição da resposta real da OpenAI quando a quota estiver ativa.

## Regra de produto

O DilsAI Estudos não deve fingir que consultou IA externa quando a OpenAI falhar.

Se houver material enviado, o sistema deve aproveitar o contexto de forma honesta e limitada.

Se a resposta vier de base interna, os campos de fonte interna podem ser usados.

Se a resposta vier de material enviado pelo aluno, source_title/source_path/source_type/source_score devem permanecer nulos até existir um contrato formal de fonte enviada/upload.

## Próximo passo recomendado

Após validar este ciclo, avançar para OCR de PDF escaneado/imagem ou melhorar o contrato de fonte para materiais enviados pelo usuário.
