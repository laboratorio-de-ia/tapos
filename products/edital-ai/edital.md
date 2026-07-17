# ESPECIFICAÇÕES TÉCNICAS: EDITAL-AI

**Versão**: 1.0.0  
**Data**: 13/07/2026  
**Status**: Pronto para Claude Code + VSCode  
**Plataforma**: TAPOS (Tecle AI Platform Operating System)

---

## 📋 RESUMO EXECUTIVO

O **edital-ai** é um produto SaaS integrado à plataforma TAPOS que automatiza a análise de editais públicos (licitações). Utilizando IA local (Ollama) e processamento inteligente, o sistema:

- **Lê e interpreta** editais em múltiplos formatos (PDF, DOCX, etc)
- **Extrai informações críticas**: prazos, documentos obrigatórios, objetos, valores, modalidades
- **Gera artefatos** em Excel, PDF, Word e e-mail
- **Reduz tempo operacional** em até 95% comparado à leitura manual
- **Roda localmente** sem dependência de provedores externos
- **Integra-se perfeitamente** ao backend TAPOS via adapter

---

## 🎯 OBJETIVO E ESCOPO

### Objetivo Principal
Automatizar a análise de editais de licitação pública, transformando documentos não-estruturados em informações estruturadas e acionáveis, reduzindo drasticamente o tempo de processamento manual.

### Público-Alvo
- Empresas que participam regularmente de licitações públicas
- Distribuidoras e revendedoras de produtos/serviços
- Fabricantes com portfólio em órgãos públicos
- Departamentos de compliance e gestão de licitações

### Casos de Uso

#### 1. Análise Rápida de Edital
```
Usuário faz upload de PDF do edital
    ↓
Sistema extrai texto + estrutura
    ↓
IA analisa e identifica seções
    ↓
Gera resumo executivo + checklist
    ↓
Usuário visualiza em segundos (vs. horas manualmente)
```

#### 2. Extração de Requisitos
```
Edital contém múltiplos objetos/itens
    ↓
Sistema extrai cada objeto com:
   - Descrição
   - Quantidade
   - Valor estimado
   - Modalidade de entrega
    ↓
Gera planilha Excel estruturada
    ↓
Usuário importa em sistema interno
```

#### 3. Verificação de Conformidade
```
Edital especifica documentos obrigatórios
    ↓
Sistema extrai lista completa:
   - Documentos de habilitação
   - Certificações necessárias
   - Prazos de validade
    ↓
Compara com base de dados interna
    ↓
Gera relatório de gaps
```

#### 4. Monitoramento de Prazos
```
Sistema extrai todos os prazos do edital:
   - Abertura de inscrições
   - Encerramento
   - Datas de sessão
   - Prazos de recurso
    ↓
Cria alertas automáticos
    ↓
Envia e-mail com cronograma
```

#### 5. Análise Competitiva
```
Edital permite identificar concorrentes
    ↓
Sistema extrai:
   - Objetos similares ao portfólio
   - Faixa de preço
   - Modalidades de entrega
    ↓
Compara com histórico interno
    ↓
Gera insights para estratégia de preço
```

---

## 🏗️ ARQUITETURA TÉCNICA

### Camadas da Plataforma

```
┌─────────────────────────────────────────┐
│ USUÁRIOS (WEB/MOBILE/API CLIENTS)       │
└──────────────┬──────────────────────────┘
               │ HTTP REST (JSON)
               ▼
┌─────────────────────────────────────────┐
│ SaaS Backend (FastAPI - porta 8000)     │
│ - Auth (JWT)                            │
│ - Endpoints /products/edital-ai/*       │
│ - Adapter para edital-ai                │
└──────────────┬──────────────────────────┘
               │ Subprocess + CLI
               ▼
┌─────────────────────────────────────────┐
│ EDITAL-AI (Produto)                     │
│ - Pipeline de análise                   │
│ - IA local (Ollama)                     │
│ - Geração de artefatos                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Infraestrutura (/data/platform)         │
│ - PostgreSQL (metadados)                │
│ - Ollama (IA local)                     │
│ - MinIO (storage de arquivos)           │
└─────────────────────────────────────────┘
```

### Estrutura de Diretórios

