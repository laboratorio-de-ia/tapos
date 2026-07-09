"""
=========================================================
Speech Service
---------------------------------------------------------
Speech AI Platform

Responsável exclusivamente pela síntese de voz.

Fluxo

Narration File
        │
        ▼
SpeechProfile
        │
        ▼
Provider Factory
        │
        ▼
TTS Engine
        │
        ▼
Audio

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging
from pathlib import Path

from models.speech_profile import SpeechProfile

from providers.provider_factory import ProviderFactory

from services.tts_engine import TTSEngine

logger = logging.getLogger(__name__)


class SpeechService:

    # -------------------------------------------------

    def __init__(self):

        pass

    # -------------------------------------------------

    def synthesize(

        self,

        speech_profile: SpeechProfile,

        narration_file: Path,

        output_file: Path

    ) -> Path:

        logger.info("=" * 60)
        logger.info("Speech Service")
        logger.info("=" * 60)

        narration_file = Path(narration_file)

        if not narration_file.exists():

            raise FileNotFoundError(

                f"Narration file not found:\n{narration_file}"

            )

        text = narration_file.read_text(
            encoding="utf-8"
        )

        logger.info(
            "Characters: %d",
            len(text)
        )

        # =====================================================
        # Provider
        # =====================================================

        provider = ProviderFactory.create_from_speech_profile(

            speech_profile

        )

        logger.info(
            "Provider: %s",
            provider
        )

        # =====================================================
        # Engine
        # =====================================================

        engine = TTSEngine(
            provider
        )

        audio = engine.generate(

            text=text,

            output_path=output_file

        )

        logger.info("Speech synthesis completed.")

        return audio