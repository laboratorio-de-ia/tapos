from src.conversor_markdown import ConvertorUniversal


def main():

    conversor = ConvertorUniversal(
        diretorio_saida="output"
    )

    print("=" * 60)
    print("CODE-AI")
    print("=" * 60)

    resultados = conversor.converter_pasta(
        "input"
    )

    conversor.gerar_relatorio()

    print(f"\n✅ Arquivos processados: {len(resultados)}")

    for arquivo in resultados:
        print(f"   {arquivo}")


if __name__ == "__main__":
    main()