"""
=========================================================
Speech Intelligence Engine
---------------------------------------------------------
Speech AI Platform

Centraliza toda a inteligência da narração.

Fluxo:

Presentation
      │
      ▼
Language Detection
      │
      ▼
Voice Selection
      │
      ▼
Speech Analysis
      │
      ▼
Timing Calculation
      │
      ▼
Speech Optimization
      │
      ▼
SpeechProfile

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging

from config.config_manager import ConfigManager

from services.language_detector import LanguageDetector
from services.voice_selector import VoiceSelector
from services.speech_analyzer import SpeechAnalyzer
from services.timing_calculator import TimingCalculator
from services.speech_optimizer import SpeechOptimizer

logger = logging.getLogger(__name__)


class SpeechIntelligenceEngine:

    # -------------------------------------------------

    def __init__(
        self,
        cfg: ConfigManager
    ):

        self.cfg = cfg

        self.language_detector = LanguageDetector()

        self.voice_selector = VoiceSelector(cfg)

        self.speech_analyzer = SpeechAnalyzer()

        self.timing_calculator = TimingCalculator()

        self.speech_optimizer = SpeechOptimizer()

    # -------------------------------------------------

    def build_profile(
        self,
        presentation
    ):

        logger.info("=" * 60)
        logger.info("Speech Intelligence Engine")
        logger.info("=" * 60)

        text = presentation.to_text()

        # ------------------------------------------
        # Language
        # ------------------------------------------

        language = self.language_detector.detect(
            text
        )

        logger.info(
            "Language detected: %s",
            language.code
        )

        # ------------------------------------------
        # Voice
        # ------------------------------------------

        voice_profile = self.voice_selector.select(
            language
        )

        # ------------------------------------------
        # Analysis
        # ------------------------------------------

        analysis = self.speech_analyzer.analyze(
            presentation,
            language
        )

        # ------------------------------------------
        # Timing
        # ------------------------------------------

        analysis = self.timing_calculator.calculate(
            analysis
        )

        # ------------------------------------------
        # Final Speech Profile
        # ------------------------------------------

        speech_profile = self.speech_optimizer.optimize(
            analysis,
            voice_profile
        )

        logger.info(
            "Speech Profile generated successfully."
        )

        return speech_profile