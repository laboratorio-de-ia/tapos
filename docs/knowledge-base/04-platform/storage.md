# Plataforma — Storage

## Princípio: dados nunca dentro de containers

Por regra de arquitetura (ver [Constituição](../05-development/constitution.md)), toda persistência vive fora dos containers, em `/data/platform`, separado em `infra/`, `runtime/` e `storage/`. Essa regra foi verificada diretamente no sistema de arquivos, não é apenas uma intenção documentada:

```text
/data/platform/storage/
├── db/           → dados do PostgreSQL
├── redis/        → dados do Redis
├── rabbitmq/     → mnesia do RabbitMQ (filas, exchanges)
├── minio/        → armazenamento de objetos (MinIO)
├── qdrant/       → coleções vetoriais (inclui raft_state.json)
├── models/       → modelos (inclui um par de chaves id_ed25519 e um diretório cache/ — vale revisão de segurança sobre o que está versionado aqui)
└── portainer/    → dados do Portainer
```

`/data`, `/runtime` e `/storage` estão excluídos do controle de versão via `.gitignore` — persistência nunca é versionada junto ao código.

## Bancos e sistemas usados

| Sistema | Papel atual |
|---|---|
| PostgreSQL | dados estruturados: usuários, produtos, assinaturas, jobs, análises de edital |
| Redis | reservado para cache/sessões — ainda não usado ativamente pelo backend |
| RabbitMQ | fila de mensagens para execução assíncrona (ver [gateway.md](gateway.md)) |
| MinIO | armazenamento de objetos — reservado; os produtos hoje gravam artefatos em disco local, não em MinIO (ver limitação em [../03-products/edital-ai.md](../03-products/edital-ai.md)) |
| Qdrant | banco vetorial — reservado para uso futuro de RAG |
| Ollama | modelos de IA local (usado hoje pelo `edital-ai`, modelo `mistral`) |

## Persistência ao nível de produto

Os três produtos ainda gravam entrada/saída em diretórios locais dentro de seu próprio caminho (`input/`, `output/`, `processados/`), não em MinIO — uma lacuna conhecida para operação multi-tenant (ver [../01-tapos/roadmap.md](../01-tapos/roadmap.md)).

---

## Ver também

- [runtime.md](runtime.md) — os containers que produzem estes dados
- [../01-tapos/roadmap.md](../01-tapos/roadmap.md) — migração para object storage como próximo passo mapeado
- [../05-development/constitution.md](../05-development/constitution.md) — o princípio de "persistência correta"
