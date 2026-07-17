from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional


@dataclass
class EditalRunResult:
    status: str
    edital_id: str
    numero_edital: Optional[str]
    orgao: Optional[str]
    modalidade: Optional[str]
    objetos_identificados: int
    requisitos_identificados: int
    prazos_identificados: int
    score_conformidade: float
    ia_utilizada: bool
    resumo_executivo: str
    prazos_criticos: List[dict] = field(default_factory=list)
    riscos: List[str] = field(default_factory=list)
    oportunidades: List[str] = field(default_factory=list)
    recomendacoes: List[str] = field(default_factory=list)
    arquivos_gerados: Dict[str, Optional[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)
