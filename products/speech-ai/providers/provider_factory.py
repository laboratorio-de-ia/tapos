"""
=========================================================
Provider Factory
---------------------------------------------------------
Speech AI Platform

Factory responsável por instanciar Providers TTS.

Suporta:

- VoiceProfile (compatibilidade)
- SpeechProfile (nova arquitetura)

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

from config.config_manager import ConfigManager

from models.voice_profile import VoiceProfile
from models.speech_profile import SpeechProfile

from providers import ProviderRegistry


class ProviderFactory:

    # -------------------------------------------------

    @staticmethod
    def create(cfg: ConfigManager):
        """
        Método legado utilizado por partes antigas do projeto.
        """

        provider_class = ProviderRegistry.get(
            cfg.provider.lower()
        )

        return provider_class(
            voice=cfg.voice,
            rate=cfg.rate,
            pitch=cfg.pitch,
            volume=cfg.volume
        )

    # -------------------------------------------------

    @staticmethod
    def create_from_profile(
        profile: VoiceProfile
    ):
        """
        Compatibilidade com a Sprint 8.5
        """

        provider_class = ProviderRegistry.get(
            profile.provider.lower()
        )

        return provider_class(
            voice=profile.voice,
            rate=profile.rate,
            pitch=profile.pitch,
            volume=profile.volume
        )

    # -------------------------------------------------

    @staticmethod
    def create_from_speech_profile(
        profile: SpeechProfile
    ):
        """
        Nova arquitetura (Sprint 8.6).

        Cria um Provider utilizando um SpeechProfile.
        """

        provider_class = ProviderRegistry.get(
            profile.provider.lower()
        )

        return provider_class(
            voice=profile.voice,
            rate=profile.rate,
            pitch=profile.pitch,
            volume=profile.volume
        )