#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://localhost:8000"
EMAIL="teste2@tecle.com"
PASSWORD="123456"

print_step() {
  echo
  echo "=== $1 ==="
}

extract_token() {
  python3 -c 'import json,sys; data=json.load(sys.stdin); print(data.get("access_token",""))'
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

echo "$LOGIN_RESPONSE"

TOKEN=$(echo "$LOGIN_RESPONSE" | extract_token)

if [ -z "$TOKEN" ]; then
  echo "❌ token não gerado"
  exit 1
fi

# -----------------------------------------
# 3. Subscription
# -----------------------------------------
print_step "3. Garantir subscription"

curl -s -X POST "$BASE_URL/subscriptions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_slug":"speech-ai"}'
echo

# -----------------------------------------
# 4. Access (CORRIGIDO)
# -----------------------------------------
print_step "4. Validar acesso"

ACCESS_RESPONSE=$(curl -s "$BASE_URL/products/speech-ai/access" \
  -H "Authorization: Bearer $TOKEN")

echo "$ACCESS_RESPONSE"

echo "$ACCESS_RESPONSE" | python3 -c '
import json, sys
data = json.load(sys.stdin)
assert data.get("access") == True, "Acesso inválido"
print("✅ acesso OK")
'

# -----------------------------------------
# 5. Run speech-ai
# -----------------------------------------
print_step "5. Executar speech-ai"

RUN_RESPONSE=$(curl -s -X POST "$BASE_URL/products/speech-ai/run" \
  -H "Authorization: Bearer $TOKEN")

echo "$RUN_RESPONSE"

# -----------------------------------------
# 6. Validar resposta
# -----------------------------------------
print_step "6. Validar execução"

echo "$RUN_RESPONSE" | python3 -c '
import json, sys
from pathlib import Path

data = json.load(sys.stdin)

assert data["status"] == "executed"

for field in ["input_file","narration_file","speech_file","audio_file"]:
    assert field in data, f"campo faltando: {field}"
    assert Path(data[field]).exists(), f"arquivo não existe: {data[field]}"

print("✅ execução speech-ai OK")
'

# -----------------------------------------
# 7. Sem token
# -----------------------------------------
print_step "7. Teste sem token"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "$BASE_URL/products/speech-ai/run")

echo "$STATUS"

[ "$STATUS" = "401" ] && echo "✅ proteção OK" || {
  echo "❌ esperado 401"
  exit 1
}

echo
echo "🚀 ✅ TASK 014B COMPLETA"