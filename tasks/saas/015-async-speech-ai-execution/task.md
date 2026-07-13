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

