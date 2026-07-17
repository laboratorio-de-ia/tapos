# Task 010 — User Profile Enrichment (/users/me)

## Context

A TAPOS já possui:

- autenticação com JWT
- rota protegida /users/me
- modelo User básico

Atualmente a rota retorna apenas o email.

---

## Objective

Evoluir o endpoint /users/me para retornar um perfil completo do usuário.

---

## Requirements

- atualizar endpoint GET /users/me
- retornar:

{
  "id": number,
  "email": string,
  "created_at": datetime,
  "is_active": boolean
}

- usar campos do modelo User

---

## Constraints

- não alterar autenticação
- não alterar login
- não alterar register
- manter simplicidade

---

## Technical Notes

- usar o current_user já existente
- não criar nova lógica de negócio

---

## Acceptance Criteria

- endpoint retorna estrutura completa
- dados corretos do banco
- continua protegido com JWT

---

## Notes

Esse endpoint será base para:

- frontend
- controle de acesso
- logging de usuário
