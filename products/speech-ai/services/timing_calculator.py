"""
=========================================================
Timing Calculator
---------------------------------------------------------
Speech AI Platform

Calcula automaticamente o ritmo ideal da narração.

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class TimingCalculator:

    def calculate(self, analysis):

        logger.info("Calculating speech timing...")

        average = analysis.average_words_per_sentence

        # -------------------------------
        # Complexidade
        # -------------------------------

        if average >= 22:

            complexity = "High"

            wpm = 130

            rate = "-15%"

        elif average >= 16:

            complexity = "Medium"

            wpm = 140

            rate = "-10%"

        else:

            complexity = "Low"

            wpm = 150

            rate = "-5%"

        # -------------------------------
        # Ajuste por idioma
        # -------------------------------

        if analysis.language == "pt":

            wpm -= 5

        # -------------------------------
        # Atualiza o objeto
        # -------------------------------

        analysis.complexity = complexity

        analysis.recommended_wpm = wpm

        analysis.recommended_rate = rate

        logger.info(

            "Complexity..... %s",

            complexity

        )

        logger.info(

            "Recommended WPM %s",

            wpm

        )

        logger.info(

            "Recommended Rate %s",

            rate

        )

        return analysis