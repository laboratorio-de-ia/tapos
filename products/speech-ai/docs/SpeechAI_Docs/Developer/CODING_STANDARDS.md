# Coding Standards

## 1. Philosophy

The Speech AI project adheres to strict coding standards to ensure readability, maintainability, and consistency across the codebase. We prioritize clear, self-documenting code over clever, terse solutions.

## 2. Python Style Guide

We generally follow **PEP 8**, with some specific adaptations for this project.

### 2.1. Formatting
-   **Indentation**: Use 4 spaces per indentation level. Never use tabs.
-   **Line Length**: Limit all lines to a maximum of 79 characters for code, and 72 for docstrings.
-   **Blank Lines**: Use blank lines to separate logical sections of code within functions to improve readability.
-   **Imports**: Imports should be grouped in the following order:
    1.  Standard library imports.
    2.  Related third-party imports.
    3.  Local application/library specific imports.

### 2.2. Naming Conventions
-   **Classes**: Use `CamelCase` (e.g., `SpeechIntelligenceEngine`).
-   **Functions and Variables**: Use `snake_case` (e.g., `calculate_statistics`).
-   **Constants**: Use `UPPER_CASE_WITH_UNDERSCORES` (e.g., `DEFAULT_TIMEOUT`).
-   **Private Members**: Prefix internal methods and variables with a single underscore (e.g., `_configure_logging`).

## 3. Documentation and Comments

### 3.1. Docstrings
Every module, class, and public function must have a docstring. We use a structured format that clearly defines the purpose, arguments, and return values.

Example module header:
```python
"""
=========================================================
Module Name
---------------------------------------------------------
Brief description of what the module does.

Author: Name
=========================================================
"""
```

### 3.2. Inline Comments
Use inline comments sparingly. Code should be self-explanatory. If you need a comment to explain *what* the code is doing, consider refactoring the code to be clearer. Use comments to explain *why* a particular approach was taken, especially if it is non-obvious.

## 4. Architecture Rules

1.  **Dependency Injection**: Components should receive their dependencies (like `ConfigManager`) via their constructors rather than instantiating them internally. This makes unit testing significantly easier.
2.  **Immutability**: Where possible, treat domain models (like `Presentation`) as immutable after the initial parsing phase to prevent unintended side effects later in the pipeline.
3.  **Error Handling**: Catch specific exceptions rather than using bare `except:` clauses. Log all significant errors with appropriate context before re-raising or handling them gracefully.
