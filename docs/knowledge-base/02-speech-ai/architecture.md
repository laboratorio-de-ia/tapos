# Speech-AI — Arquitetura

## Camadas

```
app/                 → orquestrador standalone (uso via `python main.py`)
  ↓
pipeline/            → texto bruto → modelo de domínio (Presentation/Slide/Paragraph)
  ↓
services/            → Speech Intelligence + orquestração de síntese
  ↓
providers/           → abstração de motor de TTS (hoje: Edge TTS)
  ↓
models/              → dataclasses de domínio compartilhadas por todas as camadas
  ↓
config/              → settings.json + voices.json, carregados por ConfigManager
```

`config.config_manager.ConfigManager` é construído uma vez e passado adiante para `TextAnalyzer`, `NarrationBuilder` e `SpeechBuilder`; internamente ele possui um `VoiceManager` (`services/voice_manager.py`), carregado a partir de `config/voices.json`.

## Pontos de entrada

Existem dois caminhos de entrada que convergem para o mesmo pipeline:

1. **Standalone**: `main.py` → `app/speech_ai_app.py::SpeechAIApp.run()` — usado para execução manual/local.
2. **Integração TAPOS**: `integration/cli.py` → `integration/facade.py::run_speech_ai()` → `integration/runner.py::execute_current_pipeline()` — usado pelo backend SaaS via subprocesso (`platform/saas-backend/app/products/speech_ai_adapter.py`).

Ambos chamam exatamente a mesma sequência: `TextAnalyzer.run()` → `SpeechIntelligenceEngine.build_profile()` → `NarrationBuilder` → `SpeechBuilder` → `SpeechService.synthesize()` — mas a lógica está duplicada entre `app/speech_ai_app.py` e `integration/runner.py`, não compartilhada em uma única função.

## Duplicação encontrada: dois diretórios `integration/`

Existem **dois** diretórios de integração: `products/speech-ai/integration/` (raiz do produto: `facade.py`, `runner.py`, `schemas.py`, `cli.py`) e `products/speech-ai/app/integration/` (`facade.py`, `runner.py`, `schemas.py` — sem `cli.py`). Os dois são quase idênticos (o de `app/` tem pequenas diferenças de docstring e de cálculo de `project_root`). Confirmado em `platform/saas-backend/app/products/speech_ai_adapter.py` que **apenas o `integration/` de nível raiz está conectado à TAPOS** — `app/integration/` é código morto, resquício de uma refatoração que moveu a integração para fora de `app/`. Deve ser removido em uma limpeza futura.

## Diagrama de dependências (resumo)

```
TAPOS backend (adapter)
  → subprocess: .venv do speech-ai + integration/cli.py
    → integration/facade.py
      → integration/runner.py
        → pipeline/text_analyzer.py      (Presentation)
        → services/speech_intelligence.py (SpeechProfile)
        → pipeline/narration_builder.py   (narration.txt)
        → pipeline/speech_builder.py      (speech.txt)
        → services/speech_service.py
          → providers/provider_factory.py → providers/edge_provider.py
```

## Ver também

- [pipeline.md](pipeline.md) — detalhamento passo a passo do fluxo de processamento
- [components.md](components.md) — inventário de cada módulo
- [execution-engine.md](execution-engine.md) — como este pipeline é acionado de forma síncrona e assíncrona pela TAPOS
