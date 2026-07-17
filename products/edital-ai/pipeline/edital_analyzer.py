from pathlib import Path

from config import ConfigManager
from models import Analise, Edital
from services.ollama_service import OllamaService

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "generate_summary.txt"


class EditalAnalyzer:
    """Gera a análise qualitativa do edital usando Ollama, com fallback
    determinístico caso o Ollama esteja indisponível ou a resposta não
    possa ser interpretada."""

    def __init__(self, cfg: ConfigManager):
        self.cfg = cfg
        self.ollama = OllamaService(
            base_url=cfg.ollama_base_url,
            model=cfg.ollama_model,
            timeout=cfg.ollama_timeout,
        )
        self.prompt = PROMPT_FILE.read_text(encoding="utf-8")

    def analyze(self, edital: Edital) -> Analise:
        analise = Analise(
            edital_id=edital.id,
            objetos_identificados=edital.objetos,
            requisitos_identificados=edital.requisitos,
            prazos_identificados=edital.prazos,
        )

        try:
            contexto = self._construir_contexto(edital)
            dados = self.ollama.generate_json(self.prompt, contexto)
            analise.resumo_executivo = dados.get("resumo_executivo", "") or ""
            analise.riscos = list(dados.get("riscos", []) or [])
            analise.oportunidades = list(dados.get("oportunidades", []) or [])
            analise.recomendacoes = list(dados.get("recomendacoes", []) or [])
            analise.score_conformidade = float(dados.get("score_conformidade", 0) or 0)
            analise.ia_utilizada = True
        except Exception as exc:  # noqa: BLE001
            analise.resumo_executivo = self._resumo_fallback(edital)
            analise.score_conformidade = self._score_fallback(edital)
            analise.riscos = [f"Análise via IA indisponível ({exc}); usando resumo determinístico."]
            analise.ia_utilizada = False

        return analise

    @staticmethod
    def _construir_contexto(edital: Edital) -> str:
        """Monta um contexto compacto e estruturado para o Ollama.

        Antes, o texto_completo bruto (até 12000 caracteres) era enviado
        direto ao modelo — mas boa parte desse trecho inicial é boilerplate
        legal (citação de leis, decretos etc.), não o conteúdo que importa
        para o resumo. Isso deixava o prompt maior e mais lento sem ganho de
        qualidade, e chegou a estourar o timeout do Ollama em editais reais.
        Enviar o que o parser já extraiu de forma estruturada (número,
        órgão, itens, requisitos, prazos) é mais rápido e mais alinhado ao
        que o prompt (prompts/generate_summary.txt) já pede.
        """
        linhas = [
            f"Número: {edital.numero or '-'}",
            f"Órgão: {edital.orgao or '-'}",
            f"Modalidade: {edital.modalidade or '-'}",
            f"Objeto: {edital.objeto or '-'}",
            "",
            f"Itens/objetos identificados ({len(edital.objetos)} no total, mostrando até 30):",
        ]
        for o in edital.objetos[:30]:
            qtd = f"{o.quantidade:g}" if o.quantidade is not None else "-"
            linhas.append(f"- Item {o.numero}: {o.descricao} (qtd: {qtd} {o.unidade or ''})".strip())

        linhas.append("")
        linhas.append(f"Requisitos de habilitação identificados ({len(edital.requisitos)} no total, mostrando até 20):")
        for r in edital.requisitos[:20]:
            linhas.append(f"- {r.descricao}")

        linhas.append("")
        linhas.append(f"Prazos identificados ({len(edital.prazos)} no total):")
        for p in edital.prazos[:20]:
            linhas.append(f"- {p.descricao}: {p.data_texto}")

        linhas.append("")
        linhas.append("Trecho do texto original (início do edital, para contexto adicional):")
        linhas.append(edital.texto_completo[:3000])

        return "\n".join(linhas)

    @staticmethod
    def _resumo_fallback(edital: Edital) -> str:
        partes = []
        if edital.numero:
            partes.append(f"Edital nº {edital.numero}")
        if edital.orgao:
            partes.append(f"do órgão {edital.orgao}")
        if edital.modalidade:
            partes.append(f"na modalidade {edital.modalidade}")

        base = " ".join(partes) if partes else "Edital"
        objeto = f" Objeto: {edital.objeto}." if edital.objeto else ""

        return (
            f"{base}. {objeto} "
            f"{len(edital.objetos)} item(ns) e {len(edital.requisitos)} "
            "requisito(s) de habilitação identificados automaticamente pela extração."
        ).strip()

    @staticmethod
    def _score_fallback(edital: Edital) -> float:
        pontos = 0
        if edital.numero:
            pontos += 20
        if edital.orgao:
            pontos += 20
        if edital.modalidade:
            pontos += 20
        if edital.objeto:
            pontos += 20
        if edital.prazos:
            pontos += 20
        return float(pontos)
