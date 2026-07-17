"""Cliente HTTP minimalista para o Ollama local."""

import json

import requests


class OllamaService:
    def __init__(self, base_url: str, model: str, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate_json(self, prompt: str, context: str) -> dict:
        """Chama /api/generate em modo JSON e devolve o dict já parseado."""
        full_prompt = f"{prompt}\n\nTEXTO DO EDITAL:\n{context[:12000]}"

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "format": "json",
            },
            timeout=self.timeout,
        )
        response.raise_for_status()

        texto_resposta = response.json().get("response", "")
        return self._parse_json(texto_resposta)

    @staticmethod
    def _parse_json(texto: str) -> dict:
        texto = texto.strip()

        if texto.startswith("```"):
            texto = texto.strip("`")
            if "\n" in texto:
                texto = texto.split("\n", 1)[1]

        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            inicio = texto.find("{")
            fim = texto.rfind("}")
            if inicio != -1 and fim != -1 and fim > inicio:
                return json.loads(texto[inicio: fim + 1])
            raise
