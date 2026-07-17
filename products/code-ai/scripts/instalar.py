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
CODE-AI - INSTALADOR

Executar:

    python scripts/instalar.py

Objetivo:

- Validar Python
- Instalar requirements.txt
- Verificar estrutura do projeto
- Validar dependências
- Criar arquivo de teste
"""

from pathlib import Path
import platform
import subprocess
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# BANNER
# ============================================================

def exibir_banner():

    print(
        """
============================================================
CODE-AI - INSTALADOR
============================================================
Validador e instalador do ambiente
============================================================
"""
    )


# ============================================================
# PYTHON
# ============================================================

def verificar_python():

    print("🔍 Verificando Python...")

    if sys.version_info < (3, 8):

        print(
            "❌ Python 3.8 ou superior é obrigatório"
        )

        print(
            f"Versão atual: {sys.version}"
        )

        sys.exit(1)

    print(
        f"✅ Python {sys.version.split()[0]}"
    )


# ============================================================
# REQUIREMENTS
# ============================================================

def instalar_requirements():

    requirements = ROOT_DIR / "requirements.txt"

    if not requirements.exists():

        print(
            "❌ requirements.txt não encontrado."
        )

        return False

    print(
        "\n📦 Instalando dependências..."
    )

    try:

        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                str(requirements),
            ],
            check=True,
        )

        print(
            "✅ Dependências instaladas."
        )

        return True

    except Exception as erro:

        print(
            f"❌ Falha na instalação: {erro}"
        )

        return False


# ============================================================
# TESSERACT
# ============================================================

def verificar_tesseract():

    print(
        "\n🔍 Verificando Tesseract OCR..."
    )

    try:

        subprocess.run(
            ["tesseract", "--version"],
            capture_output=True,
            check=True,
        )

        print(
            "✅ Tesseract encontrado"
        )

        return True

    except Exception:

        sistema = platform.system()

        print(
            "⚠️ Tesseract não encontrado."
        )

        print(
            "\nInstalação recomendada:"
        )

        if sistema == "Windows":

            print(
                "Windows:"
            )
            print(
                "https://github.com/UB-Mannheim/tesseract/wiki"
            )

        elif sistema == "Linux":

            print(
                "sudo apt-get install tesseract-ocr"
            )

        elif sistema == "Darwin":

            print(
                "brew install tesseract"
            )

        return False


# ============================================================
# ESTRUTURA
# ============================================================

def verificar_estrutura():

    print(
        "\n📁 Validando estrutura..."
    )

    itens = [
        "src",
        "src/conversor_markdown.py",
        "scripts",
        "input",
        "output",
        "requirements.txt",
        "readme.md",
    ]

    faltando = []

    for item in itens:

        caminho = ROOT_DIR / item

        if caminho.exists():

            print(
                f"✅ {item}"
            )

        else:

            print(
                f"❌ {item}"
            )

            faltando.append(item)

    if faltando:

        print(
            "\nArquivos ausentes:"
        )

        for item in faltando:

            print(
                f"   - {item}"
            )

        return False

    return True


# ============================================================
# TESTE DAS DEPENDÊNCIAS
# ============================================================

def testar_dependencias():

    print(
        "\n🧪 Testando dependências..."
    )

    try:

        import pandas
        from docx import Document
        from pptx import Presentation
        from PIL import Image
        import pdfplumber

        print(
            "✅ Dependências validadas"
        )

        return True

    except Exception as erro:

        print(
            f"❌ Erro: {erro}"
        )

        return False


# ============================================================
# ARQUIVO DE TESTE
# ============================================================

def criar_arquivo_teste():

    print(
        "\n📝 Criando arquivo de teste..."
    )

    exemplo = """# Teste CODE-AI

Este é um arquivo de teste.

## Recursos

- Markdown
- Conversão
- Estrutura

| Coluna A | Coluna B |
|-----------|-----------|
| Valor 1 | Valor 2 |
"""

    destino = ROOT_DIR / "input" / "teste_exemplo.md"

    destino.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destino.write_text(
        exemplo,
        encoding="utf-8",
    )

    print(
        f"✅ Criado: {destino}"
    )


# ============================================================
# PRÓXIMOS PASSOS
# ============================================================

def exibir_proximos_passos():

    print(
        """
============================================================
✅ INSTALAÇÃO FINALIZADA
============================================================

1. Coloque arquivos para converter em:

    input/

2. Execute:

    python teste_sistema.py

ou

    python src/conversor_markdown.py input

3. Os arquivos convertidos serão salvos em:

    output/

4. Consulte:

    readme.md

============================================================
"""
    )


# ============================================================
# MAIN
# ============================================================

def main():

    exibir_banner()

    verificar_python()

    if not verificar_estrutura():
        return 1

    if not instalar_requirements():
        return 1

    verificar_tesseract()

    if not testar_dependencias():
        return 1

    criar_arquivo_teste()

    exibir_proximos_passos()

    print(
        "\n✨ Ambiente pronto!"
    )

    return 0


if __name__ == "__main__":

    sys.exit(main())