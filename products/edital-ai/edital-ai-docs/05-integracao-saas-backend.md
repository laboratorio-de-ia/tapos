# 05 — Integração com o SaaS backend

Arquivos relevantes:
- `platform/saas-backend/app/routes/products.py` (endpoints HTTP)
- `platform/saas-backend/app/products/edital_ai_adapter.py` (ponte para o subprocesso)
- `platform/tap-runtime/workers/edital-ai-worker/worker.py` (worker assíncrono)
- `platform/saas-backend/app/static/index.html` (painel de teste HTML)

## Autenticação e autorização

Todo endpoint de `edital-ai` exige:
1. JWT válido (`Depends(get_current_user)`).
2. Assinatura ativa do produto (`_require_active_subscription(db, user,
   "edital-ai")`) — consulta a tabela `Subscription` filtrando por
   `product.slug == "edital-ai"` e `is_active == True`. Sem assinatura ativa
   → `403 Access denied`.

## Endpoints

| Método/Path | Papel |
|---|---|
| `POST /products/edital-ai/upload` | Sobe o arquivo, roda a análise **de forma síncrona** e já devolve o resultado completo (JSON). |
| `POST /products/edital-ai/run` | Roda a análise síncrona sobre o edital **já enviado antes** (não recebe arquivo no request). |
| `POST /products/edital-ai/submit` | Enfileira um job assíncrono (RabbitMQ) sobre o edital já enviado; devolve `{job_id, status, product_slug}` imediatamente. |
| `GET /products/edital-ai/historico` | Lista as análises do usuário logado (ordenadas por `created_at desc`). |
| `GET /products/edital-ai/download/{analise_id}?formato=excel\|pdf\|word\|email` | Baixa um dos 4 artefatos de uma análise específica do usuário. |

### `POST /products/edital-ai/upload` — fluxo completo

```python
extension = Path(file.filename).suffix.lower()
if extension not in {".pdf", ".docx", ".doc", ".txt", ".md"}:
    raise HTTPException(400, "Formato não suportado")

EDITAL_AI_INPUT_DIR.mkdir(parents=True, exist_ok=True)
for antigo in EDITAL_AI_INPUT_DIR.iterdir():        # limpa qualquer arquivo anterior
    if antigo.is_file():
        antigo.unlink()

nome_arquivo = Path(file.filename).name             # só o nome, sem diretórios (evita path traversal)
destination = EDITAL_AI_INPUT_DIR / nome_arquivo
destination.write_bytes(await file.read())

result = run_edital_ai_product(input_file=str(destination))
_persist_edital_analise(db, current_user, result)
arquivar_processado(destination, nome_original=file.filename)
return result
```

Note que **o nome do arquivo enviado é preservado integralmente** (inclusive
extensão em maiúsculas, ex.: `.PDF`) — isso é o que garante que os artefatos
de saída e o arquivo arquivado em `processados/` fiquem identificáveis pelo
mesmo nome do documento original, do início ao fim do fluxo.

### `platform/saas-backend/app/products/edital_ai_adapter.py` — a ponte

```python
EDITAL_AI_ROOT = Path("/workspace/tecle/products/edital-ai")
EDITAL_AI_INPUT_DIR = EDITAL_AI_ROOT / "input"
EDITAL_AI_PROCESSADOS_DIR = EDITAL_AI_ROOT / "processados"

def find_current_edital_file() -> Optional[Path]:
    """O único arquivo presente em input/ (upload sempre limpa antes de salvar)."""

def arquivar_processado(input_file: Path, nome_original: Optional[str] = None) -> Optional[Path]:
    """Move input/<arquivo> -> processados/<nome>_<YYYYMMDD_HHMMSS>.<ext>
    (nome vem de nome_original se informado, senão do próprio arquivo em input/).
    Se já existir um destino com o mesmo timestamp, sufixa _1, _2, ... """

def run_edital_ai_product(input_file: Optional[str] = None) -> dict:
    """Roda: <EDITAL_AI_ROOT>/.venv/bin/python <EDITAL_AI_ROOT>/integration/cli.py <input_file>
    via subprocess.run(cwd=EDITAL_AI_ROOT, capture_output=True, text=True).
    Se input_file for None, usa find_current_edital_file().
    Se returncode != 0, levanta RuntimeError com stdout+stderr completos.
    Faz json.loads(stdout.strip()) e devolve o dict."""
```

Ponto de atenção: o subprocesso roda **no `.venv` próprio do produto**, não
no `.venv` do `saas-backend` — os dois têm dependências Python
independentes. Isso isola versões de biblioteca (ex.: `openpyxl`,
`pdfplumber`) do produto das dependências do backend (FastAPI, SQLAlchemy),
mas tem custo de manutenção (dois ambientes para instalar/atualizar).

## Fluxo assíncrono (fila + worker)

```text
POST /products/edital-ai/submit
  -> cria Job(status="queued") no Postgres
  -> publish_job(job_id, product_slug="edital-ai") no RabbitMQ (fila "edital_ai_jobs")
  -> devolve {job_id, status:"queued", product_slug} imediatamente

edital-ai-worker (processo separado, consumidor da fila):
  on_message(job_id, product_slug):
    1. UPDATE jobs SET status='running', started_at=now()
    2. atual = find_current_edital_file()
    3. result = run_edital_ai_product(input_file=atual)
    4. user_id = SELECT user_id FROM jobs WHERE job_id=...
    5. INSERT INTO edital_analises (...) ON CONFLICT (analise_id) DO NOTHING
    6. UPDATE jobs SET status='completed', finished_at=now(), result_json=...
       (ou 'failed' + error_message em caso de exceção)
    7. arquivar_processado(atual)   # só roda se completou sem exceção
    8. channel.basic_ack(...)
```

O worker (`platform/tap-runtime/workers/edital-ai-worker/worker.py`) conecta
diretamente no Postgres via `psycopg2` (não via SQLAlchemy/ORM do backend) —
usa SQL cru para `jobs` e `edital_analises`. `prefetch_count=1` garante
processamento de um job por vez (sem paralelismo dentro do mesmo worker).

**Por que existe o fluxo assíncrono**: a análise via Ollama (modelo
`mistral`, rodando em CPU neste ambiente, sem GPU) leva **1 a 2 minutos por
edital**. Um request HTTP síncrono de 1-2 minutos é aceitável para
teste/demo mas não escala para produção — daí a fila.

## Painel de teste (`static/index.html`)

É uma página HTML/JS simples embutida no próprio backend (não é a UI
comercial), usada para testar upload, disparo de job e download dos
artefatos via `fetch()` contra os endpoints acima. Chama
`/products/edital-ai/historico` e `/products/edital-ai/download/{id}` para
listar e baixar análises anteriores.

## Servindo o backend (nota operacional)

O processo do `saas-backend` é um `uvicorn app.main:app` de longa duração —
**qualquer alteração de código em `routes/products.py` ou
`edital_ai_adapter.py` só entra em vigor reiniciando o processo**, a menos
que ele seja iniciado com a flag `--reload` (watch de arquivos), que é a
configuração recomendada em ambiente de desenvolvimento/teste. Isso já
causou uma incidência real (servidor rodando código antigo em memória gerando
nomes de arquivo errados após uma correção) — ver
`07-limitacoes-e-debito-tecnico.md`.
