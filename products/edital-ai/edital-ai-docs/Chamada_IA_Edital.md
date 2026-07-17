# Chamada de IA no edital-ai

Este documento detalha a **única chamada de IA** que existe no pipeline do
`edital-ai`: onde ela acontece, por que existe, como é feita na prática (com
trechos de código reais), o que acontece quando ela falha, e onde o
resultado dela aparece (ou não) nos artefatos finais. Complementa
[`04-pipeline-e-funcoes.md`](04-pipeline-e-funcoes.md) (que descreve todo o
pipeline) focando só nesse ponto específico.

## Resumo de uma linha

Depois que o edital já foi extraído e estruturado **por regras** (regex,
tabelas), o pipeline faz **uma única chamada HTTP** a um modelo de linguagem
rodando localmente via **Ollama**, pedindo uma análise qualitativa (resumo,
riscos, oportunidades, recomendações, score) — e se essa chamada falhar por
qualquer motivo, o pipeline **nunca para**: cai automaticamente em um
resumo determinístico gerado por regras.

## Onde, no pipeline, a chamada acontece

O pipeline tem 4 estágios (ver `app/edital_ai_app.py::EditalAIApp.run`):

```
1. Extração   (pipeline/edital_extractor.py)   — texto bruto do PDF/DOCX/TXT/MD
2. Parsing    (pipeline/edital_parser.py)      — regras/regex → Edital estruturado
3. Análise    (pipeline/edital_analyzer.py)    — ★ AQUI ACONTECE A CHAMADA DE IA ★
4. Artefatos  (pipeline/artefato_generator.py) — Excel/PDF/Word/e-mail
```

A chamada de IA é o **Estágio 3**, e só ele. Os estágios 1 e 2 (extração e
parsing) são 100% determinísticos, sem IA — número do edital, órgão,
modalidade, objeto, itens/lotes e requisitos de habilitação são todos
extraídos por regex e leitura de tabelas nativas do documento, não pelo
modelo de linguagem. A IA entra **depois**, só para a parte qualitativa que
regras não conseguem fazer bem (redigir um resumo em prosa, avaliar riscos,
sugerir recomendações).

Ponto de entrada: `pipeline/edital_analyzer.py::EditalAnalyzer.analyze(edital)`,
chamado de `app/edital_ai_app.py`:

```python
def run(self, arquivo_path: str):
    nome_documento = Path(arquivo_path).stem
    texto, tabelas = EditalExtractor.extract_full(arquivo_path)   # Estágio 1
    edital = EditalParser.parse(texto, tabelas=tabelas)            # Estágio 2
    analise = self.analyzer.analyze(edital)                        # Estágio 3 — IA
    artefatos = self.artefato_generator.generate_all(...)          # Estágio 4
    ...
```

## Por que essa chamada existe (motivação)

Tudo que é **factual e estruturado** (número, órgão, itens, prazos,
requisitos) é extraído por regras porque regras são determinísticas,
auditáveis e não "alucinam" — e o parser por regex/tabela já faz esse
trabalho bem (ver `04-pipeline-e-funcoes.md` e
`Chamada_IA_Edital.md#o-que-a-ia-não-faz` abaixo).

O que regras **não fazem bem** é produzir um texto em prosa natural que:

- resuma em 2-3 parágrafos o que está sendo licitado, prazos críticos e
  requisitos principais, de um jeito legível para quem vai decidir se
  participa da licitação;
- aponte riscos e pontos de atenção "escondidos" no texto do edital;
- aponte oportunidades/vantagens competitivas;
- recomende ações concretas para quem for participar;
- estime um "score de conformidade" (o quão completo/claro está o edital
  para participação — não é uma nota da empresa, é do edital em si).

Essa é a parte qualitativa/interpretativa que justifica usar um LLM em vez
de mais regex.

## Como a chamada é feita, passo a passo

### 1. `EditalAnalyzer.__init__` monta o cliente e carrega o prompt

```python
class EditalAnalyzer:
    def __init__(self, cfg: ConfigManager):
        self.cfg = cfg
        self.ollama = OllamaService(
            base_url=cfg.ollama_base_url,
            model=cfg.ollama_model,
            timeout=cfg.ollama_timeout,
        )
        self.prompt = PROMPT_FILE.read_text(encoding="utf-8")  # prompts/generate_summary.txt
```

### 2. `_construir_contexto(edital)` monta o que será enviado ao modelo

Importante: **não** manda o texto bruto inteiro do edital para o modelo.
Manda um contexto compacto, já estruturado pelo que os Estágios 1/2
extraíram:

```python
linhas = [
    f"Número: {edital.numero or '-'}",
    f"Órgão: {edital.orgao or '-'}",
    f"Modalidade: {edital.modalidade or '-'}",
    f"Objeto: {edital.objeto or '-'}",
    "",
    f"Itens/objetos identificados ({len(edital.objetos)} no total, mostrando até 30):",
    # até 30 itens: "- Item {numero}: {descricao} (qtd: {quantidade} {unidade})"
    "",
    f"Requisitos de habilitação identificados ({len(edital.requisitos)} no total, mostrando até 20):",
    # até 20 requisitos: "- {descricao}"
    "",
    f"Prazos identificados ({len(edital.prazos)} no total):",
    # até 20 prazos: "- {descricao}: {data_texto}"
    "",
    "Trecho do texto original (início do edital, para contexto adicional):",
    edital.texto_completo[:3000],
]
```

