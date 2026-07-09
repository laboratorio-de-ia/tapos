# TAPOS — Architecture (Current State)

## 1. Objetivo

Documentar o estado atual da plataforma TAPOS após a validação da infraestrutura local e da primeira camada SaaS do backend.

---

## 2. Visão Geral

A TAPOS (Tecle AI Platform Operating System) é a base de engenharia da plataforma Tecle para produtos SaaS com Inteligência Artificial.

No estado atual, a plataforma está organizada em duas camadas principais:

1. **Laboratório local (VM Ubuntu)**
   - ambiente de desenvolvimento e execução local
   - VSCode + Claude Code
   - backend SaaS em FastAPI
   - infraestrutura Docker persistente

2. **Evolução futura para VPS**
   - publicação e operação da camada SaaS
   - espelhamento controlado do ambiente local

---

## 3. Arquitetura Atual

```text
Cliente
  ↓
SaaS Backend (FastAPI)
  ├── /health
  ├── /auth/register
  ├── /auth/login
  └── /users/me  [protegida com JWT]
  ↓
Auth Layer
  ├── hash de senha (bcrypt)
  ├── login
  ├── geração de JWT
  └── validação do usuário autenticado
  ↓
Data Layer
  └── PostgreSQL
```

---

## 4. Stack Atual

### Backend
- FastAPI
- SQLAlchemy
- passlib/bcrypt
- python-jose (JWT)

### Infraestrutura local
- Docker
- PostgreSQL
- Redis
- RabbitMQ
- MinIO
- Qdrant
- Ollama
- Open WebUI
- Portainer

---

## 5. Estrutura de Diretórios

### Workspace de desenvolvimento

```text
/workspace/tecle
├── .claude/
├── automation/
├── developers/
├── governance/
├── platform/
│   └── saas-backend/
├── products/
│   ├── speech-ai/
│   ├── edital-ai/
│   └── educa-ai/
├── shared/
├── tasks/
└── tests/
```

### Runtime e persistência

```text
/data/platform
├── infra/
├── runtime/
└── storage/
    ├── db/
    ├── redis/
    ├── rabbitmq/
    ├── minio/
    ├── qdrant/
    ├── models/
    └── portainer/
```

---

## 6. Backend SaaS — Estado Atual

### Endpoints já implementados

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /users/me`

### Comportamento atual

#### /auth/register
- cria usuário no PostgreSQL
- salva senha com hash bcrypt

#### /auth/login
- valida email e senha
- retorna JWT

#### /users/me
- exige token JWT
- retorna perfil do usuário autenticado

Exemplo de retorno atual:

```json
{
  "id": 4,
  "email": "teste2@tecle.com",
  "created_at": "2026-07-08T17:31:59.315190+00:00",
  "is_active": true
}
```

---

## 7. Segurança Atual

### Já implementado
- hash de senha com bcrypt
- JWT para autenticação
- rota protegida com dependência de usuário autenticado

### Ainda não implementado
- refresh token
- RBAC (roles/perfis)
- controle de acesso por produto
- multi-tenant

---

## 8. Produtos da Plataforma

### speech-ai
- produto já existente
- transforma entradas em áudio e vídeo
- utilizará a camada SaaS para autenticação e controle de acesso

### edital-ai
- receberá documentos relacionados a editais
- fará análise e geração de artefatos (Excel, PDF, Word, e-mail)
- utilizará a camada SaaS para autenticação e autorização

### educa-ai
- receberá dados e documentos financeiros
- apoiará educação financeira e acompanhamento de mercado
- utilizará a mesma base SaaS

---

## 9. Fluxo Atual de Autenticação

```text
Cliente
  ↓
POST /auth/login
  ↓
Backend valida usuário e senha
  ↓
JWT é gerado
  ↓
Cliente usa Authorization: Bearer <token>
  ↓
GET /users/me
  ↓
Backend valida token e retorna perfil
```

---

## 10. Modelo de Trabalho Atual

O desenvolvimento segue o padrão TAPOS:

```text
Task
↓
Claude Code
↓
Implementação de 1 módulo
↓
Teste local
↓
Git commit
↓
Git push
```

### Convenções já adotadas
- contexto persistente em `.claude/`
- tarefas documentadas em `/workspace/tecle/tasks`
- um arquivo de teste único (`test_auth.sh`) atualizado a cada etapa

---

## 11. Próxima Evolução

A próxima camada a ser construída é a **Business / SaaS Layer**.

### Próximas tarefas previstas
- enrich profile / user profile
- products
- subscriptions
- access control por produto
- integração do speech-ai com a camada SaaS

---

## 12. Resumo Executivo

A plataforma TAPOS já possui:

- infraestrutura local operacional
- backend SaaS funcional
- autenticação com JWT
- rota protegida validada
- fluxo disciplinado de desenvolvimento com Claude Code + VSCode + Git

No estado atual, a base técnica está pronta para evoluir da autenticação para a camada multi-produto do SaaS.
