"""
=========================================================
SSML Engine
---------------------------------------------------------
Speech AI Platform

Responsável por converter Clauses em SSML válido.

Transforma estrutura linguística em voz natural.

Enterprise Version 1.0

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging
import html

from models import Clause
from models import ClauseType

logger = logging.getLogger(__name__)


class SSMLEngine:
    """
    Gera SSML a partir de Clauses enriquecidas.
    """

    # -----------------------------------------------------

    def build(
        self,
        clauses: list[Clause],
        voice: str = "default",
        rate: str = "0%",
        pitch: str = "+0Hz"
    ) -> str:

        logger.info("=" * 60)
        logger.info("SSML Engine")
        logger.info("=" * 60)

        ssml = []

        ssml.append('<speak>')

        ssml.append(
            self._voice_tag(
                voice,
                rate,
                pitch
            )
        )

        for clause in clauses:

            ssml.append(
                self._render_clause(clause)
            )

        ssml.append('</speak>')

        result = "\n".join(ssml)

        logger.info("SSML generated successfully")

        return result

    # -----------------------------------------------------

    def _voice_tag(
        self,
        voice: str,
        rate: str,
        pitch: str
    ) -> str:

        return f"""
<voice name="{voice}">
    <prosody rate="{rate}" pitch="{pitch}">
""".strip()

    # -----------------------------------------------------

    def _render_clause(
        self,
        clause: Clause
    ) -> str:

        text = html.escape(clause.text)

        ssml = []

        #
        # Pausa antes da cláusula
        #

        if clause.estimated_pause_ms >= 300:

            ssml.append(
                f'<break time="{clause.estimated_pause_ms}ms"/>'
            )

        #
        # MAIN clause → enfatiza
        #

        if clause.clause_type == ClauseType.MAIN:

            ssml.append(
                f'<emphasis level="moderate">{text}</emphasis>'
            )

        #
        # ENUMERATION → ritmo mais natural
        #

        elif clause.clause_type == ClauseType.ENUMERATION:

            ssml.append(
                f'<prosody rate="95%">{text}</prosody>'
            )

        #
        # SUBORDINATE → leitura leve
        #

        elif clause.clause_type == ClauseType.SUBORDINATE:

            ssml.append(
                f'<prosody rate="98%">{text}</prosody>'
            )

        #
        # Default
        #

        else:

            ssml.append(text)

        #
        # Pausa pós-cláusula
        #

        if clause.estimated_pause_ms >= 200:

            ssml.append(
                f'<break time="{int(clause.estimated_pause_ms/2)}ms"/>'
            )

        return " ".join(ssml)

    # -----------------------------------------------------

    def wrap_complete(
        self,
        ssml_body: str
    ) -> str:

        return f"""
<speak>
    {ssml_body}
</speak>
""".strip()