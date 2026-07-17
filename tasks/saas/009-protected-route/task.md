# Task 009 — Protected Route (/users/me)

## Context

O backend SaaS já possui:

- login com JWT
- geração de token válida
- modelo User

Agora precisamos proteger rotas usando o token.

---

## Objective

Criar uma rota protegida que retorna o usuário autenticado.

---

## Requirements

- criar arquivo app/deps.py
- implementar get_current_user
- validar JWT
- buscar usuário no banco

- criar endpoint:

GET /users/me

- retornar email do usuário autenticado

---

## Constraints

- usar JWT já existente
- não criar refresh token
- manter simplicidade

---

## Error Handling

- token inválido → 401
- token ausente → 401
- usuário não encontrado → 401

---

## Acceptance Criteria

- rota exige Authorization Bearer token
- token válido retorna usuário
- sem token retorna 401

---

## Notes

Base para todas as rotas protegidas da plataforma.
