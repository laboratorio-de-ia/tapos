from pathlib import Path
from typing import List, Tuple

from services.pdf_service import extract_text_from_pdf, extract_tables_from_pdf
from services.docx_service import extract_text_from_docx
from services.text_cleaner import limpar_texto


class EditalExtractor:
    """Extrai o texto bruto (e, quando disponível, as tabelas) do documento de edital,
    qualquer que seja o formato."""

    @staticmethod
    def extract(caminho: str) -> str:
        """Compatibilidade: retorna só o texto. Prefira extract_full quando
        o parser puder aproveitar tabelas (itens/lotes de PDF)."""
        texto, _ = EditalExtractor.extract_full(caminho)
        return texto

    @staticmethod
    def extract_full(caminho: str) -> Tuple[str, List[list]]:
        caminho_path = Path(caminho)
        extensao = caminho_path.suffix.lower()
        tabelas: List[list] = []

        if extensao == ".pdf":
            texto = extract_text_from_pdf(caminho)
            tabelas = extract_tables_from_pdf(caminho)
        elif extensao in (".docx", ".doc"):
            texto = extract_text_from_docx(caminho)
        elif extensao in (".txt", ".md"):
            texto = caminho_path.read_text(encoding="utf-8", errors="replace")
        else:
            raise ValueError(f"Formato não suportado pelo edital-ai: {extensao}")

        return limpar_texto(texto), tabelas
