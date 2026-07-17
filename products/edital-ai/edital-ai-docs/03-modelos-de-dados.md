# 03 — Modelos de dados

Todos os modelos do produto `edital-ai` são `@dataclass` puras (sem ORM, sem
Pydantic, sem validação de schema) — arquivos em `products/edital-ai/models/`.
Isso é intencional: o produto não tem banco de dados próprio; ele só produz
um resultado (JSON) que o backend (`saas-backend`, esse sim com SQLAlchemy)
persiste. Os dois schemas de banco relevantes (`Job` e `EditalAnalise`) estão
na seção final deste arquivo.

## `Objeto` (`models/objeto.py`) — um item/lote da licitação

```python
@dataclass
class Objeto:
    numero: int
    descricao: str
    quantidade: Optional[float] = None
    unidade: Optional[str] = None
    valor_estimado: Optional[float] = None
    modalidade_entrega: Optional[str] = None   # não populado hoje (sempre None)
    especificacoes: Optional[str] = None
    fabricante_sugerido: Optional[str] = None  # não populado hoje (sempre None)
```

- `numero`: número do item/lote conforme a tabela do edital (coluna
  ITEM/LOTE/ORDEM/Nº) — quando ausente na linha, é tratado como continuação
  do item anterior (ver `04-pipeline-e-funcoes.md`), nunca gera número
  sequencial "fantasma" a não ser como último recurso.
- `especificacoes`: texto complementar da descrição (linhas extras dentro da
  mesma célula, ou texto de continuação vindo de quebra de página).
- `modalidade_entrega` e `fabricante_sugerido` existem no modelo mas **nunca
  são preenchidos** pelo parser atual — são campos "reservados" para uma
  extração mais rica no futuro.

## `Requisito` (`models/requisito.py`) — documento/condição de habilitação

```python
@dataclass
class Requisito:
    tipo: str                          # ex.: "habilitação", ou a categoria da tabela (ex.: "regularidade fiscal e trabalhista")
    descricao: str
    obrigatorio: bool = True           # hoje SEMPRE True — não há extração de requisitos opcionais
    prazo_validade: Optional[str] = None  # não populado hoje
    observacoes: Optional[str] = None     # não populado hoje
```

## `Prazo` (`models/prazo.py`) — data crítica do edital

```python
@dataclass
class Prazo:
    descricao: str          # ex.: "Abertura", "Recurso", "Publicação"
    data_texto: str          # a data exatamente como apareceu no texto (ex.: "13/07/2026")
    data: Optional[datetime] = None       # data_texto interpretada (dateutil), pode falhar -> None
    hora: Optional[str] = None            # nunca populado hoje (fica sempre None)
    dias_para_evento: Optional[int] = None
    critico: bool = False    # True quando 0 <= dias_para_evento < 7
```

## `Secao` e `Edital` (`models/edital.py`)

```python
@dataclass
class Secao:
    titulo: str
    conteudo: str

@dataclass
class Edital:
    id: str                              # uuid4, gerado no parser
    numero: Optional[str] = None          # ex.: "032/2026"
    orgao: Optional[str] = None
    modalidade: Optional[str] = None
    objeto: Optional[str] = None
    texto_completo: str = ""              # todo o texto extraído do documento
    data_upload: datetime = field(default_factory=datetime.now)

    secoes: List[Secao] = field(default_factory=list)   # nunca populado hoje (lista sempre vazia)
    objetos: List[Objeto] = field(default_factory=list)
    requisitos: List[Requisito] = field(default_factory=list)
    prazos: List[Prazo] = field(default_factory=list)

    status: str = "processando"           # "processando" -> "extraido" -> "concluido"
```

`secoes` existe no modelo mas o parser nunca o preenche — é vestígio de uma
ideia de segmentar o edital em seções nomeadas que não chegou a ser
implementada.

## `Analise` (`models/analise.py`) — saída qualitativa

```python
@dataclass
class Analise:
    edital_id: str
    resumo_executivo: str = ""
    objetos_identificados: List[Objeto] = field(default_factory=list)     # cópia de edital.objetos
    requisitos_identificados: List[Requisito] = field(default_factory=list)  # cópia de edital.requisitos
    prazos_identificados: List[Prazo] = field(default_factory=list)          # cópia de edital.prazos
    riscos: List[str] = field(default_factory=list)
    oportunidades: List[str] = field(default_factory=list)
    recomendacoes: List[str] = field(default_factory=list)
    score_conformidade: float = 0.0        # 0-100
    ia_utilizada: bool = False              # False quando caiu no fallback determinístico
    data_analise: datetime = field(default_factory=datetime.now)
```