```
products/edital-ai/
├── main.py                              # Ponto de entrada
├── requirements.txt                     # Dependências Python
├── .env.example                         # Variáveis de ambiente
├── README.md                            # Documentação
│
├── app/
│   └── edital_ai_app.py                # Classe EditalAIApp (orquestração)
│
├── config/
│   ├── __init__.py
│   ├── config_manager.py               # Carregamento de configuração
│   ├── settings.json                   # Configurações padrão
│   └── prompts.json                    # Prompts para IA
│
├── models/
│   ├── __init__.py
│   ├── edital.py                       # @dataclass Edital
│   ├── secao.py                        # @dataclass Secao
│   ├── objeto.py                       # @dataclass Objeto
│   ├── requisito.py                    # @dataclass Requisito
│   ├── prazo.py                        # @dataclass Prazo
│   ├── analise.py                      # @dataclass Analise
│   ├── artefato.py                     # @dataclass Artefato
│   └── relatorio.py                    # @dataclass Relatorio
│
├── pipeline/
│   ├── __init__.py
│   ├── edital_extractor.py             # Extração de texto do PDF
│   ├── edital_parser.py                # Parse e estruturação
│   ├── edital_analyzer.py              # Análise com IA
│   └── artefato_generator.py           # Geração de artefatos
│
├── services/
│   ├── __init__.py
│   ├── pdf_service.py                  # Extração de PDF
│   ├── docx_service.py                 # Extração de DOCX
│   ├── text_cleaner.py                 # Limpeza de texto
│   ├── ollama_service.py               # Integração com Ollama
│   ├── excel_generator.py              # Geração de Excel
│   ├── pdf_generator.py                # Geração de PDF
│   ├── word_generator.py               # Geração de Word
│   ├── email_generator.py              # Geração de e-mail
│   └── database_service.py             # Persistência de dados
│
├── prompts/
│   ├── extract_sections.txt            # Prompt: extração de seções
│   ├── extract_objects.txt             # Prompt: extração de objetos
│   ├── extract_requirements.txt        # Prompt: extração de requisitos
│   ├── extract_deadlines.txt           # Prompt: extração de prazos
│   ├── generate_summary.txt            # Prompt: resumo executivo
│   └── competitive_analysis.txt        # Prompt: análise competitiva
│
├── input/
│   └── (editais em PDF/DOCX)
│
├── output/
│   ├── (análises em JSON)
│   ├── (planilhas em XLSX)
│   ├── (documentos em DOCX)
│   └── (relatórios em PDF)
│
├── logs/
│   └── edital_ai.log
│
├── tests/
│   ├── test_extractor.py
│   ├── test_parser.py
│   ├── test_analyzer.py
│   └── test_generators.py
│
└── integration/
    ├── __init__.py
    ├── schemas.py                      # EditalRunResult, etc
    ├── facade.py                       # run_edital_ai()
    ├── runner.py                       # execute_pipeline()
    └── cli.py                          # CLI entry point
```

---

## 📥 ENTRADA (INPUT)

### Formatos Suportados
- **PDF** (editais digitalizados ou nativos)
- **DOCX** (Word)
- **TXT** (texto bruto)
- **URL** (link para edital em portal governamental)

### Estrutura do Edital Típico
```
1. Cabeçalho (órgão, modalidade, número)
2. Objeto (o que está sendo licitado)
3. Prazos (inscrição, abertura, recurso)
4. Documentos de habilitação
5. Especificações técnicas
6. Critérios de julgamento
7. Valores e formas de pagamento
8. Condições gerais
```

### Exemplo de Upload
```
POST /products/edital-ai/upload
Content-Type: multipart/form-data

{
  "arquivo": <PDF do edital>,
  "modalidade": "pregão",
  "orgao": "Prefeitura de Curitiba",
  "numero_edital": "2026/001"
}
```

---

## 🔄 PIPELINE DE PROCESSAMENTO

### Estágio 1: Extração de Texto
```python
# edital_extractor.py
class EditalExtractor:
    def extract_from_pdf(caminho: str) -> str:
        """Extrai texto de PDF (pdfplumber + OCR)"""
        # Usa pdfplumber para PDFs nativos
        # Fallback para OCR (pytesseract) para PDFs scaneados
        # Retorna texto limpo
    
    def extract_from_docx(caminho: str) -> str:
        """Extrai texto de DOCX (python-docx)"""
    
    def extract_from_url(url: str) -> str:
        """Faz download e extrai de URL"""
```

