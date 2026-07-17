from dataclasses import dataclass
from typing import Optional


@dataclass
class Artefato:
    excel: Optional[str] = None
    pdf: Optional[str] = None
    word: Optional[str] = None
    email: Optional[str] = None
