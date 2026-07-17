# Speech-AI — Pipeline

O pipeline de produção (idêntico nos dois pontos de entrada — ver [architecture.md](architecture.md)) segue cinco etapas:

## 1. Texto de entrada — análise

`pipeline/text_analyzer.py::TextAnalyzer`:
- `load()` — lê o arquivo definido em `cfg.script_file`.
- `normalize()` — limpeza de espaços em branco via regex.
- `detect_slides()` — divide o texto por ocorrências de `slide\s+\d+` (regex).
- `parse_slide()` — constrói `Slide` → `Paragraph` / `ListBlock` para cada bloco.
- `calculate_statistics()` — gera `Statistics` (palavras, sentenças, parágrafos, caracteres, minutos estimados).
- `run()` retorna um `Presentation` completo.

## 2. Speech Intelligence

`services/speech_intelligence.py::SpeechIntelligenceEngine.build_profile(presentation)` encadeia:

1. `LanguageDetector.detect()` → `Language` (pt/en/es/fr)
2. `VoiceSelector.select()` → perfil de voz padrão para o idioma detectado
3. `SpeechAnalyzer.analyze()` → `SpeechAnalysis` (métricas linguísticas)
4. `TimingCalculator.calculate()` → ritmo de leitura recomendado (WPM)
5. `SpeechOptimizer.optimize()` → `SpeechProfile` final (rate/pitch/pacing/confidence)

Ver [components.md](components.md) para o detalhe de cada serviço.

## 3. Construção da narração

`pipeline/narration_builder.py::NarrationBuilder` transforma o `Presentation` em texto de narração natural (quebra sentenças longas, insere pausas "..."), exportado como `narration.txt`.

## 4. Construção do texto de fala

`pipeline/speech_builder.py::SpeechBuilder` limpa e naturaliza o texto por idioma, produzindo o texto pronto para TTS, exportado como `speech.txt`.

## 5. Síntese

`services/speech_service.py::SpeechService.synthesize()`:
- lê o arquivo de texto de fala;
- chama `providers/provider_factory.py::ProviderFactory.create_from_speech_profile(speech_profile)` para obter o provedor de TTS configurado;
- envolve o provedor em `services/tts_engine.py::TTSEngine`;
- chama `.generate()`, que produz o arquivo de áudio final (`audio.mp3`).

## Pipeline experimental paralelo (não conectado à produção)

Existe um segundo pipeline, mais avançado, em `services/text_engines/`: Lexical → Clause → SpeechBlock → PausePlanner → SSML, capaz de gerar SSML real (`<speak>`, `<prosody>`, `<break>`). Ele **não está conectado ao fluxo de produção** — só é exercitado por um script manual de teste (`input/teste.py`). É a semente de um futuro pipeline de SSML real, atualmente fora do caminho síncrono/assíncrono usado pela TAPOS. Ver [roadmap.md](roadmap.md).

## Ver também

- [components.md](components.md) — inventário de módulos
- [models.md](models.md) — as estruturas de dados que atravessam cada etapa
- [outputs.md](outputs.md) — os artefatos gerados ao final do pipeline
