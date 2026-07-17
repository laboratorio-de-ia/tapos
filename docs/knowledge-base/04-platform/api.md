# Plataforma — API

O backend SaaS (`platform/saas-backend/app/`) é um único serviço FastAPI (`app/main.py`) que expõe todos os endpoints da plataforma. Não há um framework de gateway/API separado — a própria aplicação FastAPI, com autorização por rota, cumpre esse papel (ver [gateway.md](gateway.md)).

## Endpoints existentes

| Método | Rota | Arquivo | Propósito |
|---|---|---|---|
| `GET` | `/health` | `main.py` | healthcheck |
| `POST` | `/auth/register` | `routes/auth.py` | cria usuário, senha com hash bcrypt |
| `POST` | `/auth/login` | `routes/auth.py` | valida credenciais, retorna JWT |
| `GET` | `/users/me` | `routes/users.py` | perfil do usuário autenticado |
| `GET` | `/products` | `routes/products.py` | lista produtos ativos |
| `GET` | `/products/{slug}/access` | `routes/products.py` | verifica se o usuário tem assinatura ativa |
| `POST` | `/products/speech-ai/run` | `routes/products.py` | execução síncrona |
| `POST` | `/products/speech-ai/submit` | `routes/products.py` | execução assíncrona (enfileira job) |
| `POST` | `/products/speech-ai/upload` | `routes/products.py` | upload de roteiro + execução síncrona |
| `POST` | `/products/code-ai/{run,submit,upload}` | `routes/products.py` | mesmo padrão do speech-ai |
| `POST` | `/products/edital-ai/{run,submit,upload}` | `routes/products.py` | mesmo padrão, com validação extra de extensão e slot único de entrada |
| `GET` | `/products/edital-ai/historico` | `routes/products.py` | lista análises anteriores do usuário |
| `GET` | `/products/edital-ai/download/{analise_id}` | `routes/products.py` | download de artefato (`excel`, `pdf`, `word`, `email`) |
| `POST` | `/subscriptions` | `routes/subscriptions.py` | cria assinatura |
| `GET` | `/subscriptions` | `routes/subscriptions.py` | lista assinaturas do usuário |
| `GET` | `/jobs/{job_id}` | `jobs/routes.py` | status de um job assíncrono |

Documentação automática do FastAPI disponível em `/docs` (Swagger) e `/openapi.json`. Um painel de teste estático (HTML puro, 1107 linhas) está montado em `/ui`, servido por `StaticFiles` a partir de `app/static/index.html` — não é uma interface de produto, é uma ferramenta de teste manual.

## Padrão de rota

Todas as rotas de produto seguem o mesmo formato:

```python
@router.post("/{produto}/run")
def run_produto(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _require_active_subscription(db, current_user, "produto-slug")
    result = run_produto_product()
    return result
```

Autenticação via `Depends(get_current_user)` (JWT), autorização via `_require_active_subscription` (verifica produto + assinatura ativa antes de qualquer execução) — ver [gateway.md](gateway.md) e [security.md](security.md).

## Upload de arquivos

`code-ai` e `edital-ai` aceitam upload (`UploadFile`), validam a extensão contra uma lista permitida (`CODE_AI_ALLOWED_EXTENSIONS`, `EDITAL_AI_ALLOWED_EXTENSIONS`), e gravam o conteúdo em um diretório fixo de input do produto — sem limite de tamanho de arquivo aplicado no código atual.

---

## Ver também

- [gateway.md](gateway.md) — o mecanismo de autorização compartilhado por todas as rotas de produto
- [security.md](security.md) — autenticação JWT/bcrypt usada por `get_current_user`
- [../05-development/coding-standards.md](../05-development/coding-standards.md) — o padrão de código do backend FastAPI
