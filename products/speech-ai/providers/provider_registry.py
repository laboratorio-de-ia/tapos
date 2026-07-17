"""
=========================================================
Provider Registry
---------------------------------------------------------
Speech AI Platform

Registro central de Providers TTS.

Responsabilidades
-----------------
- Registrar Providers
- Recuperar Providers
- Listar Providers disponíveis
- Permitir expansão dinâmica da plataforma

Author: Rodrigo Magalhães
=========================================================
"""

from typing import Type

from .base_provider import BaseTTSProvider


class ProviderRegistry:
    """
    Registro central dos Providers disponíveis.
    """

    _providers: dict[str, Type[BaseTTSProvider]] = {}

    # -------------------------------------------------

    @classmethod
    def register(
        cls,
        provider_id: str,
        provider_class: Type[BaseTTSProvider]
    ) -> None:
        """
        Registra um Provider.
        """

        cls._providers[provider_id.lower()] = provider_class

    # -------------------------------------------------

    @classmethod
    def get(
        cls,
        provider_id: str
    ) -> Type[BaseTTSProvider]:
        """
        Recupera a classe de um Provider.
        """

        provider = cls._providers.get(provider_id.lower())

        if provider is None:
            raise ValueError(
                f"Provider '{provider_id}' not registered."
            )

        return provider

    # -------------------------------------------------

    @classmethod
    def exists(
        cls,
        provider_id: str
    ) -> bool:
        """
        Verifica se o Provider está registrado.
        """

        return provider_id.lower() in cls._providers

    # -------------------------------------------------

    @classmethod
    def list(cls) -> list[str]:
        """
        Lista os Providers registrados.
        """

        return sorted(cls._providers.keys())

    # -------------------------------------------------

    @classmethod
    def clear(cls):
        """
        Limpa todos os registros.

        Utilizado apenas em testes.
        """

        cls._providers.clear()