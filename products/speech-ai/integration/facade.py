from .runner import execute_current_pipeline


def run_speech_ai() -> dict:
    result = execute_current_pipeline()
    return result.to_dict()