from pathlib import Path

from config import ConfigManager
from pipeline.edital_extractor import EditalExtractor
from pipeline.edital_parser import EditalParser
from pipeline.edital_analyzer import EditalAnalyzer
from pipeline.artefato_generator import ArtefatoGenerator


class EditalAIApp:
    """Orquestra a pipeline completa: extração -> parsing -> análise -> artefatos."""

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
