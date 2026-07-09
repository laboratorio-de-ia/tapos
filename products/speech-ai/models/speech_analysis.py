"""
=========================================================
Speech Analysis Model
---------------------------------------------------------
Speech AI Platform

Representa o resultado da análise textual.

Author: Rodrigo Magalhães
=========================================================
"""

from dataclasses import dataclass


@dataclass
class SpeechAnalysis:

    language: str = ""

    slides: int = 0

    words: int = 0

    characters: int = 0

    sentences: int = 0

    paragraphs: int = 0

    average_words_per_sentence: float = 0.0

    average_word_length: float = 0.0

    list_items: int = 0

    numbers: int = 0

    uppercase_words: int = 0

    estimated_minutes: float = 0.0

    complexity: str = "Unknown"

    reading_style: str = "Unknown"

    recommended_wpm: int = 145

    recommended_rate: str = "-10%"