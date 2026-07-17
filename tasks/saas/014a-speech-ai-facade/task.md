# Task 014A — Speech-AI Facade

## Context

O produto speech-ai já está funcional dentro da estrutura da TAPOS.
Atualmente ele roda como aplicação local via main.py e SpeechAIApp.

A TAPOS precisa integrar esse produto sem acoplar o código do speech-ai ao backend SaaS.

---

## Objective

Criar uma camada de integração programática no speech-ai que permita executar o pipeline completo por código.

---

## Requirements

Criar em:

app/integration/

os arquivos:

- __init__.py
- schemas.py
- runner.py
- facade.py

---

## Functional Goal

Permitir chamada assim:

from app.integration.facade import run_speech_ai

result = run_speech_ai()

---

## Expected Result

A facade deve:

- executar a pipeline atual do speech-ai
- gerar narration.txt
- gerar speech.txt
- gerar audio.mp3
- retornar um dicionário padronizado com metadados da execução

---

## Constraints

- não alterar a lógica central do produto
- não integrar ainda com o backend TAPOS
- não criar API nesta task
- preservar o comportamento atual do speech-ai

---

## Acceptance Criteria

- facade criada
- execução programática funcionando
- áudio gerado corretamente
- retorno padronizado funcionando
