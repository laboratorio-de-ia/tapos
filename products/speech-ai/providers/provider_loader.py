"""
=========================================================
Provider Loader

Responsável por descobrir automaticamente todos os
Providers disponíveis no pacote.

Author: Rodrigo Magalhães
=========================================================
"""

from importlib import import_module
from pathlib import Path

from .provider_registry import ProviderRegistry
from .base_provider import BaseTTSProvider


class ProviderLoader:

    @staticmethod
    def load():

        providers_path = Path(__file__).parent

        for file in providers_path.glob("*_provider.py"):

            if file.stem == "base_provider":
                continue

            module = import_module(
                f"providers.{file.stem}"
            )

            for obj in module.__dict__.values():

                if (
                    isinstance(obj, type)
                    and issubclass(obj, BaseTTSProvider)
                    and obj is not BaseTTSProvider
                ):

                    provider_id = (
                        obj.__name__
                        .replace("Provider", "")
                        .lower()
                    )

                    ProviderRegistry.register(
                        provider_id,
                        obj
                    )