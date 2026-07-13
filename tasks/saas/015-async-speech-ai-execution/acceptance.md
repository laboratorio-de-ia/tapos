# Acceptance Criteria — Task 015 — Execução Assíncrona com Fila

## Objetivo de Aceite

A Task 015 será considerada concluída quando a TAPOS conseguir submeter uma execução do Speech-AI de forma assíncrona, retornar um `job_id`, processar a solicitação por worker e permitir consulta de status até `completed` ou `failed`.

---

## Critérios Obrigatórios

### AC-001 — Baseline 014B preservada

Antes da implementação:

```bash
POST /auth/login
GET /products
POST /subscriptions
GET /products/speech-ai/access
POST /products/speech-ai/run
```

devem funcionar.

Após a implementação, os mesmos pontos devem continuar funcionando.

---

### AC-002 — Modelo Job criado

Deve existir entidade Job persistida no banco.

Campos mínimos:

```text
id
job_id
user_id
product_slug
status
created_at
started_at
finished_at
result_json
error_message
```

---

### AC-003 — Status suportados

O sistema deve suportar os status:

```text
queued
running
completed
failed
```

---

### AC-004 — Submit assíncrono

Endpoint esperado:

```text
POST /products/speech-ai/submit
```

Deve:

1. Exigir JWT.
2. Exigir subscription ativa para `speech-ai`.
3. Criar job.
4. Publicar mensagem no RabbitMQ.
5. Retornar imediatamente `job_id` e `status=queued`.

---

### AC-005 — Consulta de Job

Endpoint esperado:

```text
GET /jobs/{job_id}
```

Deve:

1. Exigir JWT.
2. Retornar apenas jobs do usuário autenticado.
3. Retornar status atual.
4. Retornar resultado quando status for `completed`.
5. Retornar erro quando status for `failed`.

---

### AC-006 — Worker consome fila

O worker deve:

1. Consumir mensagem do RabbitMQ.
2. Atualizar status para `running`.
3. Executar o Speech-AI.
4. Atualizar status para `completed` em caso de sucesso.
5. Atualizar status para `failed` em caso de erro.

---

### AC-007 — Execução gera outputs

Ao final de um job concluído, devem existir saídas do Speech-AI em:

```text
products/speech-ai/output/
```

Saídas esperadas, quando geradas pelo pipeline:

```text
narration.txt
speech.txt
audio.mp3
speech.xml
speech_report.json
```

---

### AC-008 — Painel `/ui` não quebrado

O painel de teste criado após a Task 014B deve continuar acessível:

```text
GET /ui
```

O fluxo antigo deve continuar funcional.

---

### AC-009 — Teste sem token

Chamadas protegidas devem continuar retornando erro de credencial quando não houver JWT.

### AC-010 — Teste sem subscription

Usuário autenticado, mas sem subscription ativa, não deve conseguir submeter execução assíncrona do Speech-AI.

### AC-011 — RabbitMQ operacional

Deve ser possível publicar e consumir uma mensagem de teste antes de conectar o worker ao Speech-AI.

---

## Teste Manual Mínimo

### 1. Login

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@tapos.local","password":"admin123"}' | jq -r .access_token)
```

### 2. Criar subscription

```bash
curl -s -X POST http://localhost:8000/subscriptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_slug":"speech-ai"}' | jq
```

### 3. Submeter job

```bash
curl -s -X POST http://localhost:8000/products/speech-ai/submit \
  -H "Authorization: Bearer $TOKEN" | jq
```

### 4. Consultar job

```bash
curl -s http://localhost:8000/jobs/<job_id> \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## Critério Final de Conclusão

A task será considerada concluída quando o fluxo abaixo funcionar:

```text
Login
  ↓
JWT
  ↓
Subscription ativa
  ↓
POST /products/speech-ai/submit
  ↓
Job queued
  ↓
RabbitMQ
  ↓
Worker
  ↓
Speech-AI
  ↓
Job completed
  ↓
GET /jobs/{job_id}
  ↓
Resultado disponível
```

E quando o fluxo síncrono antigo da Task 014B continuar funcionando.

