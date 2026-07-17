# Padrões de Código

Não existe hoje um guia de estilo formal e único (nenhum arquivo `STYLEGUIDE.md` ou equivalente). Os padrões abaixo foram observados diretamente no código real e devem ser tratados como a convenção vigente até que sejam formalizados em `governance/standards/` (hoje vazio).

## Formatação

`.editorconfig` (raiz) define, para todos os arquivos:

```ini
root = true
[*]
indent_style = space
indent_size = 4
```

Nenhuma regra adicional de charset, final de linha ou espaço em branco está declarada — apenas indentação por espaços, 4 posições.

## O padrão de integração de produtos: facade / runner / schemas / cli

Todo produto (Speech-AI, Edital-AI, Code-AI) expõe exatamente a mesma estrutura de integração em `integration/`, e a plataforma consome cada produto sempre da mesma forma. Este é o padrão de código mais importante do repositório, porque é o mecanismo concreto que garante o desacoplamento exigido pela [constituição](constitution.md):

- **`schemas.py`** — um `@dataclass` de resultado (ex.: `SpeechRunResult`, `EditalRunResult`, `CodeAIRunResult`) com um método `to_dict()` (via `dataclasses.asdict`).
- **`runner.py`** — a orquestração real do pipeline (`execute_current_pipeline()` / `execute_pipeline()`), importando os módulos internos do produto (`config`, `pipeline`, `services`) e retornando o dataclass de resultado.
- **`facade.py`** — ponto de entrada público e enxuto (ex.: `run_speech_ai()`, `run_edital_ai()`, `run_code_ai()`), que chama o runner e retorna `.to_dict()`. É esta a costura que o backend SaaS chama.
- **`cli.py`** — script apenas com stdlib, adiciona a raiz do projeto ao `sys.path`, chama a facade, e:
  - em sucesso: `print(json.dumps(result))` — só a saída final vai para stdout;
  - em falha: `traceback.print_exc(file=sys.stderr)` seguido de `sys.exit(1)`.

Do lado do backend, cada produto tem um *adapter* espelhado (`platform/saas-backend/app/products/{speech_ai,edital_ai,code_ai}_adapter.py`) que executa o `cli.py` do produto como subprocesso, usando **o `.venv` do próprio produto** (não o do backend):

```python
subprocess.run([python_bin, cli_file], cwd=product_root, capture_output=True, text=True)
```

O adapter verifica `returncode`, levanta `RuntimeError` com stdout/stderr capturados em caso de falha, e faz `json.loads(stdout)` em caso de sucesso. Este contrato — JSON de entrada/saída sobre um subprocesso isolado — é literalmente o "produtos nunca acessam o banco diretamente, comunicação sempre via API" da constituição, aplicado no nível de processo.

## Estilo do backend FastAPI

Visto em `platform/saas-backend/app/routes/auth.py` e `app/security.py`:

- Rotas como funções simples com `APIRouter(prefix=..., tags=[...])`.
- Schemas de request definidos como `Pydantic BaseModel` diretamente no arquivo de rota (sem pasta `schemas/` separada no backend).
- Injeção de sessão via `Depends(get_db)`.
- Consultas diretas com SQLAlchemy (`.query().filter().first()`), sem camada de repositório.
- Erros via `HTTPException(status_code, detail)`.
- `security.py` centraliza hashing (`passlib.CryptContext(schemes=["bcrypt"])`) e JWT (`python-jose`), com segredo e expiração configuráveis por variável de ambiente (defaults de desenvolvimento: `dev-secret-key`, 60 minutos).
- Arquivos pequenos e diretos (tipicamente 25–90 linhas) — sem camada de serviço, sem abstrações extras.

## Disciplina de escopo por tarefa

Os arquivos em `tasks/saas/*/task.md` reforçam repetidamente: "um módulo por vez", "evitar abstração desnecessária", "não antecipar problemas futuros sem evidência". Isso aparece na prática — por exemplo, a tarefa `007-login` proíbe explicitamente adicionar JWT naquele mesmo passo, deixando-o para a tarefa `008-jwt`. Esse escopo estreito e sequencial é, na prática, o padrão de código mais importante do repositório: cada módulo faz uma coisa, e a próxima camada só é adicionada quando a anterior está validada.

## Ver também

- [development-flow.md](development-flow.md) — como esse escopo por tarefa se conecta ao ciclo de commits
- [../04-platform/gateway.md](../04-platform/gateway.md) — o gateway que consome os adapters descritos acima
