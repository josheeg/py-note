"""Regenerate the project scaffold files.

This script creates the same files that make up the scaffold:

- pyproject.toml   (uv project config)
- main.py          (the CLI program)
- AGENTS.md        (AI agent guidelines)
- README.md        (project readme)
- note.txt         (the current project idea, drives the BMad pipeline)

Run it with:

    uv run python scaffold.py

It is idempotent: re-running it overwrites the scaffold files with the
canonical contents, so the project can always be rebuilt from scratch.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent

FILES: dict[str, str] = {
    "pyproject.toml": """\
[project]
name = "game-note-py"
version = "0.1.0"
description = "A Python CLI hello world program."
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
package = false

[dependency-groups]
dev = [
    "pytest>=9.1.1",
]
""",
    "main.py": """\
\"\"\"A Python CLI hello world program.\"\"\"

import argparse

__version__ = "0.1.0"


def hello(name: str) -> str:
    \"\"\"Return a greeting for name, stripping whitespace and falling back to World when empty.\"\"\"
    return f"Hello, {name.strip() or 'World'}!"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument("--name", default="World", help="Name to greet")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    args = parser.parse_args(argv)
    print(hello(args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    "AGENTS.md": """\
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
""",
    "README.md": """\
# game-note-py

A note-driven Python CLI project. The idea in `note.txt` drives the BMad method
pipeline (`@bmad-*` skills), which produces planning documents that guide the
evolution of `main.py`.

## Quick Start

```bash
# Set up the virtual environment
uv sync

# Run the CLI
uv run python main.py
# → Hello, World!

uv run python main.py --name "Ada"
# → Hello, Ada!

# Regenerate the scaffold
uv run python scaffold.py
```

## How It Works

1. Put your project idea in `note.txt` (e.g. `a python cli hello world program`).
2. Run the BMad pipeline on the note contents:
   `@bmad-project-context → @bmad-brainstorming → @bmad-forge-idea → @bmad-deep-recon → @bmad-product-brief → @bmad-prfaq → @bmad-prd → @bmad-ux → @bmad-spec → @bmad-architecture → @bmad-create-epics-and-stories → @bmad-sprint-planning → @bmad-build-auto`
3. `main.py` gets built from the resulting plans.

## Project Structure

```
├── main.py          # The CLI program
├── scaffold.py      # Script that regenerates the project scaffold files
├── note.txt         # The current project idea
├── pyproject.toml   # uv project config
├── AGENTS.md        # AI agent guidelines
└── README.md
```
""",
}

NOTE_DEFAULT = "a python cli hello world program\n"


def write_scaffold_files() -> None:
    """Write every scaffold file to disk, overwriting existing contents."""
    for name, contents in FILES.items():
        path = ROOT / name
        path.write_text(contents, encoding="utf-8")
        print(f"  wrote {name}")

    note_path = ROOT / "note.txt"
    if not note_path.exists():
        note_path.write_text(NOTE_DEFAULT, encoding="utf-8")
        print(f"  wrote {note_path.name}")
    else:
        print(f"  kept existing {note_path.name}")


def main() -> None:
    print(f"Regenerating scaffold in {ROOT}")
    write_scaffold_files()
    print("Done.")


if __name__ == "__main__":
    main()