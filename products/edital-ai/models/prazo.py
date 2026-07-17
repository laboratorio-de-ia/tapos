from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Prazo:
    descricao: str
    data_texto: str
    data: Optional[datetime] = None
    hora: Optional[str] = None
    dias_para_evento: Optional[int] = None
    critico: bool = False
