# TAPOS — Tecnologias

## Backend SaaS (`platform/saas-backend/requirements.txt`)

| Tecnologia | Papel |
|---|---|
| FastAPI | framework web do backend |
| Uvicorn | servidor ASGI |
| SQLAlchemy | ORM |
| psycopg2-binary | driver PostgreSQL |
| python-jose | geração/validação de JWT |
| passlib[bcrypt] + bcrypt<4.1 | hash de senha |
| Pydantic | schemas de request/response |
| python-multipart | upload de arquivos (`UploadFile`) |
| pika | cliente RabbitMQ (publicação de jobs) |
| pytest (dev) | testes automatizados do backend |

## Infraestrutura local (`/data/platform`, containers Docker verificados ativos)

| Serviço | Imagem | Papel |
|---|---|---|
| PostgreSQL | `postgres:15` | dados estruturados |
| Redis | `redis:7-alpine` | cache/sessões (reservado, ainda não usado ativamente) |
| RabbitMQ | `rabbitmq:3-management` | fila de mensagens para execução assíncrona |
| MinIO | `minio/minio` | armazenamento de objetos (reservado) |
| Qdrant | `qdrant/qdrant` | banco vetorial (reservado, uso futuro em RAG) |
| Ollama | `ollama/ollama` | runtime de IA local (usado hoje pelo `edital-ai`, modelo `mistral`) |
| Open WebUI | `ghcr.io/open-webui/open-webui` | interface de administração/teste de modelos Ollama |
| Portainer | `portainer/portainer-ce` | administração dos containers Docker |

## Dependências por produto

- **speech-ai**: `edge-tts`, `langdetect`, `python-dotenv` (ver [../02-speech-ai](../02-speech-ai/));
- **edital-ai**: `pdfplumber`, `pytesseract`, `pdf2image`, `python-docx`, `openpyxl`, `reportlab`, `requests` (+ Tesseract OCR e Poppler como dependências de sistema; `jinja2`/`python-pptx` presentes mas não usadas — ver [../03-products/edital-ai.md](../03-products/edital-ai.md));
- **code-ai**: `pdfplumber`, `python-docx`, `pandas`, `python-pptx`, OCR via `pytesseract`/`pdf2image` (ver [../03-products/code-ai.md](../03-products/code-ai.md)).

## Ambiente de desenvolvimento

- VSCode remoto (SSH) + Claude Code, operando a partir da raiz única `/workspace/tecle`;
- `.editorconfig` na raiz: indentação de 4 espaços, sem outras regras de estilo declaradas;
- sem linter/formatter configurado (nenhum `ruff`, `flake8`, `pylint`, `mypy`/`pyright` encontrado no repositório) — ver [../05-development/coding-standards.md](../05-development/coding-standards.md);
- controle de versão: Git, com o desenvolvimento disciplinado por tarefa documentado em `tasks/saas/`.

## Automação e infraestrutura como código

`automation/` reúne os diretórios reservados para Terraform, Ansible, Packer, scripts Bash/Python e GitHub Actions — nenhum deles populado ainda; a automação real hoje é o script `start_tapos_env.sh` na raiz do workspace.

---

## Ver também

- [architecture.md](architecture.md) — como estas tecnologias se conectam
- [../04-platform/runtime.md](../04-platform/runtime.md) — o runtime desses serviços em detalhe
- [../05-development/coding-standards.md](../05-development/coding-standards.md) — convenções de código observadas
