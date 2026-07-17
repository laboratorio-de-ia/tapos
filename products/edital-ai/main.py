import sys

from app.edital_ai_app import EditalAIApp


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_edital>")
        sys.exit(1)

    arquivo = sys.argv[1]

    app = EditalAIApp()

    print("=" * 60)
    print("EDITAL-AI")
    print("=" * 60)

    edital, analise, artefatos = app.run(arquivo)

    print(f"\nEdital: {edital.numero or '(número não identificado)'}")
    print(f"Órgão: {edital.orgao or '-'}")
    print(f"Score de conformidade: {analise.score_conformidade:.0f}%")
    print(f"Análise via IA: {'sim' if analise.ia_utilizada else 'não (fallback)'}")
    print("\nArtefatos gerados:")
    print(f"  Excel: {artefatos.excel}")
    print(f"  PDF:   {artefatos.pdf}")
    print(f"  Word:  {artefatos.word}")
    print(f"  Email: {artefatos.email}")


if __name__ == "__main__":
    main()
