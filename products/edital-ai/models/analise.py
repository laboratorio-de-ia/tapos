from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from .objeto import Objeto
from .requisito import Requisito
from .prazo import Prazo


@dataclass
class Analise:
    edital_id: str
    resumo_executivo: str = ""
    objetos_identificados: List[Objeto] = field(default_factory=list)
    requisitos_identificados: List[Requisito] = field(default_factory=list)
    prazos_identificados: List[Prazo] = field(default_factory=list)
    riscos: List[str] = field(default_factory=list)
    oportunidades: List[str] = field(default_factory=list)
    recomendacoes: List[str] = field(default_factory=list)
    score_conformidade: float = 0.0
    ia_utilizada: bool = False
    data_analise: datetime = field(default_factory=datetime.now)
