# Task 007 — User Login

## Context

A TAPOS backend SaaS já possui:

- modelo User
- endpoint /auth/register
- senha armazenada com hash (bcrypt)
- módulo app/security.py com verify_password

---

## Objective

Implementar endpoint de login de usuário.

---

## Requirements

- criar endpoint POST /auth/login
- receber JSON:
  - email
  - password

- buscar usuário pelo email
- validar senha usando verify_password
- retornar resposta simples:

{
  "message": "login successful"
}

---

## Constraints

- não criar JWT ainda
- não criar sessão
- não alterar register
- manter código simples

---

## Error Handling

- usuário não encontrado → 401 Unauthorized
- senha inválida → 401 Unauthorized

---

## Notes

Este endpoint será base para:
- autenticação via JWT (Task futura)
- proteção de rotas
