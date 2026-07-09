"""
=========================================================
Speech Profile
---------------------------------------------------------
Speech AI Platform

Representa todas as decisões tomadas pelo
Speech Optimizer.

Author: Rodrigo Magalhães
=========================================================
"""

from dataclasses import dataclass


@dataclass
class SpeechProfile:

    language: str = ""

    voice: str = ""

    locale: str = ""

    provider: str = ""

    rate: str = "-10%"

    pitch: str = "+0Hz"

    volume: str = "+0%"

    recommended_wpm: int = 145

    reading_style: str = "Default"

    pacing: str = "Normal"

    complexity: str = "Medium"

    confidence: float = 1.0

    estimated_minutes: float = 0.0