Note que `objetos_identificados`/`requisitos_identificados`/
`prazos_identificados` são exatamente as mesmas listas já extraídas
estruturalmente pelo `EditalParser` — a IA (Ollama) **não participa** da
extração de itens/requisitos/prazos, só do resumo/riscos/oportunidades/
recomendações/score. Isso é uma decisão de design importante: a extração
estrutural é 100% determinística (regex + leitura de tabela), e só a camada
qualitativa depende de LLM.

## `Artefato` (`models/artefato.py`) — paths dos arquivos gerados

```python
@dataclass
class Artefato:
    excel: Optional[str] = None
    pdf: Optional[str] = None
    word: Optional[str] = None
    email: Optional[str] = None
```

## `EditalRunResult` (`integration/schemas.py`) — o JSON de saída do subprocesso

Este é o contrato entre o produto `edital-ai` e o adapter do backend — é
literalmente o que sai no `stdout` do `cli.py`:

```python
@dataclass
class EditalRunResult:
    status: str                            # sempre "executed" quando não lança exceção
    edital_id: str
    numero_edital: Optional[str]
    orgao: Optional[str]
    modalidade: Optional[str]
    objetos_identificados: int             # contagem, não a lista completa
    requisitos_identificados: int
    prazos_identificados: int
    score_conformidade: float
    ia_utilizada: bool
    resumo_executivo: str
    prazos_criticos: List[dict] = field(default_factory=list)   # {"descricao", "data"} — só os críticos ou os 3 primeiros
    riscos: List[str] = field(default_factory=list)
    oportunidades: List[str] = field(default_factory=list)
    recomendacoes: List[str] = field(default_factory=list)
    arquivos_gerados: Dict[str, Optional[str]] = field(default_factory=dict)  # {"excel":..., "pdf":..., "word":..., "email":...}
```

Importante: `EditalRunResult` **não inclui a lista completa de itens,
requisitos e prazos** — só as contagens. Quem quiser a lista completa precisa
abrir o Excel gerado (aba "Objetos e Itens" etc.) ou o PDF/Word. Isso é uma
limitação de API a considerar na versão comercial (ver
`08-briefing-para-comercializacao.md`).

## Schemas de banco de dados (SQLAlchemy, em `platform/saas-backend/app/models.py`)

```python
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_slug = Column(String, nullable=False)   # "edital-ai", "code-ai", "speech-ai"
    status = Column(String, nullable=False, default="queued")  # queued -> running -> completed/failed
    created_at = Column(DateTime(timezone=True), ...)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    result_json = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)

class EditalAnalise(Base):
    __tablename__ = "edital_analises"
    id = Column(Integer, primary_key=True, index=True)
    analise_id = Column(String, unique=True, index=True, nullable=False)  # = Edital.id
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(String, nullable=True)     # preenchido só no fluxo assíncrono
    numero_edital = Column(String, nullable=True)
    orgao = Column(String, nullable=True)
    modalidade = Column(String, nullable=True)
    score_conformidade = Column(Float, nullable=True)
    resumo_executivo = Column(String, nullable=True)
    arquivos_gerados = Column(JSON, nullable=True)   # os 4 paths locais no disco do servidor
    result_json = Column(JSON, nullable=True)        # o EditalRunResult completo
    created_at = Column(DateTime(timezone=True), ...)
```

`Job` é compartilhado entre todos os produtos (speech-ai, code-ai, edital-ai)
— é o mecanismo genérico de fila/status. `EditalAnalise` é específico do
edital-ai e é o que alimenta o histórico (`GET /products/edital-ai/historico`)
e os downloads (`GET /products/edital-ai/download/{analise_id}`).

Ponto de atenção para a versão comercial: **`arquivos_gerados` guarda paths
absolutos no disco local do servidor** (`/workspace/tecle/products/edital-ai/
output/...`) — não URLs de um object storage. Isso funciona apenas enquanto
houver uma única instância do backend rodando na mesma máquina que gerou os
arquivos (ver `07-limitacoes-e-debito-tecnico.md`).
