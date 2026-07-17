"""
=========================================================
Voice Profile
---------------------------------------------------------
Speech AI Platform

Representa um perfil completo de voz utilizado pelos
Providers TTS.

Este objeto é compartilhado entre:

- VoiceManager
- VoiceSelector
- ProviderFactory
- SpeechService

Author: Rodrigo Magalhães
=========================================================
"""

from dataclasses import dataclass, asdict


@dataclass(slots=True)
class VoiceProfile:
    """
    Perfil completo de voz.
    """

    profile_id: str

    provider: str

    language: str

    locale: str

    voice: str

    name: str

    description: str

    rate: str

    pitch: str

    volume: str

    style: str

    role: str

    gender: str

    is_default: bool = False

    # -------------------------------------------------

    @property
    def is_male(self) -> bool:

        return self.gender.lower() == "male"

    # -------------------------------------------------

    @property
    def is_female(self) -> bool:

        return self.gender.lower() == "female"

    # -------------------------------------------------

    @property
    def is_portuguese(self) -> bool:

        return self.language == "pt"

    # -------------------------------------------------

    @property
    def is_english(self) -> bool:

        return self.language == "en"

    # -------------------------------------------------

    @property
    def display_name(self) -> str:

        return f"{self.name} ({self.voice})"

    # -------------------------------------------------

    def provider_config(self) -> dict:
        """
        Configuração utilizada pelo ProviderFactory.
        """

        return {

            "voice": self.voice,

            "rate": self.rate,

            "pitch": self.pitch,

            "volume": self.volume

        }

    # -------------------------------------------------

    def to_dict(self) -> dict:

        return asdict(self)

    # -------------------------------------------------

    def __str__(self):

        return (
            f"{self.display_name} "
            f"[{self.provider}]"
        )