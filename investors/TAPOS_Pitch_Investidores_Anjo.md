# TAPOS — Tecle AI Platform Operating System
### Documento para Investidores-Anjo

*Versão 1.0 — 15 de julho de 2026*

---

## Resumo Executivo

A Tecle está construindo a TAPOS — a Tecle AI Platform Operating System —, uma plataforma SaaS multi-produto que já opera três verticais de Inteligência Artificial aplicada: **speech-ai** (inteligência de fala e narração de áudio), **edital-ai** (automação de análise de licitações públicas) e **code-ai** (conversão universal de documentos para consumo por LLMs).

O que diferencia a Tecle não é ter construído três produtos de IA. É ter construído, junto com eles, a infraestrutura comum — autenticação, controle de assinatura, fila de execução assíncrona, gateway de produtos — que transforma cada novo produto em uma vertical de receita adicional sobre uma base já paga, e não em um novo projeto de engenharia do zero. Essa é a tese central deste documento: TAPOS não é um produto de IA. É o sistema operacional sobre o qual produtos de IA viram negócio.

Este mesmo documento foi narrado pelo speech-ai, o primeiro produto da plataforma, como prova viva do que a Tecle construiu.

---

## O Problema: IA fragmentada não vira empresa

Nos últimos anos, times técnicos em todo o mundo aprenderam a construir protótipos de IA rapidamente. O gargalo real deixou de ser "conseguimos fazer a IA funcionar?" e passou a ser "conseguimos transformar isso em um produto vendável, cobrável e escalável?". A maioria dos projetos de IA corporativa morre exatamente nessa transição: entre o notebook que funciona e o SaaS que fatura.

Isso acontece porque cada novo produto de IA tende a reconstruir, do zero, a mesma infraestrutura de negócio: autenticação de usuários, controle de quem pagou por quê, execução assíncrona para não travar sob carga, filas, workers, histórico, exportação de resultados. É trabalho de engenharia real, caro, e que não tem nada a ver com o diferencial de cada produto.

A Tecle resolveu esse problema uma única vez, na camada de plataforma, e já colhe o resultado: três produtos de IA completamente diferentes entre si — voz, documentos jurídicos de licitação, conversão de arquivos corporativos — rodando hoje sobre a mesma esteira de autenticação, assinatura e execução assíncrona.

---

## A Plataforma TAPOS

No centro da Tecle está um backend SaaS construído em FastAPI e PostgreSQL que funciona como o sistema nervoso central de todos os produtos. Ele resolve, de forma genérica e reutilizável, os seguintes problemas:

- **Autenticação e identidade** — cadastro, login e sessão protegida por JWT, com senhas protegidas por hash bcrypt.
- **Produtos e assinaturas** — cada vertical de IA é um "produto" com um slug único; cada usuário tem assinaturas ativas ou inativas por produto, o que já habilita, sem nenhuma reengenharia, um modelo comercial de módulos vendidos separadamente.
- **Gateway de produtos** — todo acesso a um produto passa por uma única camada de autorização central, que valida token e assinatura antes de liberar qualquer execução. Um produto nunca é exposto diretamente ao usuário final; ele é sempre mediado pela plataforma.
- **Execução assíncrona real** — além do fluxo síncrono de teste, a plataforma já processa jobs de forma assíncrona: o pedido do usuário é publicado em uma fila RabbitMQ, consumido por um worker dedicado por produto, e o status do processamento pode ser consultado a qualquer momento, do estado "na fila" até "concluído" ou "falhou". Essa arquitetura é o que permite escalar de um usuário de teste para centenas de execuções simultâneas sem travar a experiência de ninguém.
- **Isolamento por produto** — cada produto roda em seu próprio ambiente Python isolado, como um subprocesso independente, comunicando-se com a plataforma central através de um contrato simples de entrada e saída em JSON. Isso significa que um produto pode evoluir, quebrar ou ser reescrito em outra tecnologia sem colocar em risco os demais nem o núcleo da plataforma.

