# speech-ai-worker

Worker que consome a fila `speech_ai_jobs` do RabbitMQ e atualiza a tabela `jobs`
criada pelo SaaS Backend (Task 015).

## Rodando localmente

```bash
source /workspace/tecle/platform/saas-backend/.venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL=postgresql://admin:admin@localhost:5432/platform
export RABBITMQ_URL=amqp://admin:admin@localhost:5672/

python worker.py
```

## Comportamento (Etapa 015.7)

Ao receber uma mensagem `{"job_id": ..., "product_slug": ...}`:

1. Marca o job como `running`.
2. Marca o job como `completed` (execução real do Speech-AI ainda não conectada).

A Etapa 015.8 substitui o passo 2 pela execução real via `speech_ai_adapter`.
