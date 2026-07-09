import json
import sys
import traceback
from pathlib import Path

# garantir que a raiz do speech-ai está no sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from integration.facade import run_speech_ai

try:
    result = run_speech_ai()
    print(json.dumps(result))
except Exception:
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)