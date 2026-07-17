# 02 — Arquitetura

## Visão em camadas

```text
┌───────────────────────────────────────────────────────────┐
│ Cliente (painel de teste HTML / API client)                │
└───────────────────────────┬───────────────────────────────┘
                            │ HTTP REST (JSON), JWT bearer
                            ▼
┌───────────────────────────────────────────────────────────┐
│ SaaS Backend — FastAPI (platform/saas-backend), porta 8000  │
│  - Auth (JWT)                                               │
│  - Checagem de assinatura ativa por produto                 │
│  - Endpoints /products/edital-ai/*                           │
│  - Adapter: app/products/edital_ai_adapter.py                │
│  - Persistência: tabela edital_analises (Postgres)           │
│  - Fila (opcional): publica em RabbitMQ p/ processamento async│
└───────────────────────────┬───────────────────────────────┘
                            │ subprocess (venv próprio do produto)
                            ▼
┌───────────────────────────────────────────────────────────┐
│ edital-ai (products/edital-ai/) — processo Python isolado    │
│  integration/cli.py <arquivo>                                │
│    → integration/facade.py → integration/runner.py           │
│    → app/edital_ai_app.py (EditalAIApp.run)                   │
│    → pipeline/* (extração → parsing → análise → artefatos)   │
│  stdout: um único JSON (EditalRunResult) consumido pelo adapter│
└───────────────────────────┬───────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────┐
│ Infraestrutura                                               │
│  - Ollama (IA local, HTTP em localhost:11434, modelo mistral) │
│  - PostgreSQL (metadados de jobs e análises)                  │
│  - RabbitMQ (fila "edital_ai_jobs" para o fluxo assíncrono)    │
│  - Filesystem local: input/ · output/ · processados/           │
└───────────────────────────────────────────────────────────┘
```

Ponto de design importante: **o produto `edital-ai` não conhece o backend**.
Ele é um programa de linha de comando autocontido, com seu próprio
`.venv`, que lê um caminho de arquivo e devolve um único JSON no stdout. Toda
a integração com autenticação, banco de dados, filas etc. vive **fora** dele,
no adapter do `saas-backend`. Isso permite rodar/testar o produto
isoladamente (`python main.py <arquivo>` ou `python integration/cli.py
<arquivo>`) sem subir o backend inteiro.

## Duas formas de disparar o processamento

1. **Síncrono** (`POST /products/edital-ai/upload` ou `/run`): o request HTTP
   fica bloqueado até o subprocesso terminar (extração + IA + geração de
   artefatos). Como a chamada ao Ollama pode levar 1-2 minutos numa máquina
   sem GPU, isso é aceitável só para teste/demo, não para produção com muitos
   usuários simultâneos.
2. **Assíncrono** (`POST /products/edital-ai/submit` → fila RabbitMQ →
   `edital-ai-worker`): cria um `Job` com status `queued`, devolve
   imediatamente o `job_id`, e o worker dedicado (processo separado,
   `platform/tap-runtime/workers/edital-ai-worker/worker.py`) consome a fila,
   roda o mesmo adapter, e atualiza o status do job (`running` →
   `completed`/`failed`) além de gravar o resultado em `edital_analises`.

Ambos os fluxos, síncrono e assíncrono, convergem no mesmo ponto: o adapter
`run_edital_ai_product()` em
`platform/saas-backend/app/products/edital_ai_adapter.py`.

## Estrutura de diretórios real (`products/edital-ai/`)

