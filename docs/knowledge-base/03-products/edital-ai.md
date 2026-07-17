# Edital-AI

## O que é

O Edital-AI automatiza a leitura e análise de editais de licitação pública brasileira. Um analista humano hoje lê um edital inteiro — frequentemente entre 50 e 300 páginas, em linguagem jurídica repetitiva, com tabelas de itens que se espalham por dezenas de páginas — para decidir se vale a pena participar, o que precisa ser entregue e até quando. O Edital-AI automatiza exatamente essa etapa.

O usuário faz upload de um edital em PDF, DOCX, TXT ou MD. O sistema extrai, de forma **determinística** (leitura de tabelas nativas do documento e reconhecimento de padrões — sem depender de IA para os dados críticos): número do edital, modalidade, órgão licitante, objeto da licitação, cada item e lote com quantidade e valor estimado, os documentos obrigatórios de habilitação, e todos os prazos críticos (sinalizando automaticamente quando resta menos de 7 dias para um prazo importante).

Sobre essa base estruturada, um modelo de IA rodando **localmente via Ollama** (modelo `mistral`) gera um resumo executivo, identifica riscos e oportunidades, e calcula um score de conformidade de 0 a 100. Se a camada de IA falhar ou estiver indisponível, um mecanismo de segurança determinístico garante que o pipeline nunca trava por causa da IA — confiabilidade antes de sofisticação.

O resultado chega em quatro formatos prontos para uso: planilha Excel (5 abas), documento Word, PDF executivo e rascunho de e-mail já destacando os prazos mais urgentes.

## Documentação detalhada

O produto já possui documentação técnica interna madura em `products/edital-ai/edital-ai-docs/`, que serve como fonte primária e não é reproduzida aqui na íntegra:

| Tópico | Arquivo |
|---|---|
| Visão de negócio e casos de uso | `01-visao-geral-e-negocio.md` |
| Arquitetura em camadas, fluxo síncrono/assíncrono | `02-arquitetura.md` |
| Modelos de dados (dataclasses e schemas de banco) | `03-modelos-de-dados.md` |
| Pipeline função a função | `04-pipeline-e-funcoes.md` |
| Integração com o SaaS backend | `05-integracao-saas-backend.md` |
| Configuração e execução local | `06-configuracao-e-execucao.md` |
| Limitações e débito técnico | `07-limitacoes-e-debito-tecnico.md` |
| Briefing para comercialização | `08-briefing-para-comercializacao.md` |
| A chamada de IA em detalhe | `Chamada_IA_Edital.md` |

## Arquitetura e pipeline

```
Upload (PDF/DOCX/TXT/MD)
  ↓
edital_extractor.py    → extração bruta do documento
  ↓
edital_parser.py       → 100% regex/heurística, sem IA: número, modalidade, órgão,
                          objeto, itens/lotes, habilitação, prazos
  ↓
edital_analyzer.py     → única chamada de IA (Ollama, modelo mistral):
                          resumo executivo, riscos, oportunidades, score 0–100
                          (fallback determinístico se a IA falhar)
  ↓
artefato_generator.py  → Excel (a partir do template "Dom de Limpar - Modelo
                          Precificacao.xlsx"), Word, PDF, e-mail
```

## Modelos de dados

Dataclasses internas: `Objeto`, `Requisito`, `Prazo`, `Edital`/`Secao`, `Analise`, `Artefato`, `EditalRunResult`. Do lado da plataforma: `Job`, `EditalAnalise` (tabelas de banco). Detalhamento completo em `03-modelos-de-dados.md`.

## Exemplo real

`output/Edital_CasaGrande_16072026.{pdf,docx,xlsx}` + `_email.txt` — Edital nº 014/2026, Município de Casa Grande - MG, pregão eletrônico, 62 itens, 30 requisitos, score de conformidade 100%. A pasta `processados/` arquiva 11 editais reais já processados (municípios de MGS, São Joaquim de Bicas, Fortuna Minas, Casa Grande, MGM Panos) — confirmando uso repetido com documentos reais, não apenas um teste isolado.

## Integração com a TAPOS

Segue o mesmo padrão facade/runner/schemas/cli dos demais produtos (ver [../05-development/coding-standards.md](../05-development/coding-standards.md)):

- `integration/facade.py::run_edital_ai`
- `integration/runner.py::execute_pipeline` → `EditalRunResult`
- `integration/cli.py` — stdout reservado ao JSON final; exceções vão para stderr + exit code 1
- Adapter na plataforma: `platform/saas-backend/app/products/edital_ai_adapter.py`
- Worker dedicado: `platform/tap-runtime/workers/edital-ai-worker/worker.py`

## Maturidade e limitações

Piloto validado em modo **single-tenant**: `input/`/`output/` tratam apenas um edital "em foco" por vez em toda a instalação — este é o principal bloqueador para operação multi-cliente. Outros pontos de débito técnico conhecido (detalhados em `07-limitacoes-e-debito-tecnico.md`):

- caminhos em disco local, não armazenamento de objetos;
- `EditalRunResult` retorna apenas contagens, não a lista completa de itens/requisitos/prazos;
- a heurística de extração de tabelas já precisou de correção uma vez (um edital real produziu 0 itens por nomes de coluna não reconhecidos e tabela dividida em múltiplas páginas — corrigido, mas ainda heurístico, não garantido);
- `score_conformidade` mede completude de extração, não risco jurídico;
- sem limite de tamanho de arquivo ou timeout aplicado apesar de existirem campos para isso em `settings.json`;
- dependências não utilizadas (`jinja2`, `python-pptx`);
- vários campos de modelo nunca populados (`Edital.secoes`, `Objeto.modalidade_entrega`/`fabricante_sugerido`, `Requisito.prazo_validade`/`observacoes`, `Prazo.hora`).

## Roadmap

Isolamento de dados por cliente, armazenamento de objetos com URLs assinadas, indicador de confiança por extração, extração assistida por IA como fallback, API mais rica expondo os dados estruturados completos, pipeline de deploy real, e decisão entre IA local ou provedor gerenciado — todos detalhados em `08-briefing-para-comercializacao.md`.

## Ver também

- [code-ai.md](code-ai.md) — pode se tornar camada de conversão de entrada reaproveitável pelo próprio Edital-AI no futuro
- [../01-tapos/roadmap.md](../01-tapos/roadmap.md) — lacunas de multi-tenancy no nível da plataforma
