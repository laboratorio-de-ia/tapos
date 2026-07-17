# 04 — Pipeline e funções (referência completa)

O pipeline tem 4 estágios sequenciais, orquestrados por
`app/edital_ai_app.py::EditalAIApp.run()`. Cada estágio é descrito abaixo com
as funções reais (assinatura + comportamento), não pseudo-código.

```python
# app/edital_ai_app.py
class EditalAIApp:
    def __init__(self):
        self.cfg = ConfigManager()
        self.project_root = Path(__file__).resolve().parent.parent
        self.analyzer = EditalAnalyzer(self.cfg)
        self.artefato_generator = ArtefatoGenerator(
            output_dir=str(self.project_root / self.cfg.output_directory)
        )

    def run(self, arquivo_path: str):
        nome_documento = Path(arquivo_path).stem
        texto, tabelas = EditalExtractor.extract_full(arquivo_path)
        edital = EditalParser.parse(texto, tabelas=tabelas)
        analise = self.analyzer.analyze(edital)
        artefatos = self.artefato_generator.generate_all(
            edital, analise, nome_documento=nome_documento
        )
        edital.status = "concluido"
        return edital, analise, artefatos
```

`nome_documento` (o nome do arquivo sem extensão) é propagado até o gerador
de artefatos para que os 4 arquivos de saída tenham **o mesmo nome do
documento carregado**, do início ao fim do fluxo — essa é uma característica
deliberada do produto (histórico: antes disso, o nome do arquivo enviado se
perdia e os outputs saíam com nomes genéricos ou baseados no número do
edital extraído do texto).

---

## Estágio 1 — Extração (`pipeline/edital_extractor.py` + `services/*_service.py`)

```python
class EditalExtractor:
    @staticmethod
    def extract(caminho: str) -> str:
        """Compatibilidade: só o texto."""

    @staticmethod
    def extract_full(caminho: str) -> Tuple[str, List[list]]:
        """Extensão determina o extrator:
        .pdf         -> extract_text_from_pdf + extract_tables_from_pdf
        .docx/.doc   -> extract_text_from_docx (sem tabelas)
        .txt/.md     -> leitura direta (sem tabelas)
        qualquer outra -> ValueError("Formato não suportado pelo edital-ai")
        Texto sempre passa por limpar_texto() (normaliza espaços/quebras)."""
```

- `services/pdf_service.py`:
  - `extract_text_from_pdf(caminho)`: usa **pdfplumber** página a página. Se o
    PDF não tiver camada de texto (escaneado), cai em **fallback OCR**
    (`pdf2image.convert_from_path` + `pytesseract.image_to_string(lang="por")`).
  - `extract_tables_from_pdf(caminho)`: usa `page.extract_tables()` do
    pdfplumber em cada página, retornando **cada tabela detectada como um
    bloco independente** (lista de linhas). Isso é crítico: tabelas de itens
    que atravessam várias páginas **não vêm como um bloco único** — vêm como
    vários blocos separados, e só o primeiro normalmente repete o cabeçalho
    (ver a heurística de continuação no Estágio 2).
- `services/docx_service.py::extract_text_from_docx`: usa `python-docx`,
  concatena parágrafos e também achata tabelas do Word em linhas
  `"célula1 | célula2 | ..."`.
- `services/text_cleaner.py::limpar_texto`: normaliza `\r\n`/`\r` para `\n`,
  colapsa espaços/tabs repetidos, e reduz 3+ quebras de linha seguidas a
  apenas 2 (preserva parágrafos).

---

## Estágio 2 — Parsing (`pipeline/edital_parser.py`)

Toda a extração estrutural é **regex + heurística determinística** — não usa
IA. Ponto de entrada:

```python
class EditalParser:
    @staticmethod
    def parse(texto_completo: str, tabelas: Optional[List[list]] = None) -> Edital:
        edital = Edital(id=str(uuid.uuid4()), texto_completo=texto_completo)
        edital.numero = extract_numero(texto_completo)
        edital.orgao = extract_orgao(texto_completo)
        edital.modalidade = extract_modalidade(texto_completo)
        edital.objeto = extract_objeto(texto_completo)
        edital.prazos = extract_prazos(texto_completo)
        # tabelas nativas são preferidas; cai para regex em prosa só se não houver tabela reconhecível
        requisitos_tabela = extract_requisitos_de_tabelas(tabelas or [])
        edital.requisitos = requisitos_tabela if requisitos_tabela else extract_requisitos(texto_completo)
        objetos_tabela = extract_objetos_de_tabelas(tabelas or [])
        edital.objetos = objetos_tabela if objetos_tabela else extract_objetos(texto_completo)
        edital.status = "extraido"
        return edital
```

