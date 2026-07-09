"""
=========================================================
Speech Block Builder
---------------------------------------------------------
Speech AI Platform

Responsável por transformar Clauses em blocos
naturais de leitura para TTS.

Esta engine define como o texto será falado.

Enterprise Version 1.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging

from models import Clause
from models import ClauseType

logger = logging.getLogger(__name__)


class SpeechBlockBuilder:
    """
    Constrói blocos de fala naturais a partir de Clauses.
    """

    # -----------------------------------------------------

    def build(
        self,
        clauses: list[Clause]
    ) -> list[str]:

        logger.info("=" * 60)
        logger.info("Speech Block Builder")
        logger.info("=" * 60)

        blocks = []

        current_block = []

        for clause in clauses:

            if self._is_break_point(clause):

                if current_block:

                    blocks.append(
                        self._join(current_block)
                    )

                    current_block = []

            current_block.append(clause.text)

        if current_block:

            blocks.append(
                self._join(current_block)
            )

        self._log(blocks)

        return blocks

    # -----------------------------------------------------

    def _is_break_point(
        self,
        clause: Clause
    ) -> bool:

        #
        # MAIN clauses sempre iniciam novo bloco
        #

        if clause.clause_type == ClauseType.MAIN:

            return True

        #
        # ENUMERATION quebra bloco naturalmente
        #

        if clause.clause_type == ClauseType.ENUMERATION:

            return True

        #
        # Cláusulas muito complexas quebram fluxo
        #

        if clause.is_complex:

            return True

        #
        # Pausas longas também criam quebra
        #

        if clause.estimated_pause_ms >= 400:

            return True

        return False

    # -----------------------------------------------------

    def _join(
        self,
        clauses: list[str]
    ) -> str:

        text = ""

        for i, clause in enumerate(clauses):

            if i == 0:

                text += clause

            else:

                #
                # ENUMERAÇÕES recebem pausa leve
                #

                if clause.endswith(","):

                    text += " " + clause

                else:

                    text += ". " + clause

        return text.strip()

    # -----------------------------------------------------

    def _log(
        self,
        blocks: list[str]
    ):

        logger.info(
            "Speech Blocks generated: %d",
            len(blocks)
        )

        for i, b in enumerate(blocks):

            logger.info(
                "Block %d: %s",
                i + 1,
                b[:80] + ("..." if len(b) > 80 else "")
            )