# ⚡ Guia Rápido - CODE-AI

## Objetivo

Converter documentos para Markdown de forma rápida para utilização em:

- ChatGPT
- Claude
- Gemini
- Copilot
- RAG
- Bases Vetoriais

Tempo estimado para o primeiro teste:

✅ Menos de 5 minutos

---

# 1️⃣ Instalação

## Passo 1

Abra o terminal na raiz do projeto:

```text
code-ai/
```

---

## Passo 2

Crie ambiente virtual (opcional)

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Passo 3

Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Passo 4

Instale OCR (opcional)

### Ubuntu

```bash
sudo apt-get install tesseract-ocr
```

### macOS

```bash
brew install tesseract
```

---

# 2️⃣ Estrutura Esperada

```text
code-ai/
│
├── input/
├── output/
│
├── scripts/
├── src/
│
├── requirements.txt
├── teste_sistema.py
└── readme.md
```

---

# 3️⃣ Primeiro Teste

Coloque um arquivo dentro da pasta:

```text
input/
```

Exemplo:

```text
input/
└── Stellantis_Copilot_Token_Optimization_Best_Practices.pdf
```

---

# 4️⃣ Executar Conversão

## Opção 1 (Recomendada)

Criar ou usar:

```python
# teste_sistema.py

from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal(
    diretorio_saida="output"
)

resultado = conversor.converter_arquivo(
    r"input/Stellantis_Copilot_Token_Optimization_Best_Practices.pdf"
)

conversor.gerar_relatorio()

print(resultado)
```

Executar:

```bash
python teste_sistema.py
```

---

## Opção 2 (CLI)

```bash
python src/conversor_markdown.py input/Stellantis_Copilot_Token_Optimization_Best_Practices.pdf
```

---

## Opção 3 (Pasta Completa)

```bash
python src/conversor_markdown.py input
```

---

# 5️⃣ Resultado

Os arquivos convertidos serão criados em:

```text
output/
```

Exemplo:

```text
output/
├── Stellantis_Copilot_Token_Optimization_Best_Practices.md
└── relatorio.json
```

---

# 6️⃣ Uso em Python

## Conversão Simples

```python
from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal()

resultado = conversor.converter_arquivo(
    "input/documento.pdf"
)

print(resultado)
```

---

## Conversão de Múltiplos Arquivos

```python
from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal()

arquivos = [
    "input/doc1.pdf",
    "input/doc2.docx",
    "input/doc3.xlsx"
]

resultado = conversor.converter_multiplos(
    arquivos
)

conversor.gerar_relatorio()
```

---

## Conversão de uma Pasta

```python
from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal()

resultado = conversor.converter_pasta(
    "input"
)

conversor.gerar_relatorio()
```

---

# 7️⃣ Workflows

## Arquivo Único

```bash
python scripts/workflow.py 1 input/documento.pdf
```

---

## Múltiplos Arquivos

```bash
python scripts/workflow.py 2 input/doc1.pdf input/doc2.docx
```

---

## Pasta Completa

```bash
python scripts/workflow.py 3 input
```

---

## Otimizar Markdown

```bash
python scripts/workflow.py 4 input/documento.pdf
```

---

## Preparar para IA

```bash
python scripts/workflow.py 5 input/documento.pdf
```

---

# 8️⃣ Modo Rápido

Converter um único arquivo:

```bash
python scripts/rapido.py input/documento.pdf
```

Converter uma pasta:

```bash
python scripts/rapido.py input
```

---

# 9️⃣ Relatório

Após a execução:

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
  "arquivos_processados": [],
  "erros": []
}
```

---

# 🔟 Formatos Suportados

| Formato | Suporte |
|----------|----------|
| PDF | ✅ |
| DOCX | ✅ |
| XLSX | ✅ |
| XLS | ✅ |
| CSV | ✅ |
| PPTX | ✅ |
| PNG | ✅ |
| JPG | ✅ |
| JPEG | ✅ |
| TXT | ✅ |
| MD | ✅ |

---

# 🆘 Problemas Comuns

## ImportError

Execute:

```bash
pip install -r requirements.txt
```

---

## Tesseract não encontrado

Instale:

```bash
sudo apt-get install tesseract-ocr
```

ou:

```bash
brew install tesseract
```

---

## Arquivo não encontrado

Verifique se está dentro da pasta:

```text
input/
```

---

## Nenhum Markdown foi gerado

Validar:

```text
output/
```

e verificar:

```text
output/relatorio.json
```

---

# 📈 Benefícios

Economia típica:

| Tipo | Economia |
|--------|--------|
| PDF | 70–85% |
| Word | 70–80% |
| Excel | 70–80% |
| PPT | 75–85% |

---

# ✅ Fluxo Recomendado

```text
1. Colocar documento em input/

2. Executar conversão

3. Ler arquivo gerado em output/

4. Validar resultado

5. Utilizar no Claude, ChatGPT, Gemini ou Copilot
```

---

# 🚀 Comando Mais Simples

```bash
python teste_sistema.py
```

Se funcionar, o ambiente está pronto.