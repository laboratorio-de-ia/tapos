# Speech-AI — Visão Geral

## O que é

O Speech-AI é o primeiro produto integrado à TAPOS de ponta a ponta, e o mais maduro em validação técnica dentro da plataforma. Ele recebe um roteiro de texto e o transforma em áudio narrado — mas seu diferencial não é apenas converter texto em voz.

Antes de gerar qualquer áudio, o Speech-AI analisa o conteúdo: detecta automaticamente o idioma (português, inglês, espanhol ou francês), avalia a complexidade linguística, calcula o ritmo de leitura ideal, define pausas e escolhe o perfil de voz mais adequado ao conteúdo. Só então o texto é transformado em narração. Essa camada de análise prévia é o que a Tecle chama de **Speech Intelligence**, e é o que separa o produto de um simples conversor de texto em voz.

## Problema que resolve

Produção de áudio narrado hoje exige ou gravação humana (cara, lenta, difícil de manter atualizada) ou ferramentas de texto-em-voz genéricas que ignoram estrutura, ritmo e adequação de tom ao conteúdo. O Speech-AI insere uma camada de inteligência entre o texto e a síntese, para que o resultado soe natural e adequado ao contexto — sem depender de locução humana para cada atualização de conteúdo.

## Casos de uso

- Narração de treinamentos corporativos e conteúdos de e-learning
- Geração de áudio para apresentações institucionais
- Acessibilidade — leitura de documentos
- Comunicação corporativa em múltiplos idiomas
- Criação de conteúdo em escala (validado com um texto de livro inteiro, +29 mil linhas, processado ponta a ponta sem falhas)

O mercado global de tecnologias de conversão de texto em voz está estimado entre US$ 4–6 bilhões em 2026, com crescimento anual de dois dígitos, impulsionado por assistentes de voz, plataformas de aprendizado digital e automação de atendimento.

## Prova viva

O próprio [documento institucional para investidores](../../../investors/TAPOS_Pitch_Investidores_Anjo.md) da Tecle foi narrado pelo Speech-AI processando seu próprio texto através do mesmo pipeline de produção descrito nesta documentação — a prova de conceito é o meio pelo qual a mensagem chega ao ouvinte.

## Maturidade

Pipeline central (análise de texto → inteligência de fala → construção de narração → síntese via Edge TTS) é real, funcional e evidenciado por logs e artefatos de execução reais. A integração com a TAPOS (execução síncrona e assíncrona via fila e worker dedicado) também está implementada e operacional. Partes da visão de produto — um segundo pipeline de SSML mais avançado e uma camada de IA local para nuances de emoção/intenção — já têm código-base parcial ou planejamento detalhado, mas ainda não estão em produção. Ver [roadmap.md](roadmap.md).

## Ver também

- [architecture.md](architecture.md) — como os componentes se conectam
- [pipeline.md](pipeline.md) — o fluxo de processamento passo a passo
- [../00-tecle/vision.md](../00-tecle/vision.md) — o papel do Speech-AI na tese de plataforma da Tecle
