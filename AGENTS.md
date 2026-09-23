# AGENTS.md - Development Guidelines for AI Agents

Last Updated: 2026-09-22

## Project Overview

This is a note-driven Python CLI project. The workflow is:

1. `note.txt` holds the current project idea (its contents change over time).
2. The BMad method pipeline (`@bmad-*` skills) processes the idea in `note.txt`
   into planning documents (PRD, UX, spec, architecture, epics, sprint).
3. `main.py` is the actual CLI program that gets built and evolved from those plans.

## Build & Test Commands

```bash
# Create/refresh the virtual environment
uv sync

# Run the CLI
uv run python main.py

# Run with arguments
uv run python main.py --name "Ada"

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Regenerate the project scaffold from scratch
uv run python scaffold.py
```

## Code Style Guidelines

- **Type Hints**: Always use type hints for function signatures and variables
- **Naming**:
  - `snake_case` for functions, variables, and modules
  - `PascalCase` for classes
  - `CONSTANTS` for module-level constants
- **Imports**: Group by standard library / third-party / local
- **Formatting**: Follow ruff defaults (line length 88, indent 4 spaces)
- **Error Handling**: Never use bare `except:` - catch specific exceptions
- **No Type Suppression**: Never use `as any`, `@ts-ignore`, or similar

## Project Structure

```
game-note-py/
├── main.py          # The CLI program
├── scaffold.py      # Script that regenerates the project scaffold files
├── note.txt         # The current project idea (drives the BMad pipeline)
├── pyproject.toml   # uv project config
├── AGENTS.md        # Agent guidelines (this file)
├── README.md
└── .venv/           # Virtual environment (for AI agents and tooling)
```

## Working with the Note-Driven Workflow

- When the user changes `note.txt`, re-run the BMad pipeline to refresh the plans.
- Keep planning documents in sync with the current `note.txt` contents.
- `main.py` should always reflect the latest agreed-upon plan for the CLI.

## Error Handling

1. **Specific Exceptions**: Catch specific exceptions, never bare `except:`
2. **Log Errors**: Use proper logging, not print statements (except in the CLI entry point)
3. **Graceful Degradation**: Handle errors without crashing
4. **User Feedback**: Show meaningful error messages to users
