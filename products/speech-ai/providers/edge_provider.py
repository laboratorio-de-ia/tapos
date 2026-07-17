"""
=========================================================
Edge TTS Provider
---------------------------------------------------------
Speech AI Platform

Implementação do Provider utilizando Microsoft Edge TTS.

Responsabilidades
-----------------
- Gerar áudio utilizando Microsoft Edge TTS
- Expor informações do Provider
- Encapsular toda a implementação do Edge
- Preparar suporte futuro para SSML

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import edge_tts

from .base_provider import BaseTTSProvider
from .provider_info import ProviderInfo

logger = logging.getLogger(__name__)


class EdgeProvider(BaseTTSProvider):
    """
    Provider Microsoft Edge TTS.
    """

    # -------------------------------------------------

    def __init__(
        self,
        voice: str,
        rate: str,
        pitch: str,
        volume: str
    ):

        super().__init__(
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )

        self.info = ProviderInfo(

            provider_id="edge",

            name="Microsoft Edge TTS",

            vendor="Microsoft",

            version="1.1.0",

            description="Microsoft Neural Text-to-Speech Provider",

            supports_ssml=False,

            supports_streaming=False,

            supports_multivoice=False,

            supports_neural=True,

            supported_languages=[

                "pt-BR",

                "en-US",

                "es-ES",

                "fr-FR",

                "de-DE",

                "it-IT",

                "ja-JP"

            ],

            supported_formats=[

                "mp3"

            ],

            max_characters=100000

        )

        logger.info(

            "Provider initialized: %s",

            self.info

        )

    # -------------------------------------------------

    async def _generate_async(

        self,

        text: str,

        output_path: Path

    ) -> None:

        logger.info("Generating audio...")

        logger.info("Voice.....: %s", self.voice)

        logger.info("Rate......: %s", self.rate)

        logger.info("Pitch.....: %s", self.pitch)

        logger.info("Volume....: %s", self.volume)

        communicate = edge_tts.Communicate(

            text=text,

            voice=self.voice,

            rate=self.rate,

            pitch=self.pitch,

            volume=self.volume

        )

        await communicate.save(

            str(output_path)

        )

        logger.info("Audio generated successfully.")

    # -------------------------------------------------

    def generate(

        self,

        text: str,

        output_path: Path

    ) -> Path:

        """
        Gera um arquivo de áudio.
        """

        output_path = Path(output_path)

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        asyncio.run(

            self._generate_async(

                text=text,

                output_path=output_path

            )

        )

        return output_path

    # -------------------------------------------------

    @property
    def provider_info(self) -> ProviderInfo:
        """
        Retorna os metadados do Provider.
        """

        return self.info

    # -------------------------------------------------

    def supports_language(
        self,
        locale: str
    ) -> bool:

        return locale in self.info.supported_languages

    # -------------------------------------------------

    def __str__(self):

        return str(self.info)