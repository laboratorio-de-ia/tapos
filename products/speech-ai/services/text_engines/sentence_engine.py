"""
=========================================================
Sentence Engine
---------------------------------------------------------
Speech AI Platform

Responsável por transformar frases longas em
blocos naturais de leitura para mecanismos TTS.

Enterprise Version 1.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import re


class SentenceEngine:

    DEFAULT_MAX_WORDS = 28

    DEFAULT_MAX_COMMAS = 3

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
        "moreover",
        "furthermore",
        "thereby",
        "thus",
        "yet",
    }

    # ---------------------------------------------------------

    def process(
        self,
        text: str
    ) -> str:

        sentences = self._split_sentences(text)

        output = []

        for sentence in sentences:

            output.extend(
                self._optimize_sentence(sentence)
            )

        return "\n\n".join(output)

    # ---------------------------------------------------------

    def _split_sentences(
        self,
        text: str
    ) -> list[str]:

        sentences = re.split(

            r"(?<=[.!?])\s+",

            text.strip()

        )

        return [

            s.strip()

            for s in sentences

            if s.strip()

        ]

    # ---------------------------------------------------------

    def _optimize_sentence(
        self,
        sentence: str
    ) -> list[str]:

        if not self._needs_break(sentence):

            return [sentence]

        return self._split_by_commas(sentence)

    # ---------------------------------------------------------

    def _needs_break(
        self,
        sentence: str
    ) -> bool:

        words = self._words(sentence)

        if len(words) > self.DEFAULT_MAX_WORDS:

            return True

        commas = sentence.count(",")

        if commas > self.DEFAULT_MAX_COMMAS:

            return True

        connectors = self._connector_count(sentence)

        if connectors >= 3:

            return True

        return False

    # ---------------------------------------------------------

    def _split_by_commas(
        self,
        sentence: str
    ) -> list[str]:

        pieces = [

            p.strip()

            for p in sentence.split(",")

            if p.strip()

        ]

        if len(pieces) <= 1:

            return [sentence]

        result = []

        current = ""

        for piece in pieces:

            candidate = piece

            if current:

                candidate = current + ", " + piece

            if len(self._words(candidate)) <= 14:

                current = candidate

            else:

                if current:

                    result.append(current)

                current = piece

        if current:

            result.append(current)

        return result

    # ---------------------------------------------------------

    def _connector_count(
        self,
        sentence: str
    ) -> int:

        words = self._words(sentence.lower())

        return sum(

            word in self.CONNECTORS

            for word in words

        )

    # ---------------------------------------------------------

    def _words(
        self,
        text: str
    ) -> list[str]:

        return re.findall(

            r"[A-Za-zÀ-ÿ0-9'-]+",

            text

        )

    # ---------------------------------------------------------

    def statistics(
        self,
        text: str
    ) -> dict:

        sentences = self._split_sentences(text)

        total_words = sum(

            len(self._words(s))

            for s in sentences

        )

        total_commas = sum(

            s.count(",")

            for s in sentences

        )

        return {

            "sentences": len(sentences),

            "words": total_words,

            "commas": total_commas,

            "average_words": round(

                total_words / max(len(sentences), 1),

                2

            )

        }