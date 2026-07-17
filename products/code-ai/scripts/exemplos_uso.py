#!/usr/bin/env python3

"""
===============================================================================
Projeto:
Descrição:

Desenvolvido por Eduardo Ferreira
Cargo: CTO da TAPOS

© 2026 TAPOS. Todos os direitos reservados.
===============================================================================
"""
"""
EXEMPLOS DE USO - CODE-AI

Local esperado:
    scripts/exemplos_uso.py

Executar a partir da raiz do projeto:

    python scripts/exemplos_uso.py
"""
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from pathlib import Path

from src.conversor_markdown import (
    ConvertorUniversal,
    ConversorDocx,
    ConversorExcel,
    ConversorPDF,
)


# ============================================================
# EXEMPLO 1 - CONVERTER UM ARQUIVO
# ============================================================

def exemplo_arquivo_unico():
    """
    Converte um único arquivo.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultado = conversor.converter_arquivo(
        "input/documento.pdf"
    )

    print(f"✅ Arquivo convertido: {resultado}")


# ============================================================
# EXEMPLO 2 - CONVERTER MULTIPLOS ARQUIVOS
# ============================================================

def exemplo_multiplos_arquivos():
    """
    Converte vários arquivos.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    arquivos = [
        "input/relatorio.docx",
        "input/dados.xlsx",
        "input/apresentacao.pptx",
        "input/documento.pdf",
    ]

    resultados = conversor.converter_multiplos(
        arquivos
    )

    conversor.gerar_relatorio()

    print("\n✅ Arquivos convertidos:")

    for arquivo in resultados:
        print(f"   {arquivo}")


# ============================================================
# EXEMPLO 3 - CONVERTER UMA PASTA INTEIRA
# ============================================================

def exemplo_converter_pasta():
    """
    Converte todos os arquivos da pasta input.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultados = conversor.converter_pasta(
        "input"
    )

    conversor.gerar_relatorio()

    print(
        f"\n✅ {len(resultados)} arquivos convertidos"
    )


# ============================================================
# EXEMPLO 4 - CONVERSORES ESPECIFICOS
# ============================================================

def exemplo_conversores_especificos():
    """
    Utiliza os conversores individualmente.
    """

    markdown_pdf = ConversorPDF.converter(
        "input/documento.pdf"
    )

    Path(
        "output/documento_pdf.md"
    ).write_text(
        markdown_pdf,
        encoding="utf-8",
    )

    markdown_excel = ConversorExcel.converter(
        "input/dados.xlsx"
    )

    Path(
        "output/dados_excel.md"
    ).write_text(
        markdown_excel,
        encoding="utf-8",
    )

    markdown_docx = ConversorDocx.converter(
        "input/relatorio.docx"
    )

    Path(
        "output/relatorio_docx.md"
    ).write_text(
        markdown_docx,
        encoding="utf-8",
    )

    print(
        "✅ Conversores individuais executados"
    )


# ============================================================
# EXEMPLO 5 - PREPARAR PARA LLM
# ============================================================

def exemplo_llm():
    """
    Converte e lê o markdown para envio
    em Claude, ChatGPT, Gemini ou Copilot.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultado = conversor.converter_arquivo(
        "input/documento.pdf"
    )

    if not resultado:
        return

    conteudo = Path(resultado).read_text(
        encoding="utf-8"
    )

    print("\n✅ Documento preparado para IA")
    print(
        f"📄 Tamanho: {len(conteudo):,} caracteres"
    )

    print("\nPrimeiros 500 caracteres:\n")

    print(
        conteudo[:500]
    )


# ============================================================
# EXEMPLO 6 - PROCESSAMENTO EM LOTE
# ============================================================

def exemplo_batch():
    """
    Processa todos os PDFs da pasta input.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    pdfs = list(
        Path("input").glob("*.pdf")
    )

    print(
        f"\n📁 PDFs encontrados: {len(pdfs)}"
    )

    for pdf in pdfs:
        conversor.converter_arquivo(
            str(pdf)
        )

    conversor.gerar_relatorio()


# ============================================================
# EXEMPLO 7 - EXIBIR AJUDA
# ============================================================

def mostrar_menu():
    """
    Exibe exemplos disponíveis.
    """

    print(
        """
==================================================
CODE-AI - EXEMPLOS DE USO
==================================================

1 - Conversão de arquivo único
2 - Conversão de múltiplos arquivos
3 - Conversão de pasta inteira
4 - Conversores específicos
5 - Preparação para IA (LLM)
6 - Processamento em lote

Exemplo:

    from src.conversor_markdown import ConvertorUniversal

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultado = conversor.converter_arquivo(
        "input/documento.pdf"
    )
"""
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    mostrar_menu()