### Estágio 2: Parse e Estruturação
```python
# edital_parser.py
class EditalParser:
    def parse(texto_bruto: str) -> Edital:
        """
        Estrutura o texto em:
        - Cabeçalho (órgão, número, modalidade)
        - Seções (objeto, prazos, documentos, etc)
        - Objetos/Itens (descrição, quantidade, valor)
        - Requisitos (documentos obrigatórios)
        - Prazos (datas críticas)
        """
        edital = Edital()
        
        # Regex + heurísticas para detectar seções
        edital.cabecalho = extract_cabecalho(texto)
        edital.objeto = extract_objeto(texto)
        edital.prazos = extract_prazos(texto)
        edital.documentos = extract_documentos(texto)
        edital.valores = extract_valores(texto)
        
        return edital
```

### Estágio 3: Análise com IA
```python
# edital_analyzer.py
class EditalAnalyzer:
    def analyze(edital: Edital) -> Analise:
        """
        Usa Ollama para análise profunda:
        
        1. Resumo executivo (2-3 parágrafos)
        2. Objetos principais (lista estruturada)
        3. Requisitos críticos (checklist)
        4. Prazos importantes (timeline)
        5. Riscos/Oportunidades (insights)
        6. Recomendações (ações sugeridas)
        """
        
        # Prompt 1: Resumo
        resumo = ollama.generate(
            prompt=PROMPT_SUMMARY,
            context=edital.texto_completo
        )
        
        # Prompt 2: Objetos
        objetos = ollama.generate(
            prompt=PROMPT_OBJECTS,
            context=edital.objeto
        )
        
        # Prompt 3: Requisitos
        requisitos = ollama.generate(
            prompt=PROMPT_REQUIREMENTS,
            context=edital.documentos
        )
        
        # ... mais análises
        
        return Analise(
            resumo=resumo,
            objetos=objetos,
            requisitos=requisitos,
            # ...
        )
```

### Estágio 4: Geração de Artefatos
```python
# artefato_generator.py
class ArtefatoGenerator:
    def generate_excel(analise: Analise) -> str:
        """Gera planilha Excel com:
        - Aba 1: Resumo executivo
        - Aba 2: Objetos/Itens
        - Aba 3: Requisitos/Documentos
        - Aba 4: Prazos/Timeline
        - Aba 5: Checklist de conformidade
        """
    
    def generate_pdf(analise: Analise) -> str:
        """Gera PDF com:
        - Capa com dados do edital
        - Resumo executivo formatado
        - Tabelas de objetos
        - Checklist de requisitos
        - Timeline de prazos
        """
    
    def generate_word(analise: Analise) -> str:
        """Gera DOCX editável com:
        - Estrutura profissional
        - Espaços para anotações
        - Tabelas estruturadas
        """
    
    def generate_email(analise: Analise) -> str:
        """Gera e-mail com:
        - Assunto: [EDITAL] Número - Órgão
        - Corpo: Resumo + prazos críticos
        - Anexos: Excel com detalhes
        """
```

---

## 📊 MODELOS DE DADOS

### Edital
```python
@dataclass
class Edital:
    id: str                           # UUID
    numero: str                       # Ex: "2026/001"
    orgao: str                        # Ex: "Prefeitura de Curitiba"
    modalidade: str                   # "pregão", "concorrência", "tomada de preço"
    objeto: str                       # Descrição do que está sendo licitado
    texto_completo: str               # Texto bruto do edital
    data_upload: datetime
    data_publicacao: Optional[datetime]
    
    # Estrutura
    secoes: List[Secao]              # Seções identificadas
    objetos: List[Objeto]            # Itens/Objetos
    requisitos: List[Requisito]      # Documentos obrigatórios
    prazos: List[Prazo]              # Datas críticas
    
    # Status
    status: str                       # "processando", "concluído", "erro"
    progresso: int                    # 0-100%
```

