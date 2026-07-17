# Task 15 — Teste Integrado (014A + 014B + 015 + Painel `/ui`)

Roteiro de teste manual, passo a passo, para validar de ponta a ponta tudo que já
foi construído até a Task 015: cadastro, login, produtos, assinatura (subscrição),
processamento de arquivo (síncrono e assíncrono) e a fila (RabbitMQ + worker).

A seção 8 cobre o produto `code-ai` (qualquer documento → Markdown), integrado à
plataforma seguindo o mesmo padrão de speech-ai (facade, adapter, rotas, fila e worker).

---

## 0. Pré-requisitos

### 0.1 Infraestrutura Docker no ar

```bash
docker ps
```

Confirme que estes containers estão `Up`:

| Container   | Uso neste teste                          | Porta          |
|-------------|-------------------------------------------|----------------|
| `postgres`  | banco de dados (users, products, jobs...) | 5432           |
| `rabbitmq`  | fila `speech_ai_jobs`                     | 5672 / 15672   |
| `redis`     | não usado diretamente neste teste          | 6379           |

Se algum estiver parado, suba antes de continuar (`docker start <nome>`).

### 0.2 Backend SaaS no ar

```bash
cd /workspace/tecle/platform/saas-backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Validar:

```bash
curl -s http://localhost:8000/health
```

Esperado: `200` com corpo indicando serviço saudável.

### 0.3 Painel de teste acessível

Abrir no navegador:

```
http://localhost:8000/ui
```

O painel tem 5 blocos: **1. Cadastro**, **2. Login**, **3. Produtos e assinatura**,
**4. Speech-AI (arquivo/síncrono)**, **5. Speech-AI (fila/assíncrono)** — mais os
blocos de **Resultado** e **Log de atividades**.

---

## 1. Teste de Inclusão (Cadastro de Usuário) — base da Task 014A/B

### Via painel `/ui`

1. Bloco **1. Cadastro**: usar um e-mail novo (ex.: `teste.integrado@tecle.com`) e senha `123456`.
2. Clicar **Cadastrar**.
3. Esperado: feedback verde "Usuário ... cadastrado com sucesso." e log de atividade com tag `sucesso`.
4. Repetir o cadastro com o mesmo e-mail → esperado feedback vermelho (e-mail já existe, erro 400).

### Via curl (equivalente)

```bash
curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"teste.integrado@tecle.com","password":"123456"}'
```

Esperado: `{"id": <n>, "email": "teste.integrado@tecle.com"}`

---

## 2. Teste de Login

### Via painel `/ui`

1. Bloco **2. Login**: mesmo e-mail/senha do cadastro.
2. Clicar **Entrar**.
3. Esperado: badge no topo da página muda de "Sem token." (vermelho) para "Token ativo" (verde).
4. Testar também senha errada → deve falhar (401) e log com tag `erro`.

### Via curl

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste.integrado@tecle.com","password":"123456"}' | python3 -c "import json,sys;print(json.load(sys.stdin)['access_token'])")

echo "$TOKEN"
```

Guarde esse `$TOKEN` — ele será reutilizado nos comandos curl abaixo.

---

## 3. Teste de Produtos e Subscrição (Task 014B)

### 3.1 Listar produtos disponíveis

Painel: botão **Listar produtos** (bloco 3).

```bash
curl -s http://localhost:8000/products | python3 -m json.tool
```

Esperado: lista incluindo o produto `speech-ai` (`slug: "speech-ai"`, `is_active: true`).

> Se a lista vier vazia, o produto ainda não foi cadastrado no banco — isso bloqueia
> todos os passos seguintes. Nesse caso, cadastrar o registro `speech-ai` na tabela
> `products` antes de prosseguir.

### 3.2 Assinar o produto speech-ai

Painel: campo "Slug do produto" com `speech-ai` → botão **Assinar** (bloco 3).

```bash
curl -s -X POST http://localhost:8000/subscriptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_slug":"speech-ai"}' | python3 -m json.tool
```

