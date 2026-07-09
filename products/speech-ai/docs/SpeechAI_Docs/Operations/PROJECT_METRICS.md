# Project Metrics

## 1. Overview

This document outlines the key performance indicators (KPIs) and operational metrics used to evaluate the health, efficiency, and quality of the Speech AI platform.

## 2. Operational Metrics

These metrics are essential for monitoring the system's performance in a production environment.

| Metric | Description | Target / Threshold |
| :--- | :--- | :--- |
| **Processing Latency** | The total time taken from reading the input script to saving the final audio file. | Dependent on text length; monitor for unusual spikes indicating provider latency. |
| **Provider Error Rate** | The percentage of failed requests to external TTS providers (e.g., HTTP 5xx or 4xx errors). | < 1% |
| **Pipeline Success Rate** | The percentage of input scripts successfully converted into audio files without internal application errors. | > 99% |

## 3. Code Quality Metrics

These metrics are tracked during the development lifecycle to ensure the codebase remains maintainable.

| Metric | Description | Current Status (Sprint 9) |
| :--- | :--- | :--- |
| **Code Volume** | Total lines of Python code, excluding comments and blank lines. | ~4,289 lines across 44 files. |
| **Test Coverage** | The percentage of code executed by the automated test suite. | *To be measured via `coverage.py`* |
| **Static Analysis Score** | Code quality score determined by linters (e.g., Pylint, Flake8). | *To be integrated in CI/CD* |

## 4. Domain Metrics

These metrics are calculated internally by the `TextAnalyzer` and `SpeechIntelligenceEngine` for each processed script. They provide insight into the workload characteristics.

-   **Total Words / Characters**: Measures the volume of text processed.
-   **Estimated Duration**: The calculated audio length based on the text volume and selected voice profile's Words Per Minute (WPM).
-   **Language Distribution**: Tracking the frequency of different languages processed (e.g., 60% English, 30% Portuguese, 10% Spanish) helps prioritize future voice profile tuning.
