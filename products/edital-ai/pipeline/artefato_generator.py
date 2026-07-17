import re
from pathlib import Path
from typing import Optional

from models import Artefato, Edital, Analise
from services.excel_generator import gerar_excel
from services.pdf_generator import gerar_pdf
from services.word_generator import gerar_word
from services.email_generator import gerar_email


class ArtefatoGenerator:
    """Gera os 4 artefatos de saída (Excel, PDF, Word, e-mail) a partir
    do edital estruturado e da análise."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sanitizar(nome: str) -> str:
        nome = re.sub(r"[^\w\-]+", "_", nome.strip(), flags=re.UNICODE)
        return nome.strip("_") or "edital"

    def generate_all(
        self, edital: Edital, analise: Analise, nome_documento: Optional[str] = None
    ) -> Artefato:
        # Mantém o nome do arquivo enviado do início ao fim do fluxo: os
        # artefatos gerados devem ser identificáveis pelo mesmo nome do
        # documento carregado. Só cai para o número do edital/id quando o
        # nome original não estiver disponível (ex.: chamada direta da API).
        if nome_documento:
            slug = self._sanitizar(nome_documento)
        else:
            numero_ou_id = (edital.numero or edital.id[:8]).replace("/", "_").replace(" ", "_")
            slug = f"edital_{numero_ou_id}"
        base = self.output_dir / slug

        return Artefato(
            excel=gerar_excel(edital, analise, f"{base}.xlsx"),
            pdf=gerar_pdf(edital, analise, f"{base}.pdf"),
            word=gerar_word(edital, analise, f"{base}.docx"),
            email=gerar_email(edital, analise, f"{base}_email.txt"),
        )
