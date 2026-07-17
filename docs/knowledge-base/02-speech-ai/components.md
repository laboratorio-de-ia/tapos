# Speech-AI — Componentes

## Pipeline (`pipeline/`)

| Módulo | Responsabilidade |
|---|---|
| `text_analyzer.py::TextAnalyzer` | Texto bruto → `Presentation` (slides/parágrafos/listas/estatísticas) |
| `narration_builder.py::NarrationBuilder` | `Presentation` → texto de narração natural |
| `speech_builder.py::SpeechBuilder` | `Presentation` → texto limpo, pronto para TTS |

## Serviços (`services/`)

| Módulo | Responsabilidade |
|---|---|
| `speech_intelligence.py::SpeechIntelligenceEngine` | Orquestra os 5 sub-passos de inteligência em um `SpeechProfile` |
| `language_detector.py::LanguageDetector` | Detecção de idioma offline (`langdetect`), determinística (seed=0), cache por hash de texto, pt/en/es/fr |
| `voice_selector.py::VoiceSelector` | Escolhe o `VoiceProfile` padrão para um `Language` + provedor configurado, via `VoiceManager` |
| `voice_manager.py::VoiceManager` | Repositório somente-leitura de `VoiceProfile`s, carregado de `config/voices.json` |
| `speech_analyzer.py::SpeechAnalyzer` | Análise linguística baseada em estatística/regex (métricas de palavra/sentença, diversidade lexical, heurísticas de complexidade/estilo/ritmo) → `SpeechAnalysis` |
| `timing_calculator.py::TimingCalculator` | Mapeia faixas de complexidade de sentença para WPM recomendado (com ajuste de -5 WPM para `pt`) |
| `speech_optimizer.py::SpeechOptimizer` | Converte `SpeechAnalysis` + `VoiceProfile` em `SpeechProfile` final; contém o hook no-op `_apply_future_ai_rules()`, reservado para regras de IA futura |
| `text_optimizer.py::TextOptimizer` | Regras de divisão/limpeza de sentença usadas por `SpeechOptimizer.optimize_text()` — este método não parece ser chamado pelo pipeline de produção atual |
| `speech_service.py::SpeechService` | Orquestrador de topo: arquivo de narração + `SpeechProfile` → provedor → arquivo de áudio |
| `tts_engine.py::TTSEngine` | Adaptador fino que chama `provider.generate()`, desacoplando `SpeechService` de classes concretas de provedor |

### `services/text_engines/` — pipeline experimental (não conectado à produção)

| Módulo | Responsabilidade |
|---|---|
| `lexical_analyzer.py::LexicalAnalyzer` | Tokenizador regex (Token/TokenType) — "base para IA futura", sem dependências externas |
| `clause_analyzer.py::ClauseAnalyzer` | Tokens → objetos `Clause` (MAIN/SUBORDINATE/etc.) com estimativas de pausa/confiança |
| `sentence_engine.py::SentenceEngine` | Divisor alternativo de sentenças longas (heurísticas de palavra/vírgula/conector) |
| `speech_block_builder.py::SpeechBlockBuilder` | Agrupa `Clause`s em blocos de fala naturais |
| `pause_planner.py::PausePlanner` | Atribui `estimated_pause_ms` por cláusula, conforme tipo/complexidade/posição |
| `ssml_engine.py::SSMLEngine` | Renderiza `Clause`s em SSML real (`<speak>`, `<prosody>`, `<break>`) |

## Provedores (`providers/`)

Ver [providers.md](providers.md) para o detalhamento completo da abstração.

## Modelos (`models/`)

Ver [models.md](models.md).

## Configuração (`config/`)

Ver [configuration.md](configuration.md).

## Ver também

- [architecture.md](architecture.md) — como estes componentes se conectam
- [pipeline.md](pipeline.md) — a ordem de execução real
