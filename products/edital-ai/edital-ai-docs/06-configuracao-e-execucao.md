# 06 — Configuração e execução

## Rodando o produto isoladamente (sem o backend)

```bash
cd products/edital-ai
source .venv/bin/activate     # ou use .venv/bin/python diretamente
python main.py input/<arquivo.pdf>
```

`main.py` imprime um resumo legível no terminal (número, órgão, score,
se usou IA, paths dos 4 artefatos). Para consumir como JSON (o mesmo que o
adapter do backend consome):

```bash
python integration/cli.py input/<arquivo.pdf>
```

`cli.py` redireciona qualquer `print()` de progresso interno para um buffer
e garante que **o único conteúdo no stdout real seja o JSON final** — isso é
o que permite ao adapter (`subprocess.run(..., capture_output=True)`) fazer
`json.loads(stdout)` com segurança. Erros vão para stderr com traceback
completo e `sys.exit(1)`.

## `config/settings.json`

```json
{
    "input": {
        "diretorio": "input",
        "formatos_suportados": ["pdf", "docx", "txt", "md"]
    },
    "output": {
        "diretorio": "output",
        "formatos": ["excel", "pdf", "word", "email"]
    },
    "ollama": {
        "base_url": "http://localhost:11434",
        "model": "mistral",
        "timeout": 300
    },
    "processamento": {
        "max_tamanho_mb": 50,
        "timeout_segundos": 300
    },
    "projeto": {
        "nome": "Edital AI",
        "versao": "1.0.0"
    }
}
```

`config/config_manager.py::ConfigManager` carrega este arquivo uma vez no
início (`project_root / "config" / "settings.json"`) e expõe propriedades
tipadas (`input_directory`, `output_directory`, `ollama_base_url`,
`ollama_model`, `ollama_timeout`, `max_tamanho_mb`). `ollama_base_url` e
`ollama_model` podem ser sobrescritos por variáveis de ambiente
(`OLLAMA_BASE_URL`, `OLLAMA_MODEL`) — o resto do `settings.json` **não** tem
override por env var hoje.

Observação: `max_tamanho_mb` e `timeout_segundos` de `processamento` estão
definidos no `settings.json` mas **não são de fato aplicados em nenhum lugar
do código** (não há checagem de tamanho de arquivo antes de processar, nem
uso desse timeout específico) — são campos de configuração "mortos" hoje.

## Dependências (`requirements.txt` do produto)

```text
# Extração de documentos
pdfplumber
pdf2image
pytesseract
python-docx
python-pptx
Pillow

# Processamento
pandas
tabulate

# Geração de artefatos
openpyxl
reportlab
jinja2

# IA e integração
requests

# Utilitários
python-dotenv
```

Dependências de sistema operacional (não Python, necessárias para OCR/PDF):
**Tesseract OCR** (usado por `pytesseract`) e **Poppler** (usado por
`pdf2image` para rasterizar páginas de PDF). Sem elas, o fallback de OCR para
PDFs escaneados falha silenciosamente (a exceção é capturada e relançada como
`RuntimeError` com a mensagem de falha de extração).

`jinja2` e `python-pptx` estão no requirements mas **não são usados por
nenhum módulo atual** (vestígios de uma versão anterior do escopo).

## Variáveis de ambiente relevantes

| Variável | Onde é lida | Efeito |
|---|---|---|
| `OLLAMA_BASE_URL` | `config_manager.py` | Sobrescreve a URL do Ollama (default `http://localhost:11434`) |
| `OLLAMA_MODEL` | `config_manager.py` | Sobrescreve o modelo usado (default `mistral`) |
| `DATABASE_URL` | `saas-backend/app/db.py` e o worker | String de conexão Postgres |
| `RABBITMQ_URL` | worker e `saas-backend/app/jobs/publisher.py` | String de conexão RabbitMQ |
| `SAAS_BACKEND_ROOT` | worker (`worker.py`) | Path para importar `app.products.edital_ai_adapter` de dentro do worker |

## Subindo o backend (com `--reload`, recomendado)

```bash
cd platform/saas-backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

`--reload` faz o uvicorn recarregar o processo automaticamente a cada
alteração de arquivo Python dentro de `platform/saas-backend/` — **sem essa
flag, correções em `routes/products.py` ou `edital_ai_adapter.py` exigem
reiniciar o processo manualmente**, ou o servidor continua servindo o código
antigo indefinidamente (isso já causou um bug em produção — ver
`07-limitacoes-e-debito-tecnico.md`).

## Subindo o worker assíncrono

```bash
cd platform/tap-runtime/workers/edital-ai-worker
source /workspace/tecle/platform/saas-backend/.venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://admin:admin@localhost:5432/platform
export RABBITMQ_URL=amqp://admin:admin@localhost:5672/
python worker.py
```

O worker usa o `.venv` do **backend** (não o do produto edital-ai) porque só
precisa de `pika`/`psycopg2` para falar com RabbitMQ/Postgres — ele delega
todo o trabalho pesado (extração/IA/geração) ao subprocesso do produto via o
mesmo adapter usado pelas rotas HTTP.

## Ollama (IA local)

O modelo usado é `mistral`, rodando via Ollama localmente
(`http://localhost:11434`). Não há dependência de nenhum provedor de nuvem
de IA — é 100% local. Trade-off conhecido: em CPU (sem GPU, ambiente atual),
uma análise leva 1-2 minutos, e o timeout configurado
(`ollama.timeout = 300s`) já foi visto estourando em documentos maiores (ver
próximo arquivo).
