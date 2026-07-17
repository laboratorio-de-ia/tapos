# 01 — Visão geral e negócio

## O que é

`edital-ai` é um produto da plataforma TAPOS (Tecle AI Platform Operating
System) que automatiza a leitura e análise de **editais de licitação
pública brasileira** (pregão eletrônico, concorrência, tomada de preços,
dispensa, etc.). O usuário sobe o arquivo do edital (PDF/DOCX/TXT) e recebe,
em segundos a poucos minutos, uma análise estruturada + 4 artefatos prontos
para uso (Excel, PDF, Word, e-mail).

## Problema que resolve

Editais públicos são documentos longos (frequentemente 50-300+ páginas),
com linguagem jurídica repetitiva, tabelas de itens que se espalham por
dezenas de páginas, e prazos críticos (abertura de sessão, impugnação,
recurso) que custam caro se perdidos. Ler manualmente cada edital para
decidir "vale a pena participar? o que precisamos entregar? até quando?" é
um trabalho manual, lento e sujeito a erro humano — sobretudo quando a
empresa participa de muitas licitações por mês.

## Para quem

- Empresas que participam regularmente de licitações públicas (fornecedores,
  distribuidoras, fabricantes com portfólio para o setor público).
- Departamentos de compliance/licitação dentro dessas empresas.
- Escritórios/consultorias que assessoram terceiros na participação em
  licitações.

## O que o sistema efetivamente extrai hoje

A partir do texto e das tabelas nativas do documento (sem uso de OCR quando
o PDF já tem camada de texto), o pipeline identifica:

- **Número do edital** (ex.: `032/2026`) e **modalidade** (pregão eletrônico,
  concorrência, tomada de preços, convite, concurso, leilão, dispensa,
  inexigibilidade, credenciamento).
- **Órgão licitante** (via a fórmula legal padrão "A/O `<órgão>` torna
  público...", com fallback por palavras-chave no cabeçalho do documento).
- **Objeto da licitação** (o que está sendo comprado/contratado).
- **Itens/lotes** da licitação: número, descrição, quantidade, unidade,
  valor unitário estimado, especificações técnicas — lidos preferencialmente
  das **tabelas nativas do PDF** (mais confiável que regex em texto corrido).
- **Requisitos de habilitação** (documentos obrigatórios para participar):
  também lidos preferencialmente de tabelas quando o edital as usa, com
  fallback para busca em prosa na seção "DA HABILITAÇÃO".
- **Prazos críticos** (abertura, encerramento, recebimento de propostas,
  sessão pública, recurso, impugnação, publicação), com data interpretada e
  marcação de "crítico" quando faltam menos de 7 dias.
- **Resumo executivo, riscos, oportunidades, recomendações e um score de
  conformidade (0-100)** — gerados por um LLM local (Ollama) a partir do que
  já foi extraído estruturalmente; se a IA falhar/não estiver disponível, um
  fallback determinístico simples garante que o pipeline nunca quebra por
  causa da IA (ver [`07-limitacoes-e-debito-tecnico.md`](07-limitacoes-e-debito-tecnico.md)).

## Casos de uso reais suportados hoje

1. **Análise rápida de edital** — upload → resumo executivo + score em
   segundos/minutos, em vez de leitura manual de dezenas de páginas.
2. **Extração de itens/lotes para cotação** — a aba "Objetos e Itens" do
   Excel gerado lista cada item com quantidade e valor estimado, pronta para
   ser usada como base de uma planilha de cotação interna.
3. **Checklist de conformidade documental** — a aba/seção de requisitos de
   habilitação vira um checklist do que a empresa precisa ter em mãos antes
   de participar.
4. **Alerta de prazos** — o e-mail gerado já destaca os prazos críticos e
   pode ser encaminhado para quem cuida da submissão da proposta.

## O que o sistema **não** faz hoje (importante para o brief comercial)

- Não monitora portais de compras automaticamente (é sempre um upload manual
  de um arquivo já em mãos do usuário).
- Não compara preços/histórico entre editais (a "análise competitiva"
  mencionada na especificação original em `edital.md` da raiz do projeto
  nunca foi implementada).
- Não persiste nem versiona o documento original de forma durável por usuário
  — hoje há apenas **um edital "em foco"** por vez em todo o produto (ver
  [`07-limitacoes-e-debito-tecnico.md`](07-limitacoes-e-debito-tecnico.md) — isso é a limitação mais crítica para
  virar produto multi-tenant).
- Não tem UI própria rica — a análise hoje é consumida via JSON de API e o
  painel de testes é uma página HTML simples do backend
  (`platform/saas-backend/app/static/index.html`).

Esse contraste entre "o que o piloto faz" e "o que falta para vender" é
detalhado no arquivo [`08-briefing-para-comercializacao.md`](08-briefing-para-comercializacao.md).
