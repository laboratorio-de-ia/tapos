# Acceptance Criteria — Task 005

## Functional

- função hash_password gera hash bcrypt válido
- função verify_password valida corretamente senha

---

## Technical

- usar passlib + bcrypt
- código isolado (sem dependências externas do projeto)
- fácil de testar

---

## Validation

Teste manual Python:

```python
from app.security import hash_password, verify_password

hashed = hash_password("123456")

assert verify_password("123456", hashed) == True
assert verify_password("wrong", hashed) == False
