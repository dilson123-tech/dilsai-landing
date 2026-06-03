# DilsAI Estudos — Commercial Readiness Roadmap V1

## 1. Natureza do ciclo

Este documento inicia a fase pós-MVP do DilsAI Estudos.

O MVP inicial foi fechado oficialmente na tag:

`v0.1.20-dilsai-estudos-mvp-readiness-v1`

A partir deste ponto, o projeto não deve ser tratado como laboratório, brincadeira, tela bonita ou experimento descartável.

O DilsAI Estudos é um produto real, com objetivo de apoiar alunos em estudos, revisões, testes, provas e organização de conteúdo educacional.

A nova meta não é apenas “funcionar”.  
A nova meta é chegar a um produto 100% vendável, confiável e apresentável para clientes reais.

## 2. Estado atual

Régua atual:

- MVP técnico inicial: 100%
- Produto para piloto real acompanhado: 90%
- Produto vendável com segurança inicial: 70% a 75%
- Produto comercial 100% pronto: em construção

O MVP já entrega:

- backend funcional;
- frontend funcional;
- tela cheia de estudos;
- seleção de nível, matéria e modo;
- base interna simples;
- resposta com fonte;
- upload de texto e Markdown;
- upload de PDF textual;
- OCR em imagem;
- OCR em PDF escaneado;
- fallback seguro quando a IA externa está indisponível;
- fonte amigável no frontend;
- documentação e QA por ciclo.

## 3. Decisão estratégica

O projeto não vai parar no MVP.

O MVP fechado serve como fundação estável.

A próxima fase deve transformar essa fundação em produto comercial real, com:

- posicionamento claro;
- segurança jurídica mínima;
- privacidade;
- controle de acesso;
- controle de custo;
- demonstração comercial;
- piloto com usuários reais;
- roadmap técnico para RAG/embeddings;
- evolução sem quebrar OCR, upload, fallback ou fonte.

## 4. O que NÃO fazer nesta fase

Para proteger o projeto, ficam proibidas as seguintes ações sem decisão explícita:

- refazer backend do zero;
- refazer frontend do zero;
- trocar FastAPI sem necessidade;
- iniciar banco de dados sem escopo claro;
- iniciar RAG/embeddings direto no código sem planejamento;
- misturar RAG com OCR V2 no mesmo PR;
- remover fallback seguro;
- remover rastreabilidade de fonte;
- fingir que OCR é perfeito;
- prometer aprovação em prova;
- prometer resposta infalível;
- salvar material do aluno sem política clara;
- expor chave OpenAI;
- commitar `.env`;
- transformar o produto em bagunça de features sem prioridade comercial.

## 5. O que falta para produto 100% vendável

### 5.1 Comercial e apresentação

Status atual: pendente

Entregas necessárias:

- landing/page comercial clara;
- proposta de valor objetiva;
- público-alvo definido;
- roteiro de demonstração;
- benefícios sem exagero;
- limitações honestas;
- plano piloto;
- modelo simples de preço;
- material para apresentar a pais, alunos, professores ou cursinhos.

### 5.2 Segurança jurídica e privacidade

Status atual: pendente

Entregas necessárias:

- termos de uso inicial;
- política de privacidade inicial;
- aviso de uso educacional;
- aviso de que não garante nota ou aprovação;
- aviso de que respostas devem ser conferidas;
- regra sobre material enviado pelo aluno;
- regra de não armazenar arquivo permanentemente sem consentimento explícito.

### 5.3 Acesso controlado

Status atual: pendente

Entregas necessárias:

- login simples ou chave de acesso;
- controle básico de sessões;
- separação mínima por usuário;
- proteção de rotas futuras;
- base para plano gratuito/pago no futuro.

### 5.4 Controle de custo e uso

Status atual: pendente

Entregas necessárias:

- limite de perguntas por usuário;
- limite de upload;
- limite de OCR;
- limite de PDF escaneado;
- controle de custo com IA externa;
- mensagens claras quando o limite for atingido;
- evitar uso infinito sem controle.

