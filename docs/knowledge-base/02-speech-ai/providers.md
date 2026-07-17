# Speech-AI — Provedores

## A abstração

O Speech-AI foi construído para ser independente de fornecedor de síntese de voz, através de uma camada de abstração de provedores:

- `providers/base_provider.py::BaseTTSProvider` (classe abstrata) — construtor recebe `voice, rate, pitch, volume`; método abstrato único: `generate(text, output_path) -> Path`.
- `providers/edge_provider.py::EdgeProvider(BaseTTSProvider)` — única implementação real hoje. Usa `edge_tts.Communicate(...).save()` (assíncrono, encapsulado via `asyncio.run`). Expõe um `ProviderInfo` (`providers/provider_info.py`, dataclass congelada) com flags de capacidade: `supports_ssml=False`, `supports_streaming=False`, `supports_neural=True`, idiomas suportados (pt-BR, en-US, es-ES, fr-FR, de-DE, it-IT, ja-JP), formatos (mp3), `max_characters=100000`.
- `providers/provider_registry.py::ProviderRegistry` — dicionário `{provider_id: ProviderClass}` no nível de classe, com `register/get/exists/list/clear`.
- `providers/provider_loader.py::ProviderLoader.load()` — **auto-descoberta**: varre `providers/*_provider.py` (ignorando `base_provider.py`), importa cada módulo, localiza qualquer subclasse de `BaseTTSProvider` e registra-a com um `provider_id` derivado do nome da classe (remove "Provider", minúsculas — ex.: `EdgeProvider` → `"edge"`). Disparado uma vez, na importação, via `providers/__init__.py`.
- `providers/provider_factory.py::ProviderFactory` — três construtores estáticos (`create`, `create_from_profile`, `create_from_speech_profile` — este último é o usado em produção), todos resolvendo via `ProviderRegistry.get(provider_id)` e instanciando com `voice/rate/pitch/volume`.

## Como adicionar um novo provedor

Basta criar um arquivo `providers/azure_provider.py` definindo `class AzureProvider(BaseTTSProvider)` com `generate()` implementado — ele é **automaticamente registrado** como `"azure"`, sem nenhuma outra mudança de código. Depois, basta configurar `"tts": {"provider": "azure", ...}` em `config/settings.json` e adicionar entradas correspondentes com `"provider": "azure"` em `config/voices.json`. Este desenho plugável está confirmado tanto no código quanto na documentação interna do produto (`docs/SpeechAI_Docs/Sprint/ADR.md`, ADR-003; `docs/SpeechAI_Docs/Foundation/ARCHITECTURE.md`).

## Roadmap de provedores

A documentação interna do produto (`ROADMAP.md`, síntese técnica) nomeia consistentemente **Azure Cognitive Services** e **OpenAI TTS** como próximos provedores (meta interna "Q3 2026"), seguidos por AWS Polly e ElevenLabs mais adiante. Nenhum destes está implementado ainda — apenas o Edge TTS está em produção hoje.

## Ver também

- [architecture.md](architecture.md)
- [local-ai.md](local-ai.md) — provedores de voz não devem ser confundidos com a camada de IA local planejada para análise de conteúdo
- [roadmap.md](roadmap.md)