Esperado: objeto com `product_slug: "speech-ai"`, `is_active: true`.

### 3.3 Confirmar assinatura

Painel: **Minhas assinaturas** (bloco 3).

```bash
curl -s http://localhost:8000/subscriptions -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Esperado: a assinatura criada aparece na lista.

### 3.4 Teste negativo — sem token

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/subscriptions \
  -H "Content-Type: application/json" -d '{"product_slug":"speech-ai"}'
```

Esperado: `401`.

### 3.5 Teste negativo — assinar produto inexistente

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/subscriptions \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"product_slug":"produto-que-nao-existe"}'
```

Esperado: `404`.

---

## 4. Teste de Acesso ao Produto (`GET /products/{slug}/access`)

```bash
curl -s http://localhost:8000/products/speech-ai/access -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Esperado: `{"product_slug": "speech-ai", "access": true}`.

Teste negativo — usuário autenticado, sem assinatura desse produto (usar um usuário novo,
sem passar pelo passo 3.2):

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/products/speech-ai/access \
  -H "Authorization: Bearer $TOKEN_SEM_SUBSCRIPTION"
```

Esperado: `403`.

---

## 5. Teste de Processamento de Arquivo — Fluxo Síncrono (Task 014A/014B)

Este bloco valida a facade (`run_speech_ai`) chamada via HTTP síncrono, sem fila.

### 5.1 Upload de um novo arquivo `.txt`

Painel, bloco **4. Speech-AI — enviar arquivo fonte**:

1. Selecionar um arquivo `.txt` de teste (ex.: criar um `teste_integrado.txt` com 2-3 frases).
2. Clicar **Enviar e processar**.
3. Esperado: bloco "Resultado" mostra JSON com `status: "executed"` e os caminhos:
   `input_file`, `narration_file`, `speech_file`, `audio_file`.

```bash
echo "Este é um teste integrado da Task 15 da plataforma TAPOS." > /tmp/teste_integrado.txt

curl -s -X POST http://localhost:8000/products/speech-ai/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/teste_integrado.txt" | python3 -m json.tool
```

### 5.2 Validar arquivos gerados no disco

```bash
ls -la /workspace/tecle/products/speech-ai/output/audio.mp3 \
       /workspace/tecle/products/speech-ai/output/narration.txt \
       /workspace/tecle/products/speech-ai/output/speech.txt
```

Esperado: os 3 arquivos existem e foram atualizados agora (checar timestamp com `-la`).

### 5.3 Reexecutar sem novo arquivo

Painel: botão **Rodar novamente (sem novo arquivo)** (bloco 4).

```bash
curl -s -X POST http://localhost:8000/products/speech-ai/run \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Esperado: mesmo padrão de retorno, reprocessando o último `script.txt` salvo.

### 5.4 Teste negativo — sem token

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/products/speech-ai/run
```

Esperado: `401`.

### 5.5 Teste negativo — sem subscription ativa

Repetir 5.3 com `$TOKEN_SEM_SUBSCRIPTION` (usuário que não passou pelo passo 3.2).

Esperado: `403`.

---

## 6. Teste de Fila (RabbitMQ) — Fluxo Assíncrono (Task 015)

Este é o bloco mais importante deste documento: valida a fila ponta a ponta.

### 6.1 Confirmar que a fila está acessível

Console de gerência do RabbitMQ (login `admin` / senha `admin`, salvo configuração diferente):

```
http://localhost:15672
```

Ir em **Queues** → confirmar que existe (ou será criada no primeiro submit) a fila:

```
speech_ai_jobs
```

Também é possível checar via CLI dentro do container:

```bash
docker exec rabbitmq rabbitmqctl list_queues name messages consumers
```

Esperado antes de qualquer submit: fila `speech_ai_jobs` com `messages = 0` (ou ausente,
se ninguém publicou ainda).

### 6.2 Submeter execução assíncrona (sem worker rodando ainda)

**Propositalmente não suba o worker ainda** — o objetivo deste passo é ver a mensagem
parada na fila.

Painel, bloco **5. Speech-AI — execução assíncrona (fila)**:

1. Clicar **Executar assíncrono**.
2. Esperado: feedback com `job_id` (uuid) e `status: queued`. O campo "Job ID" é
   preenchido automaticamente.

```bash
SUBMIT=$(curl -s -X POST http://localhost:8000/products/speech-ai/submit \
  -H "Authorization: Bearer $TOKEN")
