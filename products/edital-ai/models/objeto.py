from dataclasses import dataclass
from typing import Optional


@dataclass
class Objeto:
    numero: int
    descricao: str
    quantidade: Optional[float] = None
    unidade: Optional[str] = None
    valor_estimado: Optional[float] = None
    modalidade_entrega: Optional[str] = None
    especificacoes: Optional[str] = None
    fabricante_sugerido: Optional[str] = None
