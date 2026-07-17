# code-ai-worker

Worker que consome a fila `code_ai_jobs` do RabbitMQ e atualiza a tabela `jobs`
criada pelo SaaS Backend (Task 015), reaproveitada para o produto code-ai.

## Rodando localmente

```bash
source /workspace/tecle/platform/saas-backend/.venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL=postgresql://admin:admin@localhost:5432/platform
export RABBITMQ_URL=amqp://admin:admin@localhost:5672/

python worker.py
```

## Comportamento

Ao receber uma mensagem `{"job_id": ..., "product_slug": "code-ai"}`:

1. Marca o job como `running`.
2. Executa o code-ai via `app.products.code_ai_adapter.run_code_ai_product()`,
   que reprocessa o conteúdo atual de `products/code-ai/input/`.
3. Marca o job como `completed` com o `result_json` da conversão, ou `failed`
   com a mensagem de erro em caso de exceção.
