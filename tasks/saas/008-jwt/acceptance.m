# Acceptance Criteria — Task 008

## Functional

- POST /auth/login retorna token JWT para credenciais válidas
- credenciais inválidas continuam retornando 401

---

## Response Format

Resposta esperada:

```json
{
  "access_token": "jwt-aqui",
  "token_type": "bearer"
}
