# Forged Idea: python cli hello world

**Status:** HARDENED
**Source:** note.txt — "a python cli hello world program"
**Forge:** `_bmad-output/forge/python-cli-hello-world/.memlog.md`

## The idea (locked)

A minimal, zero-dependency Python CLI that prints `Hello, {name}!`, defaulting the name to `World` so a bare run prints the canonical `Hello, World!`.

## Locked decisions

- **Entry point:** `uv run python main.py`
- **CLI:** stdlib `argparse`; `--name` (single, default `World`); `--version`
- **Structure:** pure `hello(name: str) -> str` + `main(argv: list[str] | None = None) -> int` returning the exit code — testable without subprocess
- **Edge behavior:** empty/whitespace `--name` falls back to `World`
- **Exit codes:** `0` success, `2` bad args (argparse default)
- **Constraints:** zero runtime dependencies, no color, no network, no file writes, ASCII-safe output (PowerShell-safe)
- **Tests:** bare run → `Hello, World!`; custom `--name`; `--version` prints a version

## Rejected (with reasons)

- `sys.argv`-only main — less teachable, no free `--help`/`--version`
- Positional name argument — breaks the bare-run canonical output contract
- `--repeat`, `--caps`, `--lang`, env-var greeting, colored/rich output, PyPI packaging — deferred to a later teaching-pack iteration (note.txt must change to pull them in)

## Surviving weak points

- `--name` is single-value, last-one-wins; multiple greetings are not supported yet (accepted for now)
- Version string source of truth (hardcoded vs. package metadata) is not pinned for a flat, non-packaged project — decide at build time using the simplest option

## Next

Feed into `@bmad-deep-recon` → `@bmad-product-brief` → `@bmad-prfaq` → `@bmad-prd` → `@bmad-ux` → `@bmad-spec` → `@bmad-architecture` → `@bmad-create-epics-and-stories` → `@bmad-sprint-planning` → `@bmad-build-auto`.