echo "$SUBMIT" | python3 -m json.tool
JOB_ID=$(echo "$SUBMIT" | python3 -c "import json,sys;print(json.load(sys.stdin)['job_id'])")
```

Esperado: `{"job_id": "<uuid>", "status": "queued", "product_slug": "speech-ai"}`.

### 6.3 Confirmar a mensagem parada na fila

```bash
docker exec rabbitmq rabbitmqctl list_queues name messages consumers
```

Esperado: `speech_ai_jobs` com `messages = 1` e `consumers = 0` (ninguém consumindo ainda).

Também dá pra ver visualmente em `http://localhost:15672` → Queues → `speech_ai_jobs`.

### 6.4 Consultar status do job (ainda `queued`)

Painel: campo "Job ID" já preenchido → botão **Consultar job** (bloco 5).

```bash
curl -s http://localhost:8000/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Esperado: `status: "queued"`, `result: null`.

### 6.5 Subir o worker e observar o consumo

Em outro terminal:

```bash
cd /workspace/tecle/platform/tap-runtime/workers/speech-ai-worker
source /workspace/tecle/platform/saas-backend/.venv/bin/activate
export DATABASE_URL=postgresql://admin:admin@localhost:5432/platform
export RABBITMQ_URL=amqp://admin:admin@localhost:5672/
python worker.py
```

Esperado no terminal: `speech-ai-worker: aguardando jobs...` e, em seguida, o
processamento da mensagem pendente (sem precisar reenviar nada).

Reconferir a fila:

```bash
docker exec rabbitmq rabbitmqctl list_queues name messages consumers
```

Esperado: `messages = 0`, `consumers = 1` (worker consumindo).

### 6.6 Consultar status até `completed`

Painel: botão **Consultar job** de novo (bloco 5).

```bash
curl -s http://localhost:8000/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Esperado (pode levar alguns segundos, repetir o comando até mudar):
`status: "completed"`, `result` preenchido com `input_file`, `narration_file`,
`speech_file`, `audio_file`.

### 6.7 Teste de múltiplos jobs na fila (concorrência/ordem)

Com o worker ainda rodando, submeter 3 jobs seguidos:

```bash
for i in 1 2 3; do
  curl -s -X POST http://localhost:8000/products/speech-ai/submit \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
done
```

Esperado: 3 `job_id` distintos, todos com `status: queued` na criação. Acompanhar via
`GET /jobs/{job_id}` que cada um evolui para `running` e depois `completed`/`failed`
em sequência (o worker atual processa um de cada vez — `prefetch_count=1`).

### 6.8 Teste de falha — job com erro

Forçar uma falha (ex.: renomear temporariamente o binário Python do speech-ai ou
usar um `.txt` de entrada vazio/corrompido, se a pipeline validar isso) e confirmar:

```bash
curl -s http://localhost:8000/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Esperado: `status: "failed"`, `error_message` preenchido com a mensagem de erro real
(stdout/stderr do subprocesso), e a fila segue consumindo as próximas mensagens
normalmente (uma falha não deve travar o worker).

> Lembre de reverter qualquer alteração feita só para forçar a falha antes de seguir.

### 6.9 Teste negativo — consultar job de outro usuário

Job criado pelo usuário A não pode ser lido pelo usuário B:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/jobs/$JOB_ID \
  -H "Authorization: Bearer $TOKEN_OUTRO_USUARIO"
```

Esperado: `404` (o endpoint filtra por `user_id`, então job de outro usuário não é encontrado).

### 6.10 Teste negativo — submit sem subscription

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/products/speech-ai/submit \
  -H "Authorization: Bearer $TOKEN_SEM_SUBSCRIPTION"
