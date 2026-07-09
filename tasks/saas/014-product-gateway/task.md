# Task 014 — Product Gateway (speech-ai integration)

## Context

A TAPOS já possui:

- autenticação com JWT
- autorização por produto (Task 013)
- products e subscriptions

Agora precisamos integrar um produto real.

---

## Objective

Criar um gateway SaaS que valida acesso e simula chamada para o product `speech-ai`.

---

## Requirements

- criar endpoint:

GET /products/{product_slug}/run

- fluxo:

1. validar JWT
2. validar autorização (subscription ativa)
3. retornar execução simulada do produto

---

## Response Format

```json
{
  "product": "speech-ai",
  "status": "executed",
  "message": "Product executed successfully"
}
