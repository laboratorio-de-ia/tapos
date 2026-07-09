"""
=========================================================
Text Optimizer
---------------------------------------------------------
Speech AI Platform

Responsável por preparar o texto para síntese de voz.

Enterprise Version 1.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import re


class TextOptimizer:

    MAX_WORDS_PER_SENTENCE = 35

    MAX_COMMAS = 4

    CONNECTORS = {
        "and",
        "or",
        "but",
        "because",
        "however",
        "therefore",
        "although",
        "while",
        "since",
    }

    # -----------------------------------------------------

    def optimize(
        self,
        text: str
    ) -> str:

        text = self._normalize_whitespace(text)

        text = self._cleanup(text)

        text = self._split_long_sentences(text)

        return text

    # -----------------------------------------------------

    def _normalize_whitespace(
        self,
        text: str
    ) -> str:

        text = text.replace("\r\n", "\n")

        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    # -----------------------------------------------------

    def _cleanup(
        self,
        text: str
    ) -> str:

        return text.strip()

    # -----------------------------------------------------

    def _split_long_sentences(
        self,
        text: str
    ) -> str:

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        optimized = []

        for sentence in sentences:

            if self._needs_split(sentence):

                optimized.extend(
                    self._split_sentence(sentence)
                )

            else:

                optimized.append(sentence)

        return "\n\n".join(optimized)

    # -----------------------------------------------------

    def _needs_split(
        self,
        sentence: str
    ) -> bool:

        words = sentence.split()

        commas = sentence.count(",")

        connectors = self._count_connectors(sentence)

        return (
            len(words) > self.MAX_WORDS_PER_SENTENCE
            or commas > self.MAX_COMMAS
            or connectors >= 3
        )

    # -----------------------------------------------------

    def _count_connectors(
        self,
        sentence: str
    ) -> int:

        words = re.findall(
            r"\b[\w']+\b",
            sentence.lower()
        )

        return sum(

            word in self.CONNECTORS

            for word in words

        )

    # -----------------------------------------------------

    def _split_sentence(
        self,
        sentence: str
    ) -> list[str]:

        chunks = re.split(
            r",\s*",
            sentence
        )

        if len(chunks) <= 1:

            return [sentence]

        result = []

        current = ""

        for part in chunks:

            if len(current.split()) < 18:

                if current:

                    current += ", " + part

                else:

                    current = part

            else:

                result.append(current.strip())

                current = part

        if current:

            result.append(current.strip())

        return result