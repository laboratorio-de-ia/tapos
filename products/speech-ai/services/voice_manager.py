"""
=========================================================
Voice Manager
---------------------------------------------------------
Speech AI Platform

Centraliza o gerenciamento dos perfis de voz disponíveis
na plataforma.

Responsabilidades
-----------------
- Carregar perfis de voz
- Fornecer consultas rápidas
- Gerenciar perfis padrão
- Disponibilizar estatísticas
- Servir como repositório somente leitura

Author: Rodrigo Magalhães
=========================================================
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from models import VoiceProfile

logger = logging.getLogger(__name__)


class VoiceManager:
    """
    Repositório central dos Voice Profiles.

    Após carregado, opera como um repositório somente leitura.
    """

    # -------------------------------------------------

    def __init__(
        self,
        voices_file: str | Path
    ) -> None:

        self.voices_file = Path(voices_file)

        self._profiles: dict[str, VoiceProfile] = {}

        self._defaults: dict[str, str] = {}

        self._languages: list[str] = []

        self._providers: list[str] = []

        self._load()

    # -------------------------------------------------

    def _load(self) -> None:
        """
        Carrega o arquivo voices.json.
        """

        logger.info(
            "Loading Voice Profiles..."
        )

        if not self.voices_file.exists():

            raise FileNotFoundError(
                self.voices_file
            )

        try:

            with open(
                self.voices_file,
                "r",
                encoding="utf-8"
            ) as fp:

                data = json.load(fp)

        except Exception:

            logger.exception(
                "Failed loading Voice Profiles."
            )

            raise

        self._profiles.clear()

        self._defaults = data.get(
            "defaults",
            {}
        )

        for profile_id, item in data["profiles"].items():

            profile = VoiceProfile(

                profile_id=profile_id,

                **item

            )

            self._profiles[profile_id] = profile

        self._languages = sorted({

            profile.language

            for profile in self._profiles.values()

        })

        self._providers = sorted({

            profile.provider

            for profile in self._profiles.values()

        })

        logger.info(

            "Loaded %d Voice Profiles.",

            len(self._profiles)

        )

    # -------------------------------------------------

    def reload(self) -> None:
        """
        Recarrega os perfis de voz.
        """

        logger.info(
            "Reloading Voice Profiles..."
        )

        self._load()

    # -------------------------------------------------

    def get(
        self,
        profile_id: str
    ) -> VoiceProfile:
        """
        Retorna um VoiceProfile pelo ID.
        """

        return self._profiles[profile_id]

    # -------------------------------------------------

    def exists(
        self,
        profile_id: str
    ) -> bool:
        """
        Verifica se um perfil existe.
        """

        return profile_id in self._profiles

    # -------------------------------------------------

    def list(
        self
    ) -> list[VoiceProfile]:
        """
        Lista todos os perfis.
        """

        return list(
            self._profiles.values()
        )

    # -------------------------------------------------

    def list_languages(
        self
    ) -> list[str]:
        """
        Lista os idiomas disponíveis.
        """

        return self._languages.copy()

    # -------------------------------------------------

    def list_providers(
        self
    ) -> list[str]:
        """
        Lista os providers disponíveis.
        """

        return self._providers.copy()

    # -------------------------------------------------

    def get_default_by_language(
        self,
        language: str,
        provider: str | None = None
    ) -> VoiceProfile | None:
        """
        Retorna o VoiceProfile padrão para um idioma.
        """

        language = language.lower()

        if provider:

            provider = provider.lower()

        profile_id = self._defaults.get(
            language
        )

        if profile_id is None:

            return None

        profile = self._profiles.get(
            profile_id
        )

        if profile is None:

            return None

        if provider:

            if profile.provider.lower() != provider:

                return None

        return profile

    # -------------------------------------------------

    def get_by_provider(
        self,
        provider: str
    ) -> list[VoiceProfile]:
        """
        Lista perfis por provider.
        """

        provider = provider.lower()

        return [

            profile

            for profile in self._profiles.values()

            if profile.provider.lower() == provider

        ]

    # -------------------------------------------------

    def get_by_voice(
        self,
        voice: str
    ) -> VoiceProfile | None:
        """
        Pesquisa pelo nome da voz.
        """

        for profile in self._profiles.values():

            if profile.voice == voice:

                return profile

        return None

    # -------------------------------------------------

    def search(
        self,
        text: str
    ) -> list[VoiceProfile]:
        """
        Pesquisa livre.
        """

        text = text.lower()

        return [

            profile

            for profile in self._profiles.values()

            if (

                text in profile.name.lower()

                or text in profile.voice.lower()

                or text in profile.language.lower()

                or text in profile.locale.lower()

            )

        ]

    # -------------------------------------------------

    @property
    def statistics(
        self
    ) -> dict[str, int]:
        """
        Estatísticas do repositório.
        """

        return {

            "profiles": len(self),

            "languages": len(self._languages),

            "providers": len(self._providers)

        }

    # -------------------------------------------------

    def __contains__(
        self,
        profile_id: str
    ) -> bool:

        return profile_id in self._profiles

    # -------------------------------------------------

    def __len__(
        self
    ) -> int:

        return len(
            self._profiles
        )

    # -------------------------------------------------

    def __iter__(
        self
    ):

        return iter(
            self._profiles.values()
        )

    # -------------------------------------------------

    def __repr__(
        self
    ) -> str:

        return (

            "VoiceManager("

            f"profiles={len(self)}, "

            f"languages={len(self._languages)}, "

            f"providers={len(self._providers)})"

        )