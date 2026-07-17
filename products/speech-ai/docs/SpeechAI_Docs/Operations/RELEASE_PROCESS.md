# Release Process

## 1. Introduction

This document details the standard procedure for releasing new versions of the Speech AI platform. It ensures that deployments are consistent, tested, and documented.

## 2. Pre-Release Checklist

Before a release candidate is finalized, the following steps must be completed:

1.  **Code Freeze**: A code freeze is enacted on the `develop` branch. Only critical bug fixes are permitted.
2.  **Testing**: All unit and integration tests must pass successfully.
3.  **Documentation Update**: Ensure that the `CHANGELOG.md` is updated with all notable changes for the upcoming release. Verify that the `ROADMAP.md` and any relevant architectural documents accurately reflect the new state of the system.
4.  **Version Bump**: Update the `version` field in `config/settings.json` to reflect the new semantic version (e.g., from `1.0.0` to `1.1.0`).

## 3. Release Execution

1.  **Merge to Main**: Create a Pull Request from `develop` to the `main` branch.
2.  **Tagging**: Once merged, create a Git tag on the `main` branch corresponding to the new version number (e.g., `v1.1.0`).
3.  **Artifact Generation**: Create a release package containing the source code, configuration files, and documentation.
4.  **Deployment**: Deploy the new release package to the target production servers following the instructions in the `OPERATIONS_GUIDE.md`.

## 4. Post-Release

1.  **Verification**: Perform a smoke test in the production environment by running a standard input script through the pipeline to ensure the system is functioning correctly.
2.  **Monitoring**: Closely monitor the `app.log` file for any unexpected errors or performance degradation following the deployment.
3.  **Communication**: Notify stakeholders that the new version has been successfully deployed and highlight the key features introduced.
