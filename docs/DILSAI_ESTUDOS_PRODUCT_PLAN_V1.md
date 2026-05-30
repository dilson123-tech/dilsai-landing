# DilsAI Estudos — Product Plan V1

## 1. Visão oficial

O DilsAI Estudos é uma plataforma de inteligência artificial para estudo, explicação, revisão, simulados e respostas guiadas por base confiável.

Este projeto deve ser tratado como produto real para venda e comercialização, não como experimento solto.

A proposta não é criar apenas mais um chatbot genérico. A proposta é criar uma IA de estudos com:

- resposta clara;
- explicação didática;
- controle contra resposta inventada;
- modos de estudo;
- temas organizados;
- possibilidade futura de responder com base em PDFs, apostilas, materiais próprios e fontes cadastradas.

## 2. Regra principal: precisão acima de volume

A prioridade do DilsAI Estudos é responder com responsabilidade.

Regra obrigatória:

> Quando não houver informação suficiente para responder com segurança, a IA deve avisar que não encontrou base suficiente, em vez de inventar uma resposta.

Resposta segura padrão:

> Não encontrei informação suficiente na base atual para responder com segurança. Posso explicar o conceito geral, mas para uma resposta precisa preciso que você envie o material, apostila, PDF ou contexto da aula.

Essa regra é central para o produto.

## 3. Posicionamento comercial

Nome inicial:

**DilsAI Estudos**

Frase comercial:

**Seu professor de bolso com IA, explicação clara, revisão inteligente e respostas mais confiáveis.**

Promessa:

Ajudar estudantes, profissionais e concurseiros a aprender melhor, revisar conteúdos, resolver dúvidas e testar conhecimento com uma IA prática, acessível e cuidadosa.

## 4. Problema que o produto resolve

Muitos alunos usam IAs genéricas para estudar, mas enfrentam problemas:

- respostas bonitas, mas erradas;
- falta de fonte;
- explicação rasa;
- ausência de plano de estudo;
- falta de simulado;
- dificuldade para revisar;
- risco de copiar sem entender;
- excesso de confiança em resposta sem base.

O DilsAI Estudos deve resolver isso com uma IA mais orientada para aprendizado real.

## 5. Público-alvo inicial

Públicos recomendados para o MVP:

1. Estudantes de programação.
2. Alunos de cursos técnicos.
3. Concurseiros iniciantes.
4. Estudantes que precisam reforçar português, matemática e lógica.
5. Profissionais que querem estudar usando apostilas e PDFs próprios.

## 6. Temas iniciais do MVP

O MVP não deve começar tentando cobrir todos os assuntos do mundo.

Temas iniciais oficiais:

### 6.1 Programação

- lógica de programação;
- Python;
- HTML;
- CSS;
- JavaScript;
- Git;
- APIs;
- banco de dados.

### 6.2 Português e redação

- interpretação de texto;
- gramática básica;
- reescrita;
- resumo;
- argumentação;
- redação.

### 6.3 Matemática e raciocínio lógico

- operações básicas;
- porcentagem;
- regra de três;
- lógica;
- problemas matemáticos;
- matemática para concursos.

Temas futuros possíveis:

- Direito;
- Administração;
- Informática para concursos;
- Segurança do Trabalho;
- Logística;
- Educação financeira;
- Treinamentos internos empresariais.

## 7. Modos de resposta

O DilsAI Estudos deve ter modos claros para o aluno escolher como quer estudar.

### 7.1 Modo Direto

Resposta curta e objetiva.

Uso:

- dúvida rápida;
- revisão simples;
- pergunta conceitual.

### 7.2 Modo Professor

Resposta didática, com explicação passo a passo e exemplos.

Uso:

- aluno iniciante;
- conteúdo difícil;
- explicação detalhada.

### 7.3 Modo Passo a Passo

A IA resolve junto com o aluno, explicando o raciocínio.

Uso:

- exercícios;
- matemática;
- lógica;
- programação.

### 7.4 Modo Simulado

A IA gera perguntas, alternativas, correção e explicação.

Uso:

- preparação para prova;
- concurso;
- revisão;
- teste de conhecimento.

### 7.5 Modo Revisão

A IA cria resumo, tópicos principais e perguntas de fixação.

Uso:

- revisar aula;
- estudar apostila;
- preparar prova.

### 7.6 Modo Fonte Segura

A IA responde priorizando material carregado ou base cadastrada.

Uso:

- PDFs;
- apostilas;
- documentos de curso;
- materiais próprios.

Regra:

Quando o Modo Fonte Segura estiver ativo, a IA deve evitar resposta livre sem avisar o usuário.

## 8. Motor de precisão

O caminho técnico do produto deve evoluir para RAG.

RAG significa que a IA consulta uma base de conhecimento antes de responder.

Fluxo esperado:

1. Usuário faz uma pergunta.
2. Sistema identifica tema e modo de resposta.
3. Sistema busca conteúdo relevante na base.
4. IA responde usando o conteúdo encontrado.
5. IA informa quando não existe base suficiente.
6. Resposta pode indicar fonte, tema e nível de confiança.

## 9. Política contra resposta inventada

A IA deve evitar:

- inventar fonte;
- inventar autor;
- inventar artigo;
- inventar fórmula;
- afirmar certeza sem base;
- dar resposta avançada para aluno iniciante sem explicar;
- resolver exercício sem ensinar quando o modo professor estiver ativo.

A IA deve preferir:

- explicar com clareza;
- separar fato, exemplo e hipótese;
- declarar incerteza;
- pedir material quando necessário;
- mostrar raciocínio;
- ajudar o aluno a aprender, não apenas copiar.