### Objeto
```python
@dataclass
class Objeto:
    numero: int                       # Ex: 1, 2, 3
    descricao: str                    # Descrição do objeto
    quantidade: float
    unidade: str                      # "un", "kg", "m", etc
    valor_estimado: Optional[float]
    modalidade_entrega: str           # "FOB", "CIF", etc
    especificacoes: Optional[str]     # Detalhes técnicos
    fabricante_sugerido: Optional[str]
```

### Requisito
```python
@dataclass
class Requisito:
    tipo: str                         # "habilitação", "técnico", "legal"
    descricao: str
    obrigatorio: bool
    prazo_validade: Optional[str]
    observacoes: Optional[str]
```

### Prazo
```python
@dataclass
class Prazo:
    descricao: str                    # Ex: "Encerramento de inscrições"
    data: datetime
    hora: Optional[str]
    dias_para_evento: int             # Dias até este prazo
    critico: bool                     # True se próximo (< 7 dias)
```

### Analise
```python
@dataclass
class Analise:
    edital_id: str
    resumo_executivo: str             # 2-3 parágrafos
    objetos_identificados: List[Objeto]
    requisitos_identificados: List[Requisito]
    prazos_identificados: List[Prazo]
    riscos: List[str]                 # Potenciais problemas
    oportunidades: List[str]          # Vantagens competitivas
    recomendacoes: List[str]          # Ações sugeridas
    score_conformidade: float         # 0-100%
    data_analise: datetime
```

---

## 📤 SAÍDA (OUTPUT)

### Formatos de Saída

#### 1. Excel (.xlsx)
```
Abas:
- Resumo Executivo
  - Dados do edital
  - Resumo em texto
  - Prazos críticos
  
- Objetos/Itens
  - Número
  - Descrição
  - Quantidade
  - Valor
  - Especificações
  
- Requisitos/Documentos
  - Tipo
  - Descrição
  - Obrigatório?
  - Prazo de validade
  
- Prazos/Timeline
  - Data
  - Descrição
  - Dias para evento
  - Status (crítico?)
  
- Checklist de Conformidade
  - Item
  - Conformidade (Sim/Não/Parcial)
  - Observações
```

#### 2. PDF (.pdf)
```
Conteúdo:
- Capa (logo, dados do edital)
- Resumo executivo (1 página)
- Tabela de objetos (formatada)
- Checklist de requisitos
- Timeline de prazos
- Análise de riscos/oportunidades
- Recomendações finais
```

#### 3. Word (.docx)
```
Conteúdo:
- Estrutura profissional
- Espaços para anotações
- Tabelas editáveis
- Campos para preenchimento manual
- Espaço para assinatura
```

#### 4. E-mail
```
Assunto: [EDITAL] Nº 2026/001 - Prefeitura de Curitiba - AÇÃO REQUERIDA

Corpo:
- Resumo do edital (2 parágrafos)
- Prazos críticos (lista)
- Score de conformidade
- Link para análise completa

Anexo: Planilha Excel com detalhes
```

### Exemplo de Resposta JSON (CLI)
```json
{
  "status": "success",
  "edital_id": "uuid-123",
  "numero_edital": "2026/001",
  "orgao": "Prefeitura de Curitiba",
  "tempo_processamento_segundos": 45,
  "objetos_identificados": 5,
  "requisitos_identificados": 12,
  "prazos_identificados": 8,
  "score_conformidade": 85.5,
  "arquivos_gerados": {
    "excel": "output/edital_2026_001.xlsx",
    "pdf": "output/edital_2026_001.pdf",
    "word": "output/edital_2026_001.docx",
    "email": "output/edital_2026_001_email.txt"
  },
  "resumo_executivo": "Edital de pregão para fornecimento de...",
  "prazos_criticos": [
    {
      "descricao": "Encerramento de inscrições",
      "data": "2026-08-15",
      "dias_para_evento": 3
    }
  ],
  "recomendacoes": [
    "Verificar certificação ISO 9001",
    "Preparar proposta de preço competitiva",
    "Confirmar capacidade de entrega"
  ]
}
```

---

## 🔌 INTEGRAÇÃO COM TAPOS

### Camada de Integração (integration/)

