# .claude — Context System (TAPOS)

## Purpose

A pasta `.claude` define o contexto permanente utilizado pelo Claude Code dentro da plataforma TAPOS.

Este contexto garante que o desenvolvimento siga padrões consistentes de arquitetura, engenharia e evolução incremental.

---

## Files Overview

Esta pasta contém apenas quatro arquivos iniciais:

- workspace.md → Define a arquitetura e estrutura da plataforma
- constitution.md → Define regras e princípios de engenharia
- current-phase.md → Define foco e etapa atual do projeto
- README.md → Explica o funcionamento deste contexto

---

## How Claude Uses This Folder

Ao iniciar o Claude Code a partir da raiz do workspace:

```
/workspace/tecle
```

O Claude passa a utilizar automaticamente:

- arquitetura (workspace.md)
- regras (constitution.md)
- foco atual (current-phase.md)

Isso transforma o Claude em um assistente orientado por contexto, não apenas um gerador de código.

---

## Development Model

O desenvolvimento deve seguir o seguinte fluxo disciplinado:

```
Definir tarefa
↓
Gerar um único módulo
↓
Revisar código
↓
Testar
↓
Commit
↓
Próxima tarefa
```

---

## Important Rules

- Sempre iniciar o Claude na raiz `/workspace/tecle`
- Nunca trabalhar em subpastas isoladas
- Nunca gerar múltiplos módulos ao mesmo tempo
- Nunca pular validação
- Sempre commitar após cada etapa

---

## Expansion Strategy

Novos elementos serão adicionados de forma controlada:

Fases futuras:

- agents/ → agentes especializados
- skills/ → capacidades reutilizáveis
- memory/ → contexto persistente
- rules/ → regras adicionais

Estes diretórios só devem ser criados após estabilidade do backend SaaS.

---

## Goal

Criar um ambiente onde o Claude Code opere como um engenheiro consistente, respeitando arquitetura, contexto e regras da plataforma TAPOS.
