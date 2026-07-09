# Product Roadmap

## Vision

To provide the most flexible, intelligent, and scalable Text-to-Audio enterprise pipeline, enabling automated generation of high-quality narrations, presentations, and accessibility features across multiple languages and voice providers.

## Phase 1: Foundation & Intelligence (Completed)

The initial phase focused on establishing a robust, modular pipeline capable of intelligent text analysis and basic audio synthesis.

| Milestone | Key Features | Status |
| :--- | :--- | :--- |
| **Core Pipeline** | Text normalization, slide detection, domain models (`Presentation`). | ✅ Completed |
| **Speech Intelligence** | Automatic language detection, pacing calculation, dynamic voice profile selection. | ✅ Completed |
| **Provider Abstraction** | Implementation of the Factory pattern, decoupling the core engine from `edge-tts`. | ✅ Completed |

## Phase 2: Enterprise Integrations (Current Focus)

The current phase aims to expand the capabilities of the platform by integrating premium, commercial TTS engines to offer higher quality and varied voice styles.

| Milestone | Key Features | Target |
| :--- | :--- | :--- |
| **Azure Integration** | Full support for Azure Cognitive Services TTS, including advanced SSML features and neural voices. | Q3 2026 |
| **OpenAI Integration** | Integration with OpenAI's TTS API for ultra-realistic conversational voices. | Q3 2026 |
| **Plugin System** | Allow third-party developers to drop in custom provider modules without modifying core code. | Q4 2026 |

## Phase 3: Accessibility & Interfaces (Future)

The final planned phase transitions the tool from a backend CLI utility to a fully accessible service.

| Milestone | Key Features | Target |
| :--- | :--- | :--- |
| **REST API** | Development of a FastAPI-based RESTful interface for programmatic integration by other enterprise systems. | Q1 2027 |
| **Web Dashboard** | A React-based user interface for uploading scripts, previewing voices, and managing generated audio files. | Q1 2027 |
| **Batch Processing** | Support for asynchronous batch processing of large document repositories using message queues (e.g., Celery/RabbitMQ). | Q2 2027 |