**Por que não o texto bruto completo:** a primeira versão mandava até 12000
caracteres do texto bruto do edital direto para o modelo. Boa parte desse
trecho inicial é boilerplate jurídico (citação de leis, decretos, preâmbulo
padrão) — não é o conteúdo que importa para o resumo. Isso deixava o prompt
maior e mais lento **sem ganho de qualidade**, e chegou a estourar o timeout
do Ollama em editais reais. Mandar o que o parser (Estágios 1/2) já
extraiu de forma estruturada é mais rápido e mais alinhado ao que o prompt
pede — só os últimos 3000 caracteres do texto original entram "crus", como
contexto complementar.

### 3. A chamada HTTP em si — `OllamaService.generate_json`

```python
def generate_json(self, prompt: str, context: str) -> dict:
    full_prompt = f"{prompt}\n\nTEXTO DO EDITAL:\n{context[:12000]}"
    response = requests.post(
        f"{self.base_url}/api/generate",
        json={
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "format": "json",
        },
        timeout=self.timeout,
    )
    response.raise_for_status()
    return self._parse_json(response.json().get("response", ""))
```

- Endpoint: `POST {OLLAMA_BASE_URL}/api/generate` — a API nativa do Ollama
  (não a API compatível com OpenAI).
- `"format": "json"` — pede ao Ollama para forçar saída em JSON válido.
- `"stream": False` — espera a resposta completa de uma vez (mais simples
  de tratar do que parsear um stream de tokens, ao custo de não ter feedback
  incremental).
- Note que `context` já vem cortado em ~poucos milhares de caracteres por
  `_construir_contexto`, mas o cliente **também** corta em 12000 caracteres
  por segurança (`context[:12000]`) antes de montar o prompt final.
