# Acceptance — Task 006

## Functional

- POST /auth/register continua funcionando
- usuário é criado normalmente

---

## Technical

- campo password no banco contém hash bcrypt
- não contém senha em texto puro

---

## Validation

1. Criar usuário
2. Verificar no banco:

```sql
SELECT email, password FROM users;
