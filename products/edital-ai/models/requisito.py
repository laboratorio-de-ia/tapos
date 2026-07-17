from dataclasses import dataclass
from typing import Optional


@dataclass
class Requisito:
    tipo: str
    descricao: str
    obrigatorio: bool = True
    prazo_validade: Optional[str] = None
    observacoes: Optional[str] = None
