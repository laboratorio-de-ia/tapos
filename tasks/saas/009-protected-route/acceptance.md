# Acceptance — Task 009

## Functional

- GET /users/me protegido por JWT
- retorna dados do usuário autenticado

---

## Validation

### 1. Login

Obter token:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste2@tecle.com","password":"123456"}'
``
