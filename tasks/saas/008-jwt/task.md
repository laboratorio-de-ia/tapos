# Task 008 — JWT Token Generation

## Context

O backend SaaS da TAPOS já possui:

- modelo User
- endpoint /auth/register
- senha com hash
- endpoint /auth/login funcionando com email e senha

Atualmente o login retorna apenas uma mensagem simples de sucesso.

---

## Objective

Atualizar o login para retornar um token JWT.

---

## Requirements

- criar geração de token JWT
- criar utilitário em `app/security.py` ou módulo equivalente
- atualizar `POST /auth/login`
- retorno do login deve ser:

{
  "access_token": "<jwt>",
  "token_type": "bearer"
}

---

## JWT Payload

O token deve conter:

- sub → email do usuário
- exp → data de expiração

---

## Constraints

- não proteger rotas ainda
- não criar middleware ainda
- não criar refresh token
- manter simplicidade

---

## Technical Notes

- usar algoritmo HS256
- usar chave secreta simples via variável de ambiente
- expiração inicial simples (ex.: 60 minutos)

---

## Acceptance Criteria

- login válido retorna JWT
