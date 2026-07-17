# Acceptance — Task 013

## Functional

- `GET /products/{slug}/access` valida autorização por produto
- usa JWT do usuário autenticado
- usa subscriptions ativas

---

## Validation

### 1. Login

```bash
POST /auth/login
