# query-watch

A lightweight Python library to observe, analyze, and report SQL queries executed by ORM frameworks


## Status

🚧 **In Development** - This project is currently under active development.


## Development

### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to ensure code quality. The hooks run automatically on every commit and include:

- **Ruff**: Linting and code formatting (replaces flake8 and black)
- **mypy**: Static type checking

To set up the pre-commit hooks:

```bash
pre-commit install
```

To manually run all hooks:

```bash
pre-commit run --all-files
```
