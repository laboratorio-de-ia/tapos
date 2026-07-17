# TAPOS — Princípios de Engenharia

Estes princípios são a versão de plataforma da [Constituição de Engenharia](../05-development/constitution.md) (`.claude/constitution.md`), que é a fonte normativa vigente — `governance/constitution/` existe apenas como diretório reservado, ainda vazio.

## 1. Modularidade

Backend SaaS, produtos e infraestrutura são componentes independentes, sem dependência direta entre si.

## 2. Desacoplamento

- Produtos **nunca** acessam o banco de dados diretamente — toda comunicação é via API ou via o contrato facade/runner/schemas/cli.
- Infraestrutura não é exposta ao domínio de negócio.

Evidência concreta: os três produtos rodam como subprocessos em `.venv` isolados, comunicando-se com o backend apenas por JSON via stdout (ver [architecture.md](architecture.md)).

## 3. Simplicidade

Evitar complexidade desnecessária; implementar apenas o necessário; não antecipar problemas sem evidência. Observado na prática: rotas FastAPI simples, sem camada de serviço ou repositório intermediária (ver [../05-development/coding-standards.md](../05-development/coding-standards.md)).

## 4. Incrementalidade

Um módulo por vez, testado antes de avançar, commit constante — como princípio de planejamento. As 13 tarefas em `tasks/saas/` (005 a 015) mostram exatamente esse encadeamento incremental no nível de escopo. Na prática de versionamento em Git, porém, esse princípio **não foi seguido à risca**: todo o histórico até a v1.0.0 está em um único commit — ver [roadmap.md](roadmap.md) e [../05-development/development-flow.md](../05-development/development-flow.md) para o registro honesto dessa divergência.

## 5. Testabilidade

Código deve ser executável isoladamente e validável sem depender de contexto implícito. Testes automatizados existem para o backend (`platform/saas-backend/tests/`); os produtos são validados principalmente por critérios de aceite manuais (`tasks/saas/*/acceptance.md`) — ainda não há suíte de testes automatizados por produto.

## 6. Reprodutibilidade

Ambiente reconstruível do zero: infraestrutura declarativa (Docker Compose), versionamento completo, sem dependências ocultas. `start_tapos_env.sh` automatiza esse bootstrap.

## 7. Persistência correta

Dados nunca dentro de containers — sempre em `/data/platform/storage`, fora do controle de versão. Verificado diretamente no sistema de arquivos (ver [../04-platform/storage.md](../04-platform/storage.md)).

## Regra de arquitetura (camadas)

```text
User
  ↓
SaaS Backend
  ↓
Products
  ↓
Infrastructure
```

## Práticas proibidas

- acesso direto ao banco por produtos;
- lógica de negócio dentro da infraestrutura;
- hardcode de configurações críticas (nota: o segredo padrão de JWT em desenvolvimento, `"dev-secret-key"`, é um risco a corrigir antes de produção — ver [../04-platform/security.md](../04-platform/security.md));
- implementar múltiplas features sem validação.

---

## Ver também

- [../05-development/constitution.md](../05-development/constitution.md) — o texto normativo completo
- [architecture.md](architecture.md) — onde estes princípios se manifestam em código
- [roadmap.md](roadmap.md) — onde a prática já divergiu do princípio, e o que fazer a respeito