### `extract_numero(texto)`

```python
REGEX_NUMERO_EDITAL = re.compile(
    r"(?:edital|processo(?:\s+administrativo)?|preg[aã]o|licita[cç][aã]o)\s*"
    r"n?[ºo°]?\s*[:\-]?\s*([\d]{1,6}\s*[/\-]\s*[\d]{2,4})",
    re.IGNORECASE,
)
```
Casa "Edital nº 032/2026", "Pregão 014/2026", etc. Primeira ocorrência.

### `extract_orgao(texto)`

Duas estratégias, na ordem:
1. `REGEX_ORGAO_FORMULA`: casa a fórmula legal padrão brasileira **"A/O
   `<ÓRGÃO>` ... torna público/pública"** — muito mais confiável que buscar
   palavras-chave soltas (evita capturar menções incidentais no meio de
   cláusulas, ex.: "Secretaria da Receita Federal" citada dentro de uma regra
   de habilitação).
2. Fallback: `REGEX_ORGAO` busca por palavras-chave (`prefeitura`,
   `secretaria`, `ministério`, `universidade`, `câmara municipal`, `governo
   do estado`, `autarquia`, `fundação`, `instituto federal`), mas **só dentro
   dos primeiros 2000 caracteres do documento** (`TAMANHO_CABECALHO_ORGAO`),
   para não pegar menções fora do cabeçalho.

### `extract_modalidade(texto)`

Busca substring simples (case-insensitive) contra a lista fixa:
`pregão eletrônico, pregão presencial, concorrência, tomada de preços,
convite, concurso, leilão, dispensa de licitação, inexigibilidade,
credenciamento`. Primeira que der match.

### `extract_objeto(texto)`

Duas estratégias:
1. `REGEX_OBJETO_CABECALHO`: casa um cabeçalho `"OBJETO: <descrição>"` nos
   primeiros 3000 caracteres — padrão comum em editais de portais estaduais.
2. Fallback `REGEX_OBJETO_CLAUSULA`: casa frases como "tem por objeto",
   "do objeto", "objeto:" em qualquer parte do texto.

### `extract_prazos(texto)`

Varre linha a linha procurando uma das `PALAVRAS_CHAVE_PRAZO` (`abertura,
encerramento, recebimento das propostas, sessão pública, recurso,
impugnação, entrega dos envelopes, publicação`). Ao achar, olha uma **janela
das próximas 3 linhas** (a palavra-chave e a data frequentemente ficam em
linhas separadas por causa de como o PDF quebra o cabeçalho em caixas) e
extrai a primeira data via `REGEX_DATA`. Tenta interpretar com
`dateutil.parser.parse(dayfirst=True, fuzzy=True)`; se falhar, guarda só o
texto bruto da data (`data=None`). Marca `critico=True` quando
`0 <= dias_para_evento < 7`. Deduplica por `(palavra, data_texto)`.

### `extract_requisitos_de_tabelas(tabelas)` / `extract_requisitos(texto)`

- **Tabelas**: procura um bloco de 2 colunas cujo cabeçalho contenha
  "HABILITA" — comum em editais que listam documentos exigidos numa tabela
  numérica + descrição, intercalada com linhas de subtítulo de categoria
  (coluna da descrição vazia = atualiza só a "categoria corrente", não vira
  um requisito).
- **Fallback em prosa**: localiza a seção de habilitação (cabeçalho numerado
  "N. DA HABILITAÇÃO" ou, se ausente, a primeira ocorrência da palavra
  "habilitação"/"documentos de habilitação"), corta o bloco até a próxima
  seção (`REGEX_PROXIMA_SECAO`, limitado a 6000 caracteres), e extrai cada
  linha que comece com marcador de item (`a)`, `I -`, `7.6.1.`, `-`, `•`).

### `extract_objetos_de_tabelas(tabelas)` — a função mais crítica do pipeline

Esta é a função responsável por preencher a tabela de itens da aba "Modelo"
(a única aba da planilha de precificação) e as tabelas equivalentes no
PDF/Word. Ela já passou por uma correção
importante (ver `07-limitacoes-e-debito-tecnico.md` para o histórico) e hoje
funciona assim:

