from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .objeto import Objeto
from .requisito import Requisito
from .prazo import Prazo


@dataclass
class Secao:
    titulo: str
    conteudo: str


@dataclass
class Edital:
    id: str
    numero: Optional[str] = None
    orgao: Optional[str] = None
    modalidade: Optional[str] = None
    objeto: Optional[str] = None
    texto_completo: str = ""
    data_upload: datetime = field(default_factory=datetime.now)

    secoes: List[Secao] = field(default_factory=list)
    objetos: List[Objeto] = field(default_factory=list)
    requisitos: List[Requisito] = field(default_factory=list)
    prazos: List[Prazo] = field(default_factory=list)

    status: str = "processando"
