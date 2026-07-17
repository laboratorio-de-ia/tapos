"""
Parser heurístico do edital-ai.

Estrutura o texto bruto extraído do documento em campos objetivos
(número, órgão, modalidade, objeto, prazos, requisitos, itens) usando
regex/heurísticas — sem depender de IA. A análise qualitativa (resumo,
riscos, oportunidades, recomendações, score) fica a cargo do
EditalAnalyzer (services/ollama_service.py), que roda em cima do
resultado deste parser.

Por ser baseado em regex, a extração é best-effort: editais fogem de
um layout único, então nem todo campo é encontrado em todo documento.
Campos não encontrados ficam None/lista vazia.
"""

import re
import uuid
from datetime import datetime
from typing import List, Optional

from dateutil import parser as date_parser

from models import Edital, Objeto, Prazo, Requisito

MODALIDADES = [
    "pregão eletrônico",
    "pregão presencial",
    "concorrência",
    "tomada de preços",
    "convite",
    "concurso",
    "leilão",
    "dispensa de licitação",
    "inexigibilidade",
    "credenciamento",
]

PALAVRAS_CHAVE_PRAZO = [
    "abertura",
    "encerramento",
    "recebimento das propostas",
    "sessão pública",
    "recurso",
    "impugnação",
    "entrega dos envelopes",
    "publicação",
]

REGEX_DATA = re.compile(
    r"\b(\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4}|\d{1,2}\s+de\s+\w+\s+de\s+\d{4})\b",
    re.IGNORECASE,
)
# Entre a palavra-chave (edital/processo/pregão/licitação) e o "Nº <número>"
# em si, alguns editais intercalam qualificadores (ex.: "PROCESSO
# LICITATÓRIO Nº 51/2026", "PREGÃO ELETRÔNICO PARA REGISTRO DE PREÇOS Nº
# 17/2026") — daí o `(?:\s+[a-zà-ú]+){0,4}?`, que tolera até 4 palavras
# soltas entre os dois (lazy: só consome o que precisar para achar o "Nº").
# Sem essa tolerância, "PROCESSO LICITATÓRIO Nº 51/2026" não casava porque
# "LICITATÓRIO" quebrava a adjacência exigida entre "processo" e "Nº".
REGEX_NUMERO_EDITAL = re.compile(
    r"(?:edital|processo|preg[aã]o|licita[cç][aã]o)(?:\s+[a-zà-ú]+){0,4}?\s*"
    r"n?[ºo°]?\s*[:\-]?\s*([\d]{1,6}\s*[/\-]\s*[\d]{2,4})",
    re.IGNORECASE,
)
# Fórmula padrão dos editais brasileiros: "A <ÓRGÃO>[, qualificação...] torna
# público/pública a realização de licitação...". É bem mais confiável que
# procurar palavras-chave soltas, que podem casar com trechos incidentais no
# meio do documento (ex.: menção a "Secretaria da Receita Federal" dentro de
# uma cláusula de habilitação, não relacionada ao órgão licitante).
# O trecho entre o nome do órgão e "torna público" é limitado a ~300
# caracteres (`.{0,300}?`, não `.*?` sem limite) — sem esse limite, o
# DOTALL deixava o regex "pular" parágrafos inteiros não relacionados para
# alcançar a primeira ocorrência de "torna público" em qualquer lugar do
# documento, inclusive a partir de um artigo solto ("o"/"a") minúsculo
# incidental bem antes do preâmbulo real (ex.: "...será observado o horário
# de Brasília/DF e, dessa forma [...várias páginas depois...] torna
# pública" virava órgão = "horário de Brasília/DF e").
REGEX_ORGAO_FORMULA = re.compile(
    r"\b[AO]\s+([A-ZÀ-Ú][^\n,]{2,150}?)(?:\s*,.{0,300}?)?\btorna\s+p[uú]blic[ao]\b",
    re.IGNORECASE | re.DOTALL,
)
# Fallback: procura por palavra-chave de órgão público, mas só no cabeçalho
# do documento — evita capturar menções incidentais em cláusulas no meio do
# texto (ex.: "Certidão ... fornecida pela Secretaria da Receita Federal").
REGEX_ORGAO = re.compile(
    r"^.*(prefeitura|secretaria|minist[ée]rio|universidade|c[âa]mara municipal|"
    r"governo do estado|autarquia|funda[cç][aã]o|instituto federal).*$",
    re.IGNORECASE | re.MULTILINE,
)
TAMANHO_CABECALHO_ORGAO = 2000

