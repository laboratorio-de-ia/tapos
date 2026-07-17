# TAPOS — Roadmap

## Histórico de construção (tasks/saas, 005 → 015)

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

Esse encadeamento é evidenciado nas próprias notas de tarefa: `007-login` adia explicitamente "adicionar JWT" para a tarefa `008`; `013-authorization` adia "integração com speech-ai" e "integração com edital-ai" para `014a`/`014b`. O escopo estreito e sequencial foi seguido de forma consistente no planejamento.

## Divergência conhecida: disciplina de commit

A constituição prescreve commit constante, um módulo por vez. Na prática, todo o histórico do repositório até esta documentação está em um único commit (`a48b7b5 — TAPOS v1.0.0 - operational SaaS baseline`), reunindo o trabalho de todas as 12 tarefas. O princípio não foi invalidado — precisa ser aplicado de forma mais rigorosa a partir daqui. Ver [../05-development/development-flow.md](../05-development/development-flow.md).

## Riscos conhecidos e lacunas mapeadas (da perspectiva de investimento)

Descritos com transparência no [documento para investidores-anjo](../../../investors/TAPOS_Pitch_Investidores_Anjo.md) e confirmados tecnicamente pela pesquisa desta documentação:

- **isolamento completo de dados por cliente** (multi-tenancy) — hoje há isolamento por usuário, não por organização/cliente; o `edital-ai`, em particular, tem um único slot de "edital em foco" por instalação inteira;
- **paralelização do processamento assíncrono** — a fila e o worker já existem, mas a capacidade de processar múltiplos usuários verdadeiramente em paralelo, em escala, ainda não foi validada sob carga;
- **hardening de segurança no recebimento de arquivos** — sem limite de tamanho/timeout de upload, sem sanitização adicional (ver [../04-platform/security.md](../04-platform/security.md));
- **pipeline de implantação contínua em produção** — hoje o ambiente é local (VM Ubuntu); a evolução para VPS/produção ainda não foi construída;
- **definição final do modelo de cobrança** — a infraestrutura de assinatura (produtos + assinaturas ativas/inativas) já existe; falta apenas a decisão comercial entre cobrança por análise, por volume ou por assinatura fixa.

Nenhum desses itens exige redesenhar a plataforma — são extensões naturais de uma arquitetura já construída pensando em desacoplamento e escala desde o primeiro dia.

## Próximos passos técnicos observados no código

- consolidar a checagem de assinatura duplicada entre `routes/products.py::_require_active_subscription` e `deps.py::get_product_access` (ver [../04-platform/gateway.md](../04-platform/gateway.md));
- conectar os workers de `edital-ai` e `code-ai` ao script de bootstrap automático (`start_tapos_env.sh`), hoje limitado ao worker do Speech-AI;
- migrar artefatos de produto de disco local para object storage (MinIO), hoje reservado mas não usado;
- popular `.claude/skills`, `agents`, `rules`, `memory` — reservados desde o início e liberados para uso "após estabilidade do backend SaaS", condição já atendida pela baseline v1.0.0 (ver [../05-development/claude-code.md](../05-development/claude-code.md));
- corrigir o valor padrão inseguro do segredo JWT (`dev-secret-key`) antes de qualquer exposição em produção.

---

## Ver também

- [overview.md](overview.md) — estado atual consolidado
- [../00-tecle/vision.md](../00-tecle/vision.md) — por que estas lacunas são vistas como oportunidade, não como bloqueio
- [../05-development/development-flow.md](../05-development/development-flow.md) — o ciclo de trabalho por trás deste histórico
