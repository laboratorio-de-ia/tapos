# Plataforma — Observabilidade

## Estado atual: nenhuma observabilidade estruturada

Uma busca direta no código não encontrou métricas, tracing distribuído ou agregação de logs em nenhum ponto de `platform/`. O diretório `platform/tap-observability/` existe como namespace reservado, mas está vazio.

O que existe hoje é apenas:

- **logs em arquivo simples**, gravados pelo script de bootstrap: `.runtime/logs/saas-backend.log`, `.runtime/logs/speech-ai-worker.log`;
- **`print()` em workers**, sem formatação estruturada (ex.: mensagens como `"speech-ai-worker: aguardando jobs..."` impressas diretamente no processo);
- **critérios de aceite manuais** (`tasks/saas/*/acceptance.md`) com comandos `curl`, que funcionam como validação funcional pontual, não como observabilidade contínua.

## O que não existe

- métricas (latência, taxa de erro, throughput de fila);
- tracing distribuído entre backend → adapter → subprocesso do produto → worker;
- dashboards ou alertas;
- logs estruturados (JSON) ou correlação de request-id entre camadas.

## Por que isso importa

A ausência de observabilidade é uma lacuna conhecida e coerente com o estágio da plataforma (piloto validado, não operação multi-cliente em escala) — mas se torna prioritária assim que a plataforma precisar diagnosticar falhas de execução assíncrona (jobs presos em `running`, filas acumulando, workers travados) sem depender de inspeção manual de log.

---

## Ver também

- [runtime.md](runtime.md) — os processos que hoje só geram logs de arquivo
- [gateway.md](gateway.md) — o fluxo assíncrono que mais se beneficiaria de tracing
- [../01-tapos/roadmap.md](../01-tapos/roadmap.md) — lacunas mapeadas para produção
