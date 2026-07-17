from pathlib import Path
from typing import Optional

from src.conversor_markdown import ConvertorUniversal

from .schemas import CodeAIRunResult, ConvertedFile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"


def _build_result(conversor: ConvertorUniversal, files_processed: int) -> CodeAIRunResult:
    converted = [
        ConvertedFile(
            input_file=info["arquivo_original"],
            output_file=info["arquivo_convertido"],
            size_input_kb=info["tamanho_original_kb"],
            size_output_kb=info["tamanho_convertido_kb"],
            savings_percent=info["economia_percentual"],
        )
        for info in conversor.relatorio["arquivos_processados"]
    ]

    report_file = conversor.gerar_relatorio()

    return CodeAIRunResult(
        status="executed",
        files_processed=files_processed,
        converted=converted,
        errors=conversor.relatorio["erros"],
        report_file=report_file,
    )


def execute_current_pipeline(input_file: Optional[str] = None) -> CodeAIRunResult:
    conversor = ConvertorUniversal(diretorio_saida=str(OUTPUT_DIR))

    if input_file:
        resultado = conversor.converter_arquivo(input_file)
        if resultado is None:
            raise RuntimeError(
                f"code-ai falhou ao converter {input_file}: {conversor.relatorio['erros']}"
            )
        return _build_result(conversor, files_processed=1)

    resultados = conversor.converter_pasta(str(INPUT_DIR))
    return _build_result(conversor, files_processed=len(resultados))
