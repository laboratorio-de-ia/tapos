"""
=========================================================
Language Model

Representa um idioma reconhecido pelo Speech AI.

Este objeto é utilizado pelo LanguageDetector,
VoiceSelector e SpeechService.

Author: Rodrigo Magalhães
=========================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Language:
    """
    Representa um idioma suportado pela plataforma.

    Attributes
    ----------
    code
        Código ISO-639-1.

    locale
        Localidade.

    name
        Nome amigável.

    confidence
        Confiança da detecção.
    """

    # -------------------------------------------------

    code: str

    locale: str

    name: str

    confidence: float = 1.0

    # -------------------------------------------------

    @property
    def is_portuguese(self) -> bool:

        return self.code == "pt"

    # -------------------------------------------------

    @property
    def is_english(self) -> bool:

        return self.code == "en"

    # -------------------------------------------------

    @property
    def is_spanish(self) -> bool:

        return self.code == "es"

    # -------------------------------------------------

    @property
    def is_french(self) -> bool:

        return self.code == "fr"

    # -------------------------------------------------

    def to_dict(self) -> dict:

        return {
            "code": self.code,
            "locale": self.locale,
            "name": self.name,
            "confidence": self.confidence,
        }

    # -------------------------------------------------

    def __str__(self) -> str:

        return (
            f"{self.name} "
            f"({self.locale}) "
            f"{self.confidence:.2%}"
        )