Esse desenho já está validado ponta a ponta, não é uma proposta de arquitetura no papel. Hoje, um usuário autenticado consegue assinar um produto, enviar um arquivo, disparar a execução — síncrona ou assíncrona — e consultar o resultado, para os três produtos da plataforma. É essa esteira comum que faz da Tecle uma plataforma, e não uma coleção de três aplicativos de IA separados.

---

## speech-ai — Inteligência de Fala

O speech-ai é o primeiro produto integrado à TAPOS de ponta a ponta, e é também o mais amadurecido em termos de validação técnica dentro da plataforma.

Ele recebe um roteiro de texto e o transforma em áudio narrado, mas seu diferencial não é apenas converter texto em voz. Antes de gerar qualquer áudio, o speech-ai analisa o conteúdo: detecta automaticamente o idioma do texto — português, inglês, espanhol ou francês —, avalia a complexidade linguística, calcula o ritmo de leitura ideal, define pausas e escolhe o perfil de voz mais adequado ao conteúdo. Só então o texto é transformado em narração. É essa camada de análise prévia que a Tecle chama de Speech Intelligence, e é o que separa o produto de um simples conversor de texto em voz.

A arquitetura foi construída para ser independente de fornecedor. Hoje a síntese de voz roda sobre o motor Microsoft Edge TTS, mas o produto já foi desenhado com uma camada de abstração de provedores que permite plugar, no futuro, outros motores de voz — Azure, motores de código aberto executados localmente, ou provedores especializados — sem alterar o restante do pipeline. Essa decisão de arquitetura protege o produto de ficar refém de um único fornecedor de tecnologia de voz.

Dentro da plataforma, o speech-ai já roda nos dois modelos de execução: o usuário pode disparar uma narração e receber o resultado na hora, ou submeter o pedido para a fila assíncrona e acompanhar o status até a conclusão, com um worker dedicado processando em segundo plano. Essa dupla capacidade — síncrona para casos simples, assíncrona para escala — é exatamente o que permite ao speech-ai atender desde uma narração pontual até um volume de produção de conteúdo em lote.

As aplicações são amplas: narração de treinamentos corporativos e conteúdos de e-learning, geração de áudio para apresentações institucionais, acessibilidade para leitura de documentos, comunicação corporativa em múltiplos idiomas e criação de conteúdo em escala. O mercado global de tecnologias de conversão de texto em voz já está estimado entre quatro e seis bilhões de dólares em 2026, com crescimento anual de dois dígitos, impulsionado pela adoção de assistentes de voz, plataformas de aprendizado digital e automação de atendimento.

---

## edital-ai — Automação de Licitações Públicas

O edital-ai ataca um problema muito concreto e muito brasileiro: editais de licitação pública são documentos longos, frequentemente entre cinquenta e trezentas páginas, escritos em linguagem jurídica repetitiva, cheios de tabelas de itens que se espalham por dezenas de páginas e de prazos críticos — abertura de sessão, impugnação, recurso — que custam caro para qualquer empresa quando são perdidos.

Empresas que participam de licitações com frequência hoje pagam esse custo com tempo humano: um analista lê o edital inteiro, manualmente, para decidir se vale a pena participar, o que precisa ser entregue e até quando. O edital-ai automatiza exatamente essa etapa.

O usuário faz upload do edital em PDF, DOCX ou TXT, e o sistema extrai, de forma determinística — usando leitura de tabelas nativas do documento e reconhecimento de padrões, sem depender de inteligência artificial para os dados críticos — o número do edital, a modalidade, o órgão licitante, o objeto da licitação, cada item e lote com quantidade e valor estimado, os documentos obrigatórios de habilitação e todos os prazos críticos, sinalizando automaticamente quando resta menos de sete dias para um prazo importante. Sobre essa base estruturada, um modelo de inteligência artificial rodando localmente gera um resumo executivo, identifica riscos e oportunidades, e calcula um score de conformidade de zero a cem. Se a camada de inteligência artificial falhar ou estiver indisponível, existe um mecanismo de segurança determinístico que garante que o pipeline nunca trava por causa da IA — uma decisão de arquitetura que prioriza confiabilidade sobre sofisticação.

O resultado final chega ao usuário em quatro formatos prontos para uso imediato: uma planilha Excel com cinco abas de análise, um documento Word, um PDF executivo e um rascunho de e-mail já destacando os prazos mais urgentes.

Este não é um protótipo testado apenas com dados sintéticos. O edital-ai já processou editais públicos reais de prefeituras e órgãos públicos brasileiros, com resultados arquivados e rastreáveis. E, assim como o speech-ai, já está integrado à esteira completa da plataforma: autenticação, assinatura ativa, execução síncrona e assíncrona via fila dedicada, histórico de análises por usuário e download dos artefatos gerados.

O tamanho do mercado que o edital-ai endereça é expressivo. Só o portal federal de compras públicas movimentou mais de quatrocentos e sessenta e cinco bilhões de reais em 2025, distribuídos em cerca de duzentos e oitenta e dois mil processos de contratação conduzidos por mais de três mil órgãos públicos. Somando estados, municípios e demais esferas, as compras governamentais no Brasil ultrapassaram um trilhão de reais no mesmo ano. Cada um desses processos gera, do outro lado, uma ou mais empresas fornecedoras que precisam ler, entender e responder a um edital — o exato problema que o edital-ai resolve.

É importante ser transparente sobre o estágio atual: o edital-ai hoje opera como um piloto validado, com um único edital em processamento por vez em toda a instalação. Para se tornar um produto comercial multi-cliente, o caminho já está mapeado e é bem definido — isolamento de dados por cliente, processamento paralelo em maior escala, e um indicador explícito de confiança sobre cada extração. Nenhum desses itens exige redesenhar o produto: exige investir na próxima camada sobre uma base que já funciona e já processa documentos reais.

---

## code-ai — A Ponte de Dados para IA Corporativa

Toda empresa que hoje tenta adotar Inteligência Artificial de forma séria esbarra no mesmo problema: seus dados mais importantes não estão em texto limpo. Estão espalhados em PDFs, planilhas, apresentações, documentos Word e imagens escaneadas — formatos que modelos de linguagem não conseguem consumir de forma eficiente.

O code-ai resolve esse gargalo de entrada. É um conversor universal que recebe documentos nos formatos mais comuns do ambiente corporativo — PDF, Word, Excel, PowerPoint, CSV, imagens e texto — e produz uma versão padronizada em Markdown, limpa e pronta para ser consumida por ferramentas de IA como Claude, ChatGPT, Copilot ou bases de dados vetoriais internas. Para documentos digitalizados ou imagens, o produto usa reconhecimento óptico de caracteres para extrair o texto mesmo quando ele não existe em formato digital nativo.

O ganho não é apenas de compatibilidade — é de custo. Cada consulta a um modelo de linguagem é cobrada por token, e documentos corporativos brutos, com formatação pesada, desperdiçam uma quantidade enorme de tokens em ruído estrutural. As estimativas internas de economia de tokens, por tipo de documento, variam entre setenta e oitenta e cinco por cento, dependendo do formato de origem. Isso torna qualquer pipeline de inteligência artificial corporativa mais barato de operar e mais rápido de treinar.

Assim como os demais produtos, o code-ai já está conectado ao gateway central da plataforma, com fila assíncrona e worker dedicado processando documentos em segundo plano. Seu público é técnico por natureza — equipes de dados e engenharia que constroem pipelines de IA e RAG dentro das empresas — o que o posiciona tanto como produto autônomo quanto como camada de infraestrutura reaproveitável por baixo de outras verticais da própria Tecle, incluindo o próprio edital-ai no futuro.

---

## A Tese de Plataforma

O que conecta esses três produtos não é semelhança de funcionalidade — voz, licitações e conversão de documentos não têm nada em comum do ponto de vista de usuário final. O que os conecta é que todos rodam sobre a mesma fundação: o mesmo sistema de autenticação, o mesmo modelo de assinatura por produto, o mesmo gateway de autorização, a mesma arquitetura de execução assíncrona por fila e worker.

Isso muda fundamentalmente a economia de lançar um quarto, um quinto, um sexto produto. A próxima vertical de IA que a Tecle lançar não vai precisar reconstruir autenticação, cobrança ou infraestrutura de execução — vai herdar tudo isso no primeiro dia, e o time de engenharia poderá investir cem por cento do seu tempo no que realmente diferencia o novo produto. Essa é, literalmente, a definição de uma plataforma, e é o motivo pelo qual já existe uma quarta vertical, educa-ai, reservada na estrutura da plataforma para os próximos ciclos de desenvolvimento.

