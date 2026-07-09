# Testing Guide

## 1. Testing Strategy

The Speech AI project relies on a comprehensive testing strategy to ensure the reliability of the text-to-audio pipeline. Because the system integrates with external APIs, we separate unit testing of the core logic from integration testing of the providers.

## 2. Test Structure

Tests are located in the `tests/` directory and are organized to mirror the application structure.

-   **Unit Tests**: Focus on isolated components, particularly the domain models (`models/`) and the pipeline logic (`pipeline/`).
-   **Integration Tests**: Verify the interaction between the application and external TTS providers (`providers/`).

## 3. Running Tests

We utilize the standard `unittest` framework provided by Python.

To execute all tests, run the following command from the project root:
```bash
python -m unittest discover -s tests
```

To run a specific test module:
```bash
python -m unittest tests.test_app
```

## 4. Writing Unit Tests

When writing unit tests for pipeline components like `TextAnalyzer` or `SpeechIntelligenceEngine`, adhere to the following principles:

1.  **Mocking Dependencies**: Use `unittest.mock` to isolate the component being tested. For example, when testing the `SpeechIntelligenceEngine`, mock the `LanguageDetector` to return a predictable language code rather than relying on the actual detection algorithm.
2.  **Test Data**: Use the sample scripts provided in the `input/` directory (e.g., `script_pt.txt`) or create small, focused text snippets within the test file to validate specific regex patterns or parsing logic.
3.  **Assertions**: Verify that the state of the domain models (like `Presentation` or `SpeechProfile`) matches expectations after processing.

## 5. Integration Testing

Integration tests for TTS providers (like `run_test_tts.py`) actually execute network calls to the provider's API.

-   These tests should not be run automatically in every CI build unless specific API keys and network access are configured.
-   They are crucial for verifying that the `BaseProvider` implementation correctly handles the specific API requirements (e.g., SSML formatting, authentication, rate limits).
-   Ensure that integration tests clean up any generated audio files after execution to prevent cluttering the repository.
