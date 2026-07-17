"""
=========================================================
Narration Builder - Speech AI
---------------------------------------------------------
Sprint 6.4.2

Transforma a estrutura (Presentation) em um texto natural
para narração humana.

Agora utilizando Dependency Injection.
=========================================================
"""

import logging
import re

from config.config_manager import ConfigManager

from models.presentation import Presentation
from models.slide import Slide

logger = logging.getLogger(__name__)


class NarrationBuilder:

    def __init__(self, cfg: ConfigManager):

        self.cfg = cfg

        self.presentation: Presentation | None = None

        self.output_blocks: list[str] = []

    # -----------------------------------------------------

    def load(self, presentation: Presentation):

        self.presentation = presentation

    # -----------------------------------------------------

    def _break_long_sentence(self, text: str) -> str:
        """
        Divide frases muito longas simulando
        pausas naturais da fala.
        """

        text = re.sub(",", "...,", text)

        text = re.sub(
            r"\band\b",
            "and...",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\bwith\b",
            "with...",
            text,
            flags=re.IGNORECASE
        )

        return text

    # -----------------------------------------------------

    def _process_paragraph(self, text: str) -> str:

        text = text.strip()

        # Regra atual
        if len(text.split()) > 18:

            text = self._break_long_sentence(text)

        text = text.replace(":", ":\n")

        return text

    # -----------------------------------------------------

    def _process_slide(self, slide: Slide) -> str:

        lines = []

        # título

        lines.append(
            slide.title + "...\n"
        )

        # parágrafos

        for paragraph in slide.paragraphs:

            processed = self._process_paragraph(
                paragraph.text
            )

            lines.append(
                processed + "\n"
            )

        # listas

        for lst in slide.lists:

            for item in lst.items:

                lines.append(
                    "- " + item + "...\n"
                )

        return "\n".join(lines)

    # -----------------------------------------------------

    def build(self):

        if self.presentation is None:

            raise RuntimeError(
                "Presentation not loaded."
            )

        logger.info(
            "Building narration..."
        )

        self.output_blocks.clear()

        for slide in self.presentation.slides:

            block = self._process_slide(slide)

            self.output_blocks.append(block)

        logger.info(
            "%d narration blocks generated.",
            len(self.output_blocks)
        )

        return self.output_blocks

    # -----------------------------------------------------

    def export_text(self, path: str):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n\n".join(
                    self.output_blocks
                )
            )

        logger.info(
            "Narration exported to %s",
            path
        )