1. Para cada bloco de tabela (`tabelas` vem do pdfplumber, um bloco por
   página/grupo), tenta reconhecer um **cabeçalho válido**: precisa de uma
   coluna de descrição (`"DESCRI"` ou `"ESPECIFICA"` no nome normalizado) +
   uma coluna de quantidade (`"QTD"`/`"QUANT"`) + pelo menos uma coluna
   numeradora (`ITEM`, `LOTE`, `ORDEM`, `Nº`, `N°`, `SEQ`, `SEQUÊNCIA`).
   Também detecta colunas opcionais de unidade (`UNID`, `U.F`, `UN`, `UN.`) e
   valor unitário (`VALOR` + `UNIT`).
2. **Heurística de continuação entre páginas**: quando um bloco de tabela
   **não** tem cabeçalho reconhecível, mas tem o **mesmo número de colunas**
   do último cabeçalho válido visto, é tratado como continuação da mesma
   tabela de itens (comum quando a tabela atravessa uma quebra de página no
   pdfplumber). Se o número de colunas mudar, o mapeamento é descartado (não
   arrisca aplicar colunas erradas a uma tabela não relacionada).
3. Para cada linha de dados: se a coluna numeradora tiver um dígito, é um
   **item novo**. Se não tiver (linha "órfã", tipicamente a sobra de uma
   descrição que quebrou exatamente na virada de página), o texto é
   **anexado às `especificacoes` do último item já adicionado**, em vez de
   virar um item fantasma sem quantidade/valor.
4. Linhas com a célula de descrição vazia são ignoradas (linhas de template
   em branco de planilhas de proposta a preencher).
5. Limite de segurança: para de coletar em 1000 itens.

### `extract_objetos(texto)` — fallback em prosa (sem tabelas)

```python
REGEX_ITEM = re.compile(r"^\s*(?:item|lote)\s*(\d{1,3})\s*[-–:.)]\s*(.{5,200})$", re.IGNORECASE | re.MULTILINE)
REGEX_QUANTIDADE_UNIDADE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(un|und|unidade[s]?|kg|cx|caixa[s]?|pç|pçs|peça[s]?|m|metro[s]?|l|litro[s]?|serviço[s]?)", re.IGNORECASE)
REGEX_VALOR = re.compile(r"R\$\s?[\d.]+,\d{2}")
```
Usado só quando o documento não tem tabelas nativas reconhecíveis (ex.:
`.docx`/`.txt`, ou um PDF sem estrutura de tabela). Menos confiável que a
extração por tabela — é o fallback, não o caminho principal.

---

## Estágio 3 — Análise qualitativa (`pipeline/edital_analyzer.py`)

```python
class EditalAnalyzer:
    def __init__(self, cfg: ConfigManager):
        self.ollama = OllamaService(base_url=cfg.ollama_base_url, model=cfg.ollama_model, timeout=cfg.ollama_timeout)
        self.prompt = PROMPT_FILE.read_text(...)   # prompts/generate_summary.txt

    def analyze(self, edital: Edital) -> Analise:
        analise = Analise(edital_id=edital.id,
                           objetos_identificados=edital.objetos,
                           requisitos_identificados=edital.requisitos,
                           prazos_identificados=edital.prazos)
        try:
            contexto = self._construir_contexto(edital)   # resumo estruturado, não o texto bruto
            dados = self.ollama.generate_json(self.prompt, contexto)
            analise.resumo_executivo = dados.get("resumo_executivo", "")
            analise.riscos = list(dados.get("riscos", []))
            analise.oportunidades = list(dados.get("oportunidades", []))
            analise.recomendacoes = list(dados.get("recomendacoes", []))
            analise.score_conformidade = float(dados.get("score_conformidade", 0))
            analise.ia_utilizada = True
        except Exception as exc:
            analise.resumo_executivo = self._resumo_fallback(edital)
            analise.score_conformidade = self._score_fallback(edital)
            analise.riscos = [f"Análise via IA indisponível ({exc}); usando resumo determinístico."]
            analise.ia_utilizada = False
        return analise
```

Pontos de design importantes:

- **`_construir_contexto(edital)`** não manda o texto bruto completo do
  edital para o Ollama — monta um contexto compacto (número, órgão,
  modalidade, objeto, até 30 itens, até 20 requisitos, até 20 prazos, e só os
  primeiros 3000 caracteres do texto original como contexto adicional).
  Isso existe porque mandar até 12000 caracteres de boilerplate jurídico
  bruto era mais lento e chegava a estourar o timeout do Ollama sem ganho de
  qualidade — enviar o que já foi extraído estruturalmente é mais rápido e
  mais alinhado ao que o prompt pede.
- **Qualquer exceção** (timeout, Ollama fora do ar, JSON malformado) cai no
  fallback determinístico — o pipeline **nunca falha por causa da IA**.
  `ia_utilizada=False` sinaliza isso no resultado final.
