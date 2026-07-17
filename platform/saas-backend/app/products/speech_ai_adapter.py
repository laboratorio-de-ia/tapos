from pathlib import Path
import subprocess
import json


def run_speech_ai_product() -> dict:
    """
    Adapter TAPOS -> speech-ai
    Executa o speech-ai no .venv do próprio produto
    e expõe stdout/stderr reais em caso de falha.
    """
    speech_ai_root = Path("/workspace/tecle/products/speech-ai")
    python_bin = speech_ai_root / ".venv" / "bin" / "python"
    cli_file = speech_ai_root / "integration" / "cli.py"

    if not python_bin.exists():
        raise FileNotFoundError(f"Python do speech-ai não encontrado: {python_bin}")

    if not cli_file.exists():
        raise FileNotFoundError(f"CLI de integração não encontrada: {cli_file}")

    result = subprocess.run(
        [str(python_bin), str(cli_file)],
        cwd=str(speech_ai_root),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "speech-ai falhou.\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

    stdout = result.stdout.strip()
    if not stdout:
        raise RuntimeError("speech-ai não retornou saída JSON")

    return json.loads(stdout)