from dataclasses import dataclass, asdict
from typing import List


@dataclass
class ConvertedFile:
    input_file: str
    output_file: str
    size_input_kb: float
    size_output_kb: float
    savings_percent: float


@dataclass
class CodeAIRunResult:
    status: str
    files_processed: int
    converted: List[ConvertedFile]
    errors: List[str]
    report_file: str

    def to_dict(self) -> dict:
        return asdict(self)
