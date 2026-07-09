"""
=========================================================
Pipeline Package
---------------------------------------------------------
Speech AI Platform

Exporta os principais componentes da Pipeline.

Author: Rodrigo Magalhães
=========================================================
"""

from .text_analyzer import TextAnalyzer
from .narration_builder import NarrationBuilder
from .speech_builder import SpeechBuilder

__all__ = [

    "TextAnalyzer",

    "NarrationBuilder",

    "SpeechBuilder",

]