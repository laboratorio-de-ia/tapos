"""
=========================================================
Speech AI Models

Exporta todos os Domain Models da plataforma.

Author: Rodrigo Magalhães
=========================================================
"""

from .language import Language
from .list_block import ListBlock
from .paragraph import Paragraph
from .presentation import Presentation
from .slide import Slide
from .statistics import Statistics
from .voice_profile import VoiceProfile
from .clause import Clause
from .clause import ClauseType

__all__ = [
    "Language",
    "ListBlock",
    "Paragraph",
    "Presentation",
    "Slide",
    "Statistics",
    "VoiceProfile",
]