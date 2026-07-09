from dataclasses import dataclass


@dataclass
class Paragraph:
    """
    Representa um parágrafo da apresentação.
    """

    text: str
    slide_index: int = 0
    importance: int = 1  # 1 = normal, 2 = importante, 3 = destaque