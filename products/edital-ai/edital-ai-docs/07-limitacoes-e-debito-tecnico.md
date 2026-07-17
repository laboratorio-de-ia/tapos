# 07 — Limitações conhecidas e débito técnico

Este arquivo documenta o que já se sabe ser frágil ou incompleto no estado
atual — informação essencial para não repetir os mesmos problemas na versão
comercial.

## 1. Um único "edital em foco" por vez em todo o sistema (a limitação mais crítica)

`input/` é tratado como se só pudesse existir **um** documento por vez — o
upload apaga qualquer arquivo anterior antes de salvar o novo
(`for antigo in EDITAL_AI_INPUT_DIR.iterdir(): antigo.unlink()`), e
`find_current_edital_file()` simplesmente pega o único arquivo presente.

Consequência: **dois usuários (ou até o mesmo usuário em duas abas) não
podem processar editais diferentes ao mesmo tempo** sem risco de um upload
sobrescrever o arquivo do outro antes do processamento terminar. Isso é
aceitável para um piloto de usuário único, mas é **bloqueador para
multi-tenant real**. A versão comercial precisa de um diretório de
input/output isolado por usuário/sessão/job (ex.:
`input/{user_id}/{job_id}/arquivo.pdf`), não um único slot global.

## 2. Paths de arquivo em disco local, não em object storage

`arquivos_gerados` (tanto no JSON de resposta quanto na coluna
`EditalAnalise.arquivos_gerados` no banco) guarda **paths absolutos do
filesystem local** do servidor (`/workspace/tecle/products/edital-ai/output/
...`). Isso só funciona enquanto:
- Houver uma única instância do backend rodando na mesma máquina.
- Ninguém limpar `output/`/`processados/` manualmente (não há garantia de
  retenção — um artefato pode desaparecer do disco mesmo com o registro
  ainda existindo no banco, e o endpoint de download simplesmente devolve
  404 nesse caso).

Para produção/comercial: os artefatos precisam ir para object storage (ex.:
S3/MinIO) com URL assinada, não path local.

## 3. `EditalRunResult` não expõe a lista completa de itens/requisitos/prazos

O JSON de resposta da API só traz **contagens**
(`objetos_identificados: int`, não a lista de `Objeto`). Quem quiser os
dados estruturados completos hoje só consegue via o Excel gerado. Uma versão
comercial provavelmente precisa de um endpoint que devolva os dados
estruturados diretamente (não só os artefatos formatados), para permitir
integrações (ex.: importar itens direto num ERP).

## 4. Servidor sem `--reload` já serviu código desatualizado em produção (incidente real)

Aconteceu neste projeto: o processo `uvicorn` do `saas-backend` estava
rodando havia horas, sem `--reload`. Uma correção de código (preservação do
nome do arquivo original) foi aplicada em disco, mas o processo em memória
continuou servindo a versão antiga — o upload de um edital gerava artefatos
com nomes genéricos (`documento.xlsx`) mesmo depois da correção estar
"pronta". Só foi resolvido reiniciando o processo. **Ação tomada**: o
servidor de desenvolvimento agora sobe com `--reload`. Para produção real,
isso não é suficiente — é preciso um pipeline de deploy que garanta reinício
do processo a cada release (não depender de reload por watch de arquivos).

## 5. Extração de itens em tabela: heurística de cabeçalho + continuação entre páginas (corrigido, mas ainda heurístico)

Histórico do bug: em um edital real (`Edital_CasaGrande_Materiais
Limpeza_16072026.PDF`), a aba "Objetos e Itens" saiu **completamente
vazia** (`objetos_identificados: 0`) por dois motivos combinados:

1. O cabeçalho da tabela de itens usava `Ordem`/`Especificação` em vez de
   `Item`/`Lote`/`Descrição` — não reconhecido pela lista de nomes de coluna
   aceitos.
2. A tabela de itens atravessava várias páginas do PDF. O `pdfplumber`
   devolve isso como **blocos de tabela separados**, e só o primeiro bloco
   repete o cabeçalho — os blocos seguintes chegavam "crus" (primeira linha
   já é dado, não cabeçalho) e eram descartados inteiramente por "não ter
   cabeçalho reconhecível", perdendo a esmagadora maioria dos itens mesmo
   quando o cabeçalho do primeiro bloco era reconhecido.

