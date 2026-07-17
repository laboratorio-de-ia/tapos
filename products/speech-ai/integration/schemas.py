from dataclasses import dataclass, asdict


@dataclass
class SpeechRunResult:
    status: str
    input_file: str
    narration_file: str
    speech_file: str
    audio_file: str
    provider: str
    voice: str
    language: str
    estimated_minutes: float

    def to_dict(self) -> dict:
        return asdict(self)
