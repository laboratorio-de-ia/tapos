"""
=========================================================
Voice Selector
---------------------------------------------------------
Speech AI Platform

Responsável por selecionar automaticamente o VoiceProfile
mais adequado para um idioma previamente detectado.

Fluxo
-----
Language
    ↓
VoiceManager
    ↓
VoiceProfile

Responsabilidades
-----------------
- Selecionar o VoiceProfile padrão
- Validar disponibilidade da voz
- Garantir compatibilidade com o Provider configurado

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import logging

from config.config_manager import ConfigManager
from models import Language
from models import VoiceProfile

logger = logging.getLogger(__name__)


class VoiceSelector:
    """
    Serviço responsável por selecionar o VoiceProfile
    mais adequado para um idioma.
    """

    # -------------------------------------------------

    def __init__(
        self,
        cfg: ConfigManager
    ) -> None:
        """
        Inicializa o Voice Selector.

        Parameters
        ----------
        cfg : ConfigManager
            Configuração global da aplicação.
        """

        self.cfg = cfg

        self.voice_manager = cfg.voice_manager

        logger.info(
            "VoiceSelector initialized."
        )

    # -------------------------------------------------

    def select(
        self,
        language: Language
    ) -> VoiceProfile:
        """
        Seleciona automaticamente um VoiceProfile.

        Parameters
        ----------
        language : Language
            Idioma previamente detectado.

        Returns
        -------
        VoiceProfile
            Perfil de voz selecionado.

        Raises
        ------
        TypeError
            Caso o parâmetro não seja um objeto Language.

        ValueError
            Caso não exista um VoiceProfile compatível.
        """

        if not isinstance(language, Language):

            raise TypeError(

                "language must be an instance of Language."

            )

        logger.info(

            "Selecting voice for language '%s' using provider '%s'.",

            language.code,

            self.cfg.provider

        )

        profile = self.voice_manager.get_default_by_language(

            language=language.code,

            provider=self.cfg.provider

        )

        if profile is None:

            logger.error(

                "No VoiceProfile available for language '%s' and provider '%s'.",

                language.code,

                self.cfg.provider

            )

            raise ValueError(

                f"No VoiceProfile found for language "

                f"'{language.code}'."

            )

        logger.info(

            "Voice selected successfully: %s (%s)",

            profile.voice,

            profile.provider

        )

        return profile

    # -------------------------------------------------

    def __call__(
        self,
        language: Language
    ) -> VoiceProfile:
        """
        Permite utilizar o objeto como função.

        Example
        -------
        profile = selector(language)
        """

        return self.select(language)

    # -------------------------------------------------

    def __repr__(
        self
    ) -> str:

        return (

            "VoiceSelector("

            f"provider='{self.cfg.provider}')"

        )