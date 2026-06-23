# DilsAI Estudos — Beta Usage Limits V1

## Objetivo

Definir a primeira régua de limites operacionais para uso beta controlado do DilsAI Estudos.

Este documento parte da tag:

v0.1.31-dilsai-estudos-beta-readiness-checklist-v1

A intenção é preparar o produto para usuários reais sem alterar o Chat V3 aprovado e sem mexer no fluxo de OCR validado.

## Princípio principal

O beta deve ser útil, mas controlado.

O DilsAI Estudos já validou o fluxo:

imagem/print -> OCR/contexto -> API OpenAI paga -> resposta educacional explicada

Agora o produto precisa de limites para evitar:

- custo inesperado de API;
- uso excessivo;
- envio de arquivos grandes demais;
- respostas ruins por OCR fraco;
- experiência confusa quando faltar crédito ou contexto;
- uso fora do posicionamento educacional.

## Limites recomendados para beta controlado

### Uso por pessoa

Limite inicial recomendado:

- até 10 perguntas por dia por usuário beta;
- até 3 imagens/prints por dia por usuário beta;
- até 1 PDF/material maior por dia por usuário beta, quando esse fluxo estiver ativo no beta.

Motivo:

O objetivo do beta é validar qualidade e experiência, não liberar uso ilimitado.

### Tamanho de imagem/print

Limite inicial recomendado:

- imagens de até 5 MB;
- preferir prints nítidos;
- evitar fotos tortas, escuras ou com muito fundo;
- orientar o usuário a cortar apenas a questão quando possível.

Mensagem recomendada quando a imagem for grande ou ruim:

A imagem parece grande ou pouco nítida. Tente enviar um print mais claro, cortado apenas na questão, para o DilsAI conseguir ler melhor.

### Texto enviado pelo usuário

Limite inicial recomendado:

- textos curtos e médios liberados;
- materiais longos devem ser enviados por partes;
- orientar o usuário a mandar uma questão por vez.

Mensagem recomendada:

Para uma resposta melhor, envie uma questão por vez ou divida o material em partes menores.

### OCR ruim ou incompleto

Quando o OCR/contexto parecer insuficiente, o DilsAI deve responder com honestidade.

Mensagem recomendada:

Não consegui ler a questão com segurança. Envie uma imagem mais nítida ou cole o texto da questão para eu explicar corretamente.

Regra:

Não inventar enunciado.

Não completar questão ausente como se tivesse certeza.

### Crédito/API indisponível

Quando a API OpenAI estiver sem crédito, instável ou indisponível, o produto deve mostrar erro amigável.

Mensagem recomendada:

No momento a IA está temporariamente indisponível. Tente novamente em alguns minutos. Se o problema continuar, o suporte precisa verificar o crédito ou a configuração da API.

Regra:

Não expor erro técnico bruto para usuário final.

Não mostrar chave, stack trace ou detalhes internos.

### Conteúdo insuficiente

Quando o usuário pedir para resolver algo sem enviar a questão ou sem contexto suficiente:

Mensagem recomendada:

Preciso ver a questão ou o material para responder com precisão. Envie o texto, um print ou uma imagem da questão.

Regra:

Precisão acima de resposta bonita.

### Uso ético

O DilsAI Estudos deve continuar posicionado como ferramenta de aprendizado.

Mensagem de uso recomendada:

O DilsAI ajuda você a entender a questão e aprender o passo a passo. Use como apoio de estudo, não como forma de burlar avaliações.

Regra permanente:

- sem captura escondida;
- sem modo stealth;
- sem cola automática;
- sem promessa de aprovação;
- sem fingir fonte;
- sem resposta inventada quando faltar base.

## Limites técnicos futuros

Para implementação futura, considerar:

- limite por IP;
- limite por usuário;
- contador diário de perguntas;
- contador diário de imagens;
- limite de tamanho de arquivo;
- timeout de OCR;
- fallback amigável para erro da OpenAI;
- monitoramento simples de custo;
- logs mínimos de evento sem armazenar conteúdo sensível desnecessário.

## O que este PR não faz

Este PR não implementa controle técnico ainda.

Este PR não altera frontend.

Este PR não altera backend.

Este PR não altera OCR.

Este PR não altera Chat V3.

Este PR apenas define a política inicial de uso controlado para guiar os próximos passos.

## Próximo passo recomendado

Criar um PR técnico pequeno para implementar mensagens amigáveis de erro e limites básicos no frontend/backend, sem reconstruir o Chat V3.

Sugestão de próximo marco:

v0.1.33-dilsai-estudos-beta-friendly-errors-v1

## Status

BETA_USAGE_LIMITS_DEFINED_V1