### 5.5 Deploy e ambiente real

Status atual: pendente

Entregas necessárias:

- backend hospedado;
- frontend hospedado;
- variáveis de ambiente seguras;
- chave OpenAI fora do repositório;
- logs mínimos;
- healthcheck;
- instrução de rollback;
- domínio ou URL demonstrável.

### 5.6 RAG/embeddings

Status atual: não iniciado

RAG é o próximo salto técnico pesado, mas deve entrar com planejamento.

Antes de codar, definir:

- o que será indexado;
- onde os embeddings serão armazenados;
- como separar base interna de material do aluno;
- como limpar ou reindexar;
- como citar fonte;
- como evitar resposta inventada;
- como limitar custo;
- se será Chroma, FAISS, SQLite, arquivos locais ou outro caminho.

### 5.7 Base de conhecimento

Status atual: inicial

Entregas necessárias:

- ampliar conteúdos por matéria;
- organizar por nível escolar;
- criar padrão de arquivo;
- criar metadados;
- criar critérios de qualidade;
- garantir que fonte seja exibida.

### 5.8 QA com usuários reais

Status atual: pendente

Entregas necessárias:

- piloto com poucos usuários;
- coleta de feedback;
- registro de erros;
- registro de dúvidas reais;
- avaliação de OCR em documentos reais;
- avaliação de respostas para prova/teste;
- ajuste do posicionamento comercial.

## 6. Sequência recomendada de tags

A sequência sugerida para levar o produto ao 100%:

- `v0.1.21-dilsai-estudos-commercial-readiness-roadmap-v1`
- `v0.1.22-dilsai-estudos-terms-privacy-v1`
- `v0.1.23-dilsai-estudos-commercial-landing-v1`
- `v0.1.24-dilsai-estudos-access-control-v1`
- `v0.1.25-dilsai-estudos-usage-limits-v1`
- `v0.1.26-dilsai-estudos-rag-planning-v1`
- `v0.1.27-dilsai-estudos-rag-foundation-v1`
- `v0.1.28-dilsai-estudos-deploy-pilot-v1`
- `v0.1.29-dilsai-estudos-real-user-qa-v1`
- `v0.1.30-dilsai-estudos-commercial-launch-readiness-v1`

## 7. Régua de prontidão comercial

### MVP técnico

Status: 100%

O produto funciona localmente e tem recursos centrais validados.

### Piloto real acompanhado

Status: 90%

Pode ser usado com usuários reais em ambiente controlado, com acompanhamento próximo e aviso claro de limites.

### Venda inicial controlada

Status: 70% a 75%

Ainda precisa de termos, privacidade, acesso controlado, custo/limite e página comercial.

### Venda ampla

Status: pendente

Só deve ser considerada após deploy, controle de uso, QA real e estrutura comercial mínima.

## 8. Posição comercial correta

O DilsAI Estudos deve ser vendido como:

“Plataforma educacional com IA para apoio ao estudo, revisão de conteúdo, leitura de materiais enviados pelo aluno e preparação para testes e provas, com fonte/contexto quando disponível e avisos honestos sobre limites da IA e OCR.”

Não deve ser vendido como:

- garantia de aprovação;
- substituto de professor;
- corretor perfeito de prova;
- IA infalível;
- leitor perfeito de qualquer documento;
- solução final sem supervisão.

## 9. Próximo passo recomendado

O próximo ciclo após este roadmap deve ser:

`v0.1.22-dilsai-estudos-terms-privacy-v1`

Objetivo:

- criar Termos de Uso inicial;
- criar Política de Privacidade inicial;
- criar aviso educacional;
- proteger o produto antes de colocar usuários reais pagando ou testando de forma pública.

## 10. Checkpoint

`DILSAI_ESTUDOS_COMMERCIAL_READINESS_ROADMAP_V1_OK`
