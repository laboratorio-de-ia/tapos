"""
=========================================================
TTS Engine
---------------------------------------------------------
Speech AI Platform

Responsável por executar a síntese de voz utilizando
qualquer Provider compatível com BaseTTSProvider.

Este componente desacopla os Services da implementação
dos Providers.

Fluxo:

SpeechService
        │
        ▼
TTSEngine
        │
        ▼
Provider
        │
        ▼
Audio

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging
from pathlib import Path

from providers.base_provider import BaseTTSProvider

logger = logging.getLogger(__name__)


class TTSEngine:
    """
    Engine responsável pela execução da síntese de voz.
    """

    # -------------------------------------------------

    def __init__(
        self,
        provider: BaseTTSProvider
    ):

        self.provider = provider

        logger.info(
            "TTS Engine initialized with provider: %s",
            provider
        )

    # -------------------------------------------------

    @property
    def provider_name(self) -> str:
        """
        Nome do provider atualmente utilizado.
        """

        return self.provider.__class__.__name__

    # -------------------------------------------------

    def generate(
        self,
        text: str,
        output_path: Path
    ) -> Path:
        """
        Executa a geração do áudio.

        Parameters
        ----------
        text
            Texto que será sintetizado.

        output_path
            Caminho do arquivo MP3.

        Returns
        -------
        Path
            Caminho do áudio gerado.
        """

        logger.info("=" * 60)
        logger.info("TTS Engine")
        logger.info("=" * 60)

        logger.info(
            "Provider.....: %s",
            self.provider_name
        )

        logger.info(
            "Characters...: %d",
            len(text)
        )

        logger.info(
            "Output.......: %s",
            output_path
        )

        audio = self.provider.generate(
            text=text,
            output_path=output_path
        )

        logger.info("TTS finished successfully.")

        return audio

    # -------------------------------------------------

    def __str__(self) -> str:

        return (
            f"TTSEngine("
            f"{self.provider_name}"
            f")"
        )