#### integration/schemas.py
```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EditalRunResult:
    status: str                       # "success" ou "error"
    edital_id: str
    numero_edital: str
    orgao: str
    tempo_processamento: float        # segundos
    objetos_identificados: int
    requisitos_identificados: int
    prazos_identificados: int
    score_conformidade: float         # 0-100%
    resumo_executivo: str
    prazos_criticos: List[dict]
    recomendacoes: List[str]
    arquivos_gerados: dict            # paths dos artefatos
    error: Optional[str] = None
```

#### integration/facade.py
```python
from integration.runner import execute_pipeline
from integration.schemas import EditalRunResult

def run_edital_ai(arquivo_path: str) -> EditalRunResult:
    """Interface pública para execução"""
    result = execute_pipeline(arquivo_path)
    return result
```

#### integration/runner.py
```python
from app.edital_ai_app import EditalAIApp
from integration.schemas import EditalRunResult

def execute_pipeline(arquivo_path: str) -> EditalRunResult:
    """Executa a pipeline completa"""
    app = EditalAIApp()
    analise = app.run(arquivo_path)
    
    return EditalRunResult(
        status="success",
        edital_id=analise.edital_id,
        numero_edital=analise.numero_edital,
        # ... mais campos
    )
```

#### integration/cli.py
```python
import json
import sys
from integration.facade import run_edital_ai

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "error": "Uso: python cli.py <arquivo_edital>"
        }), file=sys.stderr)
        sys.exit(1)
    
    arquivo = sys.argv[1]
    
    try:
        result = run_edital_ai(arquivo)
        # Imprime JSON no stdout
        print(json.dumps(result.__dict__, indent=2))
        sys.exit(0)
    except Exception as e:
        # Erro vai para stderr
        print(json.dumps({
            "status": "error",
            "error": str(e)
        }), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Adapter no Backend

#### platform/saas-backend/app/products/edital_ai_adapter.py
```python
import subprocess
import json
from pathlib import Path

class EditalAIAdapter:
    def __init__(self, product_path: str):
        self.product_path = Path(product_path)
        self.venv_python = self.product_path / ".venv" / "bin" / "python"
        self.cli_script = self.product_path / "integration" / "cli.py"
    
    def run(self, arquivo_path: str) -> dict:
        """Executa edital-ai via subprocess"""
        cmd = [str(self.venv_python), str(self.cli_script), arquivo_path]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.product_path)
        )
        
        if result.returncode != 0:
            error_data = json.loads(result.stderr)
            raise Exception(error_data.get("error"))
        
        return json.loads(result.stdout)
```

### Endpoints no Backend

#### platform/saas-backend/app/routes/products.py

```python
@router.post("/products/edital-ai/analyze")
async def analyze_edital(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    product_access = Depends(get_product_access("edital-ai"))
):
    """
    Analisa um edital
    
    - **file**: Arquivo do edital (PDF, DOCX)
    - **Returns**: Análise estruturada + artefatos
    """
    # Salva arquivo temporário
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    # Executa via adapter
    adapter = EditalAIAdapter("products/edital-ai")
    result = adapter.run(temp_path)
    
    # Retorna resultado
    return {
        "status": "success",
        "data": result,
        "user_id": current_user.id
    }


@router.get("/products/edital-ai/historico")
async def get_historico(
    current_user: User = Depends(get_current_user),
    product_access = Depends(get_product_access("edital-ai"))
):
    """Lista análises anteriores do usuário"""
    # Busca no banco de dados
    analises = db.query(EditalAnalise).filter(
        EditalAnalise.user_id == current_user.id
    ).all()
    
    return {"analises": analises}


@router.get("/products/edital-ai/download/{analise_id}")
async def download_artefato(
    analise_id: str,
    formato: str = "excel",  # excel, pdf, word, email
    current_user: User = Depends(get_current_user),
    product_access = Depends(get_product_access("edital-ai"))
):
    """Download dos artefatos gerados"""
    # Busca análise
    analise = db.query(EditalAnalise).filter(
        EditalAnalise.id == analise_id,
        EditalAnalise.user_id == current_user.id
    ).first()
    
    if not analise:
        raise HTTPException(status_code=404)
    
    # Retorna arquivo
    caminho = analise.arquivos_gerados.get(formato)
    return FileResponse(caminho)
