from dataclasses import dataclass, field
from typing import List

from .paragraph import Paragraph
from .list_block import ListBlock


@dataclass
class Slide:
    """
    Representa um slide completo da apresentação.
    """

    number: int
    title: str

    paragraphs: List[Paragraph] = field(default_factory=list)

    lists: List[ListBlock] = field(default_factory=list)

    def add_paragraph(self, text: str, importance: int = 1):
        self.paragraphs.append(
            Paragraph(
                text=text,
                slide_index=self.number,
                importance=importance,
            )
        )

    def add_list(self, items: List[str]):
        self.lists.append(
            ListBlock(
                items=items,
                slide_index=self.number,
            )
        )