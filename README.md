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
