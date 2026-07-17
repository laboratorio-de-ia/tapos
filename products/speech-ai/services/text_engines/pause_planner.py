"""
=========================================================
Pause Planner
---------------------------------------------------------
Speech AI Platform

Responsável por calcular pausas naturais de fala
com base em estrutura linguística.

Esta engine será a base para SSML (<break>).

Enterprise Version 1.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging

from models import Clause
from models import ClauseType

logger = logging.getLogger(__name__)


class PausePlanner:
    """
    Define pausas naturais entre cláusulas.
    """

    # -----------------------------------------------------

    def plan(
        self,
        clauses: list[Clause]
    ) -> list[Clause]:

        logger.info("=" * 60)
        logger.info("Pause Planner")
        logger.info("=" * 60)

        for i, clause in enumerate(clauses):

            clause.estimated_pause_ms = self._calculate_pause(
                clause,
                i,
                clauses
            )

        self._log(clauses)

        return clauses

    # -----------------------------------------------------

    def _calculate_pause(
        self,
        clause: Clause,
        index: int,
        clauses: list[Clause]
    ) -> int:

        base = 120

        #
        # MAIN clause → pausa forte
        #

        if clause.clause_type == ClauseType.MAIN:

            base += 180

        #
        # ENUMERATION → pausa leve
        #

        elif clause.clause_type == ClauseType.ENUMERATION:

            base += 60

        #
        # SUBORDINATE → pausa média
        #

        elif clause.clause_type == ClauseType.SUBORDINATE:

            base += 100

        #
        # Complexidade aumenta pausa
        #

        if clause.is_complex:

            base += 120

        #
        # Cláusulas longas precisam respirar
        #

        if clause.word_count >= 20:

            base += 150

        #
        # Última cláusula → fechamento
        #

        if index == len(clauses) - 1:

            base += 200

        #
        # Penalidade por excesso de vírgulas
        #

        if clause.comma_count >= 3:

            base += 80

        #
        # Ajuste de confiança
        #

        base = int(base * clause.confidence)

        return max(base, 50)

    # -----------------------------------------------------

    def _log(
        self,
        clauses: list[Clause]
    ):

        logger.info("Pause Planning Result:")

        for c in clauses:

            logger.info(
                "[%s] %s | %dms",
                c.clause_type.value,
                c.text[:60],
                c.estimated_pause_ms
            )