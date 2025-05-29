# Configuration

Anknote provides flexible configuration through files, environment variables, and command-line arguments.

## Configuration Files

### Creating a Configuration File

Create a default configuration file:

```bash
anknote --init-config
```

This creates `.anknote.json` in your current directory with default settings:

```json
{
  "model": "gemini/gemini-2.0-flash-lite",
  "max_retries": 3,
  "skip_readme": true,
  "file_extensions": [".md", ".markdown"],
  "output_format": "tsv",
  "escape_tabs": true,
  "log_level": "INFO"
}
```

### Configuration File Locations

Anknote looks for configuration files in this order:

1. **Current directory**: `.anknote.json`
2. **Home directory**: `~/.config/anknote/config.json`
3. **XDG config**: `$XDG_CONFIG_HOME/anknote/config.json`

### Using Custom Configuration

Specify a custom configuration file:

```bash
anknote notes.md --config /path/to/my-config.json
```

View current configuration:

```bash
anknote --show-config
```

## Configuration Options

### AI Model Settings

```json
{
  "model": "gpt-4o-mini",
  "max_retries": 5
}
```

- **model**: AI model identifier (supports LiteLLM format)
- **max_retries**: Maximum API retry attempts

### File Processing Settings

```json
{
  "skip_readme": true,
  "file_extensions": [".md", ".markdown", ".txt"]
}
```

- **skip_readme**: Skip README files when processing directories
- **file_extensions**: File extensions to process

### Output Settings

```json
{
  "output_format": "tsv",
  "escape_tabs": true
}
```

- **output_format**: Output file format (currently only "tsv")
- **escape_tabs**: Escape tab characters in content

### Logging Settings

```json
{
  "log_level": "DEBUG"
}
```

- **log_level**: Logging verbosity (DEBUG, INFO, WARNING, ERROR)

## Environment Variables

Override configuration with environment variables:

```bash
export ANKNOTE_MODEL="claude-3-haiku-20240307"
export ANKNOTE_MAX_RETRIES="10"
export ANKNOTE_LOG_LEVEL="DEBUG"
```

Environment variables take precedence over configuration files.

## Supported AI Models

Anknote uses LiteLLM, supporting many providers:

### OpenAI
```json
{
  "model": "gpt-4o-mini"
}
```

Set API key: `export OPENAI_API_KEY="your-key"`

### Anthropic (Claude)
```json
{
  "model": "claude-3-haiku-20240307"
}
```

Set API key: `export ANTHROPIC_API_KEY="your-key"`

### Google (Gemini)
```json
{
  "model": "gemini/gemini-2.0-flash-lite"
}
```

Set API key: `export GOOGLE_API_KEY="your-key"`

### Azure OpenAI
```json
{
  "model": "azure/gpt-4o-mini"
}
```

Additional Azure environment variables required.

## Configuration Examples

### Cost-Optimized Setup

For minimal costs while maintaining quality:

```json
{
  "model": "gemini/gemini-2.0-flash-lite",
  "max_retries": 3,
  "log_level": "WARNING"
}
```

### High-Quality Setup

For maximum quality flashcards:

```json
{
  "model": "gpt-4o",
  "max_retries": 5,
  "log_level": "INFO"
}
```

### Development Setup

For development and debugging:

```json
{
  "model": "gpt-4o-mini",
  "max_retries": 1,
  "log_level": "DEBUG",
  "skip_readme": false
}
```

### Custom File Types

Process additional file types:

```json
{
  "file_extensions": [".md", ".markdown", ".txt", ".org"],
  "skip_readme": false
}
```

## Advanced Configuration

### Custom Prompts

Use a custom prompt file:

```bash
anknote notes.md --prompt-file my-prompt.txt
```

The prompt file should contain instructions for the AI model on how to generate flashcards.

### Project-Specific Configuration

For different projects, create project-specific configs:

```bash
# Academic project
anknote notes/ --config configs/academic.json

# Work notes
anknote work-notes/ --config configs/work.json
```

### Batch Configuration

For processing multiple directories with different settings:

```bash
#!/bin/bash
anknote academic-notes/ --config academic.json -o anki/academic/
anknote work-notes/ --config work.json -o anki/work/
anknote personal-notes/ --config personal.json -o anki/personal/
```

## Priority Order

Configuration values are applied in this order (highest to lowest priority):

1. **Command-line arguments**
2. **Environment variables**
3. **Configuration file**
4. **Default values**

## Validation

Anknote validates all configuration values:

- Model names are checked for basic format
- Retry counts must be positive integers
- Log levels must be valid Python logging levels
- File extensions must start with a dot

Invalid configurations will show an error message with suggestions for fixing them.
