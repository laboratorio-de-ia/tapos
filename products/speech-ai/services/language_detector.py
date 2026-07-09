"""
=========================================================
Language Detection Service
---------------------------------------------------------
Speech AI Platform

Responsável por detectar automaticamente o idioma
predominante de um texto utilizando detecção offline.

Responsabilidades
-----------------
- Detectar idioma predominante
- Normalizar textos
- Cachear resultados
- Disponibilizar estatísticas
- Servir como serviço central de detecção

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging
from pathlib import Path
from time import perf_counter

from langdetect import DetectorFactory
from langdetect import detect_langs

from models import Language

logger = logging.getLogger(__name__)

# Garante resultados determinísticos
DetectorFactory.seed = 0


class LanguageDetector:
    """
    Serviço responsável pela detecção automática do idioma
    predominante de um texto.
    """

    # -------------------------------------------------

    _LANGUAGE_MAP = {

        "pt": Language(
            code="pt",
            locale="pt-BR",
            name="Portuguese"
        ),

        "en": Language(
            code="en",
            locale="en-US",
            name="English"
        ),

        "es": Language(
            code="es",
            locale="es-ES",
            name="Spanish"
        ),

        "fr": Language(
            code="fr",
            locale="fr-FR",
            name="French"
        ),

    }

    # -------------------------------------------------

    def __init__(self) -> None:

        self._cache: dict[int, Language] = {}

        self._statistics = {

            "detections": 0,
            "cache_hits": 0

        }

        logger.info(
            "LanguageDetector initialized."
        )

    # -------------------------------------------------

    def _normalize(
        self,
        text: str
    ) -> str:

        if not isinstance(text, str):

            raise TypeError(
                "text must be a string."
            )

        text = text.strip()

        if not text:

            raise ValueError(
                "Cannot detect language from empty text."
            )

        return text

    # -------------------------------------------------

    def _cache_key(
        self,
        text: str
    ) -> int:

        return hash(text)

    # -------------------------------------------------

    def detect(
        self,
        text: str
    ) -> Language:
        """
        Detecta o idioma predominante.

        Parameters
        ----------
        text : str

        Returns
        -------
        Language
        """

        start = perf_counter()

        text = self._normalize(text)

        key = self._cache_key(text)

        if key in self._cache:

            self._statistics["cache_hits"] += 1

            logger.info(
                "Language detection cache hit."
            )

            return self._cache[key]

        logger.info(
            "Starting language detection..."
        )

        logger.info(
            "Characters: %d",
            len(text)
        )

        try:

            result = detect_langs(text)[0]

        except Exception:

            logger.exception(
                "Language detection failed."
            )

            raise

        code = result.lang.lower()

        confidence = result.prob

        base = self._LANGUAGE_MAP.get(code)

        if base is None:

            logger.warning(
                "Unsupported language detected: %s",
                code
            )

            language = Language(

                code=code,

                locale=code,

                name="Unknown",

                confidence=confidence

            )

        else:

            language = Language(

                code=base.code,

                locale=base.locale,

                name=base.name,

                confidence=confidence

            )

        self._cache[key] = language

        self._statistics["detections"] += 1

        elapsed = (
            perf_counter() - start
        ) * 1000

        logger.info(
            "Language detected: %s",
            language.name
        )

        logger.info(
            "Confidence: %.2f%%",
            confidence * 100
        )

        logger.info(
            "Detection time: %.2f ms",
            elapsed
        )

        return language

    # -------------------------------------------------

    def detect_file(
        self,
        file_path: str | Path
    ) -> Language:
        """
        Detecta o idioma de um arquivo texto.
        """

        file_path = Path(file_path)

        logger.info(
            "Reading file: %s",
            file_path
        )

        with open(
            file_path,
            encoding="utf-8"
        ) as fp:

            return self.detect(
                fp.read()
            )

    # -------------------------------------------------

    @property
    def statistics(
        self
    ) -> dict[str, int]:

        return {

            "detections":
                self._statistics["detections"],

            "cache_hits":
                self._statistics["cache_hits"],

            "cache_size":
                len(self._cache)

        }

    # -------------------------------------------------

    def clear_cache(
        self
    ) -> None:

        logger.info(
            "Clearing language cache."
        )

        self._cache.clear()

    # -------------------------------------------------

    def __repr__(
        self
    ) -> str:

        return (

            "LanguageDetector("

            f"detections={self._statistics['detections']}, "

            f"cache={len(self._cache)})"

        )