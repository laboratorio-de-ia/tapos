# Speech-AI — Configuração

## `config/settings.json`

- `input.script_file` — caminho do texto de origem
- `tts.provider` + `tts.voice_profile` — seleciona um perfil de `voices.json`
- `output.directory` / `output.filename`
- `speech.pause_short` / `pause_long` / `split_long_sentences`
- `project.name` / `project.version`

## `config/voices.json`

- `defaults` — mapa idioma → `profile_id` (hoje: `en` → `en-us-guy`, `pt` → `pt-br-francisca`)
- `profiles` — 4 perfis definidos: `en-us-guy`, `en-us-jenny`, `pt-br-francisca`, `pt-br-antonio`, cada um com `provider/language/locale/voice/name/description/rate/pitch/volume/style/role/gender`

## `config/config_manager.py::ConfigManager`

Carrega os dois arquivos JSON na construção e mantém um `VoiceManager` interno. Expõe:

- `provider`, `voice_profile_name`, `voice_profile`
- **atalhos de compatibilidade retroativa**: `voice`, `language`, `locale`, `rate`, `pitch`, `volume` — todos proxies para `voice_profile`. Um comentário no próprio código indica que **serão removidos na Sprint 9** (a mesma sprint planejada para a camada de IA local — ver [local-ai.md](local-ai.md)).
- `script_file`, `output_directory`/`output_filename`
- `pause_short`/`pause_long`/`split_sentences`
- `project_name`/`project_version`
- `words_per_minute = 145` — hardcoded no código, apesar de parecer configurável via JSON; não é de fato lido do arquivo.

## `.env`

Carregado via `python-dotenv` em `main.py`:

- `PROJECT_NAME`, `PROJECT_ENV`, `INPUT_FILE`, `OUTPUT_DIR`, `OUTPUT_AUDIO_FILE`, `LOG_LEVEL`, `TTS_PROVIDER`
- Seção **"FUTURE LOCAL AI"**: `AI_PROVIDER`, `AI_MODEL`, `AI_ENABLED` — presentes no arquivo mas **não lidos por nenhum código hoje**. Apenas `PROJECT_ENV` é de fato utilizado (em `main.py`).

## Ver também

- [local-ai.md](local-ai.md) — o significado da seção "FUTURE LOCAL AI" no `.env`
- [providers.md](providers.md) — como `tts.provider` se conecta à fábrica de provedores
- [models.md](models.md) — `VoiceProfile`, o modelo que espelha `voices.json`
