"""
=========================================================
Clause Analyzer
---------------------------------------------------------
Speech AI Platform

Responsável por transformar Tokens em Clauses.

Esta é a primeira engine semântica do SpeechAI.

Enterprise Version 1.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging

from models import Clause
from models import ClauseType
from services.text_engines.lexical_analyzer import TokenType


logger = logging.getLogger(__name__)


class ClauseAnalyzer:
    """
    Converte sequência de tokens em estruturas
    semânticas chamadas Clauses.
    """

    # -----------------------------------------------------

    CONNECTORS = {

        "and", "or", "but", "because", "however",
        "therefore", "although", "while", "since",
        "moreover", "furthermore", "thus", "yet"

    }

    # -----------------------------------------------------

    def analyze(
        self,
        tokens: list
    ) -> list[Clause]:

        logger.info("=" * 60)
        logger.info("Clause Analyzer")
        logger.info("=" * 60)

        clauses = []

        buffer = []
        clause_type = ClauseType.MAIN

        order = 0

        for token in tokens:

            if self._is_separator(token):

                if buffer:

                    clauses.append(

                        self._build_clause(
                            buffer,
                            clause_type,
                            order
                        )

                    )

                    order += 1

                    buffer = []

                    clause_type = ClauseType.SUBORDINATE

                continue

            buffer.append(token)

        if buffer:

            clauses.append(

                self._build_clause(
                    buffer,
                    clause_type,
                    order
                )

            )

        self._log(clauses)

        return clauses

    # -----------------------------------------------------

    def _build_clause(
        self,
        tokens,
        clause_type,
        order
    ) -> Clause:

        text = self._tokens_to_text(tokens)

        return Clause(

            text=text,

            clause_type=clause_type,

            order=order,

            word_count=self._count_words(tokens),

            comma_count=self._count_commas(tokens),

            connector_count=self._count_connectors(tokens),

            estimated_pause_ms=self._estimate_pause(tokens),

            confidence=self._estimate_confidence(tokens)

        )

    # -----------------------------------------------------

    def _tokens_to_text(
        self,
        tokens
    ) -> str:

        text = []

        for t in tokens:

            if t.token_type == TokenType.PUNCTUATION:

                text.append(t.text)

            else:

                if text and text[-1] not in [",", ".", "?", "!"]:

                    text.append(" ")

                text.append(t.text)

        return "".join(text).strip()

    # -----------------------------------------------------

    def _is_separator(
        self,
        token
    ) -> bool:

        return token.token_type == TokenType.COMMA

    # -----------------------------------------------------

    def _count_words(self, tokens) -> int:

        return sum(

            1 for t in tokens

            if t.token_type == TokenType.WORD

        )

    # -----------------------------------------------------

    def _count_commas(self, tokens) -> int:

        return sum(

            1 for t in tokens

            if t.token_type == TokenType.COMMA

        )

    # -----------------------------------------------------

    def _count_connectors(self, tokens) -> int:

        return sum(

            1 for t in tokens

            if t.text.lower() in self.CONNECTORS

        )

    # -----------------------------------------------------

    def _estimate_pause(self, tokens) -> int:

        words = self._count_words(tokens)

        commas = self._count_commas(tokens)

        connectors = self._count_connectors(tokens)

        base = 150

        base += commas * 120

        base += connectors * 80

        if words > 20:

            base += 150

        return base

    # -----------------------------------------------------

    def _estimate_confidence(self, tokens) -> float:

        confidence = 1.0

        words = self._count_words(tokens)

        if words < 5:

            confidence -= 0.2

        if words > 40:

            confidence -= 0.1

        connectors = self._count_connectors(tokens)

        if connectors > 3:

            confidence -= 0.1

        return round(max(confidence, 0.0), 2)

    # -----------------------------------------------------

    def _log(self, clauses):

        logger.info(
            "Clauses generated: %d",
            len(clauses)
        )

        for c in clauses:

            logger.info(
                "[%s] %s",
                c.clause_type.value,
                c.text
            )