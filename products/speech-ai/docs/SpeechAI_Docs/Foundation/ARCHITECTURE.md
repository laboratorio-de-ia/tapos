# Architecture Overview

## 1. Architectural Style

Speech AI utilizes a **Pipes and Filters** architectural style combined with a **Layered Architecture**. This ensures that data flows through distinct transformation stages while maintaining clear boundaries between core logic, external services, and configuration.

## 2. High-Level Architecture Diagram

```text
+-------------------+       +-------------------+       +-------------------+
|   Input Source    | ----> |   Text Analyzer   | ----> | Presentation Model|
|   (script.txt)    |       |   (Normalization) |       | (Slides, Stats)   |
+-------------------+       +-------------------+       +-------------------+
                                                              |
                                                              v
+-------------------+       +-------------------+       +-------------------+
|   Speech Profile  | <---- |Speech Intelligence| <---- |  Speech & Narration|
| (Voice, Rate, etc)|       | (Lang, Voice, Opt)|       |      Builders     |
+-------------------+       +-------------------+       +-------------------+
        |
        v
+-------------------+       +-------------------+       +-------------------+
|   Speech Service  | ----> | Provider Factory  | ----> |   Edge Provider   |
|   (Orchestrator)  |       |    & Registry     |       |   (edge-tts API)  |
+-------------------+       +-------------------+       +-------------------+
                                                              |
                                                              v
                                                        +-------------------+
                                                        |    Audio Output   |
                                                        |       (.mp3)      |
                                                        +-------------------+
```

## 3. Core Layers

### 3.1. Orchestration Layer (`app.py`, `speech_ai_app.py`)
Responsible for bootstrapping the application, loading configurations, and coordinating the sequence of operations. It holds the `ConfigManager` and passes state between the pipeline stages.

### 3.2. Pipeline Layer (`pipeline/`)
Handles data transformation. The input text is inherently unstructured. This layer structures it into domain models (`Presentation`, `Slide`, `Paragraph`) and then transforms it back into specialized text formats (`narration.txt`, `speech.txt`) optimized for synthesis.

### 3.3. Intelligence Layer (`services/speech_intelligence.py`)
This layer adds cognitive capabilities to the pipeline. It doesn't just pass text to a synthesizer; it:
- Detects the language (`LanguageDetector`).
- Selects the most appropriate voice profile (`VoiceSelector`).
- Analyzes text complexity (`SpeechAnalyzer`).
- Calculates pacing and pauses (`TimingCalculator`).
- Produces a final `SpeechProfile` that acts as the contract for the TTS engine.

### 3.4. Infrastructure / Provider Layer (`providers/`)
Isolates external dependencies. By using a `ProviderFactory`, the system can dynamically load the required TTS engine (currently Edge TTS) without hardcoding dependencies in the `SpeechService`. This is critical for future scalability (e.g., adding Azure, AWS Polly, or OpenAI TTS).

## 4. Data Flow Sequence

1. **Initialization**: `SpeechAIApp` loads `settings.json` and `voices.json`.
2. **Ingestion**: `TextAnalyzer` reads `script.txt`.
3. **Parsing**: Text is split into logical slides and paragraphs. Statistics (words, estimated time) are calculated.
4. **Intelligence**: `SpeechIntelligenceEngine` analyzes the presentation, detects language, and assigns a `SpeechProfile`.
5. **Formatting**: `NarrationBuilder` and `SpeechBuilder` create optimized text artifacts.
6. **Synthesis**: `SpeechService` receives the optimized text and `SpeechProfile`, requests a provider instance from `ProviderFactory`, and triggers audio generation.
7. **Output**: The provider streams the synthesized audio to an `.mp3` file in the `output/` directory.

## 5. Architectural Decisions (Summary)
- **JSON Configuration**: Chosen for ease of modification by non-developers.
- **Provider Abstraction**: Essential for avoiding vendor lock-in with TTS services.
- **Rich Domain Models**: Using classes like `Presentation` and `Slide` instead of raw dictionaries improves type safety and encapsulates business logic (like word counting).
