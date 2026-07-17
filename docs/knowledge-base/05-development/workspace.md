# Workspace

## Raiz única

Todo o desenvolvimento da Tecle acontece a partir de um único ponto de entrada:

```
/workspace/tecle
```

Esta é uma regra de engenharia, não apenas uma convenção: o Claude Code e qualquer desenvolvedor devem sempre iniciar a partir desta raiz, nunca abrindo subpastas isoladas no editor. Isso garante que o contexto de arquitetura e regras (`.claude/`) seja sempre carregado.

## Estrutura real do workspace

```text
/workspace/tecle
├── .claude/            # contexto persistente do Claude Code (ver claude-code.md)
├── .vscode/             # configuração mínima do editor
├── .runtime/           # PIDs e logs de processos rodando localmente (backend, workers)
├── platform/            # backend SaaS e serviços de plataforma (TAPOS)
├── products/            # produtos SaaS independentes (speech-ai, edital-ai, code-ai, educa-ai)
├── shared/              # SDKs, bibliotecas, templates, prompts, agentes — reservado
├── governance/          # políticas, ADRs, arquitetura, padrões — reservado
├── developers/          # configuração de ambiente (VSCode, Claude, scripts) — reservado
├── automation/          # Terraform, Ansible, scripts operacionais
├── tasks/               # tarefas de desenvolvimento documentadas (kernel/, saas/)
├── tests/               # reservado (os testes reais vivem em platform/saas-backend/tests/)
├── playground/          # reservado, vazio
├── trash/               # descarte de artefatos de diagnóstico/depuração pontuais
├── investors/           # material para investidores
├── docs/                # esta knowledge base
├── architecture.md, changelog.md, readme.md  # documentos de estado no nível raiz
└── start_tapos_env.sh   # script de bootstrap do ambiente local
```

> **Nota de precisão**: `.claude/workspace.md` documenta uma estrutura ligeiramente mais enxuta (sem `tasks/`, `trash/`, `.vscode/`, `.runtime/`). Esta seção reflete a estrutura real encontrada em disco, que é um superconjunto da documentada.

### O que está implementado vs. reservado

| Pasta | Estado |
|---|---|
| `platform/saas-backend/` | **Implementado** — FastAPI, testes próprios, rodando |
| `platform/tap-runtime/workers/` | **Implementado** — workers de speech-ai, edital-ai, code-ai |
| `products/speech-ai`, `products/edital-ai`, `products/code-ai` | **Implementados** — código real, integrados à plataforma |
| `products/educa-ai` | **Reservado** — diretório vazio, sem código |
| `tasks/saas/` | **Implementado** — 12 tarefas documentadas (005 a 015) |
| `tasks/kernel/` | **Reservado** — vazio |
| `shared/*` (agents, common, libraries, plugins, prompts, sdk-python, sdk-typescript, templates) | **Reservado** — todas as subpastas vazias |
| `governance/*` (adrs, architecture, constitution, policies, roadmap, standards) | **Reservado** — todas as subpastas vazias |
| `developers/*` (claude, extensions, scripts, snippets, vscode) | **Reservado** — todas as subpastas vazias |
| `tests/`, `playground/` | **Reservado** — vazios na raiz (os testes reais estão em `platform/saas-backend/tests/`) |

Essa distinção importa: partes significativas da árvore de diretórios foram criadas antecipadamente, como scaffolding para fases futuras (multi-produto, SDKs compartilhados, governança formal), mas ainda não foram populadas. Ver [claude-code.md](claude-code.md) para a "Expansion Strategy" que documenta essa intenção.

## Runtime e persistência

A execução da plataforma (fora do workspace de desenvolvimento) acontece em `/data/platform`, separado em `infra/`, `runtime/` e `storage/` (banco, Redis, RabbitMQ, MinIO, Qdrant, modelos, Portainer). Por princípio de arquitetura, dados nunca vivem dentro de containers. `/data`, `/runtime` e `/storage` estão explicitamente excluídos do controle de versão via `.gitignore`.

## Bootstrap do ambiente local

O script `start_tapos_env.sh` (raiz do workspace) automatiza a inicialização do backend SaaS e do worker do Speech-AI:

1. Valida que a estrutura esperada existe (diretório do backend, venv, `worker.py`, `app/main.py`).
2. Sobe `postgres` e `rabbitmq` via `docker compose up -d` (passo condicional a existir um compose file na raiz).
3. Inicia o backend FastAPI (`uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`) em background, grava PID em `.runtime/pids/saas-backend.pid` e log em `.runtime/logs/saas-backend.log`, e faz polling em `/health` até responder.
4. Inicia o worker do speech-ai (`platform/tap-runtime/workers/speech-ai-worker/worker.py`) da mesma forma, exportando `DATABASE_URL`, `WORKER_DATABASE_URL`, `RABBITMQ_URL` e `SAAS_BACKEND_ROOT`.
5. Imprime as URLs úteis: backend (`http://localhost:8000`), Swagger (`/docs`), OpenAPI (`/openapi.json`), UI (`/ui/`) e um comando `curl` de login pronto para colar.

> **Nota**: apenas o worker do speech-ai é iniciado por este script hoje. Os workers de edital-ai e code-ai já existem em `platform/tap-runtime/workers/`, mas ainda não estão conectados ao bootstrap automático — precisam ser iniciados manualmente.

## Ver também

- [claude-code.md](claude-code.md) — como o Claude Code usa este workspace
- [development-flow.md](development-flow.md) — o ciclo de trabalho sobre esta estrutura
- [../01-tapos/architecture.md](../01-tapos/architecture.md) — arquitetura técnica da plataforma que roda sobre este workspace
