# Architecture

## Overview

Python Playground is an educational repository designed to showcase Python code, concepts, and projects. The architecture is kept simple and modular to facilitate learning and understanding.

## Project Structure

```
Python-Playground/
├── .github/              # GitHub workflows and templates
│   ├── workflows/        # CI/CD, Pages deployment, releases
│   └── ISSUE_TEMPLATE/   # Issue templates
├── assets/               # GitHub Pages site assets
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript (GitHub API integration)
├── docs/                 # Documentation
├── examples/             # Python example modules
│   ├── basics/           # Variables, control flow, functions, strings
│   ├── data_structures/  # Collections, dataclasses, custom structures
│   ├── algorithms/       # Sorting, searching, recursion
│   ├── patterns/         # Design patterns (creational, behavioral, structural)
│   └── advanced/         # Generators, decorators, context managers, async
├── releases/             # Release notes
├── tests/                # Test suites
│   ├── unit/             # Unit tests for example modules
│   └── integration/      # Integration tests
├── index.html            # GitHub Pages entry point
├── conftest.py           # Pytest configuration
└── pyproject.toml        # Project configuration and tool settings
```

## Design Principles

1. **Educational Focus**: Code examples prioritize clarity and learning over optimization
2. **Modularity**: Each example is self-contained and independently runnable
3. **Documentation**: All code includes docstrings explaining concepts and complexity
4. **Testing**: Every example module has corresponding unit tests
5. **Standards**: Follows PEP 8 via ruff/black, with type hints throughout

## Example Module Structure

Each example file follows a consistent pattern:

- Module docstring explaining the topic
- Related functions/classes with educational docstrings
- Complexity analysis where applicable (algorithms)
- `if __name__ == "__main__"` block for standalone execution

## Technology Stack

- **Language**: Python 3.10+
- **Testing**: pytest with coverage reporting
- **Linting**: Ruff (pycodestyle, pyflakes, isort, bugbear, comprehensions, pyupgrade)
- **Formatting**: Black
- **Type Checking**: MyPy
- **CI/CD**: GitHub Actions (test matrix across Python 3.10, 3.11, 3.12)
- **Site**: GitHub Pages with Prism.js syntax highlighting

## GitHub Pages Site

The interactive site at `index.html` uses the GitHub API to:
- Fetch all `.py` files from the repository tree
- Load file contents on demand with proper UTF-8 decoding
- Display code with Prism.js syntax highlighting
- Support tree/flat view toggle and file search
- Enable one-click code copying

## Contributing to Architecture

When proposing architectural changes:

1. Open an issue for discussion
2. Provide rationale and examples
3. Consider backward compatibility
4. Update this document if changes are accepted
