# DilsAI Estudos — Preparação Android e Play Console

## Estado atual

- Produto web funcionando.
- Backend em produção.
- Upload de PDF, imagem e texto funcionando.
- Respostas renderizadas de forma limpa.
- Enter envia pergunta e Shift + Enter quebra linha.
- Não existe estrutura Android ainda neste repositório.

## Objetivo

Preparar o DilsAI Estudos para virar aplicativo Android publicado na Play Console, com plano gratuito e assinatura Plus.

## App Android

Nome público: DilsAI Estudos

Package name proposto: com.dilsai.estudos

Arquitetura inicial proposta: Android nativo simples com WebView.

O app Android carregará a experiência do DilsAI e terá integração nativa com Google Play Billing para liberar recursos Plus.

## Backend

Backend atual: https://dilsai-api.onrender.com

Endpoint futuro proposto: POST /api/verify-dilsai-plus

Responsabilidades:

- Receber purchaseToken enviado pelo app Android.
- Validar a assinatura na Google.
- Retornar se o usuário tem Plus ativo.
- Falhar fechado: se não validar, não libera Plus.

## Planos

### Gratuito

- Uso básico.
- Perguntas limitadas.
- Upload simples limitado.
- Serve para demonstração e aquisição de usuários.

### Plus mensal

ID proposto: dilsai_plus_monthly

Benefícios:

- Mais perguntas.
- Uso com PDF e imagem.
- Respostas mais completas.
- Histórico e recursos extras futuramente.

### Plus anual

ID proposto: dilsai_plus_yearly

Benefícios:

- Mesmos recursos do mensal.
- Preço com desconto.

## Play Console

Itens necessários:

- Criar app novo na Play Console.
- Nome: DilsAI Estudos.
- Categoria: Educação ou Ferramentas educacionais.
- Política de privacidade.
- Ícone 512x512.
- Gráfico de recursos 1024x500.
- Capturas de tela.
- Classificação indicativa.
- Segurança dos dados.
- Público-alvo.
- Produtos de assinatura.
- Teste interno ou fechado.
- AAB assinado.

## Regras importantes

- Não liberar Plus apenas pelo frontend.
- Não confiar em flag local do app.
- Toda compra precisa ser validada no backend.
- Se a validação falhar, o app deve tratar como gratuito.
- Não prometer cola, fraude acadêmica ou resposta para burlar prova.
- Posicionamento correto: apoio de estudo, explicação e revisão.

## Próximas fases

1. Criar estrutura Android.
2. Definir ícone e identidade visual.
3. Criar app na Play Console.
4. Criar assinaturas mensal e anual.
5. Integrar Play Billing.
6. Criar endpoint de validação no backend.
7. Fazer teste interno.
8. Preparar publicação.
