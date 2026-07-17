# Task 011 — Products

## Context

A TAPOS já possui:

- autenticação com JWT
- rota protegida `/users/me`
- backend SaaS funcional

Agora precisamos iniciar a camada multi-produto.

---

## Objective

Criar a base de produtos da plataforma.

---

## Requirements

- criar modelo `Product`
- criar tabela `products`
- campos mínimos:
  - `id`
  - `name`
  - `slug`
  - `is_active`
  - `created_at`

- criar endpoint:
  - `GET /products`

- retornar apenas produtos ativos

- fazer seed inicial com:
  - `speech-ai`
  - `edital-ai`
  - `educa-ai`

---

## Constraints

- não criar subscriptions ainda
- não criar controle de acesso por produto ainda
- não alterar autenticação
- manter simplicidade

---

## Response Format

O endpoint `/products` deve retornar uma lista simples:

```json
[
  {
    "id": 1,
    "name": "Speech AI",
    "slug": "speech-ai",
    "is_active": true
  }
]
