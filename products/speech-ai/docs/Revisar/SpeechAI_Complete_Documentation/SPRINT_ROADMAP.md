# Sprint Roadmap

## Overview

The Speech AI project is developed using an iterative, agile approach. This document outlines the historical progression of the project up to the current release, and the immediate focus for upcoming sprints.

## Historical Sprints (Foundation Phase)

### Sprints 1-5: Core Platform Initialization
- **Goal**: Establish the basic pipeline for text-to-speech conversion.
- **Key Deliverables**:
  - Basic `TextAnalyzer` for parsing scripts.
  - Integration with `edge-tts` for audio synthesis.
  - Initial configuration management (`settings.json`).
  - Basic logging and error handling.

### Sprints 6-8: Intelligence and Modularity
- **Goal**: Introduce "Speech Intelligence" and prepare the architecture for multiple providers.
- **Key Deliverables**:
  - **Sprint 6.3**: Refactoring of the application kernel (`SpeechAIApp`) to centralize orchestration.
  - **Sprint 7.x**: Introduction of domain models (`Presentation`, `Slide`, `SpeechProfile`).
  - **Sprint 8.5**: Advanced `TextAnalyzer` with robust slide detection and statistics calculation. Implementation of the `SpeechIntelligenceEngine` for dynamic language detection and voice selection.

### Sprint 9: Dependency Injection & Provider Abstraction (Current Focus)
- **Goal**: Completely decouple the TTS engine from the core application logic.
- **Key Deliverables**:
  - Implementation of `ProviderFactory` and `ProviderRegistry`.
  - Abstraction of `EdgeProvider` behind a common interface.
  - Voice profiles externalized to `voices.json`.

## Upcoming Sprints (Expansion Phase)

### Sprint 10: Multi-Provider Integration
- **Goal**: Add support for premium enterprise TTS providers.
- **Planned Features**:
  - Integration with Azure Cognitive Services (Speech).
  - Integration with OpenAI TTS.
  - Fallback mechanisms between providers.

### Sprint 11: Web UI and API Interface
- **Goal**: Move beyond CLI execution to provide web-based accessibility.
- **Planned Features**:
  - RESTful API (FastAPI) for programmatic access.
  - Simple Web UI for uploading scripts and downloading audio.

### Sprint 12: Enterprise Packaging & Deployment
- **Goal**: Prepare the solution for cloud-native deployment.
- **Planned Features**:
  - Dockerization of the application.
  - CI/CD pipeline setup (GitHub Actions).
  - Kubernetes deployment manifests.
