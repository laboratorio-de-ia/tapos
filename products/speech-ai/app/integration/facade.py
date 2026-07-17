from .runner import execute_current_pipeline


def run_speech_ai() -> dict:
    """
    Interface pública da integração TAPOS -> speech-ai.
    Nesta etapa, executa a pipeline atual usando a configuração existente.
    """
    result = execute_current_pipeline()
    return result.to_dict()
