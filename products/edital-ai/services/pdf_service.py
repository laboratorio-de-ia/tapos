"""Extração de texto e tabelas de arquivos PDF (nativo via pdfplumber, com fallback OCR)."""


def extract_tables_from_pdf(caminho: str) -> list:
    """Retorna todas as tabelas do PDF como lista de tabelas (cada uma, lista de linhas).

    Editais reais costumam listar os itens/lotes em tabelas (colunas LOTE/ITEM/
    DESCRIÇÃO/QTD/VALOR), não em texto corrido — o texto extraído por
    extract_text_from_pdf achata essas tabelas de um jeito que regex de prosa
    não reconhece. Esta função dá acesso à estrutura original das tabelas para
    que o parser possa extrair itens de forma confiável.
    """
    try:
        import pdfplumber

        tabelas = []
        with pdfplumber.open(caminho) as pdf:
            for page in pdf.pages:
                for tabela in page.extract_tables():
                    if tabela:
                        tabelas.append(tabela)
        return tabelas
    except Exception:
        return []


def extract_text_from_pdf(caminho: str) -> str:
    try:
        import pdfplumber

        partes = []
        with pdfplumber.open(caminho) as pdf:
            for page in pdf.pages:
                texto = page.extract_text()
                if texto:
                    partes.append(texto)

        resultado = "\n\n".join(partes).strip()
        if resultado:
            return resultado
    except Exception:
        pass

    # Fallback: PDF escaneado (sem camada de texto) -> OCR
    try:
        from pdf2image import convert_from_path
        from pytesseract import image_to_string

        imagens = convert_from_path(caminho)
        partes = [image_to_string(img, lang="por") for img in imagens]
        return "\n\n".join(partes).strip()
    except Exception as e:
        raise RuntimeError(f"Falha ao extrair texto do PDF ({caminho}): {e}")
