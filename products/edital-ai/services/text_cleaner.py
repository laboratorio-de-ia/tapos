import re


def limpar_texto(texto: str) -> str:
    """Normaliza espaços/quebras de linha excessivos preservando parágrafos."""
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()