```

Esperado: `403`.

### 6.11 Teste negativo — sem token

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/products/speech-ai/submit
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/jobs/$JOB_ID
```

Esperado: `401` nos dois casos.

---

## 7. Regressão — Compatibilidade com Task 014B e painel `/ui`

Depois de validar o fluxo assíncrono, reconfirmar que nada quebrou no fluxo antigo:

```bash
curl -s -X POST http://localhost:8000/products/speech-ai/run \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/ui
```

Esperado: `run` síncrono continua retornando `status: "executed"`; `/ui` retorna `200`.

Script automatizado equivalente a todo o bloco 014B + 015 já existe no repositório e
pode ser rodado como conferência cruzada:

```bash
/workspace/tecle/test_task015.sh
```

---

## 8. Produto `code-ai` — qualquer documento → Markdown

O `code-ai` (`/workspace/tecle/products/code-ai`) converte PDF, DOCX, XLSX, XLS, CSV,
PPTX, PNG, JPG, JPEG, TXT e MD para Markdown. Foi integrado à TAPOS seguindo exatamente
o mesmo padrão do speech-ai:

- Facade programática em `products/code-ai/integration/` (`run_code_ai`).
- `.venv` próprio do produto com as dependências de `requirements.txt` + `tabulate`
  (necessário para `pandas.DataFrame.to_markdown`).
- Adapter `platform/saas-backend/app/products/code_ai_adapter.py`.
- Rotas `POST /products/code-ai/run`, `POST /products/code-ai/upload`,
  `POST /products/code-ai/submit`.
- Fila própria `code_ai_jobs` (publisher generalizado em `app/jobs/publisher.py`) e
  worker dedicado em `platform/tap-runtime/workers/code-ai-worker/`.
- Blocos **6** (upload/execução síncrona) e **7** (execução assíncrona/fila) no painel
  `/ui`, no mesmo padrão visual dos blocos 4 e 5 do speech-ai.

> Durante a integração foi corrigido um bug no conversor original
> (`products/code-ai/src/conversor_markdown.py`): um import morto e incompatível de
> `WD_PARAGRAPH_STYLE` quebrava toda conversão de `.docx`. A linha foi removida (não é
> usada em nenhum lugar do arquivo) e a conversão de DOCX passou a funcionar
> corretamente.

### 8.1 Assinatura

Igual à seção 3, trocando o slug:

```bash
curl -s -X POST http://localhost:8000/subscriptions \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"product_slug":"code-ai"}' | python3 -m json.tool
```

### 8.2 Upload de documento (síncrono)

Painel, bloco **6. Code-AI — enviar documento**: escolher qualquer arquivo suportado
(`.pdf`, `.docx`, `.xlsx`, `.xls`, `.csv`, `.pptx`, `.png`, `.jpg`, `.jpeg`, `.txt`,
`.md`) e clicar **Enviar e converter**.

```bash
curl -s -X POST http://localhost:8000/products/code-ai/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/caminho/para/documento.pdf" | python3 -m json.tool
```

Esperado: `status: "executed"`, com `converted[0].output_file` apontando para o `.md`
gerado em `products/code-ai/output/`. O arquivo é salvo internamente como
`input/documento.<extensão original>` — cada novo upload sobrescreve o "documento atual",
igual ao `script.txt` do speech-ai.

Teste negativo — extensão não suportada (ex. `.exe`):

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/products/code-ai/upload \
  -H "Authorization: Bearer $TOKEN" -F "file=@/tmp/arquivo.exe"
```

Esperado: `400`.

### 8.3 Rodar novamente (reprocessa a pasta `input/`)

Painel: botão **Rodar novamente (reprocessa pasta input/)** (bloco 6).

```bash
curl -s -X POST http://localhost:8000/products/code-ai/run \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Esperado: `status: "executed"`, `files_processed` cobrindo todos os arquivos atualmente
em `products/code-ai/input/` (não só o último upload).

### 8.4 Execução assíncrona (fila `code_ai_jobs`)

