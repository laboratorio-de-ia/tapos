# TAPOS — Visão Geral

## O que é

A **TAPOS (Tecle AI Platform Operating System)** é a plataforma de engenharia da Tecle para construção e operação de produtos SaaS baseados em Inteligência Artificial. Ela organiza desenvolvimento, runtime e infraestrutura de forma modular, desacoplada e escalável, permitindo evolução incremental e controle técnico completo.

Não é, em si, um produto de IA — é a fundação de negócio (autenticação, produtos, assinaturas, gateway de autorização, execução assíncrona) sobre a qual produtos de IA se transformam em receita recorrente, sem que cada novo produto precise reconstruir essa infraestrutura do zero. Ver a tese completa em [../00-tecle/vision.md](../00-tecle/vision.md).

## Objetivos da plataforma

- suportar múltiplos produtos SaaS independentes;
- centralizar autenticação e controle de acesso;
- padronizar desenvolvimento e operação;
- reduzir custo e dependência de fornecedores externos de IA;
- utilizar IA local (Ollama) e arquitetura híbrida sempre que possível;
- garantir reprodutibilidade do ambiente.

## Estado atual (baseline v1.0.0)

Segundo `changelog.md` e confirmado por leitura direta do código do backend (`platform/saas-backend/`):

- autenticação JWT (bcrypt + `python-jose`);
- modelo de Produtos e Assinaturas;
- Autorização central (verificação de assinatura ativa antes de qualquer execução);
- Product Gateway (padrão de autorização + despacho aplicado a todas as rotas de produto);
- execução assíncrona real via RabbitMQ + worker dedicado por produto;
- Speech-AI integrado de ponta a ponta (síncrono e assíncrono); Edital-AI e Code-AI também conectados ao mesmo gateway.

Este é o estado real e validado — não uma proposta de arquitetura no papel. Um usuário autenticado hoje consegue assinar um produto, enviar um arquivo, disparar a execução (síncrona ou assíncrona) e consultar o resultado, para os três produtos implementados.

> **Nota de consistência**: `.claude/current-phase.md` descreve um estágio muito anterior ("SaaS Backend Initialization", construindo o endpoint `/health`) e está desatualizado — não deve ser tratado como fonte de verdade sobre o estágio atual. `changelog.md` e o histórico em `tasks/saas/` são as fontes corretas. Ver [../05-development/claude-code.md](../05-development/claude-code.md).

## Camadas

```text
Cliente
  ↓
SaaS Backend (FastAPI) — autenticação, produtos, assinaturas, gateway
  ↓
Produtos (speech-ai, edital-ai, code-ai — cada um isolado em seu próprio .venv)
  ↓
Infraestrutura (/data/platform — PostgreSQL, Redis, RabbitMQ, MinIO, Qdrant, Ollama)
```

## Duas camadas de execução hoje

1. **Laboratório local** (VM Ubuntu) — ambiente de desenvolvimento e execução, VSCode + Claude Code, backend SaaS em FastAPI, infraestrutura Docker persistente.
2. **Evolução futura para VPS** — publicação e operação da camada SaaS em produção, espelhando o ambiente local de forma controlada. Ainda não implementada.

---

## Ver também

- [architecture.md](architecture.md) — detalhamento técnico de cada camada
- [principles.md](principles.md) — princípios de engenharia que regem a plataforma
- [roadmap.md](roadmap.md) — histórico de construção e próximos passos
- [technologies.md](technologies.md) — stack técnico completo
