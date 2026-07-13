from pathlib import Path
import json
import re

ROOT=Path('.')

IGNORE={
'.git','node_modules','__pycache__','.venv','venv',
'build','dist','.pytest_cache'
}

result={
 'directories':[],
 'files':[],
 'stats':{}
}

for p in ROOT.rglob('*'):

    if any(i in p.parts for i in IGNORE):
        continue

    if p.is_dir():
        result['directories'].append(str(p))
        continue

    if not p.is_file():
        continue

    item={
        'path':str(p),
        'name':p.name,
        'ext':p.suffix.lower(),
        'size':p.stat().st_size
    }

    try:

        txt=p.read_text(
            encoding='utf-8',
            errors='ignore'
        )

        refs=re.findall(
            r'(task\\s*\\d+[a-z]?|sprint\\s*\\d+|speech-ai|edital-ai|educa-ai|code-ai|tapos)',
            txt,
            flags=re.I
        )

        item['refs']=sorted(
            list(set(refs))
        )[:200]

        item['preview']=txt[:5000]

    except:

        item['refs']=[]

    result['files'].append(item)

result['stats']={
 'dirs':len(result['directories']),
 'files':len(result['files'])
}

Path(
 'TAPOS_SEMANTIC_EXPORT.json'
).write_text(
 json.dumps(
  result,
  ensure_ascii=False,
  indent=2
 ),
 encoding='utf-8'
)

print('TAPOS_SEMANTIC_EXPORT.json gerado')