- `_score_fallback`: soma 20 pontos para cada um dos 5 campos-chave presentes
  (número, órgão, modalidade, objeto, prazos) — é uma métrica de completude
  da **extração**, não de qualidade da licitação.

`services/ollama_service.py::OllamaService.generate_json(prompt, context)`:
chama `POST {base_url}/api/generate` com `"format": "json", "stream": False`,
manda `f"{prompt}\n\nTEXTO DO EDITAL:\n{context[:12000]}"`, e faz parse
tolerante da resposta (remove cercas de code block ```` ``` ```` se vierem, e
se `json.loads` falhar tenta extrair o primeiro `{...}` balanceado do texto).

`prompts/generate_summary.txt` pede um JSON com exatamente as chaves
`resumo_executivo, riscos, oportunidades, recomendacoes, score_conformidade`
— é o único prompt usado hoje (a ideia original de múltiplos prompts por
seção, descrita em `edital.md` da raiz, não foi implementada).

---

## Estágio 4 — Geração de artefatos (`pipeline/artefato_generator.py`)

```python
class ArtefatoGenerator:
    def generate_all(self, edital, analise, nome_documento: Optional[str] = None) -> Artefato:
        if nome_documento:
            slug = self._sanitizar(nome_documento)      # troca tudo que não for [\w-] por "_"
        else:
            slug = f"edital_{(edital.numero or edital.id[:8]).replace('/', '_').replace(' ', '_')}"
        base = self.output_dir / slug
        return Artefato(
            excel=gerar_excel(edital, analise, f"{base}.xlsx"),
            pdf=gerar_pdf(edital, analise, f"{base}.pdf"),
            word=gerar_word(edital, analise, f"{base}.docx"),
            email=gerar_email(edital, analise, f"{base}_email.txt"),
        )
```

O nome base dos 4 arquivos é **sempre o nome do arquivo carregado** (quando
disponível) — só cai para `edital_<número ou id>` quando chamado sem
`nome_documento` (uso direto da API interna, não pelo fluxo normal de
upload).

- **`services/excel_generator.py::gerar_excel`** (openpyxl) — **uma única
  aba** ("Modelo"), estrutura idêntica em toda extração ao template. A
  planilha **não** é montada do zero: `gerar_excel` abre
  `Dom de Limpar - Modelo Precificacao.xlsx` (raiz do produto) como base para
  toda extração, porque essa é a planilha de precificação comercial real que
  o time usa para orçar a licitação — não um relatório genérico com abas
  extras (as demais abas do template original, que vinham de um edital de
  exemplo, são removidas ao final de `gerar_excel`, ficando só "Modelo").
  A aba tem: cabeçalho com título/subtítulo do edital, bloco de parâmetros
  (órgão, número do edital, premissas fixas de negócio — regime tributário,
  alíquota de impostos, margem líquida alvo — em
  `excel_generator.REGIME_TRIBUTARIO_PADRAO` etc.), e a tabela de itens
  (Item/Descrição/Quantidade/Unidade/Entrega preenchidos pela extração;
  colunas de embalagem/preço/impostos/margem ficam em branco — dependem de
  pesquisa de mercado que o edital não fornece, para preenchimento manual
  pelo time de precificação). `_ajustar_linhas_de_itens` insere ou remove
  linhas do bloco de itens do template (que vem de exemplo com 103 itens)
  para caber exatamente na contagem de itens do edital atual, preservando a
  formatação (moeda/percentual) das colunas de precificação, e o bloco
  "Resumo Executivo de Precificação" no rodapé (fórmulas `SUMPRODUCT`) é
  recalculado com o range de linhas correto.
- **`services/pdf_generator.py::gerar_pdf`** (reportlab) — título, tabela de
  cabeçalho, objeto, resumo executivo, tabela de até 20 itens, lista de
  prazos, checklist de requisitos (☐ por item), riscos/oportunidades/
  recomendações — tudo em um único PDF sequencial (sem paginação especial).
- **`services/word_generator.py::gerar_word`** (python-docx) — mesma
  estrutura de conteúdo do PDF, mas em `.docx` editável, com um campo de
  assinatura no final (`"Analisado por: ___ Data: ___"`) pensado para
  anotação manual da equipe.
- **`services/email_generator.py::gerar_email`** — gera um `.txt` puro
  (assunto + corpo pronto), **não envia e-mail de verdade** — é um rascunho
  para copiar/colar ou anexar. Prioriza prazos marcados como `critico=True`;
  se não houver nenhum crítico, usa os 3 primeiros prazos identificados.
