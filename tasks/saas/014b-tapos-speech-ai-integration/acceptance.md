# Acceptance — Task 014B

## Functional

- POST /products/speech-ai/run executa a facade do speech-ai
- endpoint exige autenticação JWT
- endpoint exige subscription ativa para speech-ai

---

## Validation

### 1. Login

POST /auth/login

### 2. Garantir subscription de speech-ai

POST /subscriptions
{
  "product_slug": "speech-ai"
}

### 3. Executar speech-ai

POST /products/speech-ai/run
Authorization: Bearer <TOKEN>

---

## Expected

{
  "status": "executed",
  "input_file": "...",
  "narration_file": "...",
  "speech_file": "...",
  "audio_file": "...",
  "provider": "...",
  "voice": "...",
  "language": "..."
}

---

## Definition of Done

- rota criada no backend TAPOS
- speech-ai chamado via facade
- execução validada ponta a ponta
