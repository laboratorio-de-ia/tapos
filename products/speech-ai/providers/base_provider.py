"""
=========================================================
Base TTS Provider

Contrato para qualquer mecanismo de geração de áudio.

Todo Provider deverá implementar esta interface.

Author: Rodrigo Magalhães
=========================================================
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseTTSProvider(ABC):

    def __init__(
        self,
        voice: str,
        rate: str,
        pitch: str,
        volume: str
    ):

        self.voice = voice
        self.rate = rate
        self.pitch = pitch
        self.volume = volume

    # -------------------------------------------------

    @abstractmethod
    def generate(
        self,
        text: str,
        output_path: Path
    ) -> Path:
        """
        Gera o áudio utilizando o provider.

        Deve retornar o caminho do arquivo gerado.
        """
        pass