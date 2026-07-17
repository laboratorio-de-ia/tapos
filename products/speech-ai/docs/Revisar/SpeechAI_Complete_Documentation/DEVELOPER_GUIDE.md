# Developer Guide

## 1. Introduction

Welcome to the Speech AI project. This guide is intended for software engineers, particularly junior AI engineers, who are onboarding to the project. It covers the local setup, the core data flow, and instructions on how to extend the system.

## 2. Local Environment Setup

To ensure a consistent development environment, follow these steps:

1.  **Clone the Repository**: Clone the main project repository to your local machine.
2.  **Create a Virtual Environment**: It is highly recommended to use a virtual environment to isolate dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies**: Install the required packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
4.  **Verify Setup**: Run the main script to ensure everything is working correctly.
    ```bash
    python main.py
    ```

## 3. Understanding the Core Flow

The application execution is orchestrated by `SpeechAIApp` located in `app/speech_ai_app.py`. Understanding this file is crucial.

The flow operates as follows:
1.  `TextAnalyzer` reads the input script and converts it into a `Presentation` object.
2.  `SpeechIntelligenceEngine` evaluates the text, detects the language, and generates a `SpeechProfile`.
3.  `NarrationBuilder` and `SpeechBuilder` format the text for synthesis.
4.  `SpeechService` utilizes the `ProviderFactory` to instantiate the configured TTS provider (e.g., `EdgeProvider`) and generates the final audio file.

## 4. Adding a New TTS Provider

The system is designed to be easily extensible. To add a new TTS provider (e.g., Azure or OpenAI), you must adhere to the established provider architecture.

1.  **Create the Provider Class**: Create a new file in the `providers/` directory (e.g., `azure_provider.py`).
2.  **Inherit from BaseProvider**: Your new class must inherit from `BaseProvider` and implement the required `generate()` method.
3.  **Register the Provider**: The provider must be registered within the system so the `ProviderFactory` can instantiate it based on the configuration in `settings.json`.

By following this pattern, the core application logic remains completely unaware of the specific provider implementation, adhering to the Open/Closed Principle.

## 5. Modifying Voice Profiles

Voice profiles dictate how the TTS engine sounds. They are managed via JSON configuration rather than hardcoded logic.

To modify or add a voice:
1.  Open `config/voices.json`.
2.  Add a new profile entry specifying the `provider`, `language`, `locale`, `voice` ID (specific to the provider), and characteristics like `rate` and `pitch`.
3.  Update the `defaults` section if you want this new voice to be the default for a specific language.

## 6. Debugging

Logs are automatically written to the `logs/` directory. The `app.log` file contains detailed information about the pipeline execution, including language detection results, selected voice profiles, and any errors encountered during API calls to the TTS providers. Always check this file first when troubleshooting issues arise.
