"""
=========================================================
Provider Information
---------------------------------------------------------
Speech AI Platform

Representa os metadados e capacidades de um Provider TTS.

Este objeto não possui lógica de negócio.

Ele apenas descreve o Provider.

Author: Rodrigo Magalhães
=========================================================
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ProviderInfo:
    """
    Metadados de um Provider TTS.

    Attributes
    ----------
    provider_id
        Identificador único do provider.

    name
        Nome amigável.

    vendor
        Fabricante da tecnologia.

    version
        Versão do provider.

    description
        Pequena descrição.

    supports_ssml
        Informa se aceita SSML.

    supports_streaming
        Informa se suporta streaming.

    supports_multivoice
        Suporta múltiplas vozes.

    supports_neural
        Utiliza vozes neurais.

    supported_languages
        Lista de idiomas suportados.

    supported_formats
        Lista de formatos de saída.

    max_characters
        Quantidade máxima de caracteres por requisição.
    """

    # -------------------------------------------------
    # Identificação
    # -------------------------------------------------

    provider_id: str

    name: str

    vendor: str

    version: str

    description: str

    # -------------------------------------------------
    # Capacidades
    # -------------------------------------------------

    supports_ssml: bool = False

    supports_streaming: bool = False

    supports_multivoice: bool = False

    supports_neural: bool = True

    # -------------------------------------------------
    # Idiomas e formatos
    # -------------------------------------------------

    supported_languages: list[str] = field(default_factory=list)

    supported_formats: list[str] = field(default_factory=lambda: ["mp3"])

    # -------------------------------------------------
    # Limites
    # -------------------------------------------------

    max_characters: int = 100000

    # -------------------------------------------------

    @property
    def supports_multiple_languages(self) -> bool:
        """
        Retorna True caso suporte mais de um idioma.
        """

        return len(self.supported_languages) > 1

    # -------------------------------------------------

    @property
    def language_count(self) -> int:
        """
        Quantidade de idiomas suportados.
        """

        return len(self.supported_languages)

    # -------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serializa os metadados para dicionário.

        Ideal para APIs REST ou exportação JSON.
        """

        return {
            "provider_id": self.provider_id,
            "name": self.name,
            "vendor": self.vendor,
            "version": self.version,
            "description": self.description,
            "supports_ssml": self.supports_ssml,
            "supports_streaming": self.supports_streaming,
            "supports_multivoice": self.supports_multivoice,
            "supports_neural": self.supports_neural,
            "supported_languages": self.supported_languages,
            "supported_formats": self.supported_formats,
            "max_characters": self.max_characters,
        }

    # -------------------------------------------------

    def __str__(self) -> str:
        """
        Representação amigável do Provider.
        """

        return (
            f"{self.name} "
            f"({self.vendor}) "
            f"v{self.version}"
        )