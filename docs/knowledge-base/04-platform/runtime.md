# Plataforma — Runtime

## Ambiente local de desenvolvimento

O ambiente é iniciado por `start_tapos_env.sh` (raiz do workspace), que:

1. valida que a estrutura esperada existe (diretório do backend, `.venv`, `worker.py`, `app/main.py`);
2. sobe `postgres` e `rabbitmq` via `docker compose up -d` (`/data/platform/infra/`);
3. inicia o backend FastAPI (`uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`) em background, com PID em `.runtime/pids/saas-backend.pid` e log em `.runtime/logs/saas-backend.log`, aguardando `/health` responder;
4. inicia o worker do Speech-AI (`platform/tap-runtime/workers/speech-ai-worker/worker.py`) da mesma forma, exportando `DATABASE_URL`, `WORKER_DATABASE_URL`, `RABBITMQ_URL` e `SAAS_BACKEND_ROOT`;
5. imprime URLs úteis (backend, `/docs`, `/openapi.json`, `/ui/`) e um comando `curl` de login pronto para uso.

> **Nota**: apenas o worker do Speech-AI é iniciado automaticamente por este script hoje. Os workers de `edital-ai` e `code-ai` já existem em `platform/tap-runtime/workers/`, mas precisam ser iniciados manualmente — ainda não estão conectados ao bootstrap.

## Containers ativos (verificado via `docker ps`)

| Container | Imagem |
|---|---|
| `postgres` | `postgres:15` |
| `redis` | `redis:7-alpine` |
| `rabbitmq` | `rabbitmq:3-management` |
| `qdrant` | `qdrant/qdrant:latest` |
| `minio` | `minio/minio` |
| `ollama` | `ollama/ollama:latest` |
| `open-webui` | `ghcr.io/open-webui/open-webui:main` |
| `portainer` | `portainer/portainer-ce:latest` |

O backend FastAPI e os workers **não são containerizados** — rodam como processos `uvicorn`/`python` diretos no host, gerenciados pelo script de bootstrap.

## Isolamento por produto

Cada produto (`speech-ai`, `edital-ai`, `code-ai`) tem seu próprio `.venv` Python, completamente isolado do backend e dos demais produtos. A plataforma nunca importa código de produto diretamente — sempre invoca via subprocesso (ver [gateway.md](gateway.md)). Isso é real isolamento de processo, não apenas uma intenção de design.

## Workers

```text
platform/tap-runtime/workers/
├── speech-ai-worker/worker.py   → consome fila speech_ai_jobs
├── edital-ai-worker/worker.py   → consome fila edital_ai_jobs (prefetch_count=1)
└── code-ai-worker/worker.py     → consome fila code_ai_jobs
```

Cada worker é um processo Python standalone, dedicado a um único produto, consumindo sua própria fila RabbitMQ e atualizando o status do `Job` correspondente no PostgreSQL.

## Diretórios de plataforma ainda vazios

`tap-os/`, `tap-platform/`, `tap-devops/`, `tap-ci/`, `tap-docs/` existem como namespaces reservados dentro de `platform/`, sem conteúdo implementado até o momento.

---

## Ver também

- [storage.md](storage.md) — onde os dados desses containers persistem
- [gateway.md](gateway.md) — como o gateway invoca workers e produtos isolados
- [../05-development/workspace.md](../05-development/workspace.md) — estrutura completa do workspace de desenvolvimento
