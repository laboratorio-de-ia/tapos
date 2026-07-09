# Acceptance — Task 014A

## Functional

- run_speech_ai() executa o pipeline completo
- narration.txt é gerado
- speech.txt é gerado
- audio.mp3 é gerado
- retorno contém status e caminhos dos arquivos

---

## Validation

Executar:

python - <<'PY'
from app.integration.facade import run_speech_ai
result = run_speech_ai()
print(result)
PY

---

## Expected

Retorno semelhante a:

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

- facade criada
- runner criado
- schemas criado
- chamada programática validada
