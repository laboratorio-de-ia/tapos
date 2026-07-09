# TAPOS Constitution — Tecle AI Platform

## Purpose

Esta constituição define as regras fundamentais de engenharia, arquitetura e evolução da plataforma TAPOS.

Todas as decisões técnicas devem respeitar estes princípios.

---

## Core Principles

### 1. Modularidade
Cada componente deve ser independente.

- Backend SaaS
- Produtos
- Infraestrutura

Não devem depender diretamente entre si.

---

### 2. Desacoplamento

- Produtos NUNCA acessam banco diretamente
- Comunicação SEMPRE via API
- Infraestrutura não exposta ao domínio de negócio

---

### 3. Simplicidade

- Evitar complexidade desnecessária
- Implementar apenas o necessário
- Não antecipar problemas futuros sem evidência

---

### 4. Incrementalidade

Desenvolvimento sempre em pequenos passos:

- 1 módulo por vez
- testar antes de avançar
- commit constante

---

### 5. Testabilidade

Todo código deve:

- poder ser executado isoladamente
- ser validável
- não depender de contexto implícito

---

### 6. Reprodutibilidade

O ambiente deve ser reconstruído do zero:

- infraestrutura declarativa
- versionamento completo
- sem dependências ocultas

---

### 7. Persistência correta

- dados nunca dentro de containers
- sempre em /data/platform/storage

---

## Development Rules

- Sempre iniciar em /workspace/tecle
- Nunca abrir subpastas isoladas
- Nunca gerar múltiplos módulos ao mesmo tempo
- Sempre validar antes de avançar
- Sempre versionar após mudanças

---

## Architecture Rules

```
User
  ↓
SaaS Backend
  ↓
Products
  ↓
Infrastructure
```

---

## Forbidden Practices

- Acesso direto ao banco por produtos
- Lógica de negócio dentro da infraestrutura
- Hardcode de configurações críticas
- Implementar múltiplas features sem validação

---

## Engineering Standard

Cada tarefa deve seguir:

```
Definir
↓
Implementar (1 módulo)
↓
Testar
↓
Commit
↓
Próximo
```

---

## Objective

Construir uma plataforma:

- escalável
- modular
- previsível
- sustentável
