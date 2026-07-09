# Speech-AI

## Visão Geral

Speech-AI é o primeiro produto integrado à plataforma TAPOS.

O produto recebe conteúdo textual, executa a pipeline de análise e inteligência de fala e gera arquivos de saída como:

- narration.txt
- speech.txt
- audio.mp3

---

# Estrutura

```text
products/
└── speech-ai/
    ├── app/
    ├── config/
    ├── input/
    ├── integration/
    ├── output/
    ├── pipeline/
    ├── providers/
    ├── services/
    ├── .env
    ├── .venv
    └── main.py
```

---

# Pré-requisitos

- Python 3.14+
- Ambiente virtual configurado
- Dependências instaladas

---

# Ativação do ambiente

```bash
cd /workspace/tecle/products/speech-ai

source .venv/bin/activate
```

---

# Teste Standalone

Executa o produto diretamente sem passar pela TAPOS.

## Executar

```bash
python main.py
```

## Resultado esperado

Arquivos gerados:

```text
output/
├── narration.txt
├── speech.txt
└── *.mp3
```

Exemplo:

```text
Audio_*overnance_SouthAmerica.mp3
```

--*

# Teste da Facade (Task 014A)

E*ecuta a camada de integração criad* para o produto.

## Executar

```*ash
python integration/cli.py
```
*## Resultado esperado

Retorno JSO*:

```json
{
  "status": "executed*,
  "input_file": "...",
  "*arration_file": "...",
  "*peech_file": "...",
  "audio_file"* "...",
  "*rovider": "edge",
  "voice": "pt-B*-FranciscaNeural",
  "language": "*t"
}
```

---

#*Teste Integrado com TAPOS (Task 01*B)

Valida o fluxo completo:

```t*xt
Usuário
 ↓*JWT
 ↓
Subscription
 ↓
Gateway TAP*S
 ↓
Speech-AI
 ↓
Á*dio*```

---

## Subir Backend TAPOS

*``bash
*d /workspace/tecle*platform/saas-backend

source .ven*/bin/activate

export DATABASE_URL*postgresql+psycopg2://admin:admin@*ocalhost:5432/platform
export SECR*T_KEY="tapos-dev-secret-key"

uvic*rn app.main:app*--host 0.0.0.0 --port 8000 --reloa*
```

---

## Executar teste integ*ado

```bash
cd /workspace/tecle

*/test_auth.sh
*``

---

## Resultado esperado

``*text
✅ login
✅ subscription
✅ auth*rization
✅ execução speech-ai
✅ pr*teção 401

🚀 ✅ TASK 014B COMPLETA*```

---

# Saídas Geradas

Arquiv*s de saída ficam em:

```text
prod*cts/speech-ai/output/
```

Exemplo*

```text
narration.txt
speech.txt*Audio_Governance_SouthAmerica.mp3
*``

---

# Integração com TAPOS

A*ualmente a integração ocorre via:
*```text
TAPOS
 ↓
speech_ai_adapter*py
 ↓
subprocess
 ↓
speech-ai/.ven*
 ↓
integration/cli.py
 ↓
facade.p*
 ↓
runner.py
 ↓
pipeline real
```*
---

# Estado Atual

## Plataform* TAPOS

- Auth ✅
- Products ✅
- Su*scriptions ✅
- Authorization ✅
- G*teway ✅

## Speech-AI

- Pipeline *LP ✅
- Speech Intelligence ✅
- TTS*✅
- Audio Generation ✅

## Integra*ão

- Task 014A ✅
- Task 014B ✅

-*-

# Próxima Evolução

Task 015:

*``text
Request
 ↓
RabbitMQ
 ↓
Work*r
 ↓
Speech-AI
 ↓
Resultado
```

O*jetivo:

- Execução assíncrona
- E*calabilidade
- Desacoplamento
- Pr*dução








Acessar o diretório abaixo com toda a documentação do projeto

https://github.com/laboratorio-de-ia/Speech-AI/tree/main/docs/SpeechAI_Docs