REGEX_VALOR = re.compile(r"R\$\s?[\d.]+,\d{2}")
REGEX_ITEM = re.compile(
    r"^\s*(?:item|lote)\s*(\d{1,3})\s*[-–:.)]\s*(.{5,200})$",
    re.IGNORECASE | re.MULTILINE,
)
REGEX_QUANTIDADE_UNIDADE = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*(un|und|unidade[s]?|kg|cx|caixa[s]?|pç|pçs|peça[s]?|m|metro[s]?|l|litro[s]?|serviço[s]?)",
    re.IGNORECASE,
)


def _first_match(pattern: "re.Pattern", texto: str) -> Optional[str]:
    m = pattern.search(texto)
    return m.group(0).strip() if m else None


def extract_numero(texto: str) -> Optional[str]:
    m = REGEX_NUMERO_EDITAL.search(texto)
    return m.group(1).strip() if m else None


def extract_orgao(texto: str) -> Optional[str]:
    m = REGEX_ORGAO_FORMULA.search(texto)
    if m:
        nome = re.sub(r"\s+", " ", m.group(1)).strip(" -")
        if nome:
            return nome[:200]

    linha = _first_match(REGEX_ORGAO, texto[:TAMANHO_CABECALHO_ORGAO])
    return linha.strip()[:200] if linha else None


def extract_modalidade(texto: str) -> Optional[str]:
    texto_lower = texto.lower()
    for modalidade in MODALIDADES:
        if modalidade in texto_lower:
            return modalidade
    return None


