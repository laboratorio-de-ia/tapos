# Educa-AI

## Status: reservado para desenvolvimento futuro

O Educa-AI é a quarta vertical de IA planejada para a TAPOS. Diferente de Speech-AI, Edital-AI e Code-AI, **não existe implementação hoje**: `products/educa-ai/` é um diretório completamente vazio (sem arquivos, sem subpastas), criado como reserva de estrutura desde o início do workspace.

Não há adapter, worker, pasta `integration/` ou qualquer código associado a este produto em nenhum outro ponto da plataforma.

## Por que ele existe mesmo sem código

A existência deste diretório vazio — e sua menção explícita em `architecture.md` e no documento para investidores-anjo — é, em si, parte da tese de plataforma da Tecle: a TAPOS foi desenhada para que uma nova vertical de IA seja adicionada como uma extensão sobre a infraestrutura já existente (autenticação, assinaturas, gateway, execução assíncrona), não como um novo projeto de engenharia começado do zero. O Educa-AI é a prova, no próprio código, de que essa reserva de espaço já foi planejada.

> "É o motivo pelo qual já existe uma quarta vertical, educa-ai, reservada na estrutura da plataforma para os próximos ciclos de desenvolvimento."
> — [Documento para Investidores-Anjo](../../../investors/TAPOS_Pitch_Investidores_Anjo.md)

## Escopo descrito (não implementado)

Segundo `architecture.md`, o Educa-AI receberá dados e documentos financeiros e apoiará educação financeira e acompanhamento de mercado, utilizando a mesma base SaaS dos demais produtos. Não há, além deste parágrafo, nenhum detalhamento adicional de arquitetura, pipeline, modelos de dados ou roadmap técnico em nenhum lugar do repositório.

## O que precisaria ser construído

Ao ser priorizado, o Educa-AI deverá seguir o mesmo padrão já validado pelos outros três produtos:

1. Estrutura de produto com `integration/{facade.py, runner.py, schemas.py, cli.py}` (ver [../05-development/coding-standards.md](../05-development/coding-standards.md)).
2. Adapter dedicado em `platform/saas-backend/app/products/educa_ai_adapter.py`.
3. Worker dedicado em `platform/tap-runtime/workers/educa-ai-worker/`.
4. Registro do produto no modelo de Produtos e Assinaturas da TAPOS (task 011/012), com seu próprio slug.

Nenhum desses passos exige mudança na plataforma em si — é exatamente esse reaproveitamento sem reengenharia que a tese da TAPOS promete.

## Ver também

- [edital-ai.md](edital-ai.md), [code-ai.md](code-ai.md) — os três produtos hoje implementados, cujo padrão de integração o Educa-AI deverá seguir
- [../01-tapos/roadmap.md](../01-tapos/roadmap.md) — próximos passos da plataforma
- [../00-tecle/vision.md](../00-tecle/vision.md) — a tese de plataforma que justifica esta reserva
