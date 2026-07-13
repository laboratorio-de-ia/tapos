# Plano de Implementação — Task 015

## Regra de execução

Executar uma etapa por vez.

Após cada etapa:

1. Testar.
2. Corrigir se necessário.
3. Commitar.
4. Só então avançar.

---

## Etapa 015.1 — Criar documentação

```bash
mkdir -p tasks/saas/015-async-speech-ai-execution
```

Criar:

```text
task.md
notes.md
acceptance.md
```

Commit:

```bash
git add tasks/saas/015-async-speech-ai-execution
git commit -m "docs: define task 015 async speech-ai execution"
```

---

## Etapa 015.2 — Criar modelo Job

Alterar:

```text
platform/saas-backend/app/models.py
```

Adicionar modelo `Job`.

Testar import do backend.

Commit:

```bash
git add platform/saas-backend/app/models.py
git commit -m "feat: add job model for async execution"
```

---

## Etapa 015.3 — Criar schemas

Criar:

```text
platform/saas-backend/app/jobs/schemas.py
```

Schemas mínimos:

```text
JobSubmitResponse
JobStatusResponse
```

Commit:

```bash
git add platform/saas-backend/app/jobs
git commit -m "feat: add job schemas"
```

---

## Etapa 015.4 — Criar routes de jobs

Criar:

```text
platform/saas-backend/app/jobs/routes.py
```

Endpoint:

```text
GET /jobs/{job_id}
```

Registrar em:

```text
app/main.py
```

Commit:

```bash
git add platform/saas-backend/app
git commit -m "feat: add job status endpoint"
```

---

## Etapa 015.5 — Criar Publisher RabbitMQ

Criar:

```text
platform/saas-backend/app/jobs/publisher.py
```

Responsabilidade:

```text
publish_job(job_id, product_slug)
```

Commit:

```bash
git add platform/saas-backend/app/jobs/publisher.py
git commit -m "feat: add rabbitmq publisher for jobs"
```

---

## Etapa 015.6 — Criar endpoint submit

Adicionar:

```text
POST /products/speech-ai/submit
```

Em:

```text
platform/saas-backend/app/routes/products.py
```

Responsabilidade:

```text
validar JWT
validar subscription
criar job
publicar fila
retornar job_id
```

Commit:

```bash
git add platform/saas-backend/app/routes/products.py
git commit -m "feat: add async submit endpoint for speech-ai"
```

---

## Etapa 015.7 — Worker mínimo

Criar:

```text
platform/tap-runtime/workers/speech-ai-worker/worker.py
```

Primeiro comportamento:

```text
consumir fila
marcar running
marcar completed sem executar speech-ai
```

Commit:

```bash
git add platform/tap-runtime/workers/speech-ai-worker
git commit -m "feat: add minimal speech-ai async worker"
```

---

## Etapa 015.8 — Worker executando Speech-AI

Atualizar worker para chamar o adapter/facade real.

Commit:

```bash
git add platform/tap-runtime/workers/speech-ai-worker
git commit -m "feat: execute speech-ai pipeline from async worker"
```

---

## Etapa 015.9 — Atualizar painel /ui

Adicionar opção:

```text
Executar assíncrono
Consultar job
```

Commit:

```bash
git add platform/saas-backend/app/static/index.html
git commit -m "feat: add async job controls to test panel"
```

---

## Etapa 015.10 — Teste E2E

Atualizar ou criar teste:

```text
test_auth.sh
```

Validar:

```text
health
login
subscription
submit
worker
job completed
run antigo continua funcionando
sem token retorna erro
```

Commit:

```bash
git add .
git commit -m "test: validate task 015 async speech-ai execution"
```

