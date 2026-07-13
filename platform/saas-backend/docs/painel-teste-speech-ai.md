# Painel de Teste — Login e Speech-AI (TAPOS)

Documentação da implementação da tela de teste usada para validar o fluxo de
autenticação e o produto Speech-AI antes de seguir para a próxima etapa (task 15).

## Objetivo

Fornecer uma interface HTML simples, servida pelo próprio backend, para testar
manualmente: cadastro de usuário, login, listagem/assinatura de produtos e
upload de um arquivo `.txt` para processamento pelo Speech-AI — sem depender de
Postman/curl durante o desenvolvimento.

## Onde vive

- Front-end estático: `app/static/index.html`
- Montado pelo FastAPI em `app/main.py`:
  ```python
  app.mount(
      "/ui",
      StaticFiles(directory=Path(__file__).parent / "static", html=True),
      name="ui",
  )
  ```
  Acessível em `GET /ui` (ou `/ui/index.html`).

## Fluxo implementado na tela

1. **Cadastro** (`POST /auth/register`)
   - Campos: email, senha (pré-preenchidos com `teste@tecle.com` / `123456` para agilizar testes).
   - Chama `app/routes/auth.py::register`, que cria o `User` com senha hasheada (bcrypt via `hash_password`).
2. **Login** (`POST /auth/login`)
   - Valida credenciais com `verify_password` e retorna `access_token` (JWT) via `create_access_token`.
   - O token é salvo em `localStorage` (`tapos_token`) e reaproveitado em todas as chamadas seguintes via header `Authorization: Bearer <token>`.
   - Um indicador visual ("Token ativo" / "Sem token") no topo da página mostra o estado da sessão.
3. **Produtos e assinatura**
   - `GET /products` — lista produtos disponíveis.
   - `POST /subscriptions` — assina um produto pelo `slug` (padrão: `speech-ai`).
   - `GET /subscriptions` — lista assinaturas do usuário logado.
4. **Speech-AI — envio de arquivo fonte**
   - `POST /products/speech-ai/upload` (novo endpoint, ver abaixo): recebe um `.txt`, sobrescreve o arquivo de entrada do produto e executa o pipeline.
   - `POST /products/speech-ai/run`: reexecuta o pipeline sem enviar novo arquivo (usa o último arquivo salvo).
5. **Resultado**: exibe a resposta JSON bruta de qualquer chamada (bloco `<pre>`).
6. **Log de atividades**: histórico local (client-side, não persistido) de cada ação com timestamp e status (sucesso/erro/info), para acompanhar a sequência de testes.

## Alterações de backend que suportam a tela

### `app/routes/products.py`
Novo endpoint:
```python
SPEECH_AI_INPUT_FILE = Path("/workspace/tecle/products/speech-ai/input/script.txt")

@router.post("/speech-ai/upload")
async def upload_speech_ai_source(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # valida que o produto existe
    # valida que o usuário tem assinatura ativa (Subscription.is_active == True)
    # grava o conteúdo enviado em SPEECH_AI_INPUT_FILE
    # executa run_speech_ai_product() e retorna o resultado
```
Regras de acesso: só usuários autenticados (`get_current_user`, via JWT) **e** com
assinatura ativa do produto `speech-ai` podem enviar arquivo e disparar o
processamento — mesma regra já usada em `/products/speech-ai/run`.

### `app/main.py`
- Import de `StaticFiles` e montagem do diretório `app/static` em `/ui`.

### `requirements.txt`
- Adicionado `python-multipart` (dependência exigida pelo FastAPI para suportar `UploadFile`/`multipart form-data`).

## Endpoints envolvidos (resumo)

| Método | Rota                         | Autenticação | Descrição                                   |
|--------|------------------------------|--------------|----------------------------------------------|
| POST   | `/auth/register`             | Não          | Cria usuário (email + senha com hash bcrypt) |
| POST   | `/auth/login`                | Não          | Retorna JWT (`access_token`)                 |
| GET    | `/products`                  | Não*         | Lista produtos                               |
| POST   | `/subscriptions`              | Sim (Bearer) | Cria assinatura para o usuário logado         |
| GET    | `/subscriptions`              | Sim (Bearer) | Lista assinaturas do usuário logado           |
| POST   | `/products/speech-ai/upload` | Sim (Bearer) + assinatura ativa | Recebe `.txt`, salva e executa o Speech-AI |
| POST   | `/products/speech-ai/run`    | Sim (Bearer) + assinatura ativa | Reexecuta o Speech-AI com o último arquivo salvo |

\* conforme implementação atual de `list_products` (não exige token).

## Pontos de atenção / débito técnico

- O caminho do arquivo de entrada (`SPEECH_AI_INPUT_FILE`) está **hardcoded** para
  `/workspace/tecle/products/speech-ai/input/script.txt`, fora do diretório do
  serviço (`saas-backend`). Isso funciona no ambiente atual, mas não é portável
  para outro host/ambiente sem ajuste de configuração (idealmente via variável
  de ambiente).
- O front-end (`index.html`) é puramente para teste manual (sem build step,
  sem framework) e guarda o JWT em `localStorage`, o que é aceitável para um
  painel de teste local mas não deve ser replicado em produção sem revisão de
  segurança (XSS, expiração de token, etc.).
- O log de atividades é apenas client-side (não persistido, perdido ao recarregar a página).

## Como testar manualmente

1. Subir o backend (`uvicorn app.main:app --reload`, a partir de `platform/saas-backend`).
2. Acessar `http://localhost:8000/ui`.
3. Cadastrar → Login → Assinar produto `speech-ai` → enviar um `.txt` na seção 4 → conferir resultado no bloco "Resultado" e no log de atividades.
