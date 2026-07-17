# Acceptance Criteria — Task 007

## Functional

- POST /auth/login funciona
- login com credenciais válidas retorna sucesso
- login com credenciais inválidas retorna erro

---

## Technical

- usa verify_password do app/security.py
- não expõe senha
- não retorna dados sensíveis

---

## Validation

### Teste 1 — sucesso

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste2@tecle.com","password":"123456"}'
``
