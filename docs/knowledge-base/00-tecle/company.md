# Tecle — A Empresa

## O que é a Tecle

A Tecle é uma empresa de engenharia de software especializada em transformar Inteligência Artificial em produtos SaaS vendáveis, cobráveis e escaláveis. Não constrói modelos de IA do zero: constrói a ponte de engenharia — autenticação, cobrança, execução em escala, infraestrutura — que falta entre um protótipo de IA que funciona e um negócio de software que fatura.

A tese central da empresa é simples de enunciar e difícil de executar: **a maioria dos projetos de IA corporativa morre na transição entre o notebook que funciona e o SaaS que fatura**. Cada novo produto de IA tende a reconstruir, do zero, a mesma infraestrutura de negócio — autenticação de usuários, controle de quem pagou por quê, execução assíncrona para não travar sob carga, filas, workers, histórico, exportação de resultados. É trabalho de engenharia real, caro, e que não tem nada a ver com o diferencial de cada produto de IA em si.

A Tecle resolveu esse problema uma única vez, na camada de plataforma — a **TAPOS (Tecle AI Platform Operating System)** — e a partir dela já opera três produtos de IA completamente diferentes entre si sobre a mesma esteira de autenticação, assinatura, gateway de autorização e execução assíncrona.

## O que a Tecle constrói

### A plataforma

A **TAPOS** é o sistema nervoso central de todos os produtos: um backend SaaS em FastAPI e PostgreSQL que resolve, de forma genérica e reutilizável, autenticação e identidade, produtos e assinaturas, gateway central de autorização e execução assíncrona real via fila de mensagens e workers dedicados. Ver [01-tapos/overview.md](../01-tapos/overview.md).

### Os produtos

Sobre essa plataforma, a Tecle opera hoje três verticais de IA aplicada, e reserva uma quarta para os próximos ciclos:

- **[Speech-AI](../02-speech-ai/overview.md)** — inteligência de fala: transforma roteiros de texto em narração de áudio, com análise linguística prévia (idioma, complexidade, ritmo, pausas, perfil de voz) antes da síntese. É o produto mais maduro e o primeiro integrado de ponta a ponta na plataforma.
- **[Edital-AI](../03-products/edital-ai.md)** — automação de licitações públicas brasileiras: extrai de forma determinística prazos, itens, lotes e documentos de habilitação de editais, e usa IA local para gerar resumo executivo, riscos e um score de conformidade.
- **[Code-AI](../03-products/code-ai.md)** — conversor universal de documentos corporativos (PDF, Word, Excel, PowerPoint, imagens) para Markdown limpo, pronto para consumo por LLMs e pipelines de RAG, com economia estimada de 70–85% em tokens.
- **Educa-AI** (reservado) — quarta vertical planejada, voltada a educação financeira e acompanhamento de mercado. Ver [03-products/educa-ai.md](../03-products/educa-ai.md) para o estágio atual.

## Modelo de negócio

Cada produto é uma vertical de receita independente, vendida como assinatura sobre a mesma base de plataforma. O modelo de **produtos e assinaturas** já está implementado na TAPOS: cada usuário tem assinaturas ativas ou inativas por produto, o que habilita — sem nenhuma reengenharia — a venda de módulos separadamente. O ganho de escala não está em cada produto isoladamente, mas no fato de que o próximo produto lançado herda toda a infraestrutura de autenticação, cobrança e execução no primeiro dia.

## Estágio atual

A Tecle está em estágio inicial (seed), com a plataforma tecnicamente validada e em produção local:

- infraestrutura operacional (Docker, PostgreSQL, Redis, RabbitMQ, MinIO, Qdrant, Ollama);
- autenticação, produtos, assinaturas, gateway e execução assíncrona implementados e testados (baseline v1.0.0);
- Speech-AI integrado de ponta a ponta; Edital-AI e Code-AI também conectados ao gateway central;
- Edital-AI já processou editais públicos reais de prefeituras e órgãos brasileiros, com resultados auditáveis.

As lacunas conhecidas — multi-tenancy completo, paralelização de processamento, hardening de segurança no upload de arquivos, pipeline de deploy contínuo e definição final do modelo de cobrança — estão mapeadas e são extensões naturais da arquitetura existente, não redesenhos. Ver [01-tapos/roadmap.md](../01-tapos/roadmap.md).

## Ver também

- [vision.md](vision.md) — a tese de plataforma e a filosofia de engenharia por trás da Tecle
- [competencies.md](competencies.md) — as competências técnicas e de domínio que sustentam essa tese
