# Contributing to Anknote

Thank you for your interest in contributing to Anknote! This guide will help you get started with development.

## Development Setup

### Prerequisites

- Python 3.13 or higher
- Git
- An AI model API key for testing

### Installation

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/anknote.git
cd anknote
```

2. Install development dependencies:
```bash
pip install -e ".[dev,docs]"
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

4. Set up your AI API key:
```bash
export GOOGLE_API_KEY="your-key"  # or your preferred provider
```

## Development Workflow

### Running Tests

Run the full test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=anknote --cov-report=html
```

Run specific tests:
```bash
pytest tests/test_config.py -v
```

### Code Quality

We use several tools to maintain code quality:

- **Ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **pre-commit**: Automated code quality checks

Run quality checks manually:
```bash
ruff check src/ tests/
ruff format src/ tests/
mypy src/
```

### Documentation

Build documentation locally:
```bash
uv run mkdocs serve
```

Build static documentation:
```bash
uv run mkdocs build
```

## Project Structure

```
anknote/
├── src/anknote/          # Main package
│   ├── __init__.py       # Package init and entry point
│   ├── main.py           # CLI interface
│   ├── config.py         # Configuration management
│   └── io/               # I/O modules
│       ├── card.py       # Data models
│       ├── gather.py     # File processing
│       └── write.py      # AI integration and output
├── tests/                # Test suite
├── docs/                 # Documentation
├── examples/             # Example configurations
└── scripts/              # Development scripts
```

## Contributing Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Add docstrings to all public functions and classes
- Keep functions focused and small
- Use descriptive variable and function names

### Testing

- Write tests for all new functionality
- Maintain 100% test coverage
- Use pytest fixtures for common test setup
- Mock external dependencies (AI API calls)

### Documentation

- Update documentation for any user-facing changes
- Include examples in docstrings
- Update the changelog for notable changes

### Commit Messages

We use conventional commit format:

```
feat: add support for custom prompt files
fix: handle empty markdown files gracefully
docs: update installation instructions
test: add tests for configuration loading
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `ci`: CI/CD changes

## Pull Request Process

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes**: Follow the coding guidelines above
3. **Add tests**: Ensure your changes are covered by tests
4. **Update documentation**: Add or update relevant documentation
5. **Run quality checks**: Ensure all checks pass
6. **Commit your changes**: Use conventional commit format
7. **Push and create PR**: Push to your fork and open a pull request

### PR Checklist

- [ ] Tests pass (`pytest`)
- [ ] Code quality checks pass (`ruff check`, `mypy`)
- [ ] Documentation is updated
- [ ] Changelog is updated (if applicable)
- [ ] Commit messages follow conventional format

## Release Process

Releases are automated through GitHub Actions when a new tag is pushed:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create and push a tag: `git tag v1.0.0 && git push origin v1.0.0`

## Getting Help

- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Review the documentation
- Look at the test suite for examples

## Code of Conduct

Please be respectful and inclusive in all interactions. We follow the Python community's code of conduct.
