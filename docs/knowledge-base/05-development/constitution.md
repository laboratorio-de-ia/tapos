# Constituição de Engenharia

Esta constituição é a fonte real de regras fundamentais de engenharia da TAPOS. Vive em `.claude/constitution.md` e é carregada automaticamente pelo Claude Code sempre que uma sessão é iniciada a partir de `/workspace/tecle`.

> **Nota de precisão**: `governance/constitution/` existe como diretório reservado para uma futura constituição formal de governança, mas está **vazio** — não espelha nem substitui este documento. Enquanto isso não muda, `.claude/constitution.md` é a única constituição em vigor. O mesmo vale para `governance/architecture/`, também vazio; a arquitetura de estado atual real está documentada em `/workspace/tecle/architecture.md` e em [01-tapos/architecture.md](../01-tapos/architecture.md).

## Princípios fundamentais

### 1. Modularidade
Cada componente — backend SaaS, produtos, infraestrutura — deve ser independente e não depender diretamente dos outros.

### 2. Desacoplamento
- Produtos **nunca** acessam o banco de dados diretamente.
- Toda comunicação acontece **sempre** via API (ou, no caso dos produtos, via o contrato facade/runner/schemas/cli — ver [coding-standards.md](coding-standards.md)).
- Infraestrutura não é exposta ao domínio de negócio.

### 3. Simplicidade
Evitar complexidade desnecessária; implementar apenas o necessário; não antecipar problemas futuros sem evidência.

### 4. Incrementalidade
Desenvolvimento sempre em pequenos passos: um módulo por vez, testar antes de avançar, commit constante.

### 5. Testabilidade
Todo código deve poder ser executado isoladamente, ser validável, e não depender de contexto implícito.

### 6. Reprodutibilidade
O ambiente deve poder ser reconstruído do zero: infraestrutura declarativa, versionamento completo, sem dependências ocultas.

### 7. Persistência correta
Dados nunca dentro de containers — sempre em `/data/platform/storage`.

## Regras de arquitetura

```
User
  ↓
SaaS Backend
  ↓
Products
  ↓
Infrastructure
```

## Práticas proibidas

- Acesso direto ao banco por produtos.
- Lógica de negócio dentro da infraestrutura.
- Hardcode de configurações críticas.
- Implementar múltiplas features sem validação.

## Padrão de engenharia por tarefa

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

## Objetivo

Construir uma plataforma escalável, modular, previsível e sustentável.

## Honestidade sobre a aderência real

Esta constituição descreve o padrão pretendido. Vale registrar, com transparência, onde a prática observada até agora diverge dele — ver [development-flow.md](development-flow.md) para o caso mais notável: o princípio de "commit constante" foi seguido no *planejamento* de cada tarefa (ver `tasks/saas/`), mas a execução real, até a baseline v1.0.0, resultou em um único commit acumulado (`a48b7b5 TAPOS v1.0.0 - operational SaaS baseline`), não em commits incrementais por módulo. Isso não invalida o princípio — reforça a necessidade de aplicá-lo de forma mais disciplinada daqui em diante.

## Ver também

- [coding-standards.md](coding-standards.md) — como estes princípios se manifestam em código real
- [development-flow.md](development-flow.md) — o ciclo de trabalho na prática
- [../01-tapos/principles.md](../01-tapos/principles.md) — a mesma constituição, aplicada à arquitetura da plataforma
