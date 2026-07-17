# teste_sistema.py

from src.conversor_markdown import ConvertorUniversal

conversor = ConvertorUniversal(
    diretorio_saida="output"
)

resultado = conversor.converter_arquivo(
    r"input\Stellantis_Copilot_Token_Optimization_Best_Practices.pdf"
)

conversor.gerar_relatorio()

print(f"✅ Resultado: {resultado}")