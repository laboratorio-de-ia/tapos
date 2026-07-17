"""
=========================================================
Clause Model
---------------------------------------------------------
Speech AI Platform

Representa uma unidade lógica de uma sentença.

Uma Clause pode representar:

- Oração principal
- Oração subordinada
- Enumeração
- Fechamento
- Introdução

Este modelo é utilizado por:

- ClauseAnalyzer
- SentenceEngine
- SpeechBlockBuilder
- PausePlanner
- StorytellingEngine
- EmotionEngine

Enterprise Version 1.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# =========================================================
# CLAUSE TYPE
# =========================================================


class ClauseType(Enum):

    MAIN = "MAIN"

    SUBORDINATE = "SUBORDINATE"

    ENUMERATION = "ENUMERATION"

    INTRODUCTION = "INTRODUCTION"

    CONCLUSION = "CONCLUSION"

    UNKNOWN = "UNKNOWN"


# =========================================================
# CLAUSE
# =========================================================


@dataclass(slots=True)
class Clause:
    """
    Representa uma unidade lógica de leitura.
    """

    text: str

    clause_type: ClauseType = ClauseType.UNKNOWN

    order: int = 0

    word_count: int = 0

    comma_count: int = 0

    connector_count: int = 0

    estimated_pause_ms: int = 0

    confidence: float = 1.0

    metadata: dict = field(default_factory=dict)

    # -----------------------------------------------------

    @property
    def is_main(self) -> bool:

        return self.clause_type == ClauseType.MAIN

    # -----------------------------------------------------

    @property
    def is_enumeration(self) -> bool:

        return self.clause_type == ClauseType.ENUMERATION

    # -----------------------------------------------------

    @property
    def is_subordinate(self) -> bool:

        return self.clause_type == ClauseType.SUBORDINATE

    # -----------------------------------------------------

    @property
    def is_introduction(self) -> bool:

        return self.clause_type == ClauseType.INTRODUCTION

    # -----------------------------------------------------

    @property
    def is_conclusion(self) -> bool:

        return self.clause_type == ClauseType.CONCLUSION

    # -----------------------------------------------------

    @property
    def needs_pause(self) -> bool:
        """
        Indica se uma pausa deve ser inserida
        após esta cláusula.
        """

        return self.estimated_pause_ms > 0

    # -----------------------------------------------------

    @property
    def is_complex(self) -> bool:
        """
        Indica se a cláusula é considerada
        complexa para leitura.
        """

        return (
            self.word_count >= 20
            or self.connector_count >= 3
            or self.comma_count >= 3
        )

    # -----------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value
    ) -> None:

        self.metadata[key] = value

    # -----------------------------------------------------

    def get_metadata(
        self,
        key: str,
        default=None
    ):

        return self.metadata.get(
            key,
            default
        )

    # -----------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "text": self.text,

            "type": self.clause_type.value,

            "order": self.order,

            "word_count": self.word_count,

            "comma_count": self.comma_count,

            "connector_count": self.connector_count,

            "estimated_pause_ms": self.estimated_pause_ms,

            "confidence": self.confidence,

            "metadata": self.metadata

        }

    # -----------------------------------------------------

    def __len__(self):

        return self.word_count

    # -----------------------------------------------------

    def __str__(self):

        return self.text

    # -----------------------------------------------------

    def __repr__(self):

        return (

            f"Clause("

            f"type={self.clause_type.value}, "

            f"words={self.word_count}, "

            f"pause={self.estimated_pause_ms}ms)"

        )