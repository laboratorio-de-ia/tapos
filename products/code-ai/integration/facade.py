from typing import Optional

from .runner import execute_current_pipeline


def run_code_ai(input_file: Optional[str] = None) -> dict:
    result = execute_current_pipeline(input_file=input_file)
    return result.to_dict()
