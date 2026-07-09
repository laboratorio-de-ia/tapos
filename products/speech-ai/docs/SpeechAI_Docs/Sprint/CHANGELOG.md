# Changelog

All notable changes to the Speech AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - Sprint 9 Release

### Added
- **Provider Factory Architecture**: Introduced `ProviderFactory`, `ProviderRegistry`, and `BaseProvider` to decouple the TTS engine from core logic.
- **Edge Provider Integration**: Fully abstracted `edge-tts` implementation behind the new provider interface.
- **Voice Profiles**: Externalized voice configurations to `config/voices.json`, supporting detailed attributes (rate, pitch, volume, style).
- **Speech Intelligence Engine**: Added intelligent language detection and voice selection based on input text analysis.
- **Domain Models**: Introduced `Presentation`, `Slide`, `SpeechProfile`, and `Statistics` models for robust state management.

### Changed
- Refactored `SpeechAIApp` to act purely as an orchestrator, moving business logic to specific pipeline components.
- Upgraded `TextAnalyzer` to support robust regex-based slide detection.
- Improved logging format and output structure.

### Fixed
- Addressed issues with long sentence processing by implementing `_break_long_sentence()` in `NarrationBuilder`.
- Fixed whitespace normalization bugs in raw text input.

## [0.8.0] - Sprint 8.5

### Added
- Initial implementation of `TextAnalyzer` with basic slide parsing.
- Statistics calculation (word count, estimated duration).

### Changed
- Moved text normalization logic into a dedicated pipeline stage.

## [0.6.0] - Sprint 6.3

### Added
- Centralized `SpeechAIApp` class for application bootstrapping.
- `ConfigManager` for reading `settings.json`.

### Fixed
- Basic integration with `edge-tts` stabilized.
