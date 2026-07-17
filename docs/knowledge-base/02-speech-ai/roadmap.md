# Speech-AI — Roadmap

## Maturidade atual

O pipeline central — análise de texto → Speech Intelligence → construção de narração/fala → síntese via Edge TTS — é real, funcional, e evidenciado por logs e artefatos de execução (ver [outputs.md](outputs.md)). A integração com a TAPOS (rotas síncronas e assíncronas, adapter, publisher RabbitMQ, worker dedicado) também é real e está operacional — confirmado diretamente em `platform/saas-backend` e `platform/tap-runtime/workers/speech-ai-worker`.

## O que está pronto, mas não conectado à produção

- **Pipeline experimental de SSML** (`services/text_engines/`: Lexical → Clause → SentenceEngine → SpeechBlockBuilder → PausePlanner → SSMLEngine) — código completo, produz SSML real, mas só é exercitado por um script manual (`input/teste.py`), fora do caminho de produção.
- **`SpeechOptimizer._apply_future_ai_rules()`** — hook no-op já presente no código, reservado para regras de IA (Azure OpenAI, GPT, Claude, Gemini, Ollama, Emotion Engine, Storytelling Engine).
- **Camada de IA local/SLM** (Ollama + Phi-3 mini/Mistral 7B para emoção/intenção) — planejamento detalhado em documentos internos ("Sprint 9"), zero código implementado (`slm_gateway.py`, `emotion_engine.py` não existem). Ver [local-ai.md](local-ai.md).
- Apenas **um provedor de TTS** implementado (Edge); Azure, OpenAI TTS, AWS Polly e ElevenLabs são citados em múltiplos documentos como próximos passos, mas ausentes no código.
- `Paragraph.importance` — campo existente no modelo, não utilizado por nenhuma lógica do pipeline (provável reserva para ênfase futura em SSML).
- `services/text_optimizer.py::TextOptimizer` e `SpeechOptimizer.optimize_text()` não parecem ser chamados pelo pipeline de produção atual — possível código morto a confirmar.

## Limpeza técnica pendente

- `products/speech-ai/app/integration/` é um duplicado obsoleto de `products/speech-ai/integration/` (o único conectado à TAPOS) — candidato a remoção.
- **Nenhuma suíte de testes automatizados existe** no produto (zero arquivos `test_*.py`/`conftest.py`), apesar de a documentação interna (`docs/SpeechAI_Docs/Developer/TESTING_GUIDE.md`) e materiais de síntese técnica citarem métricas como "99,2% de taxa de sucesso" e "87% de cobertura de testes" — esses números devem ser tratados como **conteúdo aspiracional/gerado**, não fato verificado (o próprio documento de origem se identifica como gerado por IA externa).

## Documentação interna desatualizada em relação ao código

Vale registrar com transparência, para futuras revisões desta knowledge base:

- `docs/SpeechAI_Docs/Sprint/ROADMAP.md` lista API REST e processamento em lote via fila de mensagens como trabalho futuro ("Q1/Q2 2027") — mas ambos **já existem** no código atual (rotas FastAPI da TAPOS + worker RabbitMQ).
- A numeração de "Sprint" é inconsistente entre documentos internos: um changelog do produto chama o trabalho de Provider Factory de "Sprint 9", enquanto `SpeechAI Platform.docx` reserva "Sprint 9" especificamente para a (ainda não iniciada) Plataforma de IA Local.
- `README.md` do produto descreve a execução assíncrona (Task 015) como "próxima evolução" — já implementada.

## Próximos passos recomendados

1. Conectar o pipeline de SSML (`text_engines/`) ao fluxo de produção, substituindo os marcadores de pausa em texto plano por SSML real.
2. Implementar a camada de IA local planejada (Ollama + SLM) para emoção/intenção, seguindo o plano de "Sprint 9" já documentado.
3. Adicionar um segundo provedor de TTS (Azure ou OpenAI) para validar de fato a abstração de provedores em produção.
4. Criar uma suíte de testes automatizados mínima antes de reivindicar qualquer métrica de cobertura.
5. Remover o diretório `app/integration/` duplicado.
6. Atualizar a documentação interna do produto para refletir o que já está implementado (rotas assíncronas, integração TAPOS).

## Ver também

- [local-ai.md](local-ai.md) — detalhamento do plano de IA local
- [providers.md](providers.md) — roadmap específico de provedores de TTS
- [../01-tapos/roadmap.md](../01-tapos/roadmap.md) — lacunas no nível da plataforma