Correção aplicada em `extract_objetos_de_tabelas`
(`pipeline/edital_parser.py`): (a) ampliou os nomes de coluna aceitos
(`ORDEM`, `Nº`, `N°`, `SEQ`, `SEQUÊNCIA`, `ESPECIFICA`); (b) quando um bloco
de tabela não tem cabeçalho válido mas tem o **mesmo número de colunas** do
último cabeçalho válido visto, é tratado como continuação da mesma tabela
(reaproveita o mapeamento de colunas); (c) uma linha sem número reconhecível
na coluna item/lote/ordem é tratada como continuação da descrição do
**item anterior** (concatenada em `especificacoes`), não como um item novo
fantasma sem quantidade/valor.

Validado com dois editais reais: o que já funcionava (`LOTE`/`ITEM`/
`DESCRIÇÃO`, 9 itens) continuou idêntico; o que estava quebrado
(`Ordem`/`Especificação` + tabela multi-página) passou de 0 para 62 itens
corretamente extraídos, com continuações de página mescladas ao item certo.

**Isso continua sendo uma heurística, não um parser garantido.** Qualquer
formato de tabela de item ainda não visto (nomes de coluna muito diferentes,
tabelas sem nenhuma coluna numeradora, PDFs com tabelas mal detectadas pelo
pdfplumber) pode voltar a produzir uma extração vazia ou incompleta **sem
lançar erro** — o pipeline simplesmente devolve `objetos: []`, o que é
silenciosamente "sucesso" do ponto de vista do sistema, mas um resultado
inútil para o usuário. Para a versão comercial, isso é o risco de qualidade
mais importante a mitigar (ver recomendações em
`08-briefing-para-comercializacao.md`: telemetria de "análise suspeita" e/ou
extração assistida por IA como camada adicional de segurança, não só regex).

## 6. Dependência forte de um formato de edital "brasileiro padrão"

Todas as regex (número, órgão, modalidade, objeto, prazos, habilitação) são
desenhadas em cima de convenções comuns em editais brasileiros de compras
públicas (fórmula "torna público", seção "DA HABILITAÇÃO", modalidades
específicas da Lei de Licitações). Editais fora desse padrão (outros
países, formatos muito não-convencionais, ou digitalizações de baixa
qualidade que dependem 100% do fallback OCR) tendem a resultar em campos
`None`/listas vazias sem nenhum aviso qualitativo sobre a confiança da
extração.

## 7. Score de conformidade mede completude da extração, não risco real

`score_conformidade` (tanto o vindo da IA quanto o fallback determinístico)
mede o quão completos estão os campos extraídos (número, órgão, modalidade,
objeto, prazos) — **não** é uma nota de adequação do edital, nem uma
avaliação de risco jurídico real. O texto do prompt (`prompts/
generate_summary.txt`) já deixa isso explícito, mas é fácil um usuário
comercial interpretar "score de conformidade: 100%" como "edital sem
problemas", o que não é o que a métrica mede.

## 8. Sem validação de tamanho/timeout de fato aplicada

`settings.json` define `max_tamanho_mb` e `timeout_segundos`, mas nenhum
lugar do código de fato os aplica (não há checagem de tamanho de upload
antes de processar, nem enforcement desse timeout específico no subprocesso
ou na chamada ao Ollama além do timeout do próprio `requests.post`). Um
upload muito grande ou uma análise muito lenta hoje só é limitada pelo
timeout do `requests` ao Ollama (`ollama.timeout`, default 300s no
`settings.json`) e pelo timeout implícito do subprocess (nenhum, na prática
— `subprocess.run` sem `timeout=` fica bloqueado indefinidamente se o
subprocesso travar).

## 9. Campos de modelo nunca preenchidos (vestígios de escopo maior)

- `Edital.secoes` (lista de `Secao`) — nunca populado.
- `Objeto.modalidade_entrega` e `Objeto.fabricante_sugerido` — nunca
  populados.
- `Requisito.prazo_validade` e `Requisito.observacoes` — nunca populados.
- `Prazo.hora` — nunca populado (a hora do evento, quando existe no texto,
  não é separada da data).

Esses campos existem no modelo (aparentemente projetados para uma extração
mais rica) mas o parser atual não os preenche. Antes de comercializar,
decidir explicitamente: implementar a extração desses campos, ou removê-los
do modelo para não sugerir uma capacidade que não existe.

## 10. `jinja2` e `python-pptx` no requirements sem uso

Dependências declaradas mas não referenciadas em nenhum módulo atual —
provavelmente vestígios de uma versão anterior do escopo (templates HTML/PPT
que não chegaram a ser implementados). Limpeza de dependências recomendada
antes de embalar a versão comercial (reduz superfície de CVEs e tempo de
build).
