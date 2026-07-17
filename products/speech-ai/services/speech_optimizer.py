"""
=========================================================
Speech Optimizer
---------------------------------------------------------
Speech AI Platform

Converte um SpeechAnalysis em um SpeechProfile.

Enterprise Version 2.1

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging
from time import perf_counter

from models.speech_profile import SpeechProfile
from services.text_optimizer import TextOptimizer

logger = logging.getLogger(__name__)


class SpeechOptimizer:
    """
    Responsável por transformar um SpeechAnalysis
    em um SpeechProfile otimizado para síntese.

    Também disponibiliza uma camada de otimização
    textual que prepara o roteiro para o mecanismo
    TTS, mantendo independência do Provider.
    """

    # ---------------------------------------------------------

    def __init__(self):

        #
        # Engine responsável pela preparação do texto
        # para síntese de voz.
        #
        self.text_optimizer = TextOptimizer()

    # ---------------------------------------------------------

    def optimize(
        self,
        analysis,
        voice_profile
    ) -> SpeechProfile:

        start = perf_counter()

        logger.info("=" * 60)
        logger.info("Speech Optimizer")
        logger.info("=" * 60)

        profile = self._create_profile()

        self._apply_voice(
            profile,
            voice_profile
        )

        self._apply_analysis(
            profile,
            analysis
        )

        self._apply_rate(
            profile,
            analysis
        )

        self._apply_pitch(
            profile,
            analysis
        )

        self._apply_reading_style(
            profile,
            analysis
        )

        self._apply_pacing(
            profile,
            analysis
        )

        self._calculate_confidence(
            profile,
            analysis
        )

        #
        # Hook para futuras regras baseadas em IA.
        #
        self._apply_future_ai_rules(
            profile,
            analysis
        )

        elapsed = round(
            (perf_counter() - start) * 1000,
            2
        )

        self._log_profile(
            profile,
            elapsed
        )

        return profile

    # ---------------------------------------------------------

    def optimize_text(
        self,
        text: str
    ) -> str:
        """
        Executa a otimização textual antes da síntese.

        Atualmente aplica:

        - limpeza
        - normalização
        - preparação para leitura

        Futuras versões:

        - SSML
        - IA Generativa
        - Storytelling
        - Emotion Engine
        - Pause Engine
        """

        logger.info("=" * 60)
        logger.info("Text Optimization")
        logger.info("=" * 60)

        optimized = self.text_optimizer.optimize(text)

        logger.info(
            "Characters: %d -> %d",
            len(text),
            len(optimized)
        )

        logger.info("=" * 60)

        return optimized

    # ---------------------------------------------------------

    def _create_profile(self):

        return SpeechProfile()

    # ---------------------------------------------------------

    def _apply_voice(
        self,
        profile,
        voice_profile
    ):

        profile.voice = voice_profile.voice
        profile.locale = voice_profile.locale
        profile.provider = voice_profile.provider

    # ---------------------------------------------------------

    def _apply_analysis(
        self,
        profile,
        analysis
    ):

        profile.language = analysis.language

        profile.complexity = analysis.complexity

        profile.estimated_minutes = analysis.estimated_minutes

        profile.recommended_wpm = analysis.recommended_wpm

    # ---------------------------------------------------------

    def _apply_rate(
        self,
        profile,
        analysis
    ):

        profile.rate = analysis.recommended_rate

    # ---------------------------------------------------------

    def _apply_pitch(
        self,
        profile,
        analysis
    ):

        complexity = str(
            analysis.complexity
        ).upper()

        if complexity == "HIGH":

            profile.pitch = "-1Hz"

        elif complexity == "MEDIUM":

            profile.pitch = "+0Hz"

        else:

            profile.pitch = "+1Hz"

    # ---------------------------------------------------------

    def _apply_reading_style(
        self,
        profile,
        analysis
    ):

        avg = analysis.average_words_per_sentence

        if avg >= 20:

            profile.reading_style = "Technical"

        elif avg >= 14:

            profile.reading_style = "Business"

        else:

            profile.reading_style = "Conversational"

    # ---------------------------------------------------------

    def _apply_pacing(
        self,
        profile,
        analysis
    ):

        complexity = str(
            analysis.complexity
        ).upper()

        if complexity == "HIGH":

            profile.pacing = "Slow"

        elif complexity == "MEDIUM":

            profile.pacing = "Normal"

        else:

            profile.pacing = "Fast"

    # ---------------------------------------------------------

    def _calculate_confidence(
        self,
        profile,
        analysis
    ):

        confidence = 1.0

        #
        # Texto muito pequeno
        #

        if analysis.words < 150:

            confidence -= 0.10

        #
        # Poucas frases
        #

        if analysis.sentences < 8:

            confidence -= 0.10

        #
        # Diversidade lexical
        #

        if hasattr(
            analysis,
            "vocabulary_density"
        ):

            if analysis.vocabulary_density < 0.35:

                confidence -= 0.05

        #
        # Confiança do detector de idioma
        #

        if hasattr(
            analysis,
            "language_confidence"
        ):

            if analysis.language_confidence < 0.80:

                confidence -= 0.05

        profile.confidence = round(

            max(
                confidence,
                0.0
            ),

            2

        )

    # ---------------------------------------------------------

    def _apply_future_ai_rules(
        self,
        profile,
        analysis
    ):

        """
        Hook reservado para Sprint 9.

        Engines previstas:

        - Azure OpenAI
        - OpenAI GPT
        - Claude
        - Gemini
        - Ollama
        - Emotion Engine
        - Storytelling Engine
        """

        return

    # ---------------------------------------------------------

    def _log_profile(
        self,
        profile,
        elapsed
    ):

        logger.info("=" * 60)
        logger.info("Speech Profile")
        logger.info("=" * 60)

        logger.info(
            "Language.......... %s",
            profile.language
        )

        logger.info(
            "Voice............. %s",
            profile.voice
        )

        logger.info(
            "Provider.......... %s",
            profile.provider
        )

        logger.info(
            "Rate.............. %s",
            profile.rate
        )

        logger.info(
            "Pitch............. %s",
            profile.pitch
        )

        logger.info(
            "Reading Style..... %s",
            profile.reading_style
        )

        logger.info(
            "Pacing............ %s",
            profile.pacing
        )

        logger.info(
            "Complexity........ %s",
            profile.complexity
        )

        logger.info(
            "Confidence........ %.2f",
            profile.confidence
        )

        logger.info(
            "Optimization Time. %.2f ms",
            elapsed
        )

        logger.info("=" * 60)