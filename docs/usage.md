# Usage Guide

## Basic Usage

### Process a Single File

Generate flashcards from a markdown file:

```bash
anknote notes/python-basics.md
```

This creates `python-basics.tsv` in the current directory.

### Process Multiple Files

Process all markdown files in a directory:

```bash
anknote notes/ -o flashcards/
```

This processes all `.md` files in `notes/` and saves the output TSV files in `flashcards/`.

## Command Line Options

### Input and Output

```bash
anknote INPUT [OPTIONS]
```

- `INPUT`: Path to markdown file or directory
- `-o, --output DIR`: Output directory (default: current directory)
- `--in-place`: Save output files next to input files
- `--force-overwrite`: Overwrite existing output files

### AI Model Configuration

```bash
anknote notes.md -m gpt-4o-mini --max-retries 5
```

- `-m, --model`: AI model to use (default: from config)
- `--max-retries`: Maximum retry attempts for API calls

### Logging and Output

```bash
anknote notes.md -v  # Verbose output
anknote notes.md -q  # Quiet mode
```

- `-v, --verbose`: Enable verbose logging
- `-q, --quiet`: Suppress non-error output

### Configuration

```bash
anknote --init-config          # Create default config file
anknote --show-config          # Show current configuration
anknote --config myconfig.json # Use custom config file
```

## Examples

### Basic Processing

```bash
# Process a single file
anknote lecture-notes.md

# Process with custom model
anknote lecture-notes.md -m claude-3-haiku-20240307

# Process with output directory
anknote lecture-notes.md -o /path/to/anki-imports/
```

### Batch Processing

```bash
# Process all markdown files in a directory
anknote study-materials/ -o flashcards/

# Process with overwrite protection
anknote study-materials/ -o flashcards/ --force-overwrite

# In-place processing (save next to source files)
anknote study-materials/ --in-place
```

### Advanced Usage

```bash
# Use custom configuration and verbose output
anknote notes/ --config my-anknote-config.json -v

# Process with custom prompt file
anknote notes.md --prompt-file custom-prompt.txt

# Maximum retries for unreliable connections
anknote notes.md --max-retries 10
```

## Output Format

Anknote generates TSV (Tab-Separated Values) files that can be directly imported into Anki:

```
Question 1	Answer 1
Question 2	Answer 2
Question 3	Answer 3
```

### Importing to Anki

1. Open Anki
2. Go to **File > Import**
3. Select your generated `.tsv` file
4. Configure import settings:
   - **Type**: Basic
   - **Deck**: Choose your target deck
   - **Fields separated by**: Tab
   - **Allow HTML in fields**: Yes (recommended)

## Tips and Best Practices

### Writing Good Notes

For best results, structure your markdown notes clearly:

```markdown
# Main Topic

Brief introduction or overview.

## Subtopic 1

Detailed explanation with key concepts.

### Important Points
- Key fact 1
- Key fact 2
- Key fact 3

## Subtopic 2

More detailed content...
```

### Model Selection

Different models have different strengths:

- **GPT-4o Mini**: Fast and cost-effective for most use cases
- **GPT-4o**: Higher quality but more expensive
- **Claude 3 Haiku**: Fast and good for factual content
- **Gemini Pro**: Good balance of speed and quality

### Processing Large Collections

For large note collections:

1. Use configuration files to avoid repeating arguments
2. Process in batches to avoid rate limits
3. Use `--verbose` to monitor progress
4. Consider using `--max-retries` for reliability

## Troubleshooting

### Common Issues

**No output files generated:**
- Check that your markdown files contain substantial content
- Verify your AI model API key is set correctly
- Use `--verbose` to see detailed processing information

**API errors:**
- Check your API key and quota
- Try a different model
- Increase `--max-retries` for temporary issues

**Empty flashcards:**
- Ensure your notes have clear, factual content
- Try a different AI model
- Check the custom prompt if using one

### Getting Help

```bash
anknote --help  # Show all options
anknote -v      # Verbose output for debugging
```

For more help, see the [Configuration Guide](configuration.md) or check the [API Reference](reference/anknote/index.md).
