#!/usr/bin/env bash
set -euo pipefail

TASK_DIR="tasks/saas/015-async-speech-ai-execution"
mkdir -p "$TASK_DIR"

cat > "$TASK_DIR/task.md" <<'EOF'
# Task 015 — Execução Assíncrona com Fila para Speech-AI

## Status

Planejada

## Contexto

A plataforma TAPOS encontra-se na baseline operacional v1.0.0, com autenticação JWT, Products, Subscriptions, Authorization, Product Gateway e Speech-AI integrado.

A Task 014B concluiu a integração síncrona entre TAPOS e Speech-AI por meio do endpoint `POST /products/speech-ai/run`, validando JWT e subscription ativa antes de executar a facade real do produto.

Após a Task 014B, foi criado também um painel HTML simples em `/ui`, servido pelo próprio backend FastAPI, para testar cadastro, login, assinatura de produto, upload de `.txt` e execução manual do Speech-AI.

A próxima evolução registrada é a Task 015: execução assíncrona com fila, usando RabbitMQ já previsto na infraestrutura da TAPOS.

---

## Objetivo

Transformar a execução do Speech-AI de síncrona para assíncrona, evitando que a request HTTP fique bloqueada durante o processamento do áudio.

O novo fluxo desejado é:

```text
Cliente
  ↓
POST /products/speech-ai/submit
  ↓
Backend TAPOS
  ↓
Criação de Job
  ↓
RabbitMQ
  ↓
Worker Speech-AI
  ↓
Execução do Speech-AI
  ↓
Atualização do Job
  ↓
Consulta de status pelo cliente
```

---

## Escopo da Task 015

### Incluído

1. Criar documentação formal da Task 015.
2. Criar modelo de Job para rastrear execuções assíncronas.
3. Criar endpoints mínimos para submissão e consulta de status.
4. Criar camada de publicação de mensagens no RabbitMQ.
5. Criar worker consumidor para processar jobs do Speech-AI.
6. Manter compatibilidade com o fluxo síncrono existente da Task 014B.
7. Estender o teste ponta a ponta após cada etapa.

### Fora de escopo nesta task

1. Multi-tenant.
2. Billing/pagamentos.
3. RBAC completo.
4. Refresh token.
5. Transformar o Speech-AI em microserviço HTTP isolado.
6. Interface produtiva final.
7. Persistência avançada de arquivos em MinIO.

---

## Requisitos Funcionais

### RF-001 — Criar Job

Ao receber uma solicitação assíncrona, o backend deve criar um registro de job no banco de dados.

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

Status possíveis:

```text
queued
running
completed
failed
```

---

### RF-002 — Submeter execução assíncrona

Criar endpoint:

```text
POST /products/speech-ai/submit
```

Responsabilidades:

1. Validar JWT.
2. Validar subscription ativa para `speech-ai`.
3. Criar job com status `queued`.
4. Publicar mensagem no RabbitMQ.
5. Retornar imediatamente o `job_id`.

Resposta esperada:

```json
{
  "job_id": "uuid",
  "status": "queued",
  "product_slug": "speech-ai"
}
```

---

### RF-003 — Consultar status do job

Criar endpoint:

```text
GET /jobs/{job_id}
```

Responsabilidades:

1. Validar JWT.
2. Garantir que o job pertence ao usuário autenticado.
3. Retornar status e resultado quando disponível.

Resposta esperada:

```json
{
  "job_id": "uuid",
  "status": "completed",
  "product_slug": "speech-ai",
  "result": {}
}
```

---

### RF-004 — Worker Speech-AI

Criar worker responsável por:

1. Consumir mensagens da fila RabbitMQ.
2. Marcar job como `running`.
3. Executar o Speech-AI usando o adapter/facade já existente.
4. Atualizar job como `completed` com `result_json`.
5. Atualizar job como `failed` em caso de erro.

---

### RF-005 — Compatibilidade

O endpoint síncrono existente deve continuar funcionando:

```text
POST /products/speech-ai/run
```

A Task 015 não deve quebrar o painel `/ui` nem o fluxo validado na Task 014B.

---

## Requisitos Não Funcionais

1. Manter desacoplamento entre backend e produtos.
2. Produtos não devem acessar banco diretamente.
3. Não adicionar lógica de negócio na infraestrutura.
4. Um módulo por vez.
5. Testar cada etapa antes de avançar.
6. Commit após cada etapa validada.
7. Não implementar múltiplos módulos simultaneamente.

---

## Arquitetura Proposta

```text
FastAPI
  ↓
Jobs API
  ↓
Job Model / PostgreSQL
  ↓
RabbitMQ Publisher
  ↓
RabbitMQ Queue
  ↓
Speech-AI Worker
  ↓
speech_ai_adapter.py
  ↓
products/speech-ai/integration/cli.py
  ↓
Speech-AI Pipeline
  ↓
Job completed/failed
```

---

## Estrutura de Arquivos Proposta

```text
platform/saas-backend/app/jobs/
├── __init__.py
├── models.py
├── schemas.py
├── publisher.py
└── routes.py

platform/tap-runtime/workers/speech-ai-worker/
├── worker.py
└── README.md

tasks/saas/015-async-speech-ai-execution/
├── task.md
├── notes.md
└── acceptance.md
```

---

## Plano de Execução Incremental

