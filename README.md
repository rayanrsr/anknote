# Anknote 📝✨

[![PyPI version](https://badge.fury.io/py/anknote.svg)](https://badge.fury.io/py/anknote)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Anknote is a powerful command-line tool that intelligently generates Anki flashcards from your markdown notes using state-of-the-art AI models.**

Stop manually creating flashcards and let Anknote help you focus on what truly matters: learning and retaining knowledge efficiently.

## Quick Start

### Recommended: Use uvx (uv tool)

```bash
# Run directly without installation
uvx anknote --help

# Process a file
export OPENAI_API_KEY="your-api-key-here"
uvx anknote my-notes.md

# Process a directory
uvx anknote notes/ -o flashcards/
```

### Alternative: Install with pip

```bash
pip install anknote
anknote my-notes.md
```

## Features

- 🤖 **AI-Powered Generation**: Uses LiteLLM to support multiple AI models (OpenAI, Anthropic, Google, etc.)
- 📝 **Markdown Processing**: Automatically processes markdown files and directories
- ⚙️ **Configurable**: Flexible configuration via files, CLI arguments, and environment variables
- 🔄 **Batch Processing**: Process multiple files at once with progress tracking
- 📊 **TSV Output**: Generates Anki-compatible TSV files for easy import
- 🛡️ **Robust**: Built-in error handling, retry logic, and validation

## Command Line Usage

### Basic Commands

```bash
# Set up your API key
export OPENAI_API_KEY="your-api-key-here"

# Process a single file
uvx anknote lecture-notes.md

# Process a directory with output folder
uvx anknote study-materials/ -o flashcards/

# Use different AI model
uvx anknote notes.md -m claude-3-haiku-20240307

# Verbose output for debugging
uvx anknote notes.md -v

# Show help
uvx anknote --help
```

### Real-World Examples

```bash
# Process course materials
uvx anknote "Biology Course/" -o "Biology Flashcards/" -v

# High reliability processing
uvx anknote important-notes/ --max-retries 10 --force-overwrite

# Create configuration file
uvx anknote --init-config
```

## How It Works

1. **Extract Content**: Anknote reads your markdown files and extracts the content
2. **AI Processing**: The content is sent to an AI model with a carefully crafted prompt
3. **Parse Cards**: The AI response is parsed to extract question-answer pairs
4. **Generate TSV**: Cards are saved in Anki-compatible TSV format for import

## Documentation

- [Installation Guide](https://anknote.readthedocs.io/installation/) - Detailed setup instructions
- [Usage Guide](https://anknote.readthedocs.io/usage/) - Complete command-line reference
- [Configuration](https://anknote.readthedocs.io/configuration/) - Customize for your workflow

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

### Commit Message Examples

```bash
# Patch release (0.1.0 → 0.1.1)
git commit -m "fix: resolve authentication issue"

# Minor release (0.1.0 → 0.2.0)
git commit -m "feat: add new export functionality"

# Major release (0.1.0 → 1.0.0)
git commit -m "feat!: redesign API with breaking changes"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
