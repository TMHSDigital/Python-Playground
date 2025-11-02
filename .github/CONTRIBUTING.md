# Contributing to Python Playground

Thank you for your interest in contributing to Python Playground! This document provides guidelines and instructions for contributing.

## How to Contribute

We welcome contributions of all kinds:

- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation
- Adding code examples and tutorials

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Python-Playground.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add: your feature description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines:

- Use 4 spaces for indentation
- Maximum line length: 88 characters (enforced by Black)
- Use descriptive variable and function names
- Add docstrings to functions and classes

### Tools

We use the following tools to maintain code quality:

- **Ruff**: Linting and import sorting
- **Black**: Code formatting
- **MyPy**: Type checking (optional but encouraged)

### Running Linters and Formatters

Before submitting a PR, ensure your code passes all checks:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run linter
ruff check .

# Format code
black .

# Type checking (optional)
mypy .
```

## Testing Requirements

### Test Structure

- Unit tests go in `tests/unit/`
- Integration tests go in `tests/integration/`
- Test files should be named `test_*.py` or `*_test.py`

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/unit/test_example.py
```

### Writing Tests

- Write tests for new features
- Ensure tests are isolated and independent
- Use descriptive test names: `test_function_name_scenario_expected_result`
- Aim for good test coverage

## Pull Request Process

1. **Update Documentation**: If you're adding features, update relevant documentation
2. **Add Tests**: Ensure new code has appropriate test coverage
3. **Update CHANGELOG**: Add entries to `CHANGELOG.md` under `[Unreleased]`
4. **Check CI**: Ensure all CI checks pass
5. **Squash Commits**: Keep commits focused and meaningful

### PR Checklist

- [ ] Tests added/updated
- [ ] Lint passes locally (`ruff check .`)
- [ ] Formatting passes locally (`black .`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or breaking changes documented)

## Commit Messages

Use clear, descriptive commit messages:

- **Format**: `Type: Brief description`
- **Types**: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`, `Test`
- **Example**: `Add: Fibonacci sequence example with tests`

## Documentation

- Code examples should include docstrings
- Update README.md if adding major features
- Add documentation to `docs/` for complex concepts
- Keep comments clear and concise

## Code Review

- All PRs require review before merging
- Be respectful and constructive in reviews
- Address review comments promptly
- Ask questions if something is unclear

## Questions?

If you have questions about contributing, please:

- Open an issue with the `question` label
- Check existing issues and discussions
- Review the documentation in `docs/`

Thank you for contributing to Python Playground! 🐍