```

---

## 🧠 INTEGRAÇÃO COM OLLAMA

### Configuração
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral  # ou neural-chat, llama2, etc
```

### Serviço Ollama
```python
# services/ollama_service.py
class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = os.getenv("OLLAMA_MODEL", "mistral")
    
    def generate(self, prompt: str, context: str = "") -> str:
        """
        Gera resposta usando Ollama
        
        Args:
            prompt: Instrução do que fazer
            context: Contexto/texto para análise
        
        Returns:
            Resposta estruturada
        """
        full_prompt = f"{prompt}\n\nContexto:\n{context}"
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False
            }
        )
        
        return response.json()["response"]
    
    def extract_json(self, prompt: str, context: str) -> dict:
        """Gera resposta em JSON estruturado"""
        response = self.generate(prompt, context)
        # Parse JSON da resposta
        return json.loads(response)
```

### Prompts Otimizados

#### Extração de Seções
```
Você é um especialista em licitações públicas. Analise o texto do edital abaixo e identifique as seguintes seções:

1. Cabeçalho (órgão, número, modalidade)
2. Objeto (o que está sendo licitado)
3. Prazos (datas críticas)
4. Documentos de habilitação
5. Especificações técnicas
6. Critérios de julgamento
7. Valores e formas de pagamento

Retorne em JSON estruturado.
```

#### Extração de Objetos
```
Extraia todos os objetos/itens do edital. Para cada um, identifique:
- Número do item
- Descrição
- Quantidade
- Unidade
- Valor estimado (se disponível)
- Especificações técnicas

Retorne como array JSON.
```

#### Resumo Executivo
```
Faça um resumo executivo do edital em 2-3 parágrafos, destacando:
- O que está sendo licitado
- Prazos críticos
- Requisitos principais
- Oportunidades/Riscos

Seja conciso e objetivo.
```

---

## 📦 DEPENDÊNCIAS

### Python
```
# Extração de documentos
pdfplumber>=0.10.0          # Extração de PDF
pdf2image>=1.16.0           # PDF → Imagem
pytesseract>=0.3.10         # OCR
python-docx>=0.8.11         # Leitura de DOCX
python-pptx>=0.6.21         # Leitura de PPTX

# Processamento
pandas>=2.0.0               # Manipulação de dados
numpy>=1.24.0               # Cálculos numéricos
regex>=2023.0.0             # Regex avançado

# Geração de artefatos
openpyxl>=3.10.0            # Geração de Excel
reportlab>=4.0.0            # Geração de PDF
python-docx>=0.8.11         # Geração de Word
jinja2>=3.1.0               # Templates

# IA e integração
requests>=2.31.0            # HTTP para Ollama
ollama>=0.1.0               # Cliente Ollama (se disponível)

# Banco de dados
sqlalchemy>=2.0.0           # ORM
psycopg2-binary>=2.9.0      # PostgreSQL driver

# Utilitários
python-dotenv>=1.0.0        # Variáveis de ambiente
pydantic>=2.0.0             # Validação de dados
loguru>=0.7.0               # Logging estruturado
```

### Sistema Operacional
```
Tesseract OCR               # OCR para imagens
Poppler                     # Renderização de PDFs
Ollama                      # IA local
```

---

## ⚙️ CONFIGURAÇÃO

### settings.json
```json
{
    "input": {
        "diretorio": "input",
        "formatos_suportados": ["pdf", "docx", "txt"]
    },
    "output": {
        "diretorio": "output",
        "formatos": ["excel", "pdf", "word", "email"]
    },
    "ollama": {
        "base_url": "http://localhost:11434",
        "model": "mistral",
        "timeout": 120
    },
    "processamento": {
        "max_tamanho_mb": 50,
        "timeout_segundos": 300,
        "usar_cache": true
    },
    "projeto": {
        "nome": "Edital AI",
        "versao": "1.0.0"
    }
}
```

### .env
```
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Banco de dados
DATABASE_URL=postgresql+psycopg2://admin:admin@postgres:5432/platform

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/edital_ai.log

# Processamento
MAX_TAMANHO_MB=50
TIMEOUT_SEGUNDOS=300
```

---

## 🔄 FLUXO DE EXECUÇÃO

