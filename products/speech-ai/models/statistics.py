"""
=========================================================
Statistics Model
---------------------------------------------------------
Speech AI Platform

Representa todas as métricas calculadas durante o
processamento do texto.

Este objeto é compartilhado entre TextAnalyzer,
Presentation e demais componentes da plataforma.

Author: Rodrigo Magalhães
=========================================================
"""

from dataclasses import dataclass, asdict


@dataclass(slots=True)
class Statistics:
    """
    Métricas calculadas da apresentação.
    """

    characters: int = 0

    words: int = 0

    sentences: int = 0

    paragraphs: int = 0

    estimated_minutes: float = 0.0

    # -------------------------------------------------

    @property
    def estimated_seconds(self) -> int:
        """
        Tempo estimado em segundos.
        """

        return int(self.estimated_minutes * 60)

    # -------------------------------------------------

    @property
    def words_per_sentence(self) -> float:

        if self.sentences == 0:
            return 0.0

        return self.words / self.sentences

    # -------------------------------------------------

    @property
    def characters_per_word(self) -> float:

        if self.words == 0:
            return 0.0

        return self.characters / self.words

    # -------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serializa o objeto.
        """

        return asdict(self)

    # -------------------------------------------------

    def __str__(self):

        return (
            f"Words={self.words} | "
            f"Sentences={self.sentences} | "
            f"Paragraphs={self.paragraphs} | "
            f"Duration={self.estimated_minutes:.2f} min"
        )