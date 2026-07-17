from pathlib import Path

from config.config_manager import ConfigManager
from pipeline import TextAnalyzer, NarrationBuilder, SpeechBuilder
from services.speech_intelligence import SpeechIntelligenceEngine
from services.speech_service import SpeechService

from .schemas import SpeechRunResult


def execute_current_pipeline() -> SpeechRunResult:
    cfg = ConfigManager()
    project_root = Path(__file__).resolve().parents[2]

    # 1. Text -> Presentation
    analyzer = TextAnalyzer(cfg)
    presentation = analyzer.run()

    # 2. Intelligence -> SpeechProfile
    intelligence = SpeechIntelligenceEngine(cfg)
    speech_profile = intelligence.build_profile(presentation)

    # 3. Output paths
    output_dir = project_root / cfg.output_directory
    output_dir.mkdir(parents=True, exist_ok=True)

    narration_file = output_dir / "narration.txt"
    speech_file = output_dir / "speech.txt"
    audio_file = output_dir / cfg.output_filename

    # 4. Narration builder
    narrator = NarrationBuilder(cfg)
    narrator.load(presentation)
    narrator.build()
    narrator.export_text(str(narration_file))

    # 5. Speech builder
    speech = SpeechBuilder(cfg)
    speech.load(presentation)
    speech.build()
    speech.export(str(speech_file))

    # 6. Audio generation
    service = SpeechService()
    service.synthesize(
        speech_profile=speech_profile,
        narration_file=speech_file,
        output_file=audio_file,
    )

    return SpeechRunResult(
        status="executed",
        input_file=str(project_root / cfg.script_file),
        narration_file=str(narration_file),
        speech_file=str(speech_file),
        audio_file=str(audio_file),
        provider=speech_profile.provider,
        voice=speech_profile.voice,
        language=speech_profile.language,
        estimated_minutes=speech_profile.estimated_minutes,
    )
