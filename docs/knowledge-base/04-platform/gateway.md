# Plataforma — Gateway de Produtos

## Não é um módulo separado — é um padrão repetido

Não existe uma classe ou serviço único chamado "Gateway" no código. O gateway de produtos é um **padrão aplicado consistentemente** em `platform/saas-backend/app/routes/products.py`: toda rota de produto chama `_require_active_subscription(db, current_user, product_slug)` antes de despachar qualquer execução.

```python
def _require_active_subscription(db, current_user, product_slug) -> Product:
    product = db.query(Product).filter(Product.slug == product_slug).first()
    if not product:
        raise HTTPException(404, "Product not found")

    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.product_id == product.id,
        Subscription.is_active == True,
    ).first()

    if not subscription:
        raise HTTPException(403, "Access denied")

    return product
```

> **Nota de precisão**: existe uma segunda implementação praticamente idêntica dessa mesma regra em `app/deps.py::get_product_access` (como uma `Depends` reutilizável), que não é usada pelas rotas atuais de `products.py` — as rotas reimplementam a checagem inline via `_require_active_subscription` em vez de reaproveitar `get_product_access`. É uma duplicação de lógica a resolver: consolidar em uma única implementação reduziria o risco de as duas regras divergirem no futuro.

## Fluxo de autorização + despacho

```text
Requisição → JWT válido? (get_current_user) → assinatura ativa? (_require_active_subscription)
   ↓ sim para ambos
Adapter do produto (subprocess no .venv do produto) → resultado JSON
   ↓ não
403 Access denied / 401 Unauthorized
```

Nenhum produto é exposto diretamente ao usuário final — todo acesso passa por essa checagem dupla (identidade + assinatura) antes de qualquer execução, síncrona ou assíncrona.

## Modo síncrono

A rota chama o adapter do produto diretamente (`run_speech_ai_product()`, `run_code_ai_product()`, `run_edital_ai_product()`), que executa `integration/cli.py` do produto como subprocesso no `.venv` isolado dele, e devolve o JSON de resultado na própria resposta HTTP.

## Modo assíncrono

A rota `/submit` cria um registro `Job` (`status="queued"`) e chama `publish_job(job_id, product_slug)` (`app/jobs/publisher.py`), que publica em uma fila RabbitMQ dedicada por produto via `pika`:

```python
QUEUE_NAMES = {
    "speech-ai": "speech_ai_jobs",
    "code-ai": "code_ai_jobs",
    "edital-ai": "edital_ai_jobs",
}
```

Cada fila é `durable=True` e a mensagem é publicada com `delivery_mode=2` (persistente). O worker dedicado do produto (`platform/tap-runtime/workers/{produto}-worker/worker.py`) consome a fila, executa o mesmo adapter/pipeline, e atualiza o `Job` (`status`: `queued` → `running` → `completed`/`failed`, com `result_json` ou `error_message`). O cliente consulta o resultado em `GET /jobs/{job_id}` (`jobs/routes.py`).

## Isolamento por produto

Cada adapter (`app/products/{speech_ai,code_ai,edital_ai}_adapter.py`) invoca o `cli.py` do respectivo produto como subprocesso, usando o **`.venv` do próprio produto** — nunca o do backend. Se o produto quebrar, o processo do backend continua rodando; o gateway apenas recebe um `returncode` diferente de zero e levanta `RuntimeError` com stdout/stderr capturados.

---

## Ver também

- [api.md](api.md) — todas as rotas que passam por este gateway
- [security.md](security.md) — a camada de autenticação que antecede a verificação de assinatura
- [../01-tapos/principles.md](../01-tapos/principles.md) — o princípio de desacoplamento que este mecanismo implementa
- [../05-development/coding-standards.md](../05-development/coding-standards.md) — o padrão facade/runner/schemas/cli usado por todo adapter
