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

