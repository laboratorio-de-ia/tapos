from pathlib import Path
from typing import Optional
import subprocess
import json


def run_code_ai_product(input_file: Optional[str] = None) -> dict:
    """
    Adapter TAPOS -> code-ai
    Executa o code-ai no .venv do próprio produto
    e expõe stdout/stderr reais em caso de falha.
    """
    code_ai_root = Path("/workspace/tecle/products/code-ai")
    python_bin = code_ai_root / ".venv" / "bin" / "python"
    cli_file = code_ai_root / "integration" / "cli.py"

    if not python_bin.exists():
        raise FileNotFoundError(f"Python do code-ai não encontrado: {python_bin}")

    if not cli_file.exists():
        raise FileNotFoundError(f"CLI de integração não encontrada: {cli_file}")

    command = [str(python_bin), str(cli_file)]
    if input_file:
        command.append(input_file)

    result = subprocess.run(
        command,
        cwd=str(code_ai_root),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "code-ai falhou.\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

    stdout = result.stdout.strip()
    if not stdout:
        raise RuntimeError("code-ai não retornou saída JSON")

    return json.loads(stdout)
