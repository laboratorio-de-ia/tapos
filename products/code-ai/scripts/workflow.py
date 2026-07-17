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
CODE-AI - WORKFLOWS DE CONVERSÃO

Executar a partir da raiz:

python scripts/workflow.py 1 input/documento.pdf
python scripts/workflow.py 2 input/doc1.pdf input/doc2.docx
python scripts/workflow.py 3 input
python scripts/workflow.py 4 input/documento.pdf
python scripts/workflow.py 5 input/documento.pdf
"""

from pathlib import Path
import sys
import re

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.conversor_markdown import ConvertorUniversal


# ============================================================
# WORKFLOW 1 - ARQUIVO ÚNICO
# ============================================================

def workflow_arquivo_unico(arquivo: str):
    """
    Processa um único arquivo.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultado = conversor.converter_arquivo(
        arquivo
    )

    conversor.gerar_relatorio()

    return resultado


# ============================================================
# WORKFLOW 2 - MÚLTIPLOS ARQUIVOS
# ============================================================

def workflow_multiplos_arquivos(lista_arquivos: list):
    """
    Processa vários arquivos.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultados = conversor.converter_multiplos(
        lista_arquivos
    )

    relatorio = conversor.gerar_relatorio()

    return {
        "arquivos": resultados,
        "relatorio": relatorio
    }


# ============================================================
# WORKFLOW 3 - PASTA COMPLETA
# ============================================================

def workflow_pasta_completa(caminho_pasta: str):
    """
    Processa toda uma pasta.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultados = conversor.converter_pasta(
        caminho_pasta
    )

    conversor.gerar_relatorio()

    return resultados


# ============================================================
# WORKFLOW 4 - CONVERTER E OTIMIZAR
# ============================================================

def workflow_otimizado(arquivo: str):
    """
    Converte e remove espaços extras.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultado = conversor.converter_arquivo(
        arquivo
    )

    if not resultado:
        return None

    caminho_md = Path(resultado)

    markdown = caminho_md.read_text(
        encoding="utf-8"
    )

    markdown = re.sub(
        r'\n\n\n+',
        '\n\n',
        markdown
    )

    markdown = re.sub(
        r'[ ]{2,}',
        ' ',
        markdown
    )

    caminho_md.write_text(
        markdown,
        encoding="utf-8"
    )

    print(
        f"✅ Markdown otimizado: {resultado}"
    )

    return resultado


# ============================================================
# WORKFLOW 5 - PREPARAR PARA COPIAR E COLAR
# ============================================================

def workflow_copia_cola(arquivo: str):
    """
    Converte e exibe prévia.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultado = conversor.converter_arquivo(
        arquivo
    )

    if not resultado:
        return None

    conteudo = Path(resultado).read_text(
        encoding="utf-8"
    )

    print("\n" + "=" * 70)
    print("✅ DOCUMENTO PRONTO PARA IA")
    print("=" * 70)

    print(
        f"\n📄 Caracteres: {len(conteudo):,}"
    )

    print(
        "\n📋 Primeiros 1000 caracteres:\n"
    )

    print(
        conteudo[:1000]
    )

    return resultado


# ============================================================
# MENU
# ============================================================

def exibir_menu():
    print(
        """
============================================================
CODE-AI - WORKFLOWS
============================================================

1 - Um arquivo

    python scripts/workflow.py 1 input/documento.pdf

2 - Múltiplos arquivos

    python scripts/workflow.py 2 input/doc1.pdf input/doc2.docx

3 - Pasta inteira

    python scripts/workflow.py 3 input

4 - Converter e otimizar

    python scripts/workflow.py 4 input/documento.pdf

5 - Preparar para IA

    python scripts/workflow.py 5 input/documento.pdf

============================================================
"""
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:
        exibir_menu()
        sys.exit(0)

    modo = sys.argv[1]

    if modo == "1":

        if len(sys.argv) < 3:
            print("Informe o arquivo.")
            sys.exit(1)

        workflow_arquivo_unico(
            sys.argv[2]
        )

    elif modo == "2":

        if len(sys.argv) < 3:
            print("Informe os arquivos.")
            sys.exit(1)

        workflow_multiplos_arquivos(
            sys.argv[2:]
        )

    elif modo == "3":

        if len(sys.argv) < 3:
            print("Informe a pasta.")
            sys.exit(1)

        workflow_pasta_completa(
            sys.argv[2]
        )

    elif modo == "4":

        if len(sys.argv) < 3:
            print("Informe o arquivo.")
            sys.exit(1)

        workflow_otimizado(
            sys.argv[2]
        )

    elif modo == "5":

        if len(sys.argv) < 3:
            print("Informe o arquivo.")
            sys.exit(1)

        workflow_copia_cola(
            sys.argv[2]
        )

    else:
        exibir_menu()