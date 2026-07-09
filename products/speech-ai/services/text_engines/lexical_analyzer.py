"""
=========================================================
Lexical Analyzer
---------------------------------------------------------
Speech AI Platform

Responsável pela análise léxica do roteiro.

Transforma texto em uma sequência estruturada de Tokens
que poderão ser utilizados pelas demais engines.

Enterprise Version 1.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


# =========================================================
# TOKEN TYPES
# =========================================================


class TokenType(Enum):

    WORD = "WORD"

    NUMBER = "NUMBER"

    PUNCTUATION = "PUNCTUATION"

    COMMA = "COMMA"

    PERIOD = "PERIOD"

    COLON = "COLON"

    SEMICOLON = "SEMICOLON"

    QUESTION = "QUESTION"

    EXCLAMATION = "EXCLAMATION"

    OPEN_PAREN = "OPEN_PAREN"

    CLOSE_PAREN = "CLOSE_PAREN"

    DASH = "DASH"

    QUOTE = "QUOTE"

    UNKNOWN = "UNKNOWN"


# =========================================================
# TOKEN
# =========================================================


@dataclass(slots=True)
class Token:

    text: str

    token_type: TokenType

    position: int


# =========================================================
# LEXICAL ANALYZER
# =========================================================


class LexicalAnalyzer:

    """
    Realiza tokenização simples.

    Esta classe NÃO possui dependências externas.

    Objetivos:

    ✔ velocidade

    ✔ determinismo

    ✔ compatibilidade offline

    ✔ base para IA futura
    """

    TOKEN_PATTERN = re.compile(

        r"""
        \d+(?:[.,]\d+)*          |
        [A-Za-zÀ-ÿ0-9'-]+        |
        [.,;:!?()]              |
        [-–—]                   |
        ["']
        """,

        re.VERBOSE

    )

    # -----------------------------------------------------

    def tokenize(
        self,
        text: str
    ) -> list[Token]:

        tokens = []

        for position, match in enumerate(

            self.TOKEN_PATTERN.finditer(text)

        ):

            value = match.group()

            tokens.append(

                Token(

                    text=value,

                    token_type=self._classify(value),

                    position=position

                )

            )

        return tokens

    # -----------------------------------------------------

    def _classify(
        self,
        value: str
    ) -> TokenType:

        if value == ",":

            return TokenType.COMMA

        if value == ".":

            return TokenType.PERIOD

        if value == ":":

            return TokenType.COLON

        if value == ";":

            return TokenType.SEMICOLON

        if value == "?":

            return TokenType.QUESTION

        if value == "!":

            return TokenType.EXCLAMATION

        if value == "(":

            return TokenType.OPEN_PAREN

        if value == ")":

            return TokenType.CLOSE_PAREN

        if value in {

            "-",

            "–",

            "—"

        }:

            return TokenType.DASH

        if value in {

            "'",

            '"'

        }:

            return TokenType.QUOTE

        if re.fullmatch(

            r"\d+(?:[.,]\d+)*",

            value

        ):

            return TokenType.NUMBER

        if re.fullmatch(

            r"[A-Za-zÀ-ÿ0-9'-]+",

            value

        ):

            return TokenType.WORD

        return TokenType.UNKNOWN

    # -----------------------------------------------------

    def words(
        self,
        text: str
    ) -> list[str]:

        return [

            token.text

            for token in self.tokenize(text)

            if token.token_type == TokenType.WORD

        ]

    # -----------------------------------------------------

    def numbers(
        self,
        text: str
    ) -> list[str]:

        return [

            token.text

            for token in self.tokenize(text)

            if token.token_type == TokenType.NUMBER

        ]

    # -----------------------------------------------------

    def punctuation(
        self,
        text: str
    ) -> list[Token]:

        return [

            token

            for token in self.tokenize(text)

            if token.token_type in {

                TokenType.COMMA,

                TokenType.PERIOD,

                TokenType.COLON,

                TokenType.SEMICOLON,

                TokenType.QUESTION,

                TokenType.EXCLAMATION

            }

        ]

    # -----------------------------------------------------

    def statistics(
        self,
        text: str
    ) -> dict:

        tokens = self.tokenize(text)

        stats = {

            "tokens": len(tokens),

            "words": 0,

            "numbers": 0,

            "punctuation": 0

        }

        for token in tokens:

            if token.token_type == TokenType.WORD:

                stats["words"] += 1

            elif token.token_type == TokenType.NUMBER:

                stats["numbers"] += 1

            else:

                stats["punctuation"] += 1

        return stats