# Plataforma — Segurança

## Autenticação

`app/security.py` centraliza as duas primitivas de segurança da plataforma:

- **Hash de senha**: `passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")`.
- **JWT**: `python-jose`, algoritmo `HS256`, com claim `sub` (email do usuário) e `exp` (expiração).

```python
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
```

> **Risco real a corrigir antes de produção**: o segredo do JWT tem um valor padrão literal, `"dev-secret-key"`, aplicado sempre que a variável de ambiente `JWT_SECRET_KEY` não está definida. Isso é adequado para desenvolvimento local, mas é um risco de segurança concreto se a aplicação subir em produção sem essa variável explicitamente configurada.

## Verificação de identidade

`app/deps.py::get_current_user` decodifica o token Bearer, extrai o `sub` (email), carrega o `User` correspondente no banco, e levanta `401 Unauthorized` em qualquer falha de validação (token ausente, inválido, expirado, ou usuário inexistente).

## O que ainda não existe

Confirmado por leitura direta do código e cruzado com `architecture.md`:

- **refresh tokens** — sessão expira e exige novo login, sem renovação;
- **RBAC (papéis/perfis)** — não há diferenciação de papel de usuário, apenas identidade + assinatura por produto;
- **rate limiting** — nenhuma limitação de taxa de requisição implementada;
- **limite de tamanho/timeout de upload** — os endpoints de upload de `code-ai`/`edital-ai` aceitam arquivo sem validação de tamanho;
- **cofre de segredos** — segredos hoje vêm de variáveis de ambiente simples, sem integração com um vault dedicado;
- **multi-tenant** — não há isolamento de dados por cliente/organização, apenas por usuário individual.

## O que já está implementado e validado

- hash de senha com bcrypt;
- autenticação via JWT em rota protegida;
- autorização por assinatura ativa antes de qualquer execução de produto (ver [gateway.md](gateway.md));
- persistência de dados fora de containers, em `/data/platform/storage` (ver [storage.md](storage.md)).

---

## Ver também

- [gateway.md](gateway.md) — como a autenticação se combina com a verificação de assinatura
- [api.md](api.md) — rotas de autenticação (`/auth/register`, `/auth/login`)
- [../01-tapos/roadmap.md](../01-tapos/roadmap.md) — hardening de segurança como lacuna mapeada para produção