- `_parse_json` é tolerante: remove cercas de code block (```` ``` ````) se
  o modelo devolver o JSON "embrulhado" em markdown (comum em modelos que
  não seguem `format: json` à risca), e se `json.loads` direto falhar,
  tenta extrair o primeiro bloco `{...}` balanceado do texto de resposta.

### 4. O prompt — `prompts/generate_summary.txt`

Único prompt usado hoje no produto (a ideia original de múltiplos prompts
por seção, mencionada em `edital.md` da raiz do workspace, nunca foi
implementada). Pede um JSON com exatamente estas chaves:

```json
{
  "resumo_executivo": "2 a 3 parágrafos resumindo o que está sendo licitado, prazos críticos e requisitos principais",
  "riscos": ["lista de riscos ou pontos de atenção identificados no edital"],
  "oportunidades": ["lista de oportunidades ou vantagens competitivas identificadas"],
  "recomendacoes": ["lista de ações recomendadas para quem for participar da licitação"],
  "score_conformidade": 0
}
```

Regras explícitas no prompt: `score_conformidade` é 0–100 e mede
completude/clareza **do edital**, não é uma nota da empresa participante;
resposta deve ser **só** o JSON (sem texto antes/depois, sem markdown, sem
comentários); campos sem informação suficiente devem vir como lista vazia
ou frase curta explicando a limitação — não devem ser inventados.

## Configuração (de onde vêm `base_url`, `model`, `timeout`)

`config/config_manager.py::ConfigManager`, lidas de `config/settings.json`
com override por variável de ambiente:

```python
@property
def ollama_base_url(self) -> str:
    return os.getenv("OLLAMA_BASE_URL", self.data["ollama"]["base_url"])

@property
def ollama_model(self) -> str:
    return os.getenv("OLLAMA_MODEL", self.data["ollama"]["model"])

@property
def ollama_timeout(self) -> int:
    return int(self.data["ollama"]["timeout"])
```

Valores padrão em `config/settings.json`:

```json
"ollama": {
    "base_url": "http://localhost:11434",
    "model": "mistral",
    "timeout": 300
}
```

Ou seja: por padrão, aponta para um Ollama **rodando localmente** (não é
uma API de nuvem paga), servindo o modelo `mistral`, com timeout de 300s
(5 minutos) por chamada. Pode ser sobrescrito sem editar o arquivo via
`OLLAMA_BASE_URL` / `OLLAMA_MODEL` no ambiente (útil, por exemplo, se o
Ollama rodar em outro host/container, ou para trocar de modelo em teste
sem tocar no `settings.json` versionado).

## O que acontece quando a chamada falha (fallback determinístico)

Este é um ponto de design central do produto: **o pipeline nunca falha por
causa da IA**. Qualquer exceção na chamada — Ollama fora do ar, timeout,
erro de rede, resposta que não é um JSON válido mesmo depois do parse
tolerante — é capturada e o pipeline cai em um resumo gerado por regras:

```python
def analyze(self, edital: Edital) -> Analise:
    analise = Analise(
        edital_id=edital.id,
        objetos_identificados=edital.objetos,       # sempre do parser (Estágio 2), IA não influencia isso
        requisitos_identificados=edital.requisitos,  # idem
        prazos_identificados=edital.prazos,          # idem
    )
    try:
        contexto = self._construir_contexto(edital)
        dados = self.ollama.generate_json(self.prompt, contexto)
        analise.resumo_executivo = dados.get("resumo_executivo", "") or ""
        analise.riscos = list(dados.get("riscos", []) or [])
        analise.oportunidades = list(dados.get("oportunidades", []) or [])
        analise.recomendacoes = list(dados.get("recomendacoes", []) or [])
        analise.score_conformidade = float(dados.get("score_conformidade", 0) or 0)
        analise.ia_utilizada = True
    except Exception as exc:
        analise.resumo_executivo = self._resumo_fallback(edital)
        analise.score_conformidade = self._score_fallback(edital)
        analise.riscos = [f"Análise via IA indisponível ({exc}); usando resumo determinístico."]
        analise.ia_utilizada = False
    return analise
```

- `_resumo_fallback`: monta uma frase a partir dos campos já extraídos por
  regra ("Edital nº X do órgão Y na modalidade Z. Objeto: ... N item(ns) e
  M requisito(s) de habilitação identificados automaticamente pela
  extração.") — não é um resumo qualitativo, é um resumo factual.
- `_score_fallback`: soma 20 pontos para cada um dos 5 campos-chave
  presentes (número, órgão, modalidade, objeto, prazos) — é uma métrica de
  **completude da extração**, não de qualidade da licitação em si (mesmo
  espírito do `score_conformidade` da IA, mas calculado sem IA).
- `analise.ia_utilizada` (bool) é o sinalizador que registra, para cada
  análise, se o resultado veio do modelo ou do fallback — é esse campo que
  aparece como "Sim" / "Não (fallback determinístico)" nos artefatos (ver
  próxima seção).
- **Itens, requisitos e prazos nunca dependem da IA** — vêm sempre do
  parser por regras (Estágio 2), IA ou fallback. Só o texto qualitativo
  (resumo/riscos/oportunidades/recomendações/score) muda entre os dois
  caminhos.

## Onde o resultado aparece nos artefatos finais

Dos 4 artefatos gerados por `pipeline/artefato_generator.py`, o resultado da
IA (ou do fallback) aparece em:

- **PDF** (`services/pdf_generator.py`) e **Word**
  (`services/word_generator.py`): resumo executivo, score de conformidade,
  indicador "Análise gerada por IA: Sim/Não", listas de riscos,
  oportunidades e recomendações.
- **E-mail** (`services/email_generator.py`): resumo executivo, score de
  conformidade, lista de recomendações.
- **Excel** (`services/excel_generator.py`): **não aparece.** A planilha
  gerada é uma única aba ("Modelo"), a partir do template comercial
  `Dom de Limpar - Modelo Precificacao.xlsx` — ela existe para precificação
  (itens/quantidades/unidades extraídos por regra + colunas de custo/margem
  para preenchimento manual), não para conteúdo qualitativo. `resumo_executivo`
  só é usado ali como *fallback* do campo "Observação Geral" quando o edital
  não tem um objeto identificado (`edital.objeto or analise.resumo_executivo`) —
  fora esse caso pontual, os campos gerados pela IA (riscos, oportunidades,
  recomendações, score, `ia_utilizada`) não são escritos na planilha.

## O que a IA não faz (para não confundir com o parser)

Para deixar explícito, já que é uma dúvida comum ao ler o pipeline pela
primeira vez: número do edital, órgão, modalidade, objeto (extração
"curta"), itens/lotes (com quantidade/unidade/valor) e requisitos de
habilitação **não vêm da IA** — são extraídos por regex e leitura de
tabelas nativas do PDF em `pipeline/edital_parser.py` (Estágio 2, antes da
chamada de IA), documentado em detalhe em
[`04-pipeline-e-funcoes.md`](04-pipeline-e-funcoes.md). A IA só entra depois
disso, e só para o texto qualitativo listado acima.

## Limitações conhecidas

- **Sem streaming real de progresso**: `"stream": False` significa que o
  processo fica bloqueado esperando a resposta completa do modelo (até
  `ollama_timeout` segundos) sem feedback incremental.
- **Um modelo local só**: não há fallback para um segundo provedor de IA
  (ex.: API de nuvem) se o Ollama estiver fora do ar — o fallback é sempre
  o resumo determinístico, nunca outro modelo.
- **Sem retentativa automática**: uma falha na chamada (timeout, erro de
  rede) vai direto para o fallback determinístico na mesma execução; não há
  novo request automático.
- **Contexto ainda pode ser grande**: mesmo compacto, o contexto estruturado
  de um edital com muitos itens/requisitos pode se aproximar do limite de
  12000 caracteres cortado em `generate_json` — nesse caso o corte acontece
  no meio do "Trecho do texto original" (o campo colocado por último na
  montagem do contexto), não nos campos estruturados.
