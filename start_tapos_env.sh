#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# TAPOS - START LOCAL ENVIRONMENT
# ============================================================
# Objetivo:
#   Subir o ambiente local validado da TAPOS para testes via UI.
#
# Componentes iniciados:
#   1. Infra Docker existente: postgres e rabbitmq
#   2. Backend FastAPI: platform/saas-backend
#   3. Worker assíncrono Speech-AI: speech-ai-worker
#
# UI validada no backend FastAPI:
#   http://localhost:8000/ui/
#
# Observação:
#   http://localhost/ui/ somente funcionará se existir proxy/reverse proxy
#   redirecionando porta 80 para 8000. Este script NÃO cria proxy.
# ============================================================

ROOT_DIR="/workspace/tecle"
BACKEND_DIR="$ROOT_DIR/platform/saas-backend"
BACKEND_VENV="$BACKEND_DIR/.venv/bin/activate"
WORKER_DIR="$ROOT_DIR/platform/tap-runtime/workers/speech-ai-worker"
LOG_DIR="$ROOT_DIR/.runtime/logs"
PID_DIR="$ROOT_DIR/.runtime/pids"

BACKEND_HOST="0.0.0.0"
BACKEND_PORT="8000"

export DATABASE_URL="postgresql+psycopg2://admin:admin@localhost:5432/platform"
export WORKER_DATABASE_URL="postgresql://admin:admin@localhost:5432/platform"
export RABBITMQ_URL="amqp://admin:admin@localhost:5672/"
export SAAS_BACKEND_ROOT="$BACKEND_DIR"

mkdir -p "$LOG_DIR" "$PID_DIR"

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
print_header() {
  echo
  echo "============================================================"
  echo "$1"
  echo "============================================================"
}

check_path() {
  local path="$1"
  local label="$2"

  if [ ! -e "$path" ]; then
    echo "ERRO: $label não encontrado: $path"
    exit 1
  fi
}

port_open() {
  local port="$1"
  ss -ltn 2>/dev/null | awk '{print $4}' | grep -q ":${port}$"
}

wait_http() {
  local url="$1"
  local max_attempts=20
  local attempt=1

  while [ "$attempt" -le "$max_attempts" ]; do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
    attempt=$((attempt + 1))
  done

  return 1
}

# ------------------------------------------------------------
# Validar estrutura
# ------------------------------------------------------------
print_header "1. Validando estrutura TAPOS"

check_path "$ROOT_DIR" "ROOT_DIR"
check_path "$BACKEND_DIR" "Backend TAPOS"
check_path "$BACKEND_VENV" "Virtualenv do backend"
check_path "$WORKER_DIR/worker.py" "Worker Speech-AI"

if [ ! -f "$BACKEND_DIR/app/main.py" ]; then
  echo "ERRO: app/main.py não encontrado em $BACKEND_DIR"
  exit 1
fi

echo "OK: estrutura encontrada"

# ------------------------------------------------------------
# Subir infraestrutura Docker existente
# ------------------------------------------------------------
print_header "2. Validando infraestrutura Docker"

cd "$ROOT_DIR"

if command -v docker >/dev/null 2>&1; then
  if [ -f "$ROOT_DIR/docker-compose.yml" ] || [ -f "$ROOT_DIR/compose.yml" ] || [ -f "$ROOT_DIR/compose.yaml" ]; then
    echo "Docker Compose encontrado. Tentando subir postgres e rabbitmq..."
    docker compose up -d postgres rabbitmq || true
  else
    echo "docker-compose.yml não encontrado. Pulando docker compose up."
  fi
else
  echo "ERRO: docker não encontrado no ambiente."
  exit 1
fi

if docker ps --format '{{.Names}}' | grep -q '^postgres$'; then
  echo "OK: container postgres em execução"
else
  echo "AVISO: container postgres não encontrado pelo nome 'postgres'"
fi

if docker ps --format '{{.Names}}' | grep -q 'rabbit'; then
  echo "OK: container RabbitMQ em execução"
else
  echo "AVISO: container RabbitMQ não encontrado pelo nome contendo 'rabbit'"
fi

# ------------------------------------------------------------
# Subir Backend FastAPI
# ------------------------------------------------------------
print_header "3. Subindo backend FastAPI"

if port_open "$BACKEND_PORT"; then
  echo "OK: porta $BACKEND_PORT já está em uso. Considerando backend já iniciado."
else
  cd "$BACKEND_DIR"
  # shellcheck disable=SC1090
  source "$BACKEND_VENV"

  nohup uvicorn app.main:app \
    --host "$BACKEND_HOST" \
    --port "$BACKEND_PORT" \
    --reload \
    > "$LOG_DIR/saas-backend.log" 2>&1 &

  echo $! > "$PID_DIR/saas-backend.pid"
  echo "Backend iniciado. PID: $(cat "$PID_DIR/saas-backend.pid")"
fi

if wait_http "http://localhost:${BACKEND_PORT}/health"; then
  echo "OK: backend respondeu em /health"
else
  echo "ERRO: backend não respondeu em /health"
  echo "Log: $LOG_DIR/saas-backend.log"
  exit 1
fi

# ------------------------------------------------------------
# Subir Worker Speech-AI
# ------------------------------------------------------------
print_header "4. Subindo worker Speech-AI"

if pgrep -f "platform/tap-runtime/workers/speech-ai-worker/worker.py" >/dev/null 2>&1; then
  echo "OK: worker Speech-AI já está em execução"
else
  cd "$WORKER_DIR"
  # shellcheck disable=SC1090
  source "$BACKEND_VENV"

  export DATABASE_URL="$WORKER_DATABASE_URL"
  export RABBITMQ_URL="$RABBITMQ_URL"
  export SAAS_BACKEND_ROOT="$BACKEND_DIR"

  nohup python worker.py \
    > "$LOG_DIR/speech-ai-worker.log" 2>&1 &

  echo $! > "$PID_DIR/speech-ai-worker.pid"
  echo "Worker iniciado. PID: $(cat "$PID_DIR/speech-ai-worker.pid")"
fi

sleep 2

if pgrep -f "platform/tap-runtime/workers/speech-ai-worker/worker.py" >/dev/null 2>&1; then
  echo "OK: worker Speech-AI ativo"
else
  echo "ERRO: worker Speech-AI não iniciou"
  echo "Log: $LOG_DIR/speech-ai-worker.log"
  exit 1
fi

# ------------------------------------------------------------
# Exibir URLs e comandos úteis
# ------------------------------------------------------------
print_header "5. Ambiente TAPOS iniciado"

echo "Backend:  http://localhost:${BACKEND_PORT}"
echo "Swagger:  http://localhost:${BACKEND_PORT}/docs"
echo "OpenAPI:  http://localhost:${BACKEND_PORT}/openapi.json"
echo "UI:       http://localhost:${BACKEND_PORT}/ui/"
echo
echo "Observação: http://localhost/ui/ só funcionará se existir proxy na porta 80."
echo
echo "Logs:"
echo "  Backend: $LOG_DIR/saas-backend.log"
echo "  Worker:  $LOG_DIR/speech-ai-worker.log"
echo
echo "PIDs:"
echo "  Backend: $PID_DIR/saas-backend.pid"
echo "  Worker:  $PID_DIR/speech-ai-worker.pid"
echo
echo "Comando rápido para testar login:"
echo "curl -i -X POST http://localhost:${BACKEND_PORT}/auth/login -H 'Content-Type: application/json' -d '{\"email\":\"admin@tapos.local\",\"password\":\"admin123\"}'"
echo
