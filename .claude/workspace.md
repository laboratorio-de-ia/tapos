
# TAPOS — Tecle AI Platform Operating System

## Overview

A TAPOS (Tecle AI Platform Operating System) é uma plataforma de engenharia para construção e operação de produtos SaaS baseados em Inteligência Artificial.

Ela organiza o desenvolvimento, runtime e infraestrutura de maneira modular, desacoplada e escalável, permitindo evolução incremental e controle técnico completo.

---

## Platform Goals

- Suportar múltiplos produtos SaaS independentes
- Centralizar autenticação e controle de acesso
- Padronizar desenvolvimento e operação
- Reduzir custo e dependência de fornecedores externos
- Utilizar IA local (Ollama) e arquitetura híbrida
- Garantir reprodutibilidade do ambiente

---

## Workspace Root

Todos os projetos são desenvolvidos a partir de:
# TAPOS — Tecle AI Platform Operating System

## Overview

A TAPOS (Tecle AI Platform Operating System) é uma plataforma de engenharia para construção de produtos SaaS baseados em Inteligência Artificial.

Ela organiza infraestrutura, runtime e desenvolvimento de forma padronizada, modular e escalável.

---

## Platform Goals

- Suportar múltiplos produtos SaaS
- Centralizar autenticação e controle de acesso
- Permitir evolução incremental e desacoplada
- Operar com modelos de IA local (Ollama) e híbrido
- Minimizar dependência de fornecedores externos

---

## Workspace Root

Todos os projetos são organizados dentro de:

/workspace/tecle

Este diretório é o ponto único de entrada para desenvolvimento.

---

## Workspace Structure

/workspace/tecle
├── platform
├── products
├── shared
├── governance
├── developers
├── automation
├── playground
├── tests
└── .claude

---

## Component Responsibilities

### platform/

Base da plataforma e serviços centrais.

Contém:

- saas-backend
- tap-os
- serviços de runtime
- componentes comuns de backend

---

### products/

Produtos SaaS independentes:

- speech-ai
- edital-ai
- educa-ai

Regras:

- Produtos não acessam diretamente a infraestrutura
- Devem consumir APIs da camada SaaS

---

### shared/

Componentes reutilizáveis:

- SDKs
- bibliotecas comuns
- templates
- prompts
- agentes

---

### governance/

Definição de padrões e regras:

- arquitetura
- políticas
- roadmap
- ADR (Architecture Decision Records)

---

### developers/

Configuração do ambiente de desenvolvimento:

- VSCode
- Claude Code
- scripts auxiliares

---

### automation/

Automação e infraestrutura como código:

- Terraform
- Ansible
- scripts operacionais

---

## Runtime Architecture

Execução da plataforma:


/data/platform

Separação:


/data/platform
├── infra
├── runtime
└── storage

### Responsabilidades

- infra → docker-compose e serviços
- runtime → execução de containers
- storage → persistência de dados

---

## Platform Stack

- FastAPI → backend SaaS
- PostgreSQL → dados estruturados
- Redis → cache e sessões (futuro)
- RabbitMQ → mensageria
- MinIO → armazenamento de objetos
- Qdrant → banco vetorial
- Ollama → runtime de IA local

---

## Architecture Layers

User
↓
SaaS Backend (platform)
↓
Products (speech-ai, edital-ai, educa-ai)
↓
Infrastructure (/data/platform)



---

## Design Principles

- Modularidade: componentes independentes
- Desacoplamento: comunicação via APIs
- Incremental: um módulo por vez
- Testabilidade: tudo validável isoladamente
- Persistência: dados fora de containers
- Reprodutibilidade: ambiente recriável
- Simplicidade: evitar complexidade desnecessária

---

## Development Rules

- Sempre trabalhar a partir de `/workspace/tecle`
- Nunca abrir submódulos isoladamente no editor
- Criar um módulo por vez
- Testar antes de avançar
- Commitar após cada etapa
- Evitar geração de múltiplos componentes simultaneamente

---

## Restrictions

- Produtos não acessam banco diretamente
- Infraestrutura não deve ser acoplada ao código
- Evitar lógica distribuída sem necessidade
- Evitar automação prematura

---

## Current State

- Infraestrutura local operacional
- Docker e serviços funcionando
- Banco de dados ativo
- Workspace estruturado
- Contexto TAPOS inicial criado

---

## Current Focus

Construção do backend SaaS base.

---

## Next Step

Criar estrutura inicial do backend:

- FastAPI
- App base
- Endpoint healthcheck

---

## Development Model

Ciclo de trabalho:

Definir tarefa
↓
Implementar módulo único
↓
Testar
↓
Commitar
↓
Próxima tarefa


---

## Objective

Construir uma plataforma SaaS de IA:

- consistente
- escalável
- desacoplada
- evolutiva
