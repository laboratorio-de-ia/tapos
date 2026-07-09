# Current Phase — TAPOS

## Current Stage

SaaS Backend Initialization

---

## Context

A infraestrutura da plataforma TAPOS já está operacional:

- Docker rodando
- PostgreSQL ativo
- Serviços base (Redis, RabbitMQ, MinIO, Qdrant, Ollama)
- Workspace estruturado em /workspace/tecle

O ambiente de desenvolvimento está configurado com:

- VSCode remoto (SSH)
- Claude Code
- Contexto inicial (.claude) criado

---

## Objective

Iniciar a construção do backend SaaS responsável por:

- autenticação
- gestão de usuários
- controle de acesso aos produtos
- ponto central de integração entre produtos e infraestrutura

---

## Current Task

Criar a estrutura inicial do backend SaaS com:

- FastAPI
- aplicação base
- endpoint /health

---

## Constraints

As seguintes regras devem ser respeitadas:

- Implementar um módulo por vez
- Não gerar múltiplos componentes simultaneamente
- Código simples e direto
- Evitar abstrações desnecessárias
- Sempre validar antes de avançar

---

## What Is NOT Allowed Now

- Criar auth completo
- Criar múltiplos endpoints ao mesmo tempo
- Implementar arquitetura complexa
- Adicionar dependências desnecessárias
- Integrar outros serviços neste momento

---

## Success Criteria

Esta fase estará concluída quando:

- FastAPI estiver rodando
- Endpoint /health funcionando
- Estrutura base criada

---

## Next Step

Após concluir esta etapa:

- adicionar conexão com PostgreSQL
- criar modelo User
- criar endpoint de registro

---

## Development Cycle

Sempre seguir:

Definir tarefa
↓
Implementar (1 módulo)
↓
Testar
↓
Commit
↓
Próxima tarefa

---

## Focus

Construir base sólida, simples e validada.
Não otimizar cedo.
Não escalar antes do necessário.
