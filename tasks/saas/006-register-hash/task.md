# Task 006 — Update Register with Password Hash

## Context

O endpoint /auth/register já existe e está funcionando.
Atualmente a senha está sendo salva em texto puro.

A Task 005 criou o módulo app/security.py com hash de senha.

---

## Objective

Atualizar o endpoint register para salvar senha com hash.

---

## Requirements

- alterar app/routes/auth.py
- usar hash_password do app/security.py
- substituir password=data.password por hash_password(data.password)

---

## Constraints

- não alterar contrato do endpoint
- não criar login
- não criar JWT
- manter simplicidade

---

## Acceptance Criteria

- senha não salva em texto puro
- banco contém hash
- endpoint continua funcionando normalmente

---

## Notes

Essa mudança é pré-requisito para login e autenticação futura.
