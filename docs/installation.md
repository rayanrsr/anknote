# Installation

## Requirements

- Python 3.13 or higher
- An API key for your chosen AI model (OpenAI, Anthropic, Google, etc.)

## Install from PyPI

The easiest way to install Anknote is from PyPI:

```bash
pip install anknote
```

## Install from Source

For development or to get the latest features:

```bash
git clone https://github.com/rayanramoul/anknote.git
cd anknote
pip install -e .
```

## Development Installation

If you want to contribute to Anknote:

```bash
git clone https://github.com/rayanramoul/anknote.git
cd anknote

# Install with development dependencies
pip install -e ".[dev,docs]"

# Install pre-commit hooks
pre-commit install
```

## Verify Installation

Check that Anknote is installed correctly:

```bash
anknote --version
```

## Set Up AI Model

Anknote uses LiteLLM, which supports many AI providers. Set up your API key:

### OpenAI
```bash
export OPENAI_API_KEY="your-api-key"
```

### Anthropic (Claude)
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### Google (Gemini)
```bash
export GOOGLE_API_KEY="your-api-key"
```

## Configuration

Create a configuration file to customize Anknote:

```bash
anknote --init-config
```

This creates a `.anknote.json` file in your current directory. See the [Configuration Guide](configuration.md) for details.

## Next Steps

- [Usage Guide](usage.md) - Learn how to use Anknote
- [Configuration](configuration.md) - Customize your setup
