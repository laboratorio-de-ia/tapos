# 08 — Briefing para gerar a versão comercial

Este arquivo é o brief direto para o LLM que for projetar/gerar a versão
comercial: resume, em um só lugar, o que já existe (e funciona) vs. o que
precisa ser decidido e construído. Leia junto com `07-limitacoes-e-debito-
tecnico.md` para o detalhe técnico de cada ponto.

## O que já é sólido e pode ser reaproveitado como está

- **A lógica de extração determinística** (regex + leitura de tabelas
  nativas do PDF) para número/órgão/modalidade/objeto/prazos/itens/
  requisitos — validada em editais reais, com heurística de continuação de
  tabela entre páginas já corrigida.
- **O desacoplamento entre extração estrutural (determinística) e análise
  qualitativa (IA)** — a IA nunca é o caminho crítico para os dados
  estruturados, só para resumo/riscos/score. Isso é um bom princípio de
  arquitetura para manter: torna o produto resiliente a indisponibilidade ou
  troca de provedor de IA.
- **O contrato de saída simples** (`EditalRunResult` → JSON) entre o produto
  e qualquer integrador — fácil de reimplementar em outra linguagem/serviço
  se necessário, já que a fronteira é um subprocesso + JSON no stdout.
- **A geração dos 4 formatos de artefato** (Excel com 5 abas, PDF, Word,
  rascunho de e-mail) — cobre bem o caso de uso "documento pronto para
  compartilhar internamente".

## Lacunas a resolver para virar produto comercial multi-tenant

### 1. Isolamento por usuário/tenant (bloqueador nº 1)
Hoje existe **um único slot de edital "em foco"** em todo o sistema
(`input/`, `output/`). Para multi-tenant é obrigatório:
- Diretório de trabalho isolado por usuário e por job
  (`input/{tenant_id}/{job_id}/...`), não um único diretório global.
- Object storage (S3/MinIO) para os artefatos gerados, com URLs
  assinadas/temporárias por download — não paths locais de disco.

### 2. Escala do processamento
O fluxo síncrono (`/upload`, `/run`) bloqueia 1-2 minutos por request (tempo
do Ollama em CPU) — inviável com mais de um usuário simultâneo. O fluxo
assíncrono (fila + worker) já existe como base, mas hoje roda com
`prefetch_count=1` (um job por vez, sem paralelismo). Decisões a tomar:
- Quantos workers em paralelo, e como escalar horizontalmente.
- Se a IA continua sendo local (Ollama/CPU) ou se passa a usar um provedor
  gerenciado (Anthropic/OpenAI/Google) para tempo de resposta previsível —
  troca de "custo zero e privado" por "rápido e escalável", uma decisão de
  produto explícita, não só técnica.
- Se falta hardware de GPU, isso deve ser um item explícito de
  infraestrutura, não assumido como resolvido.

### 3. Confiabilidade da extração precisa de sinalização de qualidade
Hoje, quando a extração de itens/requisitos falha silenciosamente (formato
de tabela não reconhecido), o sistema devolve "sucesso" com listas vazias —
sem qualquer sinal para o usuário de que o resultado é suspeito. Para
comercial, recomenda-se:
- Um indicador explícito de confiança da extração no resultado (ex.: "X% dos
  campos esperados foram encontrados"), não só o `score_conformidade`
  (que mede completude, não risco jurídico — ver limitação 7).
- Fallback assistido por IA para extração de itens quando a extração
  determinística por tabela vier vazia (hoje só há fallback por regex em
  prosa, que é ainda mais frágil que a leitura de tabela).
- Telemetria/alerta interno quando `objetos_identificados == 0` ou
  `requisitos_identificados == 0` para um documento que claramente tem
  tabelas (sinal de regressão silenciosa, como já aconteceu uma vez).

### 4. API mais rica para integração
`EditalRunResult` só devolve contagens de itens/requisitos, não as listas
completas — quem quiser os dados estruturados precisa abrir o Excel. Um
produto comercial vendido via API (não só via upload manual numa UI)
precisa de um endpoint que devolva os dados estruturados diretamente (JSON),
para permitir integração com ERPs/CRMs dos clientes.

### 5. Deploy e operação
- O incidente de servidor servindo código desatualizado (sem `--reload`, sem
  processo de deploy) mostra que é necessário um pipeline de deploy real
  (build + restart do serviço a cada release), não depender de reload por
  watch de arquivo (que é só para desenvolvimento).
- Os dois `.venv` separados (produto vs. backend) precisam de uma estratégia
  de empacotamento clara para produção (containers Docker independentes é o
  caminho mais natural, dado que o produto já roda como subprocesso isolado).
- Falta observabilidade: não há métricas de tempo de processamento, taxa de
  falha do Ollama, taxa de fallback determinístico, etc. — importante para
  saber se o produto está de fato entregando valor de forma consistente.

### 6. Modelo de precificação/negócio (decisão de produto, não técnica)
A infraestrutura de assinatura já existe (`Subscription` por produto, ativa/
inativa) — mas hoje é tudo-ou-nada por produto. Para comercializar,
considerar:
- Cobrança por análise/edital processado vs. assinatura mensal fixa vs.
  planos por volume (nº de editais/mês).
- Se o histórico de análises (`edital_analises`) deve ter retenção/expiração
  configurável por plano.
- Se o "score de conformidade" e os artefatos gerados são o produto em si, ou
  se o valor real está em recursos ainda não construídos (monitoramento de
  portais, alertas automáticos de prazo, comparação entre editais — todos
  mencionados na especificação original em `edital.md` da raiz, mas nunca
  implementados).

### 7. Superfície de segurança a revisar antes de expor externamente
- Upload hoje só valida extensão pelo nome do arquivo (`.pdf/.docx/.doc/
  .txt/.md`), não o conteúdo real (magic bytes) — um arquivo malicioso renomeado
  passaria pela validação de extensão.
- Não há limite de tamanho de upload de fato aplicado (ver limitação 8) —
  risco de DoS por upload de arquivo enorme.
- `subprocess.run` sem timeout — um subprocesso travado bloqueia
  indefinidamente o worker/request.
- Dependências desatualizadas/não usadas (`jinja2`, `python-pptx`) aumentam
  superfície de CVE sem necessidade.

## Perguntas em aberto para quem for desenhar a versão comercial

1. O produto comercial continua sendo "upload manual de um arquivo" ou
   precisa de integração direta com portais de compras (leitura automática,
   sem o usuário precisar baixar/subir o PDF manualmente)?
2. IA local (Ollama, grátis, privado, lento) ou IA gerenciada (paga, rápida,
   dados saem da infraestrutura do cliente)? Isso afeta preço, LGPD/
   compliance e SLA de tempo de resposta.
3. O histórico de análises e os artefatos gerados precisam ficar disponíveis
   indefinidamente, ou há uma política de retenção por plano?
4. Multi-usuário dentro da mesma empresa (equipe de compliance vendo o mesmo
   histórico) ou estritamente por usuário individual?
5. Vale a pena expor os dados estruturados (itens, requisitos, prazos) via
   API para integração com sistemas do cliente, além dos 4 artefatos
   prontos?

Essas perguntas não têm resposta técnica certa — são decisões de produto que
devem ser tomadas antes (ou junto) da geração da arquitetura comercial pelo
LLM, para que o resultado não apenas escale tecnicamente, mas também
corresponda ao modelo de negócio pretendido.
