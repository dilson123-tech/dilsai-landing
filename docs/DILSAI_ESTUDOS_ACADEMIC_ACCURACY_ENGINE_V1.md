# DilsAI Estudos — Academic Accuracy Engine V1

## Status

Documento oficial da próxima fase do DilsAI Estudos.

O DilsAI Estudos é produto real para estudantes, cursos, provas, concursos e estudos profissionais. A plataforma será vendida, portanto precisa priorizar precisão, explicação correta, transparência e controle contra respostas inventadas.

## Objetivo

Criar uma camada de precisão acadêmica antes de ligar o Chat Seco V3 definitivamente à API de resposta.

O objetivo não é prometer acerto absoluto, mas aumentar confiabilidade, reduzir alucinação, explicar raciocínio e avisar quando a resposta depender de material ruim, OCR falho ou informação incompleta.

## Regras principais

### 1. Prioridade ao material do aluno

Quando houver print, OCR, PDF, texto colado ou contexto extra, o DilsAI deve usar esse material como fonte principal.

Se a resposta depender do material e o material estiver incompleto ou ilegível, o sistema deve avisar.

### 2. Não inventar certeza

O DilsAI não deve fingir certeza quando:

- o OCR estiver ruim;
- a questão estiver cortada;
- faltar alternativa;
- faltar enunciado;
- houver ambiguidade;
- o tema exigir fonte específica não enviada.

Nesses casos, a resposta deve explicar a limitação e pedir complemento quando necessário.

### 3. Adaptação por nível

O motor deve adaptar a linguagem e profundidade conforme o nível selecionado:

- Alfabetização/reforço: linguagem simples.
- Fundamental: explicação básica com exemplos.
- Ensino médio: foco em compreensão e prova.
- ENEM/Vestibular: interpretação, competências e pegadinhas.
- Técnico: aplicação prática.
- Superior: precisão conceitual e termos técnicos.
- Concurso: objetividade e atenção a alternativas.
- Pós/Avançado: profundidade técnica.

### 4. Adaptação por matéria

A resposta deve considerar a matéria selecionada:

- Exatas: cálculo, fórmulas, passos e conferência.
- Linguagens: interpretação, gramática, estrutura textual.
- Natureza: conceitos, processos e relações.
- Humanas: contexto, causa, consequência e comparação.
- Tecnologia: código, lógica, erros e boas práticas.
- Jurídicas: norma, conceito, aplicação e ressalva.
- Negócios: conceito, exemplo prático e aplicação profissional.
- Saúde: precisão, cautela e linguagem responsável.

### 5. Adaptação por modo

O modo selecionado deve alterar o formato da resposta:

- Professor: explica didaticamente.
- Direto: responde de forma objetiva.
- Resumo: sintetiza.
- Revisão: organiza pontos-chave.
- Passo a passo: resolve por etapas.
- Simulado: cria perguntas.
- Fonte segura: separa o que veio do material e o que é conhecimento geral.
- Exercícios: gera prática.
- Correção de resposta: aponta erro e melhora.
- Plano de estudo: organiza sequência.
- Mapa mental: estrutura tópicos.
- Flashcards: pergunta e resposta.
- Questões comentadas: explica alternativa correta e erradas.
- Aprofundamento técnico: resposta avançada.

## Estrutura mínima de resposta

Quando for uma questão ou print, preferir:

1. Leitura do enunciado ou material.
2. Explicação curta do que está sendo pedido.
3. Resolução passo a passo.
4. Resposta final.
5. Por que essa resposta faz sentido.
6. Erro comum ou ponto de atenção.

## OCR

Se houver OCR:

- usar o texto extraído como contexto;
- avisar quando parecer ilegível;
- não transformar OCR confuso em resposta definitiva;
- permitir que o aluno reenvie ou recorte melhor.

## Checkpoints

- ACADEMIC_ACCURACY_ENGINE_V1_DEFINED
- NO_FAKE_CERTAINTY_RULE_DEFINED
- STUDY_LEVEL_ADAPTATION_DEFINED
- SUBJECT_MODE_ADAPTATION_DEFINED
- OCR_LIMITATION_RULE_DEFINED
