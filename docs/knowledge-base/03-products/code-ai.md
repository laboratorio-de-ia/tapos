# Code-AI

## O que é

O Code-AI é um conversor universal de documentos corporativos para Markdown, pensado para consumo por LLMs e pipelines de RAG. Toda empresa que tenta adotar IA de forma séria esbarra no mesmo problema: seus dados mais importantes não estão em texto limpo — estão em PDFs, planilhas, apresentações, documentos Word e imagens escaneadas, formatos que modelos de linguagem não conseguem consumir de forma eficiente.

O Code-AI recebe documentos em PDF, DOCX/DOC, XLSX/XLS/CSV, PPTX/PPT, PNG/JPG/JPEG, TXT e MD, e produz uma versão padronizada, limpa e em Markdown. Para documentos digitalizados ou imagens, usa OCR para extrair o texto mesmo quando ele não existe em formato digital nativo.

O ganho não é apenas de compatibilidade — é de custo: cada consulta a um LLM é cobrada por token, e documentos corporativos brutos desperdiçam uma quantidade grande de tokens em ruído estrutural. A documentação do produto estima economia de 70–85% de tokens dependendo do formato de origem.

> **Nota de precisão**: a única execução real capturada em `output/relatorio.json` mostra uma economia de 50,03% (348,08 KB → 173,94 KB) — abaixo da faixa de 70–85% citada na documentação de marketing do produto (`docs/`). Vale tratar 70–85% como estimativa por tipo de formato, não como resultado medido em todos os casos, até que mais execuções reais sejam registradas.

## Arquitetura

Padrão *Strategy*: `src/conversor_markdown.py::ConvertorUniversal` despacha por extensão para uma classe conversora dedicada:

| Formato | Conversor | Mecanismo |
|---|---|---|
| PDF | `ConversorPDF` | `pdfplumber`, com fallback para OCR via `pytesseract` + `pdf2image` |
| DOCX/DOC | `ConversorDocx` | `python-docx` |
| XLSX/XLS/CSV | `ConversorExcel` | `pandas`, lendo todas as abas |
| PPTX/PPT | `ConversorPowerPoint` | `python-pptx` |
| PNG/JPG/JPEG | `ConversorImagem` | OCR |
| TXT/MD | `ConversorTexto`/`ConversorMarkdown` | passthrough |

`ConfiguradorDependencias` instala automaticamente dependências ausentes via `pip install --break-system-packages` no momento da importação — uma conveniência de desenvolvimento que **não é recomendada para produção** (ver Limitações).

Pontos de entrada: `main.py` (converte todo o diretório `input/`), `scripts/rapido.py` (CLI mínima), `scripts/workflow.py` (5 workflows nomeados, incluindo "otimizar" e "preparar para IA"), `scripts/instalar.py` (validador/instalador de ambiente), `scripts/exemplos_uso.py` (exemplos de uso). O produto em si não tem lógica de fila assíncrona própria — a execução assíncrona é inteiramente responsabilidade da camada TAPOS.

## Modelos de dados

Não há dataclasses internas ao produto: `ConvertorUniversal.relatorio` é um dicionário com `data`, `arquivos_processados` (lista de `{arquivo_original, arquivo_convertido, tamanho_original_kb, tamanho_convertido_kb, economia_percentual}`) e `erros`. A camada de integração formaliza isso em `integration/schemas.py`: `ConvertedFile` (input_file, output_file, size_input_kb, size_output_kb, savings_percent) e `CodeAIRunResult` (status, files_processed, converted, errors, report_file).

## Exemplo real

`input/documento.pdf` é um edital real (MGS — Minas Gerais Administração e Serviços S.A., Pregão Eletrônico Registro de Preços nº 029/2026, materiais de limpeza), convertido em `output/documento.md` (2403 linhas, Markdown página a página, tabelas renderizadas via `df.to_markdown()`), com o relatório de economia em `output/relatorio.json`.

## Integração com a TAPOS

Mesmo padrão facade/runner/schemas/cli dos demais produtos, confirmado byte a byte idêntico ao do Edital-AI:

- `integration/facade.py::run_code_ai(input_file)` → `integration/runner.py::execute_current_pipeline` → `CodeAIRunResult.to_dict()`
- `integration/cli.py` redireciona os prints internos para um buffer e imprime só o JSON final em stdout; exceções vão para stderr + `sys.exit(1)`
- Adapter na plataforma: `platform/saas-backend/app/products/code_ai_adapter.py::run_code_ai_product()`, executando `<code-ai>/.venv/bin/python integration/cli.py <arquivo>` via subprocess
- Worker dedicado: `platform/tap-runtime/workers/code-ai-worker/worker.py`

## Maturidade e limitações

Bem menos documentado que o Edital-AI — não existe ainda um equivalente ao débito técnico ou briefing de comercialização daquele produto. Pontos a observar:

- instalação automática de dependências via `pip` na importação é um risco operacional real em produção;
- sem streaming/progresso assíncrono, sem limite de tamanho de arquivo evidente;
- tratamento de erro por conversor apenas captura exceções e retorna uma string Markdown de erro ("# Erro ao converter X"), em vez de falhar de forma explícita.

## Roadmap

Itens mencionados como aspiracionais em `docs/arquitetura_visual.md` ("Evolução Futura") e `docs/analise_projeto.md` ("Próximas Evoluções"), ainda não implementados: API REST própria, interface web, processamento assíncrono nativo do produto, cache, auto-vetorização, conectores SharePoint/OneDrive, pipeline de RAG.

## Ver também

- [edital-ai.md](edital-ai.md) — potencial consumidor futuro do Code-AI como camada de conversão de entrada
- [../01-tapos/technologies.md](../01-tapos/technologies.md) — stack compartilhado da plataforma
