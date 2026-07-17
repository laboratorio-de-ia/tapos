# Task 005 — Password Hash

## Context

Estamos na TAPOS construindo backend SaaS com FastAPI.

Já temos:
- modelo User
- endpoint register funcionando
- tabela users criada

## Objective

Adicionar suporte a hash de senha.

---

## Requirements

- criar arquivo app/security.py
- usar passlib com bcrypt
- implementar:

  - hash_password(password: str) -> str
  - verify_password(plain_password: str, hashed_password: str) -> bool

---

## Constraints

- não alterar endpoints ainda
- não criar login
- não criar JWT
- manter simplicidade

---

## Notes

Este módulo será usado futuramente por:
- register (criação de usuário)
- login (verificação de senha)