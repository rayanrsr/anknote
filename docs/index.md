# Anknote

[![PyPI version](https://badge.fury.io/py/anknote.svg)](https://badge.fury.io/py/anknote)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Anknote is a command-line tool that automatically generates Anki flashcards from your markdown notes using AI models. Transform your study materials into effective spaced repetition cards with minimal effort.

## Features

- 🤖 **AI-Powered Generation**: Uses LiteLLM to support multiple AI models (OpenAI, Anthropic, Google, etc.)
- 📝 **Markdown Processing**: Automatically processes markdown files and directories
- ⚙️ **Configurable**: Flexible configuration via files, CLI arguments, and environment variables
- 🔄 **Batch Processing**: Process multiple files at once with progress tracking
- 📊 **TSV Output**: Generates Anki-compatible TSV files for easy import
- 🛡️ **Robust**: Built-in error handling, retry logic, and validation
- 🧪 **Well-Tested**: Comprehensive test suite with 100% coverage

## Quick Start

Install Anknote:

```bash
pip install anknote
```

Generate flashcards from a markdown file:

```bash
anknote my-notes.md
```

Process an entire directory:

```bash
anknote notes/ -o flashcards/
```

## How It Works

1. **Extract Content**: Anknote reads your markdown files and extracts the content
2. **AI Processing**: The content is sent to an AI model with a carefully crafted prompt
3. **Parse Cards**: The AI response is parsed to extract question-answer pairs
4. **Generate TSV**: Cards are saved in Anki-compatible TSV format for import

## Example

Given a markdown file like this:

```markdown
# Python Basics

Python is a high-level programming language. It was created by Guido van Rossum
and released in 1991. Python emphasizes code readability and uses significant
indentation.

## Key Features
- Interpreted language
- Dynamic typing
- Object-oriented programming
```

Anknote generates flashcards like:

- **Q**: What is Python? **A**: A high-level programming language created by Guido van Rossum
- **Q**: When was Python released? **A**: 1991
- **Q**: What does Python emphasize? **A**: Code readability and uses significant indentation

## Next Steps

- [Installation Guide](installation.md) - Detailed installation instructions
- [Usage Guide](usage.md) - Learn all the command-line options
- [Configuration](configuration.md) - Customize Anknote for your workflow
- [API Reference](reference/anknote/index.md) - Complete API documentation
