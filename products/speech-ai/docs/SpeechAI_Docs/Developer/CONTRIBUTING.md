# Contributing Guide

## 1. Welcome

Thank you for your interest in contributing to the Speech AI project. This document outlines the process for submitting contributions, reporting bugs, and proposing new features.

## 2. Reporting Bugs

If you encounter a bug, please ensure you check the existing issue tracker first to avoid duplicates. When opening a new bug report, provide the following information:
-   A clear, descriptive title.
-   The exact steps to reproduce the issue.
-   The expected behavior versus the actual behavior.
-   Relevant logs from the `logs/` directory.
-   The environment details (OS, Python version).

## 3. Proposing Features

We welcome suggestions for new features, especially integrations with new TTS providers or improvements to the text analysis algorithms.
-   Open an issue describing the feature.
-   Explain the use case and why it would be beneficial to the enterprise platform.
-   If proposing a significant architectural change, consider drafting an Architecture Decision Record (ADR) draft for discussion.

## 4. Development Workflow

1.  **Branching Strategy**:
    -   `main`: Represents the stable, production-ready code.
    -   `develop`: The integration branch for the next release.
    -   Feature branches: Create a new branch off `develop` for your work, naming it descriptively (e.g., `feature/azure-tts-integration` or `bugfix/regex-slide-parsing`).

2.  **Making Changes**:
    -   Ensure your code adheres to the guidelines in `CODING_STANDARDS.md`.
    -   Write unit tests for any new logic introduced.
    -   Update relevant documentation (including the Architecture and Developer guides if necessary).

3.  **Committing**:
    -   Write clear, concise commit messages.
    -   Reference any related issue numbers in the commit message.

4.  **Pull Requests**:
    -   Submit a Pull Request (PR) against the `develop` branch.
    -   Ensure all tests pass before requesting a review.
    -   A project maintainer will review the code. Address any feedback provided during the review process. Once approved, the PR will be merged.
