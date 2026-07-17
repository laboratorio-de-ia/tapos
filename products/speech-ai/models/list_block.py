from dataclasses import dataclass
from typing import List


@dataclass
class ListBlock:
    """
    Representa listas dentro da apresentação.
    """

    items: List[str]
    slide_index: int = 0