Há ainda um segundo fio condutor entre os produtos: a filosofia de inteligência artificial local sempre que possível. Tanto o speech-ai quanto o edital-ai foram desenhados para depender do mínimo possível de provedores de IA em nuvem cobrados por token, priorizando processamento local ou determinístico sempre que a tarefa permite. Isso não é apenas uma escolha técnica — é uma escolha de margem. Enquanto muitos concorrentes no mercado de IA operam como interfaces finas sobre APIs de terceiros, pagando por token a cada execução, a arquitetura da Tecle protege a margem bruta do negócio da variação de custo de provedores externos.

---

## Tração até Aqui

Nada neste documento é uma projeção de PowerPoint. É a descrição de um sistema que está rodando agora.

A plataforma evoluiu de forma incremental e disciplinada: primeiro autenticação e controle de acesso, depois o modelo de produtos e assinaturas, depois o gateway central de autorização, depois a integração real do primeiro produto — o speech-ai — em modo síncrono, e por fim a evolução para execução assíncrona real, com fila de mensagens e workers dedicados, validada e testada em produção local. Esse mesmo modelo de execução assíncrona já foi replicado para os outros dois produtos.

O edital-ai não é uma demonstração com dados fictícios: já processou editais de licitação de órgãos públicos brasileiros reais, com resultados auditáveis. E o áudio que acompanha este documento — a narração que você está ouvindo, ou está prestes a ouvir — foi gerado pelo próprio speech-ai, processando este exato texto, através do mesmo pipeline de produção descrito aqui. A prova de conceito não é uma promessa: é o meio pelo qual esta mensagem chegou até você.

---

## Riscos Conhecidos — E Por Que Eles São a Oportunidade de Investimento

Toda plataforma em estágio inicial tem uma lista honesta de lacunas entre o piloto validado e o produto comercial em escala. A Tecle mapeou essa lista com precisão, produto por produto, e ela converge para um conjunto pequeno e bem definido de investimentos: isolamento completo de dados por cliente para operação multi-tenant, paralelização do processamento assíncrono para atender múltiplos usuários simultâneos, endurecimento de segurança no recebimento de arquivos enviados por usuários, um pipeline de implantação contínua em produção, e a definição final do modelo de cobrança — que já tem a infraestrutura de assinatura pronta, faltando apenas a decisão de negócio entre cobrança por análise, por volume ou por assinatura mensal fixa.

Nenhum desses itens exige reescrever a plataforma. Todos eles são extensões naturais de uma arquitetura que já foi construída pensando em desacoplamento e escala desde o primeiro dia. É exatamente esse tipo de lacuna — conhecida, mapeada e tecnicamente tratável — que capital semente existe para financiar.

---

## Investimento e Uso de Recursos

*[Espaço reservado para o valor da rodada de captação e a alocação detalhada do capital — a ser preenchido pela liderança da Tecle antes do envio final aos investidores.]*

Como direção geral, o capital captado nesta rodada será direcionado a fechar as lacunas descritas na seção anterior — multi-tenancy, escala de processamento, segurança e definição comercial de precificação — e a acelerar a expansão para novas verticais sobre a mesma base de plataforma já validada.

---

## Fechamento

A Tecle não está pedindo a um investidor para apostar em uma ideia. Está mostrando uma plataforma que já processa editais públicos reais, já converte documentos corporativos reais, e que gerou o próprio áudio deste discurso através do seu primeiro produto em produção.

O que foi construído até aqui é a parte mais difícil e menos visível de qualquer negócio de IA: a fundação de autenticação, cobrança e execução em escala que transforma protótipos em produtos vendáveis. Essa fundação já está pronta e validada. O capital que buscamos agora não é para provar que a tecnologia funciona — é para transformar uma plataforma tecnicamente sólida em uma empresa que atende centenas de clientes simultaneamente.

Essa é a TAPOS. Essa é a Tecle.
