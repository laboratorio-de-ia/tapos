# 📊 Análise do Projeto CODE-AI

## Data da Análise

Julho de 2026

---

# 🎯 Objetivo do Projeto

O CODE-AI é uma plataforma de conversão de documentos para Markdown focada em:

- Economia de tokens para LLMs
- Organização documental
- Preparação de conteúdo para IA
- Bases RAG
- Documentação técnica
- Processamento em lote

A proposta principal é transformar diversos formatos de documentos em Markdown padronizado, reduzindo significativamente o volume de texto processado pelas plataformas de Inteligência Artificial.

---

# 📁 Arquitetura Atual do Projeto

```text
code-ai/
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

# 🏗️ Componentes do Sistema

## Core Principal

### src/conversor_markdown.py

Responsável por:

- Conversão dos documentos
- Seleção automática do conversor
- Geração de relatórios
- Cálculo de economia
- Processamento de pastas

Classe principal:

```python
ConvertorUniversal
```

---

## Scripts Auxiliares

### scripts/instalar.py

Responsável por:

- Verificar Python
- Instalar requirements.txt
- Validar ambiente
- Criar exemplos de teste

---

### scripts/rapido.py

Interface simplificada para conversão rápida.

Exemplo:

```bash
python scripts/rapido.py input/documento.pdf
```

---

### scripts/workflow.py

Workflows padronizados:

- Arquivo único
- Múltiplos arquivos
- Pasta completa
- Otimização
- Preparação para IA

---

### scripts/exemplos_uso.py

Coleção de exemplos de integração.

Utilizado como documentação prática para desenvolvedores.

---

# 📄 Formatos Suportados

## Entrada

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

## Saída

| Formato |
|----------|
| Markdown (.md) |

---

# 🔧 Dependências

## Python

Instaladas através de:

```bash
pip install -r requirements.txt
```

Principais bibliotecas:

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

---

## Sistema Operacional

OCR utiliza:

```text
Tesseract OCR
```

Ubuntu:

```bash
sudo apt-get install tesseract-ocr
```

macOS:

```bash
brew install tesseract
```

---

# 💻 Uso do Sistema

## Conversão de Arquivo

```bash
python src/conversor_markdown.py input/documento.pdf
```

---

## Conversão de Pasta

```bash
python src/conversor_markdown.py input
```

---

## Uso via Python

```python
from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal(
    diretorio_saida="output"
)

resultado = conversor.converter_arquivo(
    "input/documento.pdf"
)
```

---

# 📊 Relatórios

Após a execução:

```python
conversor.gerar_relatorio()
```

É criado:

```text
output/relatorio.json
```

Modelo:

```json
{
  "data": "2026-07-10T10:30:00",
  "arquivos_processados": [],
  "erros": []
}
```

---

# 📈 Benefícios Esperados

## Economia de Tokens

| Documento | Economia Média |
|------------|------------|
| PDF | 70–85% |
| DOCX | 70–80% |
| XLSX | 70–80% |
| PPTX | 75–85% |

---

## Benefícios Operacionais

- Menor custo com IA
- Melhor indexação vetorial
- Processamento padronizado
- Facilidade para auditoria
- Integração simples com LLMs

---

# 🚀 Fluxo Recomendado

```text
1. Colocar arquivos em input/

2. Converter

3. Validar saída

4. Revisar relatório

5. Utilizar Markdown em:
   - Claude
   - ChatGPT
   - Gemini
   - Copilot
   - Bases Vetoriais
```

---

# ✅ Próximas Evoluções

## Curto Prazo

- Testes automatizados
- Logging estruturado
- Melhor tratamento de erros

## Médio Prazo

- Interface Web
- API REST
- Conversão assíncrona

## Longo Prazo

- Pipeline RAG integrado
- Vetorização automática
- Conectores SharePoint
- Processamento distribuído

---

# 📌 Conclusão

O CODE-AI está organizado em uma arquitetura modular baseada em:

- Core em `src/`
- Scripts em `scripts/`
- Entrada em `input/`
- Saída em `output/`
- Documentação em `docs/`

A estrutura atual permite evolução sem quebrar compatibilidade e segue boas práticas de organização de projetos Python.