# 📄 CODE-AI - Conversor Universal para Markdown

Sistema Python para conversão de documentos para Markdown com foco em produtividade, organização e economia de tokens para utilização com LLMs.

## 🚀 Objetivo

Converter automaticamente documentos diversos para Markdown:

- PDF
- Word (.docx)
- Excel (.xlsx/.xls)
- CSV
- PowerPoint (.pptx)
- Imagens (.png/.jpg/.jpeg)
- Arquivos texto (.txt)
- Markdown (.md)

Ideal para:

- Claude
- ChatGPT
- Gemini
- Copilot
- RAG
- Bases vetoriais
- Documentação

---

# 📁 Estrutura do Projeto

```text
code-ai/
├── docs/
│
├── input/
│
├── output/
│
├── scripts/
│
├── src/
│   ├── __init__.py
│   └── conversor_markdown.py
│
├── teste_sistema.py
├── requirements.txt
└── readme.md
```

---

# ⚙️ Instalação

## Criar ambiente virtual (recomendado)

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Dependências de Sistema (OCR)

### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

### macOS

```bash
brew install tesseract
brew install poppler
```

---

# 📋 Formatos Suportados

| Formato | Suporte | Observação |
|----------|----------|----------|
| PDF | ✅ | Texto + OCR |
| DOCX | ✅ | Preserva estrutura |
| XLSX | ✅ | Todas as abas |
| XLS | ✅ | Compatível |
| CSV | ✅ | Tabela Markdown |
| PPTX | ✅ | Texto dos slides |
| PNG | ✅ | OCR |
| JPG | ✅ | OCR |
| JPEG | ✅ | OCR |
| TXT | ✅ | Conversão direta |
| MD | ✅ | Conversão direta |

---

# 🧪 Teste Rápido

Coloque um arquivo de teste:

```text
input/documento.pdf
```

Execute:

```bash
python teste_sistema.py
```

Resultado:

```text
output/documento.md
```

---

# 💻 Uso em Python

## Converter um arquivo

```python
from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal(
    diretorio_saida="output"
)

resultado = conversor.converter_arquivo(
    "input/documento.pdf"
)

print(resultado)
```

---

## Converter múltiplos arquivos

```python
from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal()

arquivos = [
    "input/documento.pdf",
    "input/relatorio.docx",
    "input/dados.xlsx"
]

resultados = conversor.converter_multiplos(
    arquivos
)

for arquivo in resultados:
    print(arquivo)
```

---

## Converter uma pasta inteira

```python
from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal()

resultado = conversor.converter_pasta(
    "input"
)

conversor.gerar_relatorio()
```

---

# 🔧 Uso via Terminal

## Converter um arquivo

```bash
python src/conversor_markdown.py input/documento.pdf
```

---

## Converter todos os arquivos da pasta

```bash
python src/conversor_markdown.py input
```

---

# 📊 Relatório de Conversão

Após o processamento:

```python
conversor.gerar_relatorio()
```

Será criado:

```text
output/relatorio.json
```

Exemplo:

```json
{
  "data": "2026-07-10T10:30:00",
  "arquivos_processados": [
    {
      "arquivo_original": "documento.pdf",
      "arquivo_convertido": "documento.md"
    }
  ],
  "erros": []
}
```

---

# 📦 Estrutura de Saída

```text
output/
├── documento.md
├── relatorio.md
├── dados.md
├── apresentacao.md
└── relatorio.json
```

---

# 📈 Benefício para LLMs

Exemplo típico:

| Cenário | Tokens |
|----------|----------|
| PDF original | 10.000+ |
| Markdown convertido | 1.500 |
| Economia média | 70% - 85% |

---

# 🐛 Troubleshooting

## Erro: pytesseract não encontrado

```bash
pip install pytesseract
```

---

## Erro: pdf2image não encontrado

```bash
pip install pdf2image
```

---

## Erro: PowerPoint

```bash
pip install python-pptx
```

---

## Erro: Word

```bash
pip install python-docx
```

---

## Erro: Excel

```bash
pip install pandas openpyxl
```

---

# 🔄 Fluxo Recomendado

```text
1. Colocar arquivos em input/

2. Executar conversão

3. Gerar Markdown em output/

4. Validar conteúdo

5. Utilizar em:
   - Claude
   - ChatGPT
   - Copilot
   - RAG
   - Busca Vetorial
```

---

# ✅ Exemplo de Import Correto

Como o projeto foi reorganizado:

```python
from src.conversor_markdown import ConvertorUniversal
```

Não utilizar:

```python
from conversor_markdown import ConvertorUniversal
```

---

# 📝 Licença

Uso livre para fins educacionais e profissionais.

---

**CODE-AI**
Conversão inteligente de documentos para Markdown.