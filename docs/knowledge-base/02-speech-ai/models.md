# Speech-AI — Modelos de Dados

Todos em `models/`, majoritariamente `@dataclass` simples (alguns com `slots=True`, um `frozen=True`) — sem Pydantic.

| Modelo | Descrição |
|---|---|
| `language.py::Language` (frozen, slots) | `code, locale, name, confidence` + propriedades `is_portuguese/is_english/is_spanish/is_french`. Produzido por `LanguageDetector`. |
| `voice_profile.py::VoiceProfile` (slots) | Configuração completa de voz TTS: `profile_id, provider, language, locale, voice, name, description, rate, pitch, volume, style, role, gender, is_default`. Carregado de `config/voices.json` por `VoiceManager`. |
| `speech_profile.py::SpeechProfile` | O "contrato" final para síntese: `language, voice, locale, provider, rate, pitch, volume, recommended_wpm, reading_style, pacing, complexity, confidence, estimated_minutes`. Produzido por `SpeechOptimizer`, consumido por `SpeechService`/`ProviderFactory`. |
| `speech_analysis.py::SpeechAnalysis` | Resultado intermediário de análise linguística (palavras/sentenças/parágrafos/complexidade/estilo de leitura/WPM recomendado etc.), produzido por `SpeechAnalyzer`, refinado por `TimingCalculator`. |
| `presentation.py::Presentation` (slots) | Container de topo do documento: `title, slides: list[Slide], statistics: Statistics`; métodos `add_slide`, `to_text()` (achata tudo para detecção de idioma/análise), `summary()`. |
| `slide.py::Slide` | `number, title, paragraphs: list[Paragraph], lists: list[ListBlock]`; helpers `add_paragraph`/`add_list`. |
| `paragraph.py::Paragraph` | `text, slide_index, importance` (1=normal/2=importante/3=destaque — este campo não é usado em nenhuma lógica atual do pipeline; provável reserva para ênfase futura em SSML). |
| `list_block.py::ListBlock` | `items: list[str], slide_index`. |
| `statistics.py::Statistics` (slots) | `characters, words, sentences, paragraphs, estimated_minutes` + propriedades derivadas (`estimated_seconds`, `words_per_sentence`, `characters_per_word`). |
| `clause.py::Clause` (slots) + `ClauseType` | Enum MAIN/SUBORDINATE/ENUMERATION/INTRODUCTION/CONCLUSION/UNKNOWN — pertence ao pipeline experimental `text_engines/`, ainda não conectado à produção; docstring já lista consumidores futuros ("StorytellingEngine", "EmotionEngine") que ainda não existem no repositório. |

## Fluxo de transformação

```
Texto bruto → Presentation (Slide[Paragraph, ListBlock], Statistics)
            → Language (via LanguageDetector)
            → SpeechAnalysis (via SpeechAnalyzer)
            → SpeechProfile (via TimingCalculator + SpeechOptimizer, usando VoiceProfile)
```

## Ver também

- [pipeline.md](pipeline.md) — onde cada modelo é produzido/consumido
- [configuration.md](configuration.md) — origem dos dados de `VoiceProfile`
