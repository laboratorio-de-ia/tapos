from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from models import Edital, Analise


def gerar_pdf(edital: Edital, analise: Analise, caminho_saida: str) -> str:
    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(caminho_saida),
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Análise de Edital — TAPOS edital-ai", styles["Title"]))
    story.append(Spacer(1, 12))

    dados_cabecalho = [
        ["Número", edital.numero or "-"],
        ["Órgão", edital.orgao or "-"],
        ["Modalidade", edital.modalidade or "-"],
        ["Score de conformidade", f"{analise.score_conformidade:.0f}%"],
    ]
    tabela_cabecalho = Table(dados_cabecalho, colWidths=[4 * cm, 12 * cm])
    tabela_cabecalho.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0f2942")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(tabela_cabecalho)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Objeto", styles["Heading2"]))
    story.append(Paragraph(edital.objeto or "Não identificado.", styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Resumo Executivo", styles["Heading2"]))
    story.append(Paragraph(analise.resumo_executivo or "-", styles["BodyText"]))
    story.append(Spacer(1, 12))

    if analise.objetos_identificados:
        story.append(Paragraph("Objetos e Itens", styles["Heading2"]))
        dados = [["Nº", "Descrição", "Qtd", "Valor est."]]
        for o in analise.objetos_identificados[:20]:
            dados.append([
                str(o.numero),
                (o.descricao or "")[:70],
                str(o.quantidade or "-"),
                f"R$ {o.valor_estimado:.2f}" if o.valor_estimado else "-",
            ])
        tabela = Table(dados, colWidths=[1.5 * cm, 9 * cm, 2 * cm, 3.5 * cm])
        tabela.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f6fb8")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        story.append(tabela)
        story.append(Spacer(1, 12))

    if analise.prazos_identificados:
        story.append(Paragraph("Prazos", styles["Heading2"]))
        for p in analise.prazos_identificados:
            texto = f"• {p.descricao}: {p.data_texto}"
            story.append(Paragraph(texto, styles["BodyText"]))
        story.append(Spacer(1, 12))

    if analise.requisitos_identificados:
        story.append(Paragraph("Checklist de Requisitos de Habilitação", styles["Heading2"]))
        for r in analise.requisitos_identificados:
            story.append(Paragraph(f"☐ {r.descricao}", styles["BodyText"]))
        story.append(Spacer(1, 12))

    if analise.riscos:
        story.append(Paragraph("Riscos", styles["Heading2"]))
        for item in analise.riscos:
            story.append(Paragraph(f"• {item}", styles["BodyText"]))
        story.append(Spacer(1, 12))

    if analise.oportunidades:
        story.append(Paragraph("Oportunidades", styles["Heading2"]))
        for item in analise.oportunidades:
            story.append(Paragraph(f"• {item}", styles["BodyText"]))
        story.append(Spacer(1, 12))

    if analise.recomendacoes:
        story.append(Paragraph("Recomendações", styles["Heading2"]))
        for item in analise.recomendacoes:
            story.append(Paragraph(f"• {item}", styles["BodyText"]))

    doc.build(story)
    return str(caminho_saida)
