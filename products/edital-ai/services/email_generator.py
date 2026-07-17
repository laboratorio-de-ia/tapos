from pathlib import Path

from models import Edital, Analise


def gerar_email(edital: Edital, analise: Analise, caminho_saida: str) -> str:
    numero = edital.numero or "s/nº"
    orgao = edital.orgao or "órgão não identificado"

    prazos_criticos = [p for p in analise.prazos_identificados if p.critico] or analise.prazos_identificados[:3]
    linhas_prazos = "\n".join(
        f"  - {p.descricao}: {p.data_texto}" for p in prazos_criticos
    ) or "  - Nenhum prazo identificado automaticamente."

    assunto = f"[EDITAL] Nº {numero} - {orgao} - AÇÃO REQUERIDA"

    corpo = f"""Assunto: {assunto}

Resumo do edital:
{analise.resumo_executivo or '-'}

Prazos críticos:
{linhas_prazos}

Score de conformidade do edital: {analise.score_conformidade:.0f}%

Recomendações:
{chr(10).join('  - ' + r for r in analise.recomendacoes) or '  - Nenhuma recomendação gerada.'}

--
Gerado automaticamente pelo edital-ai (TAPOS). Anexe a planilha Excel com os detalhes completos antes de enviar.
"""

    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    Path(caminho_saida).write_text(corpo, encoding="utf-8")
    return str(caminho_saida)
