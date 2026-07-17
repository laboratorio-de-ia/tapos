# Documentação edital-ai — para geração da versão comercial

Este diretório documenta o **estado real e atual** do produto `edital-ai`
dentro da plataforma TAPOS (`products/edital-ai/` + integração em
`platform/saas-backend/`), com o nível de detalhe (arquitetura, modelos de
dados, funções, heurísticas, endpoints) necessário para que um LLM (ex.:
Google Gemini) consiga:

1. Entender o que o produto faz e como é usado hoje (uso interno/piloto).
2. Entender exatamente como cada parte do pipeline funciona por dentro.
3. Propor e gerar a versão comercial (multi-tenant, escalável, robusta a
   qualquer formato real de edital) a partir de uma base de verdade — não de
   suposições.

> **Nota sobre `edital.md` (raiz do projeto):** existe um arquivo com o mesmo
> propósito na raiz do workspace, mas ele é a **especificação original**
> escrita antes da implementação — parte do que descreve nunca foi construído
> como tal (ex.: `relatorio.py`, `database_service.py`, endpoint `/analyze`,
> múltiplos prompts de IA por seção) e parte diverge do código real. Os
> arquivos deste diretório descrevem o código **como ele existe hoje**,
> arquivo por arquivo, função por função. Em caso de conflito entre os dois,
> este diretório é a fonte confiável.

## Como ler esta documentação

| Arquivo | Conteúdo |
|---|---|
| [`01-visao-geral-e-negocio.md`](01-visao-geral-e-negocio.md) | O que é o produto, para quem, que problema resolve, casos de uso reais |
| [`02-arquitetura.md`](02-arquitetura.md) | Camadas do sistema, diagrama de execução, estrutura de diretórios real |
| [`03-modelos-de-dados.md`](03-modelos-de-dados.md) | Todas as dataclasses/entidades, campo a campo, com significado de negócio |
| [`04-pipeline-e-funcoes.md`](04-pipeline-e-funcoes.md) | Cada módulo do pipeline (extração, parsing, análise por IA, geração de artefatos), função a função, com as regras/heurísticas e regex usadas |
| [`05-integracao-saas-backend.md`](05-integracao-saas-backend.md) | Endpoints HTTP, autenticação/assinatura, fluxo síncrono vs. assíncrono (fila), schema de banco |
| [`06-configuracao-e-execucao.md`](06-configuracao-e-execucao.md) | Como rodar local, variáveis de ambiente, dependências, `settings.json` |
| [`07-limitacoes-e-debito-tecnico.md`](07-limitacoes-e-debito-tecnico.md) | O que é frágil, o que já quebrou em produção e foi corrigido, o que falta para produção real |
| [`08-briefing-para-comercializacao.md`](08-briefing-para-comercializacao.md) | Brief direto para o LLM: lacunas entre o piloto atual e um produto comercial, e o que precisa ser decidido/construído |
| [`Chamada_IA_Edital.md`](Chamada_IA_Edital.md) | A única chamada de IA do pipeline em detalhe: onde acontece, por que existe, como é feita (prompt, contexto, endpoint), o fallback determinístico e onde o resultado aparece (ou não) nos artefatos |

## Resumo de uma linha

`edital-ai` é um pipeline Python standalone (sem dependência de nuvem, roda
com IA local via Ollama) que recebe um edital de licitação pública (PDF,
DOCX, TXT ou MD), extrai texto e tabelas nativas, estrutura isso em objetos
Python (número, órgão, itens, requisitos de habilitação, prazos), gera um
resumo qualitativo via LLM local (com fallback determinístico se a IA
falhar) e produz 4 artefatos de saída (Excel, PDF, Word, e-mail) nomeados
igual ao arquivo carregado. É exposto à plataforma TAPOS via um adapter que
roda o produto como subprocesso isolado (seu próprio `.venv`), tanto de
forma síncrona (request HTTP) quanto assíncrona (fila RabbitMQ + worker).
