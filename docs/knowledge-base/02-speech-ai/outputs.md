# Speech-AI — Saídas

Artefatos reais confirmados em `products/speech-ai/output/`:

| Arquivo | Conteúdo |
|---|---|
| `narration.txt` | Texto de narração natural gerado pelo `NarrationBuilder` |
| `speech.txt` | Texto limpo pronto para TTS, gerado pelo `SpeechBuilder` |
| `speech.xml` | **Apesar da extensão `.xml`, o conteúdo é texto plano de narração com marcadores literais de pausa "..."** — não é XML/SSML real. Resquício de uma versão anterior do pipeline, anterior ao nome atual `speech.txt` em `settings.json`. |
| `speech_report.json` | Estatísticas da execução, ex.: `{"characters": 6851, "words": 974, "sentences": 90, "paragraphs": 95, "estimated_minutes": 6.72}` — corresponde ao formato de `Statistics.to_dict()` |
| `script_optimized.txt` | Saída de uma passada de otimização sobre o script de demonstração (inglês, cenário de governança de IA) |
| `audio.mp3` | Arquivo de áudio real gerado (~4 MB na última execução registrada) |

Uma execução real recente processou um livro inteiro (biografia, +29 mil linhas) como entrada — prova de que o pipeline escala além de slides/scripts curtos para textos longos, sem limite de chunking aparente.

## Subpastas reservadas, ainda vazias

`output/audio/`, `output/reports/`, `output/scripts/`, `output/ssml/` existem como estrutura, mas estão vazias hoje — scaffolding para uma organização de saída mais estruturada no futuro (por exemplo, arquivos de SSML real quando o pipeline `services/text_engines/ssml_engine.py` for conectado à produção).

## Evidência de execução completa

`logs/app.log` (301 KB) registra uma execução real de ponta a ponta: Text Analyzer → Speech Intelligence → Narration/Speech builders → síntese via Edge TTS → "Audio generated successfully".

## Ver também

- [pipeline.md](pipeline.md) — como cada saída é produzida
- [roadmap.md](roadmap.md) — o plano (ainda não implementado) de SSML real