```text
products/edital-ai/
├── main.py                     # CLI standalone (uso local/dev): python main.py <arquivo>
├── requirements.txt
├── config/
│   ├── config_manager.py       # ConfigManager: lê settings.json + env vars do Ollama
│   └── settings.json           # diretórios de input/output, timeout, modelo Ollama
├── app/
│   └── edital_ai_app.py        # EditalAIApp: orquestra a pipeline completa
├── models/                     # dataclasses puras (sem ORM, sem validação externa)
│   ├── edital.py                # Edital, Secao
│   ├── objeto.py                 # Objeto (item/lote da licitação)
│   ├── requisito.py              # Requisito (documento de habilitação)
│   ├── prazo.py                  # Prazo
│   ├── analise.py                 # Analise (saída qualitativa)
│   └── artefato.py                # Artefato (paths dos 4 arquivos gerados)
├── pipeline/                   # os 4 estágios do processamento, nesta ordem
│   ├── edital_extractor.py      # 1. extrai texto + tabelas nativas do arquivo
│   ├── edital_parser.py         # 2. estrutura texto/tabelas em Edital (regex/heurística)
│   ├── edital_analyzer.py       # 3. gera a análise qualitativa (Ollama + fallback)
│   └── artefato_generator.py    # 4. gera os 4 artefatos de saída
├── services/                   # implementações de baixo nível usadas pelo pipeline
│   ├── pdf_service.py            # pdfplumber (texto+tabelas) com fallback OCR (pytesseract)
│   ├── docx_service.py           # python-docx
│   ├── text_cleaner.py           # normalização de espaços/quebras de linha
│   ├── ollama_service.py         # cliente HTTP minimalista do Ollama
│   ├── excel_generator.py        # openpyxl — 5 abas
│   ├── pdf_generator.py          # reportlab
│   ├── word_generator.py         # python-docx
│   └── email_generator.py        # texto puro (.txt), pronto para copiar/colar num e-mail real
├── prompts/
│   └── generate_summary.txt     # único prompt usado hoje (resumo + riscos + score)
├── integration/                 # fronteira de integração com o TAPOS
│   ├── schemas.py                # EditalRunResult (o dict que sai no stdout)
│   ├── facade.py                 # run_edital_ai(arquivo) -> dict
│   ├── runner.py                 # execute_pipeline(arquivo) -> EditalRunResult
│   └── cli.py                    # entry point chamado pelo adapter via subprocess
├── input/                       # UM único edital "em foco" por vez (todo o produto)
├── output/                      # os 4 artefatos da última análise rodada
├── processados/                 # arquivo original arquivado após a análise (nome + timestamp)
├── logs/
└── .venv/                       # ambiente virtual próprio do produto (não o do backend)
```

## Fluxo de execução completo (upload síncrono)

```text
1. Usuário faz POST /products/edital-ai/upload com o arquivo
2. routes/products.py:
   a. valida JWT (get_current_user) e assinatura ativa do produto
   b. valida extensão (.pdf/.docx/.doc/.txt/.md)
   c. limpa tudo que houver em input/ (só existe UM edital em foco)
   d. salva o arquivo em input/ com o NOME ORIGINAL do upload
   e. chama run_edital_ai_product(input_file=<caminho>)
3. edital_ai_adapter.py:
   a. localiza o Python e o cli.py dentro do .venv do produto
   b. roda `subprocess.run([python, cli.py, arquivo], cwd=EDITAL_AI_ROOT)`
   c. se stderr/exit code != 0 -> levanta RuntimeError com stdout+stderr
   d. faz json.loads(stdout) -> dict (EditalRunResult serializado)
4. De volta em routes/products.py:
   a. persiste o resultado em EditalAnalise (tabela edital_analises)
   b. arquivar_processado(arquivo, nome_original=file.filename)
      -> move de input/ para processados/<nome>_<timestamp>.<ext>
   c. devolve o JSON completo como resposta HTTP
```

Dentro do subprocesso (`integration/cli.py` → `EditalAIApp.run`):

```text
EditalAIApp.run(arquivo_path):
  1. EditalExtractor.extract_full(arquivo_path) -> (texto, tabelas)
  2. EditalParser.parse(texto, tabelas) -> Edital (numero, orgao, modalidade,
     objeto, prazos, requisitos, objetos/itens)
  3. EditalAnalyzer.analyze(edital) -> Analise (resumo, riscos, oportunidades,
     recomendações, score — via Ollama, com fallback determinístico)
  4. ArtefatoGenerator.generate_all(edital, analise, nome_documento=<stem do
     arquivo>) -> Artefato (paths dos 4 arquivos, todos nomeados como o
     documento original)
```

## Diretório `input/` como "documento em foco" — implicação importante

O adapter e as rotas tratam `input/` como se só pudesse existir **um** edital
por vez em todo o sistema (`find_current_edital_file()` pega o único arquivo
presente). Isso é adequado para um piloto de usuário único, mas é a maior
limitação estrutural para um produto comercial multi-tenant — ver detalhes em
[`07-limitacoes-e-debito-tecnico.md`](07-limitacoes-e-debito-tecnico.md).
