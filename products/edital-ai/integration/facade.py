from .runner import execute_pipeline


def run_edital_ai(arquivo_path: str) -> dict:
    result = execute_pipeline(arquivo_path)
    return result.to_dict()
