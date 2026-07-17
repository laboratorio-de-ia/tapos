# TAPOS — Arquitetura

## Backend SaaS

Um único serviço FastAPI (`platform/saas-backend/app/main.py`), estruturado em routers por recurso:

```text
app/
├── main.py              → cria a app, monta routers, expõe /health e /ui
├── db.py                → engine/sessão SQLAlchemy
├── models.py             → User, Product, Subscription, Job, EditalAnalise
├── security.py           → hash bcrypt + JWT
├── deps.py               → get_current_user, get_product_access
├── routes/
│   ├── auth.py           → /auth/register, /auth/login
│   ├── users.py          → /users/me
│   ├── products.py       → /products, gateway de produtos
│   └── subscriptions.py  → /subscriptions
├── jobs/
│   ├── publisher.py       → publish_job() via pika/RabbitMQ
│   ├── routes.py          → GET /jobs/{job_id}
│   └── schemas.py
└── products/
    ├── speech_ai_adapter.py
    ├── code_ai_adapter.py
    └── edital_ai_adapter.py
```

Ver [../04-platform/api.md](../04-platform/api.md) para a lista completa de endpoints e [../04-platform/gateway.md](../04-platform/gateway.md) para o mecanismo de autorização.

## Modelo de dados central

```text
User ──< Subscription >── Product
User ──< Job                        (execução assíncrona, qualquer produto)
User ──< EditalAnalise               (histórico específico do edital-ai)
```

`Product.slug` é o identificador estável de cada vertical (`speech-ai`, `edital-ai`, `code-ai`); `Subscription.is_active` habilita, sem nenhuma reengenharia, um modelo comercial de módulos vendidos separadamente.

## Isolamento de produto por subprocesso

Cada produto roda em seu próprio ambiente Python (`.venv` isolado), como subprocesso independente, comunicando-se com a plataforma por um contrato simples de entrada/saída em JSON (padrão `facade/runner/schemas/cli`, ver [../05-development/coding-standards.md](../05-development/coding-standards.md)). Isso significa que um produto pode evoluir, quebrar ou ser reescrito em outra tecnologia sem colocar em risco os demais nem o núcleo da plataforma.

## Execução: síncrona e assíncrona

```text
Síncrono:                                    Assíncrono:
Rota /run                                    Rota /submit
  ↓                                             ↓
adapter → subprocess do produto              cria Job(status=queued) → publish_job() (RabbitMQ)
  ↓                                             ↓
JSON de resultado na resposta HTTP           worker dedicado consome fila → executa mesmo adapter
                                                ↓
                                              atualiza Job (running → completed/failed)
                                                ↓
                                              cliente consulta GET /jobs/{job_id}
```

Detalhado em [../04-platform/gateway.md](../04-platform/gateway.md).

## Infraestrutura de runtime

```text
/data/platform
├── infra/       → docker-compose e serviços
├── runtime/     → execução de containers
└── storage/     → persistência (db, redis, rabbitmq, minio, qdrant, models, portainer)
```

Containers ativos hoje (verificado): `postgres:15`, `redis:7-alpine`, `rabbitmq:3-management`, `qdrant`, `minio`, `ollama`, `open-webui`, `portainer`. O backend e os workers rodam como processos diretos no host (não containerizados). Ver [../04-platform/runtime.md](../04-platform/runtime.md) e [../04-platform/storage.md](../04-platform/storage.md).

## Fluxo de autenticação

```text
Cliente → POST /auth/login → backend valida usuário/senha → JWT gerado
  → cliente usa Authorization: Bearer <token>
  → GET /users/me → backend valida token e retorna perfil
```

---

## Ver também

- [overview.md](overview.md) — visão geral e estado atual da plataforma
- [../04-platform](../04-platform/) — detalhamento operacional de cada camada (runtime, storage, segurança, API, gateway)
- [technologies.md](technologies.md) — stack completo
