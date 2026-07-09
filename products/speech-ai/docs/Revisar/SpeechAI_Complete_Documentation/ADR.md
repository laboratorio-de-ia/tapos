# Architecture Decision Records (ADR)

This document captures the significant architectural decisions made during the development of the Speech AI platform.

## ADR 001: Use of Python for the Core Pipeline

**Date**: Sprint 1
**Status**: Accepted

**Context**: The system requires rapid prototyping, extensive string manipulation, and integration with various AI and TTS APIs.
**Decision**: Python 3.10+ was chosen as the primary programming language.
**Consequences**: Python offers excellent libraries for text processing (`re`, `langdetect`) and easy integration with external APIs. However, performance bottlenecks in pure text processing must be monitored, though I/O (network calls to TTS providers) will be the primary latency source.

## ADR 002: JSON-Based Configuration Management

**Date**: Sprint 3
**Status**: Accepted

**Context**: The application needs to support multiple voice profiles, languages, and tuning parameters without requiring code recompilation.
**Decision**: We implemented a `ConfigManager` that reads from `settings.json` and `voices.json`.
**Consequences**: This decouples configuration from code, allowing operational teams to tweak voice parameters or add new voices simply by updating JSON files. It requires strict validation of the JSON schema upon application startup.

## ADR 003: Provider Factory Pattern for TTS Engines

**Date**: Sprint 9
**Status**: Accepted

**Context**: Initially, the system was tightly coupled to the `edge-tts` library. As enterprise requirements grow, we need to support Azure, OpenAI, and AWS Polly.
**Decision**: Implement a `ProviderFactory` and `ProviderRegistry`. The core pipeline interacts only with a generic `SpeechService` interface.
**Consequences**: Adding a new provider now only requires implementing the `BaseProvider` interface and registering it. The core logic remains untouched, adhering to the Open/Closed Principle.

## ADR 004: Domain Models for Presentation State

**Date**: Sprint 7
**Status**: Accepted

**Context**: Passing raw strings or nested dictionaries between pipeline stages (Analyzer -> Intelligence -> Builder) became error-prone and difficult to debug.
**Decision**: Create explicit domain models: `Presentation`, `Slide`, `Paragraph`, and `SpeechProfile`.
**Consequences**: Increases initial boilerplate code but vastly improves type safety, readability, and encapsulation of logic (e.g., calculating word counts is now a method of the domain model, not a standalone utility function).
