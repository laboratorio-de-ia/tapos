# Task 014B — TAPOS integrates with speech-ai

## Context

A TAPOS já possui:

- autenticação com JWT
- products
- subscriptions
- authorization por produto

O speech-ai já possui uma facade programática criada na Task 014A.

Agora precisamos integrar o backend SaaS ao produto real.

---

## Objective

Criar um endpoint no backend SaaS que execute o produto speech-ai por meio da sua facade.

---

## Requirements

- criar endpoint:

POST /products/speech-ai/run

- validar:
  - JWT
  - usuário autenticado
  - subscription ativa para speech-ai

- chamar:
  from app.integration.facade import run_speech_ai

- retornar o resultado padronizado da facade

---

## Constraints

- não integrar fila nesta task
- não transformar speech-ai em microserviço ainda
- integração local, dentro do mesmo workspace
- manter simplicidade

---

## Acceptance Criteria

- usuário com subscription ativa executa speech-ai com sucesso
- usuário sem subscription recebe 403
- sem token recebe 401
- retorno contém paths do pipeline e status de execução
