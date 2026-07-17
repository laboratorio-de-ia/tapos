"""
=========================================================
Speech Builder - Speech AI
---------------------------------------------------------
Sprint 6.4.3

Responsável por gerar um texto otimizado para motores TTS.

Nesta versão o builder continua produzindo texto
natural (compatível com Edge TTS), porém já está
preparado para evolução futura para SSML real.

Dependency Injection Ready
=========================================================
"""

import logging
import re

from config.config_manager import ConfigManager
from models.presentation import Presentation

logger = logging.getLogger(__name__)


class SpeechBuilder:

    def __init__(self, cfg: ConfigManager):

        self.cfg = cfg

        self.presentation: Presentation | None = None

        self.output_text = ""

    # -----------------------------------------------------

    def load(self, presentation: Presentation):

        self.presentation = presentation

    # -----------------------------------------------------

    def _clean(self, text: str) -> str:

        text = re.sub(r"<[^>]+>", "", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # -----------------------------------------------------

    def _naturalize(self, text: str) -> str:

        language = self.cfg.language.lower()

        # Português e Espanhol utilizam
        # pausas um pouco menores

        if language.startswith(("pt", "es")):

            text = text.replace(",", ", ...")

            text = text.replace(":", ":\n...")

            text = text.replace(".", ".\n")

        else:

            # Inglês

            text = text.replace(",", ", ...")

            text = text.replace(":", ":\n...")

            text = text.replace(".", ".\n")

        return text

    # -----------------------------------------------------

    def _process_slide(self, slide):

        lines = []

        title = self._clean(slide.title)

        lines.append(title)

        lines.append("...")

        for paragraph in slide.paragraphs:

            text = self._clean(paragraph.text)

            text = self._naturalize(text)

            lines.append(text)

        for lst in slide.lists:

            for item in lst.items:

                item = self._clean(item)

                lines.append(f"- {item}")

                lines.append("...")

        lines.append("")

        lines.append("...")

        return "\n".join(lines)

    # -----------------------------------------------------

    def build(self):

        if self.presentation is None:

            raise RuntimeError(
                "Presentation not loaded."
            )

        logger.info(
            "Building speech text..."
        )

        blocks = []

        for slide in self.presentation.slides:

            blocks.append(
                self._process_slide(slide)
            )

        self.output_text = "\n".join(blocks)

        logger.info(
            "Speech text generated."
        )

        return self.output_text

    # -----------------------------------------------------

    def export(self, path: str):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(self.output_text)

        logger.info(
            "Speech text exported to %s",
            path
        )