### Etapa 015.1 — Documentação

Criar:

```text
tasks/saas/015-async-speech-ai-execution/task.md
tasks/saas/015-async-speech-ai-execution/notes.md
tasks/saas/015-async-speech-ai-execution/acceptance.md
```

### Etapa 015.2 — Modelo Job

Criar modelo SQLAlchemy para Job.

### Etapa 015.3 — Schemas

Criar schemas de request/response para Job.

### Etapa 015.4 — Endpoint de status

Criar `GET /jobs/{job_id}`.

### Etapa 015.5 — Publisher RabbitMQ

Criar publisher simples para enviar mensagem para fila.

### Etapa 015.6 — Endpoint submit

Criar `POST /products/speech-ai/submit`.

### Etapa 015.7 — Worker mínimo

Criar worker que consome mensagem e apenas atualiza status.

### Etapa 015.8 — Worker executando Speech-AI

Integrar worker com execução real do Speech-AI.

### Etapa 015.9 — Teste ponta a ponta

Validar fluxo completo.

### Etapa 015.10 — Atualizar painel `/ui`

Adicionar teste manual da execução assíncrona.

---

## Critérios de Aceite

Ver arquivo `acceptance.md`.

---

## Observações

Esta task deve iniciar pela documentação. Nenhum código deve ser implementado antes de validar o escopo desta Task 015.

EOF

cat > "$TASK_DIR/notes.md" <<'EOF'
# Notes — Task 015 — Execução Assíncrona com Fila

## Contexto Recuperado

A TAPOS está na versão 1.0.0 e possui a baseline operacional com:

- JWT Authentication
- Products
- Subscriptions
- Authorization
- Product Gateway
- Speech-AI integrado
- Task 014A concluída
- Task 014B concluída

Após a Task 014B, foi criado o painel `/ui` para teste manual do fluxo:

```text
Cadastro
Login
Assinatura
Upload TXT
Execução Speech-AI
Resultado
```

Esse painel deve continuar funcional após a Task 015.

---

## Decisão Arquitetural

A Task 015 deve preservar o conceito central da TAPOS:

```text
Produtos não acessam banco diretamente.
Comunicação ocorre via API, adapter ou fila.
Infraestrutura não contém regra de negócio.
```

Portanto, a fila RabbitMQ deve transportar mensagens de execução, mas a autorização continua no SaaS Backend.

---

## Decisão 001 — Manter endpoint síncrono

O endpoint já existente:

```text
POST /products/speech-ai/run
```

deve permanecer disponível para compatibilidade e testes da Task 014B.

A Task 015 adiciona execução assíncrona, mas não remove a execução síncrona.

---

## Decisão 002 — Novo endpoint submit

Criar novo endpoint:

```text
POST /products/speech-ai/submit
```

Motivo:

- Evita quebrar contrato existente.
- Deixa claro que a chamada é assíncrona.
- Retorna `job_id` imediatamente.

---

## Decisão 003 — Criar tabela Jobs

A execução assíncrona precisa de rastreabilidade.

A tabela `jobs` deve registrar:

- quem pediu
- qual produto
- quando pediu
- status atual
- resultado
- erro

---

## Decisão 004 — Worker isolado

O worker deve ficar fora do `saas-backend` principal.

Local sugerido:

```text
platform/tap-runtime/workers/speech-ai-worker/
```

Motivo:

- Separa API HTTP da execução longa.
- Prepara a plataforma para escalabilidade.
- Mantém a porta aberta para futuras filas e workers por produto.

---

## Decisão 005 — RabbitMQ como infraestrutura da Task 015

RabbitMQ já está previsto na infraestrutura TAPOS.

A Task 015 deve usar RabbitMQ como mecanismo inicial de fila.

---

## Decisão 006 — Escopo mínimo

Não implementar nesta task:

- retry avançado
- DLQ
- dashboard de jobs
- billing
- streaming de progresso
- cancelamento de jobs
- MinIO para outputs

Esses pontos podem virar tasks futuras.

---

## Riscos

### Risco 1 — Bloquear evolução com arquitetura grande demais

Mitigação:

Implementar apenas o mínimo:

```text
submit
queue
worker
status
```

### Risco 2 — Quebrar Task 014B

Mitigação:

Rodar teste da 014B antes e depois da Task 015.

### Risco 3 — Problema no RabbitMQ local

Mitigação:

Primeiro testar publisher e consumer com mensagem simples, antes de executar Speech-AI.

### Risco 4 — Paths hardcoded do Speech-AI

O painel pós-014B documentou que o caminho do script de entrada está hardcoded:

```text
/workspace/tecle/products/speech-ai/input/script.txt
```

Mitigação futura:

Mover para variável de ambiente em task posterior ou subtask da 015 se necessário.

---

## Futuro Possível

Após a Task 015:

1. Task 016 — Upload de Arquivos mais robusto.
2. Task 017 — Storage de resultados em MinIO.
3. Task 018 — IA Local/Ollama.
4. Task 019 — Microserviços por produto.

Esses itens aparecem como direção futura, não como escopo obrigatório da Task 015.

EOF

cat > "$TASK_DIR/acceptance.md" <<'EOF'
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

EOF

cat > "$TASK_DIR/implementation_plan.md" <<'EOF'
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

EOF

echo "Task 015 criada em: $TASK_DIR"
