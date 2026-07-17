from datetime import datetime
from pathlib import Path
from typing import Optional
import subprocess
import json

EDITAL_AI_ROOT = Path("/workspace/tecle/products/edital-ai")
EDITAL_AI_INPUT_DIR = EDITAL_AI_ROOT / "input"
EDITAL_AI_PROCESSADOS_DIR = EDITAL_AI_ROOT / "processados"


def find_current_edital_file() -> Optional[Path]:
    """Retorna o edital atualmente 'em foco' (último upload), se houver.

    O upload mantém o nome original do arquivo enviado (não mais um nome
    genérico "documento.*"), então aqui basta olhar para o único arquivo
    presente em input/ — o upload sempre limpa arquivos anteriores antes
    de salvar o novo.
    """
    if not EDITAL_AI_INPUT_DIR.exists():
        return None
    candidatos = sorted(
        f for f in EDITAL_AI_INPUT_DIR.iterdir()
        if f.is_file() and not f.name.startswith(".")
    )
    return candidatos[0] if candidatos else None


def arquivar_processado(input_file: Path, nome_original: Optional[str] = None) -> Optional[Path]:
    """Move o arquivo já processado de input/ para processados/, renomeado
    com o nome do documento enviado + data/hora do processamento.

    Evita acumular arquivos em input/ e mantém rastro de qual arquivo gerou
    qual análise. Não falha o request se o arquivo já não existir mais (ex.:
    corrida entre duas execuções sobre o mesmo "documento atual").
    """
    origem = Path(input_file)
    if not origem.exists():
        return None

    EDITAL_AI_PROCESSADOS_DIR.mkdir(parents=True, exist_ok=True)

    referencia = Path(nome_original) if nome_original else origem
    base = referencia.stem or "edital"
    extensao = referencia.suffix or origem.suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    destino = EDITAL_AI_PROCESSADOS_DIR / f"{base}_{timestamp}{extensao}"
    contador = 1
    while destino.exists():
        destino = EDITAL_AI_PROCESSADOS_DIR / f"{base}_{timestamp}_{contador}{extensao}"
        contador += 1

    origem.rename(destino)
    return destino


def run_edital_ai_product(input_file: Optional[str] = None) -> dict:
    """
    Adapter TAPOS -> edital-ai
    Executa o edital-ai no .venv do próprio produto
    e expõe stdout/stderr reais em caso de falha.

    Se input_file não for informado, reprocessa o último edital enviado
    (mesmo padrão de "documento atual" usado no code-ai).
    """
    if input_file is None:
        atual = find_current_edital_file()
        if atual is None:
            raise FileNotFoundError(
                "Nenhum edital enviado ainda. Use /products/edital-ai/upload primeiro."
            )
        input_file = str(atual)

    python_bin = EDITAL_AI_ROOT / ".venv" / "bin" / "python"
    cli_file = EDITAL_AI_ROOT / "integration" / "cli.py"

    if not python_bin.exists():
        raise FileNotFoundError(f"Python do edital-ai não encontrado: {python_bin}")

    if not cli_file.exists():
        raise FileNotFoundError(f"CLI de integração não encontrada: {cli_file}")

    command = [str(python_bin), str(cli_file), input_file]

    result = subprocess.run(
        command,
        cwd=str(EDITAL_AI_ROOT),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "edital-ai falhou.\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

    stdout = result.stdout.strip()
    if not stdout:
        raise RuntimeError("edital-ai não retornou saída JSON")

    return json.loads(stdout)
