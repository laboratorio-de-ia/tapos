# Competências

A Tecle combina três camadas de competência que, juntas, sustentam a tese de plataforma: engenharia de infraestrutura SaaS, aplicação prática de Inteligência Artificial e conhecimento de domínio vertical. Nenhuma das três sozinha diferenciaria a empresa — é a combinação das três, replicada de forma consistente entre produtos, que faz da TAPOS uma plataforma e não uma coleção de projetos.

## 1. Engenharia de plataforma SaaS

- **Autenticação e identidade**: cadastro, login e sessão protegida por JWT, com senhas protegidas por hash bcrypt.
- **Modelo de produtos e assinaturas**: cada vertical de IA como um produto com identidade própria (slug), com assinaturas ativas/inativas por usuário — infraestrutura de cobrança modular pronta antes mesmo da decisão comercial de precificação.
- **Gateway central de autorização**: nenhum produto é exposto diretamente ao usuário final; todo acesso passa por uma camada única que valida token e assinatura antes de liberar qualquer execução.
- **Execução assíncrona real**: fila de mensagens (RabbitMQ) com worker dedicado por produto, status consultável do estado "na fila" até "concluído" ou "falhou" — capacidade de escalar de um usuário de teste a centenas de execuções simultâneas sem travar a experiência de ninguém.
- **Isolamento por produto**: cada produto roda em ambiente Python isolado (subprocesso independente), comunicando-se com a plataforma central por um contrato simples de entrada/saída em JSON — um produto pode evoluir, quebrar ou ser reescrito sem colocar em risco os demais.

Ver [01-tapos/architecture.md](../01-tapos/architecture.md) e [04-platform/gateway.md](../04-platform/gateway.md) para o detalhamento técnico.

## 2. Aplicação prática de Inteligência Artificial

A Tecle não constrói modelos de fundação — aplica IA (local, em nuvem ou determinística, conforme o problema exigir) dentro de um pipeline de produto confiável:

- **Síntese e inteligência de fala** (Speech-AI): análise linguística prévia — detecção de idioma, complexidade, ritmo de leitura, pausas e seleção de perfil de voz — antes da conversão texto→áudio, com arquitetura de provedores plugável.
- **IA local para análise de documentos** (Edital-AI): modelo rodando via Ollama para resumo executivo, identificação de risco/oportunidade e score de conformidade, sempre com fallback determinístico caso a IA falhe — a extração de dados críticos em si é 100% determinística (leitura de tabelas nativas, regex e heurísticas), não dependente de IA.
- **OCR e conversão de documentos para consumo por LLM** (Code-AI): normalização de PDF, Word, Excel, PowerPoint e imagens digitalizadas em Markdown limpo, reduzindo significativamente o consumo de tokens em pipelines de IA e RAG corporativos.

A regra que atravessa os três produtos: **usar IA onde ela gera diferencial real, e determinismo onde a confiabilidade importa mais do que a sofisticação.**

## 3. Conhecimento de domínio vertical

- **Compras públicas brasileiras**: entendimento profundo da estrutura de um edital de licitação — modalidades, tabelas de itens/lotes, documentos de habilitação, prazos críticos (abertura, impugnação, recurso) — validado contra editais reais de prefeituras e órgãos públicos.
- **Produção de conteúdo em áudio corporativo**: treinamentos, e-learning, apresentações institucionais, acessibilidade e comunicação multilíngue.
- **Engenharia de dados para IA corporativa**: entendimento de como equipes de dados constroem pipelines de RAG e por que o formato de entrada (não apenas o modelo) determina custo e qualidade.

## 4. Disciplina de engenharia e operação com IA como parceira de desenvolvimento

A própria forma como a Tecle constrói é uma competência: desenvolvimento incremental e disciplinado, um módulo por vez, testado e commitado antes do próximo passo, usando o **Claude Code** como assistente de engenharia orientado por contexto persistente (`.claude/workspace.md`, `.claude/constitution.md`). Essa disciplina é o que permitiu levar a plataforma de autenticação básica até gateway multi-produto com execução assíncrona em ciclos curtos e validados. Ver [05-development/development-flow.md](../05-development/development-flow.md).

## Ver também

- [company.md](company.md)
- [vision.md](vision.md)
- [01-tapos/technologies.md](../01-tapos/technologies.md) — stack técnico concreto por trás dessas competências
