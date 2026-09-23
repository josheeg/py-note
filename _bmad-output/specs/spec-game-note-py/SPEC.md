---
id: SPEC-game-note-py
companions:
  - ../planning-artifacts/ux-designs/ux-game-note-py-2026-09-22/DESIGN.md
  - ../planning-artifacts/ux-designs/ux-game-note-py-2026-09-22/EXPERIENCE.md
sources:
  - ../planning-artifacts/prds/prd-game-note-py-2026-09-22/prd.md
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# python cli hello world

## Why

A vision to realize, and a proof to capture: a learner (Ada) runs one command,
sees `Hello, World!`, reads the entire program in one sitting, and understands
all of it. This is the first artifact of a note-driven loop — its job is to be
true. A hello world that behaves exactly as documented proves the pipeline that
produced it can be trusted with anything bigger. The canonical hello world,
done properly: invocation, output, exit code — working, tested, explainable.

## Capabilities

- **CAP-1**
  - **intent:** User can run the CLI and receive the canonical greeting.
  - **success:** Bare `uv run python main.py` prints exactly `Hello, World!` + newline on stdout, exit 0, nothing on stderr. (FR-1, UJ-1)
- **CAP-2**
  - **intent:** User can personalize the greeting with `--name`.
  - **success:** `--name Ada` prints exactly `Hello, Ada!`; empty/whitespace values fall back to `World`; repeated flags are last-one-wins; exit 0. (FR-2, UJ-1)
- **CAP-3**
  - **intent:** User can query the program version.
  - **success:** `--version` prints `main.py <version>` on stdout, exit 0, takes precedence over `--name`; version comes from the module-level `__version__` constant. (FR-3)
- **CAP-4**
  - **intent:** User gets well-formed feedback on an unclear invocation.
  - **success:** Unknown flag or missing `--name` value prints argparse `error:` + usage on stderr, exit 2, no traceback; `-h`/`--help` prints usage, exit 0. (FR-4)

## Constraints

- **Zero runtime dependencies** — stdlib `argparse` only; `pytest` is the sole dev dependency. Rules out every framework, color, and packaging option.
- **Flat project** — `[tool.uv] package = false` is non-negotiable (removing it breaks `uv sync`); forces module-level `__version__` constant as the version source (no `importlib.metadata`).
- **Deterministic ASCII output** — no color, ANSI, Unicode, network, or file writes; stdout carries data, stderr carries errors; exit codes are 0 (success) or 2 (bad args) only.
- **Readable in one sitting** — `main.py` stays ~30 lines.
- **Python 3.12+; type hints on every signature; all commands via `uv run`** (never bare `python`/`pytest`/`ruff`).

## Non-goals

- No frameworks (click/typer/rich/colorama) — argparse only.
- No installable package; no PyPI publishing; no console-script entry point.
- No teaching-pack features (`--repeat`, `--caps`, `--lang`, env-var greeting) — each deferred, note-gated (ships only when `note.txt` asks for it).
- No subcommands, no repeated multi-value flags in the name of extensibility.
- No color, decoration, banners, or ASCII art — the output is the output.

## Success signal

`uv run python main.py` prints exactly `Hello, World!` and exits 0; `uv run pytest` is green (golden-string, custom name, version, exit-code assertions); `main.py` is readable in one sitting — Ada can predict behavior (`--version`, empty `--name`, bad flag) before running it.