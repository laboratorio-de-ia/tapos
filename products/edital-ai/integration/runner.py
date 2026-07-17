from app.edital_ai_app import EditalAIApp

from .schemas import EditalRunResult


def execute_pipeline(arquivo_path: str) -> EditalRunResult:
    app = EditalAIApp()
    edital, analise, artefatos = app.run(arquivo_path)

    prazos_criticos = [
        {"descricao": p.descricao, "data": p.data_texto}
        for p in analise.prazos_identificados
    ]

    return EditalRunResult(
        status="executed",
        edital_id=edital.id,
        numero_edital=edital.numero,
        orgao=edital.orgao,
        modalidade=edital.modalidade,
        objetos_identificados=len(analise.objetos_identificados),
        requisitos_identificados=len(analise.requisitos_identificados),
        prazos_identificados=len(analise.prazos_identificados),
        score_conformidade=analise.score_conformidade,
        ia_utilizada=analise.ia_utilizada,
        resumo_executivo=analise.resumo_executivo,
        prazos_criticos=prazos_criticos,
        riscos=analise.riscos,
        oportunidades=analise.oportunidades,
        recomendacoes=analise.recomendacoes,
        arquivos_gerados={
            "excel": artefatos.excel,
            "pdf": artefatos.pdf,
            "word": artefatos.word,
            "email": artefatos.email,
        },
    )
