# Claude Code neste Workspace

## Propósito da pasta `.claude/`

A pasta `.claude/` define o contexto permanente utilizado pelo Claude Code dentro da plataforma TAPOS, garantindo que o desenvolvimento siga padrões consistentes de arquitetura, engenharia e evolução incremental — transformando o Claude em um assistente orientado por contexto, não apenas um gerador de código.

## Conteúdo atual

```text
.claude/
├── workspace.md          # arquitetura e estrutura da plataforma
├── constitution.md       # regras e princípios de engenharia
├── current-phase.md      # foco e etapa atual do projeto
├── settings.local.json   # permissões locais de ferramentas
├── scheduled_tasks.lock  # lock de execução em runtime
├── skills/               # reservado — vazio
├── agents/               # reservado — vazio
├── rules/                # reservado — vazio
└── memory/               # reservado — vazio
```

## Como o Claude usa esta pasta

Ao iniciar o Claude Code a partir da raiz do workspace (`/workspace/tecle`), ele passa a utilizar automaticamente:

- **arquitetura** ([workspace.md](workspace.md) / `.claude/workspace.md`)
- **regras** ([constitution.md](constitution.md) / `.claude/constitution.md`)
- **foco atual** (`.claude/current-phase.md`)

## Estratégia de expansão planejada

Quatro diretórios foram criados antecipadamente como scaffolding para fases futuras, e devem permanecer vazios até que sejam explicitamente necessários:

- `agents/` → agentes especializados
- `skills/` → capacidades reutilizáveis
- `memory/` → contexto persistente
- `rules/` → regras adicionais

A regra explícita é que **estes diretórios só devem ser criados/populados após estabilidade do backend SaaS** — o que hoje, com a baseline v1.0.0 operacional (autenticação, produtos, assinaturas, gateway, execução assíncrona), é uma condição já atendida, tornando esta expansão um próximo passo natural e não mais prematuro.

## `current-phase.md` está desatualizado

Vale registrar com clareza: `.claude/current-phase.md` descreve o estágio "SaaS Backend Initialization", com a tarefa atual sendo "criar estrutura inicial do backend com FastAPI, app base e endpoint `/health`", e lista explicitamente como **não permitido** neste momento: "criar auth completo", "integrar outros serviços". Esta é uma fotografia da fase mais inicial do projeto.

O `changelog.md` da raiz, porém, já documenta a **v1.0.0**, com JWT Authentication, Products, Subscriptions, Authorization, Product Gateway e Speech-AI integrado (tarefas 014A/014B concluídas) — várias fases à frente do que `current-phase.md` descreve. Ou seja: **`current-phase.md` nunca foi atualizado após a primeira tarefa** e não deve ser tratado como fonte de verdade sobre o estágio atual da plataforma. Até que seja atualizado, o `changelog.md` e o histórico em `tasks/saas/` são as fontes corretas sobre o que já foi construído.

## Regras importantes de uso

- Sempre iniciar o Claude na raiz `/workspace/tecle`.
- Nunca trabalhar em subpastas isoladas.
- Nunca gerar múltiplos módulos ao mesmo tempo.
- Nunca pular validação.
- Sempre commitar após cada etapa (ver [development-flow.md](development-flow.md) para o quanto essa regra foi seguida na prática até agora).

## Ver também

- [workspace.md](workspace.md) — estrutura completa do workspace que este contexto governa
- [constitution.md](constitution.md) — as regras que o Claude Code aplica
- [development-flow.md](development-flow.md) — o ciclo de desenvolvimento na prática
