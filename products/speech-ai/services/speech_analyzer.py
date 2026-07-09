"""
=========================================================
Speech Analyzer
---------------------------------------------------------
Speech AI Platform

Analisa o roteiro antes da síntese.

Enterprise Pipeline Version 2.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import re
import logging
from time import perf_counter

from models.speech_analysis import SpeechAnalysis

logger = logging.getLogger(__name__)


class SpeechAnalyzer:
    """
    Pipeline de análise avançada de roteiro.
    """

    DEFAULT_WPM = 145

    # =========================================================
    # PUBLIC API
    # =========================================================

    def analyze(
        self,
        presentation,
        language
    ) -> SpeechAnalysis:

        start = perf_counter()

        logger.info("=" * 60)
        logger.info("Speech Analyzer Started")
        logger.info("=" * 60)

        text = self._extract_text(presentation)

        analysis = SpeechAnalysis()

        analysis.language = language.code

        stats = presentation.statistics

        # -----------------------------
        # Basic Metrics
        # -----------------------------
        self._load_basic_metrics(analysis, stats, presentation)

        # -----------------------------
        # Text Processing
        # -----------------------------
        words = self._extract_words(text)

        sentences = stats.sentences

        # -----------------------------
        # Advanced Analysis
        # -----------------------------
        self._analyze_patterns(analysis, text, words)

        self._calculate_word_metrics(analysis, words)

        self._calculate_sentence_metrics(analysis, words, sentences)

        self._calculate_advanced_metrics(analysis, words)

        # -----------------------------
        # Final Metrics
        # -----------------------------
        analysis.lexical_diversity = self._lexical_diversity(words)

        analysis.execution_time_ms = round(
            (perf_counter() - start) * 1000,
            2
        )

        # -----------------------------
        # Logging Enterprise
        # -----------------------------
        self._log_analysis(analysis)

        logger.info("Speech Analyzer Completed")

        return analysis

    # =========================================================
    # PIPELINE METHODS
    # =========================================================

    def _extract_text(self, presentation) -> str:
        """
        Extrai texto da apresentação.
        """

        if hasattr(presentation, "to_text"):

            return presentation.to_text()

        raise AttributeError(
            "Presentation object must implement to_text()"
        )

    # ---------------------------------------------------------

    def _load_basic_metrics(
        self,
        analysis,
        stats,
        presentation
    ) -> None:

        analysis.words = stats.words
        analysis.characters = stats.characters
        analysis.sentences = stats.sentences
        analysis.paragraphs = stats.paragraphs
        analysis.estimated_minutes = stats.estimated_minutes
        analysis.slides = presentation.total_slides

    # ---------------------------------------------------------

    def _extract_words(self, text: str) -> list[str]:

        return re.findall(r"\b[\w'-]+\b", text)

    # ---------------------------------------------------------

    def _analyze_patterns(
        self,
        analysis,
        text: str,
        words: list[str]
    ) -> None:

        analysis.list_items = len(
            re.findall(r"^[-•*]", text, re.MULTILINE)
        )

        analysis.numbers = len(
            re.findall(r"\d+", text)
        )

        analysis.uppercase_words = len([
            w for w in words
            if len(w) > 1 and w.isupper()
        ])

    # ---------------------------------------------------------

    def _calculate_word_metrics(
        self,
        analysis,
        words: list[str]
    ) -> None:

        if analysis.words > 0:

            analysis.average_word_length = round(
                sum(len(w) for w in words) / analysis.words,
                1
            )

    # ---------------------------------------------------------

    def _calculate_sentence_metrics(
        self,
        analysis,
        words: list[str],
        sentences: int
    ) -> None:

        if sentences > 0:

            analysis.average_words_per_sentence = round(
                len(words) / sentences,
                1
            )

    # ---------------------------------------------------------

    def _calculate_advanced_metrics(
        self,
        analysis,
        words: list[str]
    ) -> None:

        unique_words = set(w.lower() for w in words)

        analysis.unique_words = len(unique_words)

        analysis.vocabulary_density = round(
            len(unique_words) / len(words),
            2
        ) if words else 0.0

        analysis.complexity = self._calculate_complexity(
            analysis.vocabulary_density,
            analysis.average_words_per_sentence
        )

        analysis.reading_style = self._detect_style(
            analysis.average_words_per_sentence
        )

        analysis.reading_pace = self._detect_pace(
            analysis.average_words_per_sentence
        )

    # ---------------------------------------------------------

    def _lexical_diversity(self, words: list[str]) -> float:

        if not words:
            return 0.0

        return len(set(words)) / len(words)

    # ---------------------------------------------------------

    def _calculate_complexity(
        self,
        diversity: float,
        avg_sentence_length: float
    ) -> str:

        score = diversity * avg_sentence_length

        if score < 5:
            return "LOW"

        if score < 10:
            return "MEDIUM"

        return "HIGH"

    # ---------------------------------------------------------

    def _detect_style(
        self,
        avg_sentence_length: float
    ) -> str:

        if avg_sentence_length < 10:
            return "Conversational"

        if avg_sentence_length < 18:
            return "Presentation"

        return "Technical"

    # ---------------------------------------------------------

    def _detect_pace(
        self,
        avg_sentence_length: float
    ) -> str:

        if avg_sentence_length < 10:
            return "Fast"

        if avg_sentence_length < 18:
            return "Normal"

        return "Slow"

    # ---------------------------------------------------------

    def _log_analysis(
        self,
        analysis
    ) -> None:

        logger.info("=" * 60)
        logger.info("Speech Analysis Report")
        logger.info("=" * 60)

        logger.info("Words.............. %s", analysis.words)
        logger.info("Sentences.......... %s", analysis.sentences)
        logger.info("Paragraphs......... %s", analysis.paragraphs)
        logger.info("Characters......... %s", analysis.characters)

        logger.info("List Items......... %s", analysis.list_items)
        logger.info("Numbers............ %s", analysis.numbers)
        logger.info("Uppercase Words.... %s", analysis.uppercase_words)

        logger.info("Vocabulary Density.. %.2f", analysis.vocabulary_density)
        logger.info("Complexity......... %s", analysis.complexity)
        logger.info("Reading Style...... %s", analysis.reading_style)
        logger.info("Reading Pace....... %s", analysis.reading_pace)

        logger.info("Execution Time..... %sms", analysis.execution_time_ms)

        logger.info("=" * 60)