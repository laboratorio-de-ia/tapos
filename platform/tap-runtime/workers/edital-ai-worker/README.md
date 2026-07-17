# edital-ai-worker

Worker que consome a fila `edital_ai_jobs` do RabbitMQ, executa a análise do
edital atualmente em `products/edital-ai/input/` e persiste o resultado tanto
na tabela `jobs` (Task 015) quanto na tabela `edital_analises` (histórico do
produto).

## Rodando localmente

```bash
source /workspace/tecle/platform/saas-backend/.venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL=postgresql://admin:admin@localhost:5432/platform
export RABBITMQ_URL=amqp://admin:admin@localhost:5672/

python worker.py
```

## Comportamento

Ao receber uma mensagem `{"job_id": ..., "product_slug": "edital-ai"}`:

1. Marca o job como `running`.
2. Executa `app.products.edital_ai_adapter.run_edital_ai_product()` (sem
   argumento — reprocessa o edital atualmente salvo em `input/documento.<ext>`,
   ou seja, o último enviado via `POST /products/edital-ai/upload`).
3. Busca o `user_id` do job na tabela `jobs`.
4. Insere um registro em `edital_analises` (histórico consultável via
   `GET /products/edital-ai/historico`).
5. Marca o job como `completed` com o `result_json`, ou `failed` com a
   mensagem de erro em caso de exceção.

## Observação de performance

A análise via Ollama (modelo `mistral`, CPU, sem GPU neste ambiente) leva
cerca de **1 a 2 minutos por edital**. Isso é o principal motivo para usar o
fluxo assíncrono (`submit` + fila) em vez do síncrono (`run`/`upload`) em
produção.
