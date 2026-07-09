# Task 012 — Subscriptions

## Context

A TAPOS já possui:

- usuários autenticados
- produtos cadastrados (/products)

Agora precisamos vincular usuários aos produtos.

---

## Objective

Criar sistema básico de subscriptions (assinaturas de produtos por usuário).

---

## Requirements

- criar tabela `subscriptions`
- campos:

  - id
  - user_id
  - product_id
  - is_active
  - created_at

- relacionamento:
  User → subscriptions
  Product → subscriptions

---

## Endpoints

### Criar subscription

POST /subscriptions

Body:

{
  "product_slug": "speech-ai"
}

---

### Listar subscriptions do usuário

GET /subscriptions

(retorna apenas do usuário autenticado)

---

## Constraints

- usar JWT (usuário autenticado)
- não criar billing
- não criar pagamento
- manter simples

---

## Acceptance Criteria

- tabela criada
- usuário consegue se inscrever em produto
- endpoint lista apenas seus produtos
- usa o current_user (JWT)

---

## Notes

Base para:
- controle de acesso por produto
- autorização
- monetização futura
