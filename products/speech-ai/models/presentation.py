"""
=========================================================
Presentation Model
---------------------------------------------------------
Speech AI Platform

Representa uma apresentação completa.

Responsável por armazenar:

- Slides
- Estatísticas
- Exportação do conteúdo

Author: Rodrigo Magalhães
=========================================================
"""

from dataclasses import dataclass, field

from .slide import Slide
from .statistics import Statistics


@dataclass(slots=True)
class Presentation:
    """
    Representa uma apresentação completa.
    """

    title: str = ""

    slides: list[Slide] = field(default_factory=list)

    statistics: Statistics = field(
        default_factory=Statistics
    )

    # -----------------------------------------------------

    def add_slide(
        self,
        slide: Slide
    ):

        self.slides.append(slide)

    # -----------------------------------------------------

    @property
    def total_slides(self) -> int:

        return len(self.slides)

    # -----------------------------------------------------

    @property
    def total_words(self) -> int:

        return self.statistics.words

    # -----------------------------------------------------

    @property
    def total_characters(self) -> int:

        return self.statistics.characters

    # -----------------------------------------------------

    @property
    def total_sentences(self) -> int:

        return self.statistics.sentences

    # -----------------------------------------------------

    @property
    def total_paragraphs(self) -> int:

        return self.statistics.paragraphs

    # -----------------------------------------------------

    def to_text(self) -> str:
        """
        Converte toda a apresentação para texto.
        """

        parts = []

        for slide in self.slides:

            if slide.title:
                parts.append(slide.title)

            # Paragraphs
            for paragraph in getattr(slide, "paragraphs", []):
                parts.append(paragraph.text)

            # Lists
            for list_block in getattr(slide, "lists", []):

                for item in list_block.items:
                    parts.append(item)

        return "\n".join(parts)

    # -----------------------------------------------------

    def summary(self) -> dict:
        """
        Retorna um resumo da apresentação.
        """

        return {

            "slides": self.total_slides,

            "words": self.total_words,

            "characters": self.total_characters,

            "sentences": self.total_sentences,

            "paragraphs": self.total_paragraphs,

            "estimated_minutes": self.statistics.estimated_minutes

        }

    # -----------------------------------------------------

    def __len__(self):

        return self.total_slides

    # -----------------------------------------------------

    def __str__(self):

        return (
            f"Presentation("
            f"slides={self.total_slides}, "
            f"words={self.total_words})"
        )