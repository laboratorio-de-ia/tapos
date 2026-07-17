# Engineering Documentation

## 1. Executive Summary

Speech AI is a robust, Python-based application designed to convert textual scripts into synthesized audio using advanced TTS (Text-to-Speech) engines. Built on modern software engineering principles, the solution prioritizes modularity, scalability, and maintainability. By utilizing a pipeline architecture and dependency injection concepts, the system ensures that components such as text analysis, speech intelligence, and audio synthesis remain decoupled.

## 2. System Components

The application is divided into several cohesive modules:

### 2.1. App Kernel (`app/`)
The `SpeechAIApp` class serves as the orchestrator. It initializes configurations, sets up logging, and executes the pipeline sequentially, ensuring data flows correctly from input to the final audio file.

### 2.2. Configuration Management (`config/`)
Centralized configuration handling using `ConfigManager`.
- `settings.json`: Defines input/output paths, default TTS provider, and speech pause parameters.
- `voices.json`: Contains detailed voice profiles mapping languages and locales to specific neural voices (e.g., `en-US-GuyNeural`, `pt-BR-FranciscaNeural`).

### 2.3. Data Models (`models/`)
Rich domain models that encapsulate the state of the processing:
- `Presentation` & `Slide`: Represents the structured format of the input script.
- `SpeechProfile`: The output of the intelligence engine, dictating how the text should be read (rate, pitch, volume, voice).
- `Statistics`: Tracks word count, characters, and estimated duration.

### 2.4. Processing Pipeline (`pipeline/`)
The core transformation stages:
- **TextAnalyzer**: Reads raw text, normalizes whitespace, detects slide boundaries, and parses content into the `Presentation` model.
- **NarrationBuilder**: Formats the text for human reading, inserting breaks for long sentences.
- **SpeechBuilder**: Prepares the text specifically for TTS engines, handling SSML tags or specific pause markers.

### 2.5. Intelligence & Services (`services/`)
The brain of the application:
- **SpeechIntelligenceEngine**: Orchestrates language detection, voice selection, and timing calculations to build an optimized `SpeechProfile`.
- **SpeechService**: The facade that interacts with the TTS providers to synthesize the audio.

### 2.6. Provider Layer (`providers/`)
An extensible layer for external integrations:
- **ProviderFactory & Registry**: Implements the Factory pattern to instantiate the correct TTS provider based on configuration.
- **EdgeProvider**: The current concrete implementation utilizing the `edge-tts` library to interface with Microsoft's Edge TTS API.

## 3. Technology Stack

- **Language**: Python 3.10+
- **Core Libraries**: 
  - `edge-tts`: Audio synthesis
  - `langdetect`: Language identification
  - `rich`: Console formatting
  - `python-dotenv`: Environment variable management
- **Architecture Patterns**: Pipeline, Factory, Facade, Dependency Injection.

## 4. Engineering Principles Applied

1. **Separation of Concerns (SoC)**: Each module has a single responsibility. The `TextAnalyzer` only parses text, while the `SpeechService` only generates audio.
2. **Open/Closed Principle**: The provider layer is open for extension (adding new TTS engines) but closed for modification.
3. **Configuration over Code**: Behavior is driven by JSON files, reducing the need for code changes when adding new voices or adjusting parameters.
4. **Graceful Degradation**: Robust error handling during file I/O and external API calls.
