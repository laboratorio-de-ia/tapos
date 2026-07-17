# Visão

## A tese de plataforma

TAPOS não é um produto de Inteligência Artificial. **É o sistema operacional sobre o qual produtos de Inteligência Artificial se transformam em negócio.**

Essa frase resume a visão da Tecle. O mercado está cheio de protótipos de IA que funcionam tecnicamente e morrem comercialmente, porque conseguir fazer a IA responder deixou de ser o problema difícil — o problema difícil passou a ser transformar isso em algo vendável, cobrável e escalável. Isso exige autenticação, controle de quem pagou por quê, execução assíncrona sob carga, filas, workers, histórico e exportação de resultado: infraestrutura de negócio que nada tem a ver com o diferencial de cada produto de IA, mas que sem ela nenhum produto vira empresa.

A Tecle escolheu resolver esse problema **uma única vez, na camada de plataforma**, e reaproveitá-lo em cada nova vertical. O resultado observável disso é que voz (Speech-AI), documentos jurídicos de licitação (Edital-AI) e conversão de arquivos corporativos (Code-AI) — três produtos sem nenhuma semelhança funcional entre si do ponto de vista do usuário final — rodam hoje sobre exatamente a mesma esteira de autenticação, assinatura, gateway de autorização e execução assíncrona.

## O que isso muda

Isso muda fundamentalmente a economia de lançar um quarto, um quinto, um sexto produto. A próxima vertical de IA que a Tecle lançar não precisa reconstruir autenticação, cobrança ou infraestrutura de execução — ela herda tudo isso no primeiro dia, e o time de engenharia investe cem por cento do seu tempo no que realmente diferencia o novo produto. Essa é, literalmente, a definição de uma plataforma. É também o motivo pelo qual já existe uma quarta vertical, o Educa-AI, reservada na estrutura da TAPOS para os próximos ciclos.

## Princípio: Inteligência Artificial local sempre que possível

Há um segundo fio condutor entre os produtos da Tecle, tão importante quanto o primeiro: a filosofia de **usar IA local sempre que a tarefa permitir**, minimizando dependência de provedores de IA em nuvem cobrados por token.

- O Speech-AI foi desenhado com uma camada de abstração de provedores de síntese de voz, para não ficar refém de um único fornecedor.
- O Edital-AI usa extração determinística (leitura de tabelas nativas, reconhecimento de padrões) para todos os dados críticos, e reserva IA — rodando localmente via Ollama — apenas para a camada de análise (resumo, riscos, score), com um mecanismo de segurança determinístico caso a IA falhe.

Essa não é apenas uma escolha técnica — é uma escolha de margem. Enquanto muitos concorrentes de mercado operam como interfaces finas sobre APIs de terceiros, pagando por token a cada execução, a arquitetura da Tecle protege a margem bruta do negócio da variação de custo de provedores externos.

## Princípio: confiabilidade antes de sofisticação

Onde a IA pode falhar, o pipeline não pode travar. O Edital-AI é o exemplo mais claro dessa regra: se a camada de IA falhar ou estiver indisponível, um mecanismo de segurança determinístico garante que o processo de análise continue até o fim. A Tecle prioriza sistematicamente confiabilidade sobre sofisticação sempre que as duas estiverem em tensão.

## Honestidade sobre o estágio

A visão da Tecle inclui ser transparente sobre o que já está pronto e o que ainda não está. Nenhum dos produtos é vendido como mais maduro do que é:

- o Speech-AI é o mais validado, já rodando em produção síncrona e assíncrona;
- o Edital-AI já processa editais reais, mas opera hoje como piloto validado de single-tenant (um edital por vez em toda a instalação);
- o Educa-AI é explicitamente reservado para o futuro, sem implementação ainda.

As lacunas entre piloto validado e produto comercial em escala — multi-tenancy, paralelização, hardening de segurança, deploy contínuo, modelo de cobrança final — são conhecidas, mapeadas e tecnicamente tratáveis. Nenhuma delas exige redesenhar a plataforma: todas são extensões naturais de uma arquitetura já construída, desde o primeiro dia, pensando em desacoplamento e escala.

## Onde a Tecle quer chegar

O objetivo de longo prazo é operar uma plataforma multi-produto de IA que atenda centenas de clientes simultaneamente, com cada nova vertical de IA lançada como um incremento de receita sobre uma fundação já paga — nunca como um novo projeto de engenharia começado do zero.

> "A Tecle não está pedindo a um investidor para apostar em uma ideia. Está mostrando uma plataforma que já processa editais públicos reais, já converte documentos corporativos reais, e que gerou o próprio áudio do seu discurso institucional através do seu primeiro produto em produção."
> — [Documento para Investidores-Anjo, TAPOS v1.0](../../../investors/TAPOS_Pitch_Investidores_Anjo.md)

## Ver também

- [company.md](company.md) — o que a Tecle é e constrói hoje
- [01-tapos/principles.md](../01-tapos/principles.md) — como essa visão se traduz em princípios de engenharia concretos