## 10. Estrutura técnica desejada

### 10.1 Frontend

A landing atual pode ser reaproveitada, mas deve evoluir para:

- página comercial do DilsAI Estudos;
- chat do aluno;
- seletor de tema;
- seletor de modo de resposta;
- histórico;
- painel de progresso;
- área de simulados;
- área de materiais.

### 10.2 Backend

Backend recomendado:

- FastAPI;
- endpoint de saúde;
- endpoint de chat;
- serviço de IA separado;
- configuração por ambiente;
- controle de temas;
- controle de modos;
- histórico de conversas;
- autenticação futura;
- limite de uso por plano.

### 10.3 Banco de dados futuro

Banco recomendado para produto real:

- PostgreSQL.

Tabelas futuras:

- users;
- study_topics;
- study_materials;
- conversations;
- messages;
- quizzes;
- quiz_answers;
- usage_events;
- subscriptions.

### 10.4 Configuração de IA

A chave da IA nunca deve ficar fixa no código.

Variáveis esperadas:

- OPENAI_API_KEY;
- LLM_PROVIDER;
- LLM_MODEL;
- LLM_TEMPERATURE;
- LLM_MAX_TOKENS.

## 11. Segurança mínima obrigatória

Antes de vender, o projeto precisa:

- remover qualquer chave fixa do código;
- usar `.env`;
- criar `.env.example`;
- revisar CORS;
- criar `/health`;
- criar logs básicos;
- criar README técnico do backend;
- separar ambiente local e produção;
- criar testes mínimos;
- não salvar dados sensíveis sem necessidade.

## 12. MVP vendável V1

O MVP inicial deve conter:

- landing reposicionada para estudos;
- backend com chat real;
- modos de resposta;
- temas iniciais;
- prompt base do professor;
- resposta segura quando faltar informação;
- histórico simples;
- limite de uso;
- plano gratuito/teste;
- plano estudante;
- plano pro;
- documentação comercial.

Não entra no MVP inicial:

- app mobile nativo;
- todos os temas;
- marketplace de professores;
- integração escolar completa;
- correção avançada com nota oficial;
- pagamento complexo antes de validar uso.

## 13. Planos comerciais iniciais

### Gratuito

- limite diário;
- temas básicos;
- respostas diretas.

### Estudante

Preço sugerido inicial:

- R$ 19,90 a R$ 29,90 por mês.

Inclui:

- mais mensagens;
- modo professor;
- revisão;
- simulados;
- histórico.

### Pro Estudos

Preço sugerido inicial:

- R$ 49,90 por mês.

Inclui:

- mais limite;
- upload de materiais;
- modo fonte segura;
- simulados avançados;
- trilha de estudo.

### Turmas, escolas e empresas

Preço sob consulta.

Inclui:

- usuários múltiplos;
- materiais próprios;
- base privada;
- suporte;
- painel de acompanhamento.

## 14. Régua atual

Estado estimado no início deste plano:

- Landing pública: 60%
- Identidade inicial DilsAI: 50%
- Backend inicial: 20%
- Chat real com IA: 5%
- Precisão/RAG: 0%
- Login/usuários: 0%
- Materiais/base de conhecimento: 0%
- Planos/pagamento: 0%
- Produto vendável: 15%

Meta do ciclo V1:

- Produto documentado: 100%
- Direção comercial definida: 100%
- Backend saneado: 70%
- Chat real MVP: 60%
- Modos de resposta: 60%
- Landing reposicionada: 70%
- Produto vendável inicial: 35%

## 15. Sequência oficial de desenvolvimento

### Ciclo 1 — Fundação

- Criar plano oficial do produto.
- Criar README técnico do backend.
- Criar `.env.example`.
- Remover qualquer chave fixa.
- Criar `/health`.
- Criar `/api/v1/chat`.

### Ciclo 2 — IA real controlada

- Criar serviço de LLM.
- Criar prompt base do Professor DilsAI.
- Criar modos de resposta.
- Criar validação de entrada.
- Criar resposta segura quando faltar contexto.

### Ciclo 3 — Temas de estudo

- Criar registry de temas.
- Adicionar programação.
- Adicionar português.
- Adicionar matemática/lógica.
- Permitir escolha de tema no chat.

### Ciclo 4 — Base de conhecimento

- Criar ingestão simples de materiais.
- Criar divisão em trechos.
- Criar busca semântica.
- Responder com fonte.
- Aplicar política de "não encontrei base suficiente".

### Ciclo 5 — Produto comercial

- Atualizar landing.
- Criar planos.
- Criar CTA comercial.
- Criar painel simples.
- Criar controle de uso.
- Preparar piloto com usuários reais.

## 16. Critérios para considerar o MVP vendável

O MVP só pode ser considerado vendável quando:

- responder perguntas reais com consistência;
- diferenciar resposta geral de resposta baseada em fonte;
- recusar ou avisar quando não tiver segurança;
- explicar de forma didática;
- cobrir pelo menos 3 temas iniciais;
- ter backend sem chave fixa;
- ter documentação clara;
- ter landing comercial honesta;
- ter limite básico de uso;
- ter fluxo mínimo de usuário.

## 17. Diretriz final

O DilsAI Estudos deve ser construído com foco em confiança.

O diferencial não será dizer que sabe tudo.

O diferencial será:

- ensinar melhor;
- responder com mais responsabilidade;
- admitir incerteza;
- adaptar explicação ao nível do aluno;
- transformar estudo em rotina;
- ajudar o aluno a evoluir.

Produto real não se sustenta com promessa gigante. Produto real se sustenta com resultado, segurança e clareza.
