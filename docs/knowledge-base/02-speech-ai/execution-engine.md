# Speech-AI — Motor de Execução

O Speech-AI roda nos dois modelos de execução suportados pela TAPOS: síncrono (resposta imediata) e assíncrono (fila + worker dedicado). Os dois caminhos convergem exatamente no mesmo pipeline interno (`integration/cli.py` → `facade.py` → `runner.py`) — a única diferença é se a requisição HTTP espera a resposta inline ou se um worker processa o pedido em segundo plano.

## Caminho síncrono

```
POST /products/speech-ai/run (ou /upload)
  ↓
platform/saas-backend/app/products/speech_ai_adapter.py::run_speech_ai_product()
  ↓
subprocess: <speech-ai>/.venv/bin/python integration/cli.py
  ↓
integration/cli.py — adiciona PROJECT_ROOT ao sys.path
  ↓
integration/facade.py::run_speech_ai()
  ↓
integration/runner.py::execute_current_pipeline() — pipeline completo, síncrono
  ↓
SpeechRunResult (dataclass em integration/schemas.py: status, input_file,
  narration_file, speech_file, audio_file, provider, voice, language,
  estimated_minutes) → JSON em stdout → parseado pelo adapter FastAPI
```

## Caminho assíncrono

```
POST /products/speech-ai/submit
  ↓
_submit_job() cria um registro Job (status="queued")
  ↓
publish_job(job_id, "speech-ai")  (app/jobs/publisher.py)
  ↓
RabbitMQ — fila durável "speech_ai_jobs"
  ↓
Worker dedicado: platform/tap-runtime/workers/speech-ai-worker/worker.py
  (basic_qos(prefetch_count=1))
  ↓
Para cada mensagem: marca job "running" no Postgres →
  chama a MESMA run_speech_ai_product() do caminho síncrono →
  marca job "completed"/"failed" com result_json/error_message
```

PID e log do worker em `.runtime/pids/speech-ai-worker.pid` e `.runtime/logs/speech-ai-worker.log`.

## Nota sobre documentação desatualizada

O `README.md` do produto descreve, em uma seção "Próxima Evolução — Task 015", a execução assíncrona via RabbitMQ/worker como trabalho **futuro**. Na realidade, essa capacidade **já está implementada** no código atual (worker, publisher, rotas `/submit`) — o README está desatualizado em relação ao estado real da plataforma. Trate o código (`platform/tap-runtime/workers/speech-ai-worker/`, `platform/saas-backend/app/jobs/publisher.py`) como fonte de verdade, não o README.

## Ver também

- [../04-platform/gateway.md](../04-platform/gateway.md) — o gateway central que autoriza estas chamadas
- [../04-platform/runtime.md](../04-platform/runtime.md) — arquitetura de fila e workers no nível da plataforma
- [architecture.md](architecture.md)
