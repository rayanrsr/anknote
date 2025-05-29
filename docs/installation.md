# Installation

## Requirements

- Python 3.13 or higher (uvx handles this automatically)
- An API key for your chosen AI model (OpenAI, Anthropic, Google, etc.)

## Recommended: Use uvx (uv tool)

**uvx is the recommended way to use Anknote.** It provides an isolated environment and handles dependencies automatically.

### Install uv first

If you don't have uv installed:

```bash
# On Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Use Anknote with uvx

Run Anknote directly without permanent installation:

```bash
# Show help
uvx anknote --help

# Process a file
uvx anknote my-notes.md

# Process a directory with options
uvx anknote notes/ -o flashcards/ -v
```

**Benefits of uvx:**
- No conflicts with other Python packages
- Always uses the latest version
- Automatic dependency management
- No need to manage virtual environments

## Alternative: Install from PyPI

If you prefer traditional installation:

```bash
pip install anknote
```

Then use it directly:

```bash
anknote my-notes.md
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
