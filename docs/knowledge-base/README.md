# Tecle — Knowledge Base

Bem-vindo à Knowledge Base oficial da **Tecle**. Este repositório documental reúne, de forma modular e versionada, todo o conhecimento institucional, técnico e de produto da empresa e da sua plataforma, a **TAPOS (Tecle AI Platform Operating System)**.

## Propósito

Esta Knowledge Base existe para ser a fonte única de verdade sobre:

- quem é a Tecle e qual é a sua tese de negócio;
- o que é a TAPOS e como ela é construída;
- como cada produto de Inteligência Artificial da plataforma (Speech-AI, Edital-AI, Code-AI e, futuramente, Educa-AI) funciona;
- como a plataforma opera em termos de runtime, armazenamento, segurança, observabilidade, API e gateway de produtos;
- como o time desenvolve, com quais padrões, ferramentas e fluxo de trabalho.

## Formato

A documentação é escrita em **Markdown modular**: cada assunto vive em seu próprio arquivo, dentro de uma pasta numerada por área. Essa organização permite:

- manutenção incremental (um arquivo por vez, sem afetar o restante);
- geração automática de artefatos derivados — documentação técnica, apresentações, roteiros de vídeo, treinamentos, bases de RAG, agentes de IA e documentação de sistema;
- consolidação futura em um documento único (PDF, DOCX ou site) sem perder a organização de origem.

## Como navegar

Comece pelo [SUMMARY.md](SUMMARY.md) para o índice completo. As áreas principais são:

| Pasta | Conteúdo |
|---|---|
| `00-tecle/` | Empresa, visão e competências da Tecle |
| `01-tapos/` | A plataforma TAPOS: visão geral, arquitetura, princípios, roadmap e tecnologias |
| `02-speech-ai/` | Produto Speech-AI: da análise de texto à narração em áudio |
| `03-products/` | Produtos verticais: Edital-AI, Educa-AI e Code-AI |
| `04-platform/` | Camada operacional da plataforma: runtime, storage, segurança, observabilidade, API e gateway |
| `05-development/` | Workspace, constituição de engenharia, padrões de código, Claude Code e fluxo de desenvolvimento |
| `assets/` | Diagramas, imagens e material de arquitetura de apoio |

## Versão consolidada em PDF

Todo o conteúdo desta Knowledge Base também está disponível consolidado em um único documento PDF, com capa e sumário navegável, em [`assets/TAPOS-Knowledge-Base-v1.0.pdf`](assets/TAPOS-Knowledge-Base-v1.0.pdf).

## Status

Esta é a **versão 1.0** da Knowledge Base, consolidada em julho de 2026, refletindo o estado real da plataforma TAPOS na sua baseline operacional (v1.0.0): autenticação JWT, modelo de produtos e assinaturas, gateway central de autorização, execução assíncrona via fila e workers, e o produto Speech-AI integrado de ponta a ponta.

## Manutenção

Esta base é viva. Ao evoluir a plataforma ou os produtos, os arquivos correspondentes devem ser atualizados na mesma disciplina incremental que rege o desenvolvimento da TAPOS: um módulo de documentação por vez, revisado e versionado via Git.