### Modo Standalone (main.py)
```python
from app import EditalAIApp

app = EditalAIApp()
resultado = app.run("input/edital_2026_001.pdf")

print(f"Status: {resultado.status}")
print(f"Objetos: {resultado.objetos_identificados}")
print(f"Conformidade: {resultado.score_conformidade}%")
```

### Modo TAPOS (via Backend)
```
1. Usuário faz upload via UI
   POST /products/edital-ai/analyze

2. Backend recebe arquivo
   - Valida autenticação (JWT)
   - Valida subscription ativa

3. Backend chama adapter
   - Executa CLI via subprocess
   - Captura stdout (JSON)

4. Backend retorna resultado
   - Salva no banco de dados
   - Retorna ao usuário

5. Usuário faz download de artefatos
   GET /products/edital-ai/download/{id}?formato=excel
```

---

## 🧪 TESTES

### Testes Unitários
```python
# tests/test_extractor.py
def test_extract_from_pdf():
    """Testa extração de PDF"""
    extractor = EditalExtractor()
    texto = extractor.extract_from_pdf("test_edital.pdf")
    assert len(texto) > 0
    assert "edital" in texto.lower()

# tests/test_parser.py
def test_parse_edital():
    """Testa parsing de edital"""
    parser = EditalParser()
    edital = parser.parse(texto_bruto)
    assert edital.numero is not None
    assert len(edital.objetos) > 0

# tests/test_analyzer.py
def test_analyze_edital():
    """Testa análise com IA"""
    analyzer = EditalAnalyzer()
    analise = analyzer.analyze(edital)
    assert len(analise.resumo_executivo) > 0
    assert len(analise.recomendacoes) > 0
```

### Testes de Integração
```python
# tests/test_integration.py
def test_full_pipeline():
    """Testa pipeline completa"""
    app = EditalAIApp()
    resultado = app.run("test_edital.pdf")
    assert resultado.status == "success"
    assert resultado.score_conformidade > 0
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Estrutura Base
- [ ] Criar estrutura de diretórios
- [ ] Configurar requirements.txt
- [ ] Criar ConfigManager
- [ ] Criar modelos (dataclasses)
- [ ] Criar main.py com ponto de entrada

### Fase 2: Pipeline de Extração
- [ ] Implementar EditalExtractor (PDF, DOCX, TXT)
- [ ] Implementar EditalParser (estruturação)
- [ ] Testes de extração

### Fase 3: Análise com IA
- [ ] Integrar Ollama
- [ ] Implementar prompts otimizados
- [ ] Implementar EditalAnalyzer
- [ ] Testes de análise

### Fase 4: Geração de Artefatos
- [ ] Implementar ExcelGenerator
- [ ] Implementar PDFGenerator
- [ ] Implementar WordGenerator
- [ ] Implementar EmailGenerator

### Fase 5: Integração TAPOS
- [ ] Criar integration/schemas.py
- [ ] Criar integration/facade.py
- [ ] Criar integration/runner.py
- [ ] Criar integration/cli.py
- [ ] Criar adapter no backend
- [ ] Implementar endpoints

### Fase 6: Testes e Documentação
- [ ] Testes unitários
- [ ] Testes de integração
- [ ] Documentação técnica
- [ ] README.md

---

## 🚀 PRÓXIMOS PASSOS

1. **Aprovação de Especificações**
   - Revisar com stakeholders
   - Ajustar requisitos se necessário

2. **Configuração do Ambiente**
   - VSCode + Claude Code
   - Repositório Git
   - Ambiente local com Ollama

3. **Desenvolvimento Iterativo**
   - Fase 1: Estrutura (1-2 dias)
   - Fase 2: Extração (2-3 dias)
   - Fase 3: Análise (3-4 dias)
   - Fase 4: Artefatos (2-3 dias)
   - Fase 5: Integração (2-3 dias)
   - Fase 6: Testes (1-2 dias)

4. **Deploy e Validação**
   - Deploy em ambiente de staging
   - Testes com editais reais
   - Ajustes finais
   - Deploy em produção

---

**Especificações Versão**: 1.0.0  
**Data**: 13/07/2026  
**Status**: Pronto para Claude Code  
**Próximo Passo**: Iniciar desenvolvimento com VSCode + Claude Code
