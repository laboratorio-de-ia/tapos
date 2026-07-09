# Operations Guide

## 1. System Operation

This guide provides instructions for IT Operations and DevOps teams responsible for deploying, monitoring, and maintaining the Speech AI platform.

## 2. Deployment

Currently, the application is executed as a standalone Python script. Future iterations will include Docker containerization.

### 2.1. Prerequisites
-   A Linux or Windows server environment.
-   Python 3.10 or higher installed.
-   Network access to the required external TTS provider APIs (e.g., Microsoft Edge endpoints).

### 2.2. Installation Steps
1.  Deploy the application code to the target server.
2.  Install dependencies using `pip install -r requirements.txt`.
3.  Configure the environment variables (e.g., API keys) securely.
4.  Ensure the `input/`, `output/`, and `logs/` directories exist and have the correct permissions.

## 3. Configuration Management

Operational behavior is controlled via the `config/` directory.

-   **`settings.json`**: Controls the input/output paths and the default TTS provider. Modify this file to change where the system looks for scripts or where it saves the resulting audio.
-   **`voices.json`**: Defines the available voice profiles. Operations teams can update this file to adjust speech rates, pitches, or add new voices without requiring a code deployment.

## 4. Monitoring and Logging

The application utilizes the standard Python `logging` module.

-   **Log Location**: All logs are written to the `logs/app.log` file.
-   **Log Levels**: The application logs at the `INFO` level by default, providing details on pipeline progression, language detection, and provider selection. Errors during processing or API calls are logged at the `ERROR` level.
-   **Monitoring Strategy**: Operations teams should monitor `app.log` for `ERROR` entries. Additionally, monitoring the execution time of the `SpeechService` can help identify latency issues with external TTS providers.

## 5. Troubleshooting Common Issues

| Issue | Potential Cause | Resolution |
| :--- | :--- | :--- |
| Application crashes on startup. | Missing configuration files. | Ensure `settings.json` and `voices.json` are present in the `config/` directory and contain valid JSON. |
| Audio file is not generated. | Network failure or invalid provider credentials. | Check `app.log` for connection errors or unauthorized responses from the TTS provider. Verify API keys. |
| Incorrect language detected. | Input script is too short or ambiguous. | Review the input script. The `LanguageDetector` requires sufficient text context to accurately identify the language. |
