# Contributing to Anknote

Thank you for your interest in contributing to Anknote! This guide will help you get started.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/anknote.git
   cd anknote
   ```

2. **Install dependencies**:
   ```bash
   uv sync --extra test --extra lint --extra docs
   ```

3. **Set up git for conventional commits**:
   ```bash
   ./scripts/setup-git.sh
   ```

## Development Workflow

### 1. Conventional Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning. Your commit messages should follow this format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature (triggers minor version bump)
- `fix`: A bug fix (triggers patch version bump)
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to our CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files

**Breaking Changes:**
Add `!` after the type or add `BREAKING CHANGE:` in the footer to trigger a major version bump:
```bash
feat!: redesign API with breaking changes
# or
feat: add new API

BREAKING CHANGE: The old API is no longer supported
```

### 2. Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure they follow the project standards:
   ```bash
   # Run tests
   uv run pytest

   # Run linting
   uv run pre-commit run --all-files
   ```

3. **Commit your changes** using conventional commits:
   ```bash
   git add .
   git commit -m "feat: add your new feature"
   ```

4. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

### 3. Automatic Releases

When your PR is merged to the main branch:

1. **GitHub Actions** will automatically:
   - Run all tests
   - Analyze commit messages since the last release
   - Determine the next version number based on conventional commits
   - Update version in `pyproject.toml` and `src/anknote/__init__.py`
   - Generate a changelog
   - Create a GitHub release
   - Publish the package to PyPI

2. **Version Bumping Rules**:
   - `fix:` commits → patch version (0.1.0 → 0.1.1)
   - `feat:` commits → minor version (0.1.0 → 0.2.0)
   - Breaking changes → major version (0.1.0 → 1.0.0)
   - Other commits → no version bump

## Testing

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=anknote

# Run specific test file
uv run pytest tests/test_main.py
```

## Code Quality

This project uses several tools to maintain code quality:

```bash
# Run all pre-commit hooks
uv run pre-commit run --all-files

# Run type checking
uv run mypy src/

# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/
```

## Documentation

```bash
# Build documentation locally
uv run mkdocs serve

# Build documentation for production
uv run mkdocs build
```

## Release Process

Releases are fully automated, but you can also trigger a manual release:

1. Go to the GitHub Actions tab
2. Select the "Release" workflow
3. Click "Run workflow"
4. Choose the branch (usually main)
5. Click "Run workflow"

## Questions?

If you have any questions about the development process, feel free to:
- Open an issue for discussion
- Check existing issues and discussions
- Review the README.md for additional information
