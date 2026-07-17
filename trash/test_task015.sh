#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://localhost:8000"
EMAIL="teste2@tecle.com"
PASSWORD="123456"
NOSUB_EMAIL="nosub_task015@tecle.com"
NOSUB_PASSWORD="123456"

WORKER_DIR="/workspace/tecle/platform/tap-runtime/workers/speech-ai-worker"
WORKER_VENV="/workspace/tecle/platform/saas-backend/.venv/bin/activate"

print_step() {
  echo
  echo "=== $1 ==="
}

extract_field() {
  python3 -c "import json,sys; print(json.load(sys.stdin).get('$1',''))"
}

# -----------------------------------------
# 1. Health
# -----------------------------------------
print_step "1. Healthcheck"
curl -s "$BASE_URL/health"
echo

# -----------------------------------------
# 2. Login
# -----------------------------------------
print_step "2. Login"

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")

TOKEN=$(echo "$LOGIN_RESPONSE" | extract_field access_token)

if [ -z "$TOKEN" ]; then
  echo "❌ token não gerado"
  exit 1
fi
echo "✅ login OK"

# -----------------------------------------
# 3. Subscription
# -----------------------------------------
print_step "3. Garantir subscription"

curl -s -X POST "$BASE_URL/subscriptions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_slug":"speech-ai"}' > /dev/null
echo "✅ subscription OK"

# -----------------------------------------
# 4. Submit assíncrono
# -----------------------------------------
print_step "4. Submeter execução assíncrona"

SUBMIT_RESPONSE=$(curl -s -X POST "$BASE_URL/products/speech-ai/submit" \
  -H "Authorization: Bearer $TOKEN")

echo "$SUBMIT_RESPONSE"

JOB_ID=$(echo "$SUBMIT_RESPONSE" | extract_field job_id)
JOB_STATUS=$(echo "$SUBMIT_RESPONSE" | extract_field status)

if [ -z "$JOB_ID" ]; then
  echo "❌ job_id não gerado"
  exit 1
fi

[ "$JOB_STATUS" = "queued" ] && echo "✅ job criado com status queued" || {
  echo "❌ esperado status=queued"
  exit 1
}

# -----------------------------------------
# 5. Worker processa a fila
# -----------------------------------------
print_step "5. Worker processa a fila"

(
  cd "$WORKER_DIR"
  # shellcheck disable=SC1090
  source "$WORKER_VENV"
  export DATABASE_URL=postgresql://admin:admin@localhost:5432/platform
  export RABBITMQ_URL=amqp://admin:admin@localhost:5672/
  timeout 20 python worker.py || true
)

# -----------------------------------------
# 6. Consultar job até completed
# -----------------------------------------
print_step "6. Consultar status do job"

STATUS="queued"
for i in $(seq 1 10); do
  JOB_RESPONSE=$(curl -s "$BASE_URL/jobs/$JOB_ID" -H "Authorization: Bearer $TOKEN")
  STATUS=$(echo "$JOB_RESPONSE" | extract_field status)
  [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ] && break
  sleep 1
done

echo "$JOB_RESPONSE"

[ "$STATUS" = "completed" ] && echo "✅ job completed" || {
  echo "❌ job não completou (status=$STATUS)"
  exit 1
}

echo "$JOB_RESPONSE" | python3 -c '
import json, sys
from pathlib import Path

data = json.load(sys.stdin)
result = data["result"]

assert result["status"] == "executed"
for field in ["input_file", "narration_file", "speech_file", "audio_file"]:
    assert field in result, f"campo faltando: {field}"
    assert Path(result[field]).exists(), f"arquivo não existe: {result[field]}"

print("✅ outputs do speech-ai OK")
'

# -----------------------------------------
# 7. Fluxo síncrono antigo (014B) continua funcionando
# -----------------------------------------
print_step "7. Validar endpoint síncrono (compatibilidade 014B)"

RUN_RESPONSE=$(curl -s -X POST "$BASE_URL/products/speech-ai/run" \
  -H "Authorization: Bearer $TOKEN")

echo "$RUN_RESPONSE" | python3 -c '
import json, sys
data = json.load(sys.stdin)
assert data["status"] == "executed"
print("✅ endpoint síncrono OK")
'

# -----------------------------------------
# 8. Painel /ui continua acessível
# -----------------------------------------
print_step "8. Validar painel /ui"

UI_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -L "$BASE_URL/ui")
[ "$UI_STATUS" = "200" ] && echo "✅ /ui acessível" || {
  echo "❌ /ui retornou $UI_STATUS"
  exit 1
}

# -----------------------------------------
# 9. Sem token
# -----------------------------------------
print_step "9. Teste sem token"

SUBMIT_NO_TOKEN=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/products/speech-ai/submit")
JOBS_NO_TOKEN=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/jobs/$JOB_ID")

[ "$SUBMIT_NO_TOKEN" = "401" ] && echo "✅ submit sem token protegido" || {
  echo "❌ esperado 401 no submit sem token, obtido $SUBMIT_NO_TOKEN"
  exit 1
}
[ "$JOBS_NO_TOKEN" = "401" ] && echo "✅ jobs sem token protegido" || {
  echo "❌ esperado 401 no jobs sem token, obtido $JOBS_NO_TOKEN"
  exit 1
}

# -----------------------------------------
# 10. Sem subscription
# -----------------------------------------
print_step "10. Teste sem subscription"

curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$NOSUB_EMAIL\",\"password\":\"$NOSUB_PASSWORD\"}" > /dev/null || true

NOSUB_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$NOSUB_EMAIL\",\"password\":\"$NOSUB_PASSWORD\"}" | extract_field access_token)

NOSUB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/products/speech-ai/submit" \
  -H "Authorization: Bearer $NOSUB_TOKEN")

[ "$NOSUB_STATUS" = "403" ] && echo "✅ submit sem subscription bloqueado" || {
  echo "❌ esperado 403 sem subscription, obtido $NOSUB_STATUS"
  exit 1
}

echo
echo "🚀 ✅ TASK 015 COMPLETA"
