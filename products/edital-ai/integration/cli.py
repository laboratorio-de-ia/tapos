import contextlib
import io
import json
import sys
import traceback
from pathlib import Path

# garantir que a raiz do edital-ai está no sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from integration.facade import run_edital_ai

try:
    if len(sys.argv) < 2:
        raise ValueError("Uso: python cli.py <arquivo_edital>")

    arquivo_path = sys.argv[1]

    # extração/geração de artefatos podem fazer print() de progresso;
    # o stdout real deve conter só o JSON final consumido pelo adapter
    internal_output = io.StringIO()
    with contextlib.redirect_stdout(internal_output):
        result = run_edital_ai(arquivo_path)

    print(json.dumps(result, ensure_ascii=False, default=str))
except Exception:
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
