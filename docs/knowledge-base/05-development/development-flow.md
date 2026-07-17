# Fluxo de Desenvolvimento

## O ciclo prescrito

Todo o desenvolvimento da TAPOS segue, por princípio, um ciclo disciplinado e incremental:

```
Definir tarefa
↓
Implementar (1 módulo)
↓
Testar
↓
Commit
↓
Próxima tarefa
```

## O template real de tarefa

Cada tarefa vive em `tasks/saas/NNN-nome/` e segue um template consistente, observado nas 12 pastas de `005` a `015`:

- **`task.md`** — Contexto / Objetivo / Requisitos / Restrições / Tratamento de erro / Notas — incluindo o que **não** deve ser feito ainda naquela tarefa.
- **`acceptance.md`** — critérios funcionais e técnicos, com comandos `curl` reais e executáveis que provam que o endpoint funciona.
- **`notes.md`** — decisões tomadas e o que foi explicitamente adiado para uma tarefa futura.

Exemplo concreto da disciplina de adiamento: as notas da tarefa `007-login` dizem explicitamente "Future: adicionar JWT (Task 008), criar /users/me, implementar controle de acesso" — e de fato a tarefa `008` é `008-jwt` e a `009` é `009-protected-route`. As notas da tarefa `013-authorization` adiam "middleware/dependency reutilizável", "integração com speech-ai" e "integração com edital-ai" — e `014a`/`014b` são exatamente essas integrações. O encadeamento das tarefas no repositório é evidência direta de que o ciclo Definir → Implementar → Testar → Commit → Próximo foi seguido no *planejamento e escopo* de cada etapa.

## Histórico de tarefas (005 → 015)

| Tarefa | Entregue |
|---|---|
| 005-password-hash | Hash de senha com bcrypt |
| 006-register-hash | Endpoint de registro de usuário |
| 007-login | Login com validação de credenciais |
| 008-jwt | Geração de JWT |
| 009-protected-route | Rota protegida (`/users/me`) com JWT |
| 010-user-profile | Perfil de usuário enriquecido |
| 011-products | Modelo de produtos (slug por vertical) |
| 012-subscriptions | Assinaturas ativas/inativas por produto |
| 013-authorization | Autorização central (produto + assinatura) |
| 014-product-gateway | Gateway único de acesso a produtos |
| 014a-speech-ai-facade | Contrato facade/runner/schemas/cli do Speech-AI |
| 014b-tapos-speech-ai-integration | Speech-AI integrado de ponta a ponta na plataforma |
| 015-async-speech-ai-execution | Execução assíncrona real via fila e worker |

## A realidade dos commits — uma divergência honesta

A constituição e o `workspace.md` prescrevem "commit constante" e "commitar após cada etapa". Na prática, até o momento desta documentação, **todo o histórico do repositório é um único commit**:

```
a48b7b5 TAPOS v1.0.0 - operational SaaS baseline
```

Esse commit único reúne 359 arquivos alterados e mais de 113 mil linhas inseridas — todo o `.claude/`, o backend completo, os três produtos, documentação e até artefatos binários (PDFs, imagens, um `.docx`, o áudio do pitch para investidores). Isso significa que o trabalho de todas as 12 tarefas (005–015) foi acumulado localmente e consolidado em um único commit de baseline, em vez de commits incrementais por módulo, como a constituição prescreve.

Isso não invalida o princípio — é um registro honesto de que a disciplina de commit precisa ser aplicada de forma mais rigorosa a partir daqui, tarefa por tarefa, à medida que a v1.1 e versões seguintes forem desenvolvidas.

## Testes reais

Os testes que efetivamente existem e rodam vivem em `platform/saas-backend/tests/` (`test_deps.py`, `test_security.py`), não na pasta `tests/` da raiz, que está vazia (reservada). Os critérios de aceite de cada tarefa (`acceptance.md`) também funcionam como uma camada de validação funcional via `curl`, complementar aos testes automatizados.

## Artefatos de descarte

A pasta `trash/` contém material de diagnóstico e depuração pontual (capturas de rede, transcrições de shell de debug, exports forenses, scripts de teste manuais como `test_auth.sh` e `test_task015.sh`) — não faz parte do fluxo formal de tarefas, mas foi preservada em vez de descartada, por precaução.

## Ver também

- [claude-code.md](claude-code.md) — como o Claude Code opera dentro deste ciclo
- [constitution.md](constitution.md) — os princípios que este fluxo implementa
- [../01-tapos/roadmap.md](../01-tapos/roadmap.md) — o que vem depois da tarefa 015