# Muitos editais (sobretudo os de portais de compras estaduais) trazem um
# cabeçalho no formato "OBJETO: <descrição>" logo no topo do documento,
# seguido de outro rótulo em CAIXA ALTA (ex.: "ABERTURA DA SESSÃO...:"). Esse
# padrão é bem mais confiável que procurar a primeira ocorrência solta da
# palavra "objeto" no corpo do texto, que pode cair numa cláusula genérica
# no meio de uma seção não relacionada (ex.: "...especificações do objeto
# descritas no Portal de Compras...").
REGEX_OBJETO_CABECALHO = re.compile(
    r"^\s*OBJETO\s*:\s*(.{10,800}?)(?:\n\s*\n|\n[A-ZÀ-Ú][A-ZÀ-Ú0-9 /\.\-]{3,60}:|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
# Outro padrão muito comum: título de seção numerado em caixa alta (ex.: "3 –
# OBJETO", "2. DO OBJETO"), no mesmo estilo do cabeçalho de habilitação
# (`REGEX_CABECALHO_HABILITACAO` mais abaixo) — sem isso, um edital que só usa
# esse formato (sem "OBJETO:" literal) caía direto no fallback de prosa
# (`REGEX_OBJETO_CLAUSULA`), que não tem limite de busca e podia pegar uma
# menção incidental à palavra "objeto" em qualquer cláusula do documento.
REGEX_OBJETO_SECAO_NUMERADA = re.compile(
    r"\n\s*\d{1,2}\s*[-–.]\s*(?:DO\s+)?OBJETO\b\s*\n+(?:\d{1,2}\.\d{1,2}\.?\s*)?"
    r"(.{10,800}?)(?:\n\s*\n|\n\d{1,2}\.\s*\d{1,2}\.|\n\d{1,2}\s*[-–.]\s*[A-ZÀ-Ú]|\Z)",
    re.IGNORECASE | re.DOTALL,
)
REGEX_OBJETO_CLAUSULA = re.compile(
    r"(?:tem\s+por\s+objeto|do\s+objeto|objeto\s*[:\-])\s*(.{20,800}?)(?:\n\s*\n|\n\d+\.\d|\n\d+\.\s|\nCL[ÁA]USULA|\Z)",
    re.IGNORECASE | re.DOTALL,
)


def extract_objeto(texto: str) -> Optional[str]:
    m = REGEX_OBJETO_CABECALHO.search(texto[:3000])
    if not m:
        m = REGEX_OBJETO_SECAO_NUMERADA.search(texto)
    if not m:
        m = REGEX_OBJETO_CLAUSULA.search(texto)
    if not m:
        return None
    return re.sub(r"\s+", " ", m.group(1)).strip()


def extract_prazos(texto: str) -> List[Prazo]:
    """Extrai prazos casando uma palavra-chave com uma data próxima.

    Em editais de portais de compras é comum o rótulo do prazo e a data
    ficarem em linhas diferentes depois da extração do PDF (ex.: "ABERTURA
    DA SESSÃO DE PREGÃO:" numa linha e "09:30 HORAS DO DIA 13/07/2026" na
    linha seguinte, por causa do layout em caixas do cabeçalho). Por isso a
    busca considera uma janela de até 2 linhas após a palavra-chave, não só
    a linha em que ela aparece.
    """
    prazos: List[Prazo] = []
    linhas = texto.split("\n")
    agora = datetime.now()
    vistos = set()

    for i, linha in enumerate(linhas):
        linha_lower = linha.lower()
        palavra = next((p for p in PALAVRAS_CHAVE_PRAZO if p in linha_lower), None)
        if not palavra:
            continue

        janela = "\n".join(linhas[i:i + 3])
        datas = REGEX_DATA.findall(janela)
        if not datas:
            continue

        data_texto = datas[0].strip()
        chave = (palavra, data_texto)
        if chave in vistos:
            continue
        vistos.add(chave)

        data_parseada = None
        try:
            data_parseada = date_parser.parse(data_texto, dayfirst=True, fuzzy=True)
        except (ValueError, OverflowError):
            pass

        dias_para_evento = None
        critico = False
        if data_parseada:
            dias_para_evento = (data_parseada.date() - agora.date()).days
            critico = 0 <= dias_para_evento < 7

        prazos.append(
            Prazo(
                descricao=palavra.capitalize(),
                data_texto=data_texto,
                data=data_parseada,
                dias_para_evento=dias_para_evento,
                critico=critico,
            )
        )

    return prazos


# Cabeçalho de seção dedicado (ex.: "7. DA HABILITAÇÃO"), tentado primeiro
# por ser muito mais preciso: a simples palavra "habilitação" solta aparece
# várias vezes antes da seção de habilitação propriamente dita (ex.: nas
# declarações eletrônicas da seção de propostas, que mencionam "requisitos
# de habilitação" de passagem).
REGEX_CABECALHO_HABILITACAO = re.compile(
    r"\n\s*\d{1,2}\.\s*DA\s+HABILITA[CÇ][AÃ]O\b",
    re.IGNORECASE,
)
REGEX_INICIO_HABILITACAO = re.compile(
    r"(?:habilita[cç][aã]o|documentos?\s+(?:de\s+)?habilita[cç][aã]o|"
    r"documenta[cç][aã]o\s+exigida)\s*[:\-]?\s*",
    re.IGNORECASE,
)
# Título da próxima seção do edital, usado para não deixar o bloco de
# habilitação "vazar" para a seção seguinte. Cobre tanto seções numeradas
# (ex.: "8. DA ABERTURA...") quanto o padrão comum na redação legal
# brasileira de título em CAIXA ALTA sem número, que reinicia sua própria
# numeração local (ex.: "DA ABERTURA DA SESSÃO E DA ETAPA DE LANCES" seguido
# de "1. A abertura..., 2. Iniciada...").
REGEX_PROXIMA_SECAO = re.compile(
    r"\n\s*(?:\d{1,2}\.\s*)?(?:DA|DO|DAS|DOS)\s+[A-ZÀ-Ú][A-ZÀ-Ú \-/]{3,80}(?=\n)"
)
TAMANHO_MAX_BLOCO_HABILITACAO = 6000


def extract_requisitos(texto: str) -> List[Requisito]:
    requisitos: List[Requisito] = []

    m = REGEX_CABECALHO_HABILITACAO.search(texto)
    if not m:
        m = REGEX_INICIO_HABILITACAO.search(texto)
    if not m:
        return requisitos

    inicio = m.end()
    proxima = REGEX_PROXIMA_SECAO.search(texto, inicio)
    fim = proxima.start() if proxima else min(inicio + TAMANHO_MAX_BLOCO_HABILITACAO, len(texto))
    bloco = texto[inicio:fim]

    # \d{1,2}(?:\.\d{1,3})*[.)] consome o número inteiro em cascata
    # (ex.: "7.6.1."), não só o primeiro segmento — senão "7.6.1." vira
    # prefixo "7." e o resto ("6.1. texto...") some misturado na descrição.
    linha_item = re.compile(
        r"(?:^|\n)\s*(?:[a-z]\)|[IVXLCDM]+\s*[-–.]|\d{1,2}(?:\.\d{1,3})*[.)]|[-•])\s*(.{10,300})"
    )
    for match in linha_item.finditer(bloco):
        descricao = re.sub(r"\s+", " ", match.group(1)).strip()
        if len(descricao) < 10:
            continue
        requisitos.append(
            Requisito(
                tipo="habilitação",
                descricao=descricao,
                obrigatorio=True,
            )
        )
        if len(requisitos) >= 30:
            break

    return requisitos


def extract_requisitos_de_tabelas(tabelas: List[list]) -> List[Requisito]:
    """Extrai requisitos de habilitação a partir das tabelas nativas do PDF.

    O "quadro" de documentos de habilitação citado no corpo do edital (ex.:
    "A habilitação deverá ser comprovada pela análise dos documentos
    listados no quadro abaixo") é, na prática, quase sempre uma tabela de 2
    colunas — número do item e descrição do documento exigido —, intercalada
    com subtítulos de categoria (ex.: "REGULARIDADE FISCAL E TRABALHISTA")
    cuja segunda coluna vem vazia. extract_requisitos (regex em prosa) não
    reconhece esse formato.
    """
    requisitos: List[Requisito] = []
    categoria_atual = "habilitação"
    coletando = False

    for tabela in tabelas:
        if not tabela or not tabela[0]:
            continue

        num_colunas = max(len(linha) for linha in tabela)
        primeira_celula = _normalizar_cabecalho_celula(tabela[0][0])

        if "HABILITA" in primeira_celula and num_colunas == 2:
            coletando = True
        elif num_colunas != 2:
            coletando = False
            continue
        elif not coletando:
            continue

        for linha in tabela:
            if len(linha) < 2:
                continue
            col0 = (linha[0] or "").strip()
            col1 = (linha[1] or "").strip()

            if not col1:
                # linha de subtítulo de categoria (ex.: "REGULARIDADE FISCAL
                # E TRABALHISTA", "HABILITAÇÃO JURÍDICA"), não um item em si
                # — não gera requisito, só atualiza a categoria corrente.
                if col0 and not col0.isdigit():
                    categoria = re.sub(r"^(?:DA|DO|DAS|DOS)\s+", "", col0, flags=re.IGNORECASE)
                    categoria_atual = re.sub(r"\s+", " ", categoria).strip().lower()
                continue

            if not col0.isdigit():
                continue

            descricao = re.sub(r"\s+", " ", col1).strip()
            if len(descricao) < 5:
                continue

            requisitos.append(
                Requisito(
                    tipo=categoria_atual,
                    descricao=descricao[:400],
                    obrigatorio=True,
                )
            )
            if len(requisitos) >= 100:
                return requisitos

    return requisitos


def extract_objetos(texto: str) -> List[Objeto]:
    objetos: List[Objeto] = []

    for match in REGEX_ITEM.finditer(texto):
        numero = int(match.group(1))
        linha_item = match.group(2)

        # qty/valor são procurados só dentro da própria linha do item, nunca
        # em texto de outro item — evita "vazar" dados entre itens vizinhos
        qtd_match = REGEX_QUANTIDADE_UNIDADE.search(linha_item)
        quantidade = None
        unidade = None
        if qtd_match:
            quantidade = float(qtd_match.group(1).replace(",", "."))
            unidade = qtd_match.group(2).lower()

        valor_match = REGEX_VALOR.search(linha_item)
        valor_estimado = None
        if valor_match:
            valor_texto = valor_match.group(0).replace("R$", "").strip()
            valor_texto = valor_texto.replace(".", "").replace(",", ".")
            try:
                valor_estimado = float(valor_texto)
            except ValueError:
                valor_estimado = None

        # a descrição é o trecho da linha antes da quantidade/valor, quando
        # encontrados — evita que "300 un R$ 3.200,00" fique grudado no texto
        corte = min(
            [m.start() for m in (qtd_match, valor_match) if m] or [len(linha_item)]
        )
        descricao = re.sub(r"\s+", " ", linha_item[:corte]).strip(" -–:")
        if not descricao:
            descricao = re.sub(r"\s+", " ", linha_item).strip()

        objetos.append(
            Objeto(
                numero=numero,
                descricao=descricao,
                quantidade=quantidade,
                unidade=unidade,
                valor_estimado=valor_estimado,
            )
        )
        if len(objetos) >= 50:
            break

    return objetos


def _normalizar_cabecalho_celula(celula: Optional[str]) -> str:
    return re.sub(r"\s+", " ", (celula or "")).strip().upper()


def _colunas_minimas(mapeamento: dict) -> int:
    """Menor número de colunas que uma linha precisa ter para cobrir todas
    as posições que o mapeamento do cabeçalho realmente usa."""
    indices = [
        mapeamento[chave]
        for chave in ("idx_desc", "idx_item", "idx_lote", "idx_ordem", "idx_qtd", "idx_unid", "idx_valor")
        if mapeamento[chave] is not None
    ]
    return max(indices) + 1 if indices else 0


def _numero_valido(texto: Optional[str]) -> bool:
    normalizado = (texto or "").strip().replace(".", "").replace(",", ".")
    return bool(re.fullmatch(r"\d+(\.\d+)?", normalizado))


def extract_objetos_de_tabelas(tabelas: List[list]) -> List[Objeto]:
    """Extrai itens/lotes a partir das tabelas nativas do PDF (pdfplumber).

    Editais reais quase sempre listam os itens em tabela (colunas como
    LOTE/ITEM/ORDEM/DESCRIÇÃO/ESPECIFICAÇÃO/U.F./QTD.), não em prosa "Item 1
    - Descrição...". extract_objetos (regex sobre texto corrido) não
    reconhece esse formato, então esta função lê a estrutura de tabela
    diretamente, o que é bem mais confiável para documentos reais de portais
    de compras.

    Tabelas de itens que atravessam várias páginas saem do pdfplumber como
    blocos separados — só o primeiro bloco traz o cabeçalho de novo; os
    demais vêm "crus", às vezes com a primeira linha sendo apenas a sobra de
    uma descrição que quebrou na virada da página. Por isso o mapeamento de
    colunas do último cabeçalho válido é reaproveitado enquanto o número de
    colunas continuar o mesmo (heurística de continuação de tabela), e uma
    linha sem número reconhecível na coluna de item/lote/ordem é tratada
    como continuação da descrição do item anterior, não como um item novo
    (senão o corte de página vira um item fantasma, sem quantidade/valor).
    """
    objetos: List[Objeto] = []
    numero_seq = 0
    mapeamento: Optional[dict] = None

    for tabela in tabelas:
        if not tabela or not tabela[0]:
            mapeamento = None
            continue

        num_colunas = max(len(linha) for linha in tabela)
        cabecalho = [_normalizar_cabecalho_celula(c) for c in tabela[0]]

        # "DESCRIÇÃO"/"ESPECIFICAÇÃO" são as mais comuns, mas vários portais
        # de compras usam outros rótulos para a mesma coluna (o texto do
        # item em si) — "DETALHAMENTO" e "DISCRIMINAÇÃO" apareceram em
        # editais reais e, sem eles aqui, a tabela de itens inteira era
        # descartada por não ter "cabeçalho válido" reconhecido.
        idx_desc = next(
            (
                i
                for i, c in enumerate(cabecalho)
                if "DESCRI" in c or "ESPECIFICA" in c or "DETALHAMENTO" in c or "DISCRIMINA" in c
            ),
            None,
        )
        idx_item = next((i for i, c in enumerate(cabecalho) if c == "ITEM"), None)
        idx_lote = next((i for i, c in enumerate(cabecalho) if c == "LOTE"), None)
        idx_ordem = next(
            (i for i, c in enumerate(cabecalho) if c in ("ORDEM", "Nº", "N°", "SEQ", "SEQUÊNCIA")), None
        )
        idx_qtd = next((i for i, c in enumerate(cabecalho) if "QTD" in c or "QUANT" in c), None)

        # Uma coluna de descrição sozinha não basta — tabelas de matriz de
        # risco também têm uma ("DESCRIÇÃO DO RISCO"). Exige também
        # LOTE/ITEM/ORDEM e QTD, que só existem em tabelas de catálogo de
        # itens de verdade.
        cabecalho_valido = (
            idx_desc is not None
            and idx_qtd is not None
            and (idx_item is not None or idx_lote is not None or idx_ordem is not None)
        )

        if cabecalho_valido:
            idx_unid = next(
                (i for i, c in enumerate(cabecalho) if "UNID" in c or "U.F" in c or c in ("UN", "UN.")), None
            )
            idx_valor = next(
                (i for i, c in enumerate(cabecalho) if "VALOR" in c and ("UNIT" in c or "UN " in c or c.endswith(" UN"))),
                None,
            )
            mapeamento = {
                "idx_desc": idx_desc,
                "idx_item": idx_item,
                "idx_lote": idx_lote,
                "idx_ordem": idx_ordem,
                "idx_qtd": idx_qtd,
                "idx_unid": idx_unid,
                "idx_valor": idx_valor,
                "num_colunas": num_colunas,
            }
            linhas_dados = tabela[1:]
        elif mapeamento and num_colunas >= _colunas_minimas(mapeamento):
            # sem cabeçalho próprio: provável continuação em outra página.
            # Exigir número de colunas IDÊNTICO ao cabeçalho era frágil
            # demais na prática — cabeçalhos com rótulo quebrado em duas
            # linhas (ex.: "VALOR\nUNIT.") fazem o pdfplumber contar mais
            # colunas "vazias" no bloco do cabeçalho do que nos blocos de
            # dados seguintes, e isso descartava silenciosamente quase
            # todos os itens reais (só a primeira página da tabela era
            # aproveitada). Basta que a linha tenha colunas suficientes
            # para as posições realmente usadas pelo mapeamento.
            linhas_dados = tabela
        else:
            mapeamento = None
            continue

        m = mapeamento
        for linha in linhas_dados:
            if m["idx_desc"] >= len(linha):
                continue
            descricao_bruta = (linha[m["idx_desc"]] or "").strip()
            if not descricao_bruta and len(linha) > m["idx_desc"] + 1:
                # a linha ganhou uma coluna a mais do que o cabeçalho previa
                # (célula que quebrou de forma inesperada nessa página) e o
                # texto real "escorregou" para a última posição — sem isso,
                # a linha inteira era descartada como se fosse um espaço em
                # branco de template.
                descricao_bruta = (linha[-1] or "").strip()
            if not descricao_bruta:
                continue  # linha de template em branco (planilha de proposta a preencher)

            numero = None
            for idx in (m["idx_item"], m["idx_lote"], m["idx_ordem"]):
                if idx is not None and idx < len(linha) and (linha[idx] or "").strip().isdigit():
                    numero = int(linha[idx].strip())
                    break

            if numero is None and objetos:
                # linha sem número na coluna de item/lote/ordem: sobra da
                # descrição do item anterior que quebrou na virada de página,
                # não um item novo
                texto_extra = re.sub(r"\s+", " ", descricao_bruta).strip()
                anterior = objetos[-1]
                anterior.especificacoes = (
                    f"{anterior.especificacoes} {texto_extra}" if anterior.especificacoes else texto_extra
                )[:2000]
                continue

            if numero is None:
                numero_seq += 1
                numero = numero_seq

            partes = [p.strip() for p in descricao_bruta.split("\n") if p.strip()]
            titulo = partes[0] if partes else descricao_bruta
            detalhes = " ".join(partes[1:]) if len(partes) > 1 else None

            # Em alguns editais, o cabeçalho rotula "QUANT." e "UNIDADE DE
            # MEDIDA" em posições que não batem com a ordem real das colunas
            # de dados (o texto do cabeçalho e o corpo da tabela vêm de
            # blocos de coordenadas ligeiramente diferentes no PDF de
            # origem, e o pdfplumber alinha errado). Confiar cegamente na
            # posição declarada pelo cabeçalho fazia a quantidade virar
            # texto ("FRASCO 2L") e a unidade virar número ("800"). Por
            # isso, se a coluna apontada como quantidade não parece um
            # número mas a apontada como unidade parece, os dois valores são
            # trocados para essa linha — o conteúdo real da célula manda
            # mais que a posição declarada pelo cabeçalho.
            idx_qtd_linha, idx_unid_linha = m["idx_qtd"], m["idx_unid"]
            if (
                idx_qtd_linha is not None
                and idx_unid_linha is not None
                and idx_qtd_linha < len(linha)
                and idx_unid_linha < len(linha)
                and not _numero_valido(linha[idx_qtd_linha])
                and _numero_valido(linha[idx_unid_linha])
            ):
                idx_qtd_linha, idx_unid_linha = idx_unid_linha, idx_qtd_linha

            quantidade = None
            if idx_qtd_linha is not None and idx_qtd_linha < len(linha):
                qtd_texto = (linha[idx_qtd_linha] or "").strip().replace(".", "").replace(",", ".")
                if re.fullmatch(r"\d+(\.\d+)?", qtd_texto):
                    quantidade = float(qtd_texto)

            unidade = None
            if idx_unid_linha is not None and idx_unid_linha < len(linha):
                unidade = re.sub(r"\s+", " ", (linha[idx_unid_linha] or "").strip()).strip() or None

            valor_estimado = None
            if m["idx_valor"] is not None and m["idx_valor"] < len(linha):
                valor_texto = re.sub(r"[^\d,\.]", "", (linha[m["idx_valor"]] or "").strip())
                valor_texto = valor_texto.replace(".", "").replace(",", ".")
                if valor_texto:
                    try:
                        valor_estimado = float(valor_texto)
                    except ValueError:
                        valor_estimado = None

            objetos.append(
                Objeto(
                    numero=numero,
                    descricao=titulo[:200],
                    quantidade=quantidade,
                    unidade=unidade,
                    valor_estimado=valor_estimado,
                    especificacoes=detalhes[:2000] if detalhes else None,
                )
            )
            if len(objetos) >= 1000:
                return objetos

    return objetos


class EditalParser:
    """Estrutura o texto bruto de um edital em um objeto Edital."""

    @staticmethod
    def parse(texto_completo: str, tabelas: Optional[List[list]] = None) -> Edital:
        edital = Edital(id=str(uuid.uuid4()), texto_completo=texto_completo)

        edital.numero = extract_numero(texto_completo)
        edital.orgao = extract_orgao(texto_completo)
        edital.modalidade = extract_modalidade(texto_completo)
        edital.objeto = extract_objeto(texto_completo)
        edital.prazos = extract_prazos(texto_completo)

        # Tabelas nativas do PDF são bem mais confiáveis que a extração por
        # regex em prosa; só cai para a extração em texto corrido se não
        # houver tabelas reconhecíveis (ex.: DOCX/TXT, ou PDF sem tabela).
        requisitos_tabela = extract_requisitos_de_tabelas(tabelas or [])
        edital.requisitos = requisitos_tabela if requisitos_tabela else extract_requisitos(texto_completo)

        objetos_tabela = extract_objetos_de_tabelas(tabelas or [])
        edital.objetos = objetos_tabela if objetos_tabela else extract_objetos(texto_completo)
        edital.status = "extraido"

        return edital
