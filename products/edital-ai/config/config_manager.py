"""
=========================================================
Config Manager
---------------------------------------------------------
Centraliza o carregamento das configurações do edital-ai
(config/settings.json) e das variáveis de ambiente que
controlam a integração com o Ollama.
=========================================================
"""

import json
import os
from pathlib import Path


class ConfigManager:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.config_file = self.project_root / "config" / "settings.json"

        self.data = {}
        self.load()

    def load(self):
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found:\n{self.config_file}"
            )

        with open(self.config_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    # ---------------- input/output ----------------

    @property
    def input_directory(self) -> str:
        return self.data["input"]["diretorio"]

    @property
    def formatos_suportados(self):
        return self.data["input"]["formatos_suportados"]

    @property
    def output_directory(self) -> str:
        return self.data["output"]["diretorio"]

    # ---------------- ollama ----------------

    @property
    def ollama_base_url(self) -> str:
        return os.getenv("OLLAMA_BASE_URL", self.data["ollama"]["base_url"])

    @property
    def ollama_model(self) -> str:
        return os.getenv("OLLAMA_MODEL", self.data["ollama"]["model"])

    @property
    def ollama_timeout(self) -> int:
        return int(self.data["ollama"]["timeout"])

    # ---------------- processamento ----------------

    @property
    def max_tamanho_mb(self) -> int:
        return int(self.data["processamento"]["max_tamanho_mb"])
