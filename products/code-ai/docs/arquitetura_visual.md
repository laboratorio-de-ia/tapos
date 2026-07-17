# 🏗️ Arquitetura Visual - CODE-AI

---

# 📁 Estrutura Física do Projeto

```text
code-ai/
│
├── docs/
│   ├── analise_projeto.md
│   ├── arquitetura_visual.md
│   └── guia_rapido.md
│
├── input/
│
├── output/
│
├── scripts/
│   ├── exemplos_uso.py
│   ├── instalar.py
│   ├── rapido.py
│   └── workflow.py
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

# 🔄 Fluxo Principal

```text
ARQUIVO DE ENTRADA
        │
        ▼
     input/
        │
        ▼
ConvertorUniversal
        │
        ▼
Conversor Específico
        │
        ▼
 Markdown (.md)
        │
        ▼
     output/
        │
        ├── documento.md
        ├── relatorio.md
        └── relatorio.json
```

---

# 🎯 Arquivos Suportados

```text
PDF
DOCX
XLSX
XLS
CSV
PPTX
PNG
JPG
JPEG
TXT
MD
```

---

# 🏛️ Camadas da Aplicação

## Camada de Entrada

```text
input/
```

Responsável por armazenar:

- PDFs
- Word
- Excel
- PowerPoint
- Imagens
- Arquivos texto

---

## Camada de Conversão

```text
src/conversor_markdown.py
```

Classe principal:

```python
ConvertorUniversal
```

Responsabilidades:

- Selecionar conversor
- Gerar Markdown
- Calcular métricas
- Gerar relatório

---

## Conversores Especializados

```text
ConversorPDF
ConversorDocx
ConversorExcel
ConversorPowerPoint
ConversorImagem
ConversorTexto
```

Cada classe possui responsabilidade única.

---

## Camada de Saída

```text
output/
```

Exemplo:

```text
output/
├── documento.md
├── apresentacao.md
├── planilha.md
└── relatorio.json
```

---

# 🔄 Fluxo de Conversão de um Arquivo

```text
input/documento.pdf
        │
        ▼
Validação
        │
        ▼
Detecta extensão
        │
        ▼
Seleciona ConversorPDF
        │
        ▼
Extrai texto
        │
        ▼
Extrai tabelas
        │
        ▼
OCR (se necessário)
        │
        ▼
Gera Markdown
        │
        ▼
output/documento.md
```

---

# 🧠 Arquitetura Interna

```text
ConvertorUniversal
│
├── ConversorPDF
│
├── ConversorDocx
│
├── ConversorExcel
│
├── ConversorPowerPoint
│
├── ConversorImagem
│
└── ConversorTexto
```

Padrão utilizado:

```text
Strategy Pattern
```

O formato do arquivo determina automaticamente qual conversor será utilizado.

---

# 📊 Fluxo de Processamento

```text
Arquivo
 │
 ▼
Existe?
 │
 ├── Não → Erro
 │
 └── Sim
         │
         ▼
Formato suportado?
         │
         ├── Não → Erro
         │
         └── Sim
                 │
                 ▼
Conversão
                 │
                 ▼
Relatório
                 │
                 ▼
Sucesso
```

---

# 📈 Relatório Gerado

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

Local:

```text
output/relatorio.json
```

---

# 🔧 Dependências

```text
pandas
openpyxl
python-docx
python-pptx
pdf2image
pytesseract
pdfplumber
Pillow
```

Instalação:

```bash
pip install -r requirements.txt
```

---

# 🚀 Modos de Execução

## Modo 1

Teste simples:

```bash
python teste_sistema.py
```

---

## Modo 2

Conversão direta:

```bash
python src/conversor_markdown.py input/documento.pdf
```

---

## Modo 3

Pasta completa:

```bash
python src/conversor_markdown.py input
```

---

## Modo 4

Workflow estruturado:

```bash
python scripts/workflow.py 1 input/documento.pdf
```

---

## Modo 5

Modo rápido:

```bash
python scripts/rapido.py input/documento.pdf
```

---

# 📦 Fluxo Recomendado

```text
1. Colocar arquivos em input/

2. Executar conversão

3. Validar output/

4. Revisar relatorio.json

5. Utilizar Markdown em:
   ├─ Claude
   ├─ ChatGPT
   ├─ Gemini
   ├─ Copilot
   └─ RAG
```

---

# 🔮 Evolução Futura

```text
API REST
Interface Web
Processamento Assíncrono
Cache
Vetorização Automática
Integração SharePoint
Integração OneDrive
Pipeline RAG
```

---

# ✅ Resumo Arquitetural

```text
input/
   │
   ▼
src/conversor_markdown.py
   │
   ▼
output/
   │
   ▼
Markdown pronto para IA
```

O CODE-AI segue uma arquitetura simples, modular e de fácil manutenção, separando claramente documentação, entrada, processamento e saída.