"""
=========================================================
Providers Package

Inicializa automaticamente todos os Providers.

Author: Rodrigo Magalhães
=========================================================
"""

from .base_provider import BaseTTSProvider
from .provider_registry import ProviderRegistry
from .provider_factory import ProviderFactory
from .provider_loader import ProviderLoader

ProviderLoader.load()

__all__ = [
    "BaseTTSProvider",
    "ProviderRegistry",
    "ProviderFactory",
]