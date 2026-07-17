import contextlib
import io
import json
import sys
import traceback
from pathlib import Path

# garantir que a raiz do code-ai está no sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from integration.facade import run_code_ai

try:
    input_file = sys.argv[1] if len(sys.argv) > 1 else None

    # o conversor faz print() de progresso; isso precisa ficar fora do
    # stdout real, que deve conter apenas o JSON final consumido pelo adapter
    internal_output = io.StringIO()
    with contextlib.redirect_stdout(internal_output):
        result = run_code_ai(input_file=input_file)

    print(json.dumps(result))
except Exception:
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
