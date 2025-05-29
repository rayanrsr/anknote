# Usage Guide

Anknote is a command-line tool. All examples below show both uvx (recommended) and traditional pip installation usage.

## Prerequisites

Before using Anknote, set up your AI API key:

```bash
# For OpenAI (recommended for beginners)
export OPENAI_API_KEY="your-openai-api-key-here"

# For Anthropic Claude
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"

# For Google Gemini
export GOOGLE_API_KEY="your-google-api-key-here"
```

## Basic Command Line Usage

### Process a Single File

Generate flashcards from a markdown file:

```bash
# Using uvx (recommended)
uvx anknote notes/python-basics.md

# Using pip installation
anknote notes/python-basics.md
```

This creates `python-basics.tsv` in the current directory.

### Process Multiple Files

Process all markdown files in a directory:

```bash
# Using uvx (recommended)
uvx anknote notes/ -o flashcards/

# Using pip installation
anknote notes/ -o flashcards/
```

This processes all `.md` files in `notes/` and saves the output TSV files in `flashcards/`.

## Command Line Options

### Complete Command Syntax

```bash
# uvx syntax
uvx anknote INPUT [OPTIONS]

# pip installation syntax
anknote INPUT [OPTIONS]
```

Where:
- `INPUT`: Path to a markdown file or directory containing markdown files
- `[OPTIONS]`: Optional command line flags (see below)

### Input and Output Options

```bash
# Specify output directory
uvx anknote INPUT -o DIR
uvx anknote INPUT --output DIR

# Save output files next to input files
uvx anknote INPUT --in-place

# Overwrite existing output files
uvx anknote INPUT --force-overwrite
```

**Examples:**

```bash
# Save to specific directory
uvx anknote notes.md -o /path/to/flashcards/

# Process directory and save files in-place
uvx anknote study-materials/ --in-place

# Force overwrite existing files
uvx anknote notes/ -o flashcards/ --force-overwrite
```

### AI Model Configuration

```bash
# Specify AI model
uvx anknote notes.md -m MODEL_NAME
uvx anknote notes.md --model MODEL_NAME

# Set maximum retry attempts
uvx anknote notes.md --max-retries NUMBER
```

**Examples:**

```bash
# Use GPT-4o mini (fast and cost-effective)
uvx anknote notes.md -m gpt-4o-mini

# Use Claude 3 Haiku
uvx anknote notes.md -m claude-3-haiku-20240307

# Use with retries for unreliable connections
uvx anknote notes.md -m gpt-4o-mini --max-retries 5
```

### Logging and Output Control

```bash
# Verbose output (see detailed processing info)
uvx anknote notes.md -v
uvx anknote notes.md --verbose

# Quiet mode (suppress non-error output)
uvx anknote notes.md -q
uvx anknote notes.md --quiet
```

### Configuration Management

```bash
# Create default configuration file
uvx anknote --init-config

# Show current configuration
uvx anknote --show-config

# Use custom configuration file
uvx anknote --config myconfig.json notes.md

# Show help
uvx anknote --help

# Show version
uvx anknote --version
```

## Step-by-Step Examples

### Example 1: First Time User

1. Set up your API key:
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

2. Test with a simple file:
   ```bash
   uvx anknote my-notes.md -v
   ```

3. Check the generated `.tsv` file and import to Anki.

### Example 2: Process Multiple Files

1. Organize your notes in a directory:
   ```
   study-materials/
   ├── biology-chapter1.md
   ├── chemistry-basics.md
   └── physics-motion.md
   ```

2. Process all files:
   ```bash
   uvx anknote study-materials/ -o flashcards/
   ```

3. Find your flashcards in the `flashcards/` directory.

### Example 3: Advanced Configuration

1. Create a configuration file:
   ```bash
   uvx anknote --init-config
   ```

2. Edit `.anknote.json` to customize settings.

3. Process with custom settings:
   ```bash
   uvx anknote notes/ --config .anknote.json -v
   ```

## Real-World Command Examples

### Basic Processing

```bash
# Process a lecture note
uvx anknote "Lecture 1 - Introduction to Psychology.md"

# Process with specific model
uvx anknote lecture-notes.md -m claude-3-haiku-20240307

# Process with custom output location
uvx anknote lecture-notes.md -o ~/anki-imports/
```

### Batch Processing

```bash
# Process entire course directory
uvx anknote "CS101 Notes/" -o "CS101 Flashcards/"

# Process with progress tracking
uvx anknote textbook-chapters/ -o flashcards/ -v

# Process and overwrite existing files
uvx anknote updated-notes/ -o flashcards/ --force-overwrite
```

### Production Usage

```bash
# High reliability processing
uvx anknote important-notes/ \
  -o production-flashcards/ \
  --max-retries 10 \
  --verbose \
  --force-overwrite

# Use custom configuration for specific workflow
uvx anknote research-papers/ \
  --config academic-config.json \
  -o research-flashcards/ \
  -v
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
# Show all available options
uvx anknote --help       # Using uvx
anknote --help           # Using pip installation

# Show version information
uvx anknote --version    # Using uvx
anknote --version        # Using pip installation

# Verbose output for debugging
uvx anknote notes.md -v  # Using uvx
anknote notes.md -v      # Using pip installation

# Show current configuration
uvx anknote --show-config  # Using uvx
anknote --show-config      # Using pip installation
```

### Debugging Commands

If you're having issues, try these diagnostic commands:

```bash
# Check if anknote can run at all
uvx anknote --help

# Test with verbose output on a small file
uvx anknote test-file.md -v

# Check your current configuration
uvx anknote --show-config

# Verify your API key is set
echo $OPENAI_API_KEY  # Should show your key (partially hidden for security)
```

For more help, see the [Configuration Guide](configuration.md) or check the [API Reference](reference/anknote/index.md).
