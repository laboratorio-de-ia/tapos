# Task 013 — Product Authorization

## Context

A TAPOS já possui:

- autenticação com JWT
- rota protegida `/users/me`
- produtos cadastrados
- subscriptions por usuário

Agora precisamos validar autorização por produto.

---

## Objective

Criar mecanismo de autorização que verifica se o usuário autenticado possui subscription ativa para um produto.

---

## Requirements

- criar dependência/função de autorização por produto
- validar:
  - usuário autenticado
  - existência do produto
  - existência de subscription ativa para o produto

- criar endpoint:

GET /products/{product_slug}/access

---

## Response Format

### Quando autorizado