Painel, bloco **7. Code-AI — execução assíncrona (fila)**: mesmo padrão do bloco 5 do
speech-ai, mas publicando na fila `code_ai_jobs`.

```bash
SUBMIT=$(curl -s -X POST http://localhost:8000/products/code-ai/submit \
  -H "Authorization: Bearer $TOKEN")
echo "$SUBMIT" | python3 -m json.tool
JOB_ID=$(echo "$SUBMIT" | python3 -c "import json,sys;print(json.load(sys.stdin)['job_id'])")
```

Confirmar a fila (mensagem parada se o worker não estiver rodando):

```bash
docker exec rabbitmq rabbitmqctl list_queues name messages consumers
```

Esperado: `code_ai_jobs` com `messages = 1`, `consumers = 0` antes do worker subir.

Subir o worker dedicado:

```bash
cd /workspace/tecle/platform/tap-runtime/workers/code-ai-worker
source /workspace/tecle/platform/saas-backend/.venv/bin/activate
export DATABASE_URL=postgresql://admin:admin@localhost:5432/platform
export RABBITMQ_URL=amqp://admin:admin@localhost:5672/
python worker.py
```

Consultar o job até `completed`:

```bash
curl -s http://localhost:8000/jobs/$JOB_ID -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### 8.5 Testes negativos

Mesmo padrão da seção 6 (401 sem token, 403 sem subscription, 404 para job de outro
usuário), trocando `speech-ai` por `code-ai` nos endpoints `/products/code-ai/run`,
`/products/code-ai/submit` e `/products/code-ai/upload`.

### 8.6 Regressão cruzada entre produtos

Depois de rodar os testes de `code-ai`, reconfirme que `speech-ai` continua intacto
(seções 5–7) — os dois produtos compartilham as mesmas tabelas (`products`,
`subscriptions`, `jobs`) e o mesmo publisher, então uma regressão em um pode vazar
para o outro.

---

## 9. Checklist final

- [ ] Cadastro de usuário novo funciona (201/200) e cadastro duplicado falha (400)
- [ ] Login funciona e token aparece como "ativo" no painel
- [ ] `GET /products` lista `speech-ai`
- [ ] `POST /subscriptions` cria assinatura de `speech-ai`
- [ ] `GET /products/speech-ai/access` retorna `access: true` com subscription ativa
- [ ] Upload de `.txt` processa e gera `audio.mp3`, `narration.txt`, `speech.txt`
- [ ] `POST /products/speech-ai/run` (síncrono) funciona
- [ ] `POST /products/speech-ai/submit` retorna `job_id` com `status: queued`
- [ ] Mensagem aparece na fila `speech_ai_jobs` antes do worker consumir
- [ ] Worker consome a mensagem e job evolui `queued → running → completed`
- [ ] Múltiplos jobs em sequência são processados um a um pelo worker
- [ ] Job com erro força `status: failed` sem travar o worker
- [ ] `GET /jobs/{id}` de outro usuário retorna `404`
- [ ] Chamadas sem token retornam `401`
- [ ] Chamadas sem subscription retornam `403`
- [ ] Painel `/ui` continua acessível (`200`) e fluxo antigo (014B) continua funcionando
- [ ] `code-ai`: assinatura funciona (`POST /subscriptions`)
- [ ] `code-ai`: upload de documento (`.pdf`/`.docx`/`.csv`/etc.) gera `.md` em `output/`
- [ ] `code-ai`: upload com extensão não suportada retorna `400`
- [ ] `code-ai`: `POST /products/code-ai/run` reprocessa a pasta `input/`
- [ ] `code-ai`: `POST /products/code-ai/submit` publica em `code_ai_jobs` e retorna `queued`
- [ ] `code-ai`: worker dedicado consome `code_ai_jobs` e job evolui até `completed`
- [ ] `code-ai`: testes negativos (401/403/404) equivalentes aos do speech-ai
- [ ] `code-ai` e `speech-ai` não regridem um ao outro (filas e workers independentes)
