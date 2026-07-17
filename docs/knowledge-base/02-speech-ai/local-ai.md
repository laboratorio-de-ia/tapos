# Speech-AI — IA Local

## Estado atual: nenhum modelo de IA em execução

Ao contrário do Edital-AI, o Speech-AI **não executa hoje nenhum modelo de IA local ou em nuvem** (nenhum LLM, SLM ou embedding). Tudo o que poderia ser confundido com "IA" no produto é, na realidade, determinístico:

- `services/language_detector.py` usa a biblioteca `langdetect` — um classificador estatístico simples (n-gramas), não um modelo neural, com seed fixa (`DetectorFactory.seed = 0`) para determinismo.
- Toda a "inteligência" de conteúdo (pontuação de complexidade, ritmo de leitura, seleção de tom/velocidade, planejamento de pausas) é baseada em regras e regex determinísticas: `speech_analyzer.py`, `timing_calculator.py`, `speech_optimizer.py`, e todo o pacote `services/text_engines/`. Não há inferência de machine learning em nenhum ponto do pipeline de produção.

## Um plano concreto e documentado para IA local

Existe, porém, um plano detalhado e específico para IA local no Speech-AI, descrito em `docs/Sprint 9 (Integracao com IA).docx` e `docs/SpeechAI Platform.docx` — uma visão de "Sprint 9 – Local AI Intelligence Platform" que rejeita explicitamente LLMs em nuvem ("Você NÃO deve usar LLM cloud") em favor de uma estratégia **local-first com modelos pequenos (SLM)**:

- **Runtime**: Ollama (ou llama.cpp), rodando localmente — consistente com a filosofia de IA local já usada pelo Edital-AI.
- **Modelos propostos**: Phi-3 mini (classificação de emoção/intenção, leve e rápido), Mistral 7B (fallback de NLP), LLaMA 3 8B (raciocínio mais pesado, opcional/futuro), Mixtral (alternativa mencionada).
- **Arquitetura em 3 camadas proposta**:
  1. Camada 1 = motor de regras determinístico já existente (já construído, é o pipeline atual).
  2. Camada 2 = SLM local (emoção/intenção/sumarização leve).
  3. Camada 3 = modelo local mais pesado, opcional.
- **Módulos futuros nomeados, ainda inexistentes no código**: `slm_gateway.py`, `emotion_engine.py`, um "Intent Engine", "Semantic Analyzer" e "Speech Advisor". Confirmado por busca no repositório: nenhum arquivo relacionado a `slm`/`emotion`/`intent` existe hoje — esta é uma etapa apenas de planejamento.
- Existe um plano de sprint nomeado (9.1 Infraestrutura de IA Local → 9.7 Pipeline de Fine-tuning) em `SpeechAI Platform.docx`.

## Pontos de extensão já reservados no código

Dois sinais concretos de que essa camada foi antecipada no design, mesmo sem implementação:

- `services/speech_optimizer.py::SpeechOptimizer._apply_future_ai_rules()` — um hook no-op real, já presente no código, com docstring listando "Azure OpenAI, OpenAI GPT, Claude, Gemini, Ollama, Emotion Engine, Storytelling Engine".
- `.env` do produto tem uma seção "FUTURE LOCAL AI" com chaves `AI_PROVIDER`, `AI_MODEL`, `AI_ENABLED` — presentes mas **não lidas por nenhum código** hoje (nenhum `os.getenv` referencia esses nomes).

## Conclusão

IA local é parte deliberada e de primeira classe do roadmap do próprio Speech-AI — não é "assunto do Edital-AI" por engano. Simplesmente ainda não foi implementada: tudo o que está em produção hoje é NLP determinístico.

## Ver também

- [roadmap.md](roadmap.md) — onde esta camada se encaixa nos próximos passos
- [../03-products/edital-ai.md](../03-products/edital-ai.md) — o produto onde IA local (Ollama) já está em produção
- [../00-tecle/vision.md](../00-tecle/vision.md) — a filosofia de "IA local sempre que possível" que motiva este plano
