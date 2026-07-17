#!/usr/bin/env python3
"""
CODE-AI - MODO RÁPIDO

Script minimalista para converter arquivos com
o mínimo possível de código.

Exemplos:

    python scripts/rapido.py input/documento.pdf

    python scripts/rapido.py input

Ou via Python:

    from rapido import converter_rapido

    resultado = converter_rapido(
        "input/documento.pdf"
    )
"""

from pathlib import Path
import subprocess
import sys

# ============================================================
# AJUSTE DE PATH
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.conversor_markdown import ConvertorUniversal


# ============================================================
# INSTALAÇÃO
# ============================================================

def instalar_dependencias():
    """
    Instala dependências do projeto.
    """

    requirements = ROOT_DIR / "requirements.txt"

    if not requirements.exists():
        print(
            "❌ requirements.txt não encontrado."
        )
        return

    print(
        "📦 Instalando dependências..."
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements),
        ]
    )

    print(
        "✅ Dependências instaladas."
    )


# ============================================================
# CONVERSÃO RÁPIDA
# ============================================================

def converter_rapido(arquivo: str):
    """
    Converte um único arquivo.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    return conversor.converter_arquivo(
        arquivo
    )


# ============================================================
# CONVERTER PASTA
# ============================================================

def converter_pasta(pasta: str):
    """
    Converte todos os arquivos da pasta.
    """

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    resultados = conversor.converter_pasta(
        pasta
    )

    conversor.gerar_relatorio()

    return resultados


# ============================================================
# MENU
# ============================================================

def mostrar_ajuda():

    print(
        """
==================================================
CODE-AI - MODO RÁPIDO
==================================================

Converter um arquivo:

    python scripts/rapido.py input/documento.pdf

Converter todos os arquivos:

    python scripts/rapido.py input

Instalar dependências:

    python scripts/rapido.py --install

Uso em Python:

    from rapido import converter_rapido

    resultado = converter_rapido(
        "input/documento.pdf"
    )

==================================================
FORMATOS SUPORTADOS

✅ PDF
✅ DOCX
✅ XLSX
✅ XLS
✅ CSV
✅ PPTX
✅ PNG
✅ JPG
✅ JPEG
✅ TXT
✅ MD

Saída padrão:

    output/

==================================================
"""
    )


# ============================================================
# MAIN
# ============================================================
"""
===============================================================================
Projeto:
Descrição:

Desenvolvido por Eduardo Ferreira
Cargo: CTO da TAPOS

© 2026 TAPOS. Todos os direitos reservados.
===============================================================================
"""

if __name__ == "__main__":

    if len(sys.argv) < 2:
        mostrar_ajuda()
        sys.exit(0)

    argumento = sys.argv[1]

    if argumento == "--install":
        instalar_dependencias()
        sys.exit(0)

    caminho = Path(argumento)

    if not caminho.exists():

        print(
            f"❌ Caminho não encontrado: {caminho}"
        )

        sys.exit(1)

    if caminho.is_dir():

        resultados = converter_pasta(
            str(caminho)
        )

        print(
            f"\n✅ {len(resultados)} arquivos convertidos"
        )

    else:

        resultado = converter_rapido(
            str(caminho)
        )

        print(
            f"\n✅ Resultado: {resultado}"
        )