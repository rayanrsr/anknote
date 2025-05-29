# Anknote

# Anknote 📝✨

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/your_username/anknote/actions) <!-- TODO: Replace with actual
build status badge -->

**Anknote is a powerful command-line tool that intelligently generates Anki flashcards from your markdown notes using state-of-the-art AI models.**

Stop manually creating flashcards and let Anknote help you focus on what truly matters: learning and retaining knowledge efficiently.

## Overview

Anknote processes your markdown files (either a single file or an entire directory structure) and leverages AI to identify key concepts, important
information, and insightful questions. It then transforms these into a structured format ready for import into Anki, your favorite spaced repetition
software.

The tool is designed to create flashcards that emphasize understanding and intuition rather than rote memorization of simple facts or definitions.

## Features

*   **AI-Powered Card Generation:** Uses language models via LiteLLM (e.g., Gemini, GPT) to create high-quality flashcards.
*   **Markdown Input:** Accepts individual `.md` files or recursively scans directories for notes.
*   **Anki-Compatible Output:** Generates `.tsv` files that can be directly imported into Anki.
*   **Customizable AI Model:** Easily switch between different AI models supported by LiteLLM.
*   **Selective Processing:** Avoids re-processing notes for which flashcards already exist (unless forced).
*   **In-Place Output:** Option to save generated flashcards alongside your original notes.
*   **Progress Tracking:** Clear progress bar during the generation process.
*   **Focus on Conceptual Understanding:** Prompts are designed to extract non-trivial ideas and conceptual links.

## How It Works

1.  **Input:** You provide a path to a markdown file or a directory containing markdown files.
2.  **Parsing & Retrieval:** Anknote reads your notes. If a directory is provided, it recursively finds all `.md` files.
3.  **AI Processing:** For each note, the content is sent to the configured AI model with a specialized prompt. This prompt guides the AI to extract key
information and formulate question/answer pairs suitable for flashcards.
4.  **Formatting:** The AI's response is parsed into a list of distinct flashcards.
5.  **Output:** The generated flashcards are saved as `.tsv` files (tab-separated values), with each line representing a card (prompt and answer). The
output directory structure mirrors the input structure.
=======
Generate Anki notes with LLMs.

## Installation

```bash
pip install anknote
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync --extra test --extra lint --extra docs

# Run tests
uv run pytest

# Run linting
uv run pre-commit run --all-files
```

## Automatic Versioning and Publishing

This project uses automated versioning and publishing to PyPI based on [Conventional Commits](https://www.conventionalcommits.org/).

### How it works

1. **Commit Format**: Use conventional commit messages:
   - `feat:` for new features (minor version bump)
   - `fix:` for bug fixes (patch version bump)
   - `feat!:` or `fix!:` for breaking changes (major version bump)
   - `docs:`, `style:`, `refactor:`, `test:`, `chore:` for other changes (no version bump)

2. **Automatic Release**: When you push to the main branch:
   - The system analyzes commit messages since the last release
   - Automatically determines the next version number
   - Creates a GitHub release with changelog
   - Publishes the package to PyPI

### Commit Message Examples

```bash
# Patch release (0.1.0 → 0.1.1)
git commit -m "fix: resolve authentication issue"

# Minor release (0.1.0 → 0.2.0)
git commit -m "feat: add new export functionality"

# Major release (0.1.0 → 1.0.0)
git commit -m "feat!: redesign API with breaking changes"

# No release
git commit -m "docs: update README"
git commit -m "test: add unit tests for auth module"
```

### Setting up the commit message template

To use the provided commit message template:

```bash
git config commit.template .gitmessage
```

### Manual Release

You can also trigger a release manually from the GitHub Actions tab using the "Release" workflow.

## PyPI Publishing Setup

The package is automatically published to PyPI using GitHub's trusted publishing feature. No API tokens are required.

### First-time setup on PyPI:

1. Go to [PyPI](https://pypi.org) and create an account
2. Create a new project named `anknote`
3. Go to the project settings and add a "Trusted Publisher"
4. Configure it with:
   - Repository: `your-username/anknote`
   - Workflow: `release.yaml`
   - Environment: `pypi`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
