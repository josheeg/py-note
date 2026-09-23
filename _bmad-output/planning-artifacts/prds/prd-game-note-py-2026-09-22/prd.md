---
title: python cli hello world
created: '2026-09-22'
updated: '2026-09-22'
status: final
---

# PRD: python cli hello world
*Working title — confirm.*

## 0. Document Purpose

This PRD defines the first deliverable of the game-note-py pipeline: a minimal,
zero-dependency Python CLI that prints `Hello, {name}!`. It is for the
downstream workflow owners (UX, architecture, epics, sprint-planning, build) and
for the human learner as the product's primary user. It builds on — and does not
duplicate — the forged idea (`_bmad-output/forge/python-cli-hello-world/`), the
technical research (`_bmad-output/planning-artifacts/research/.../research.md`),
the product brief (`_bmad-output/planning-artifacts/briefs/brief-game-note-py-2026-09-22/brief.md`),
and the PRFAQ (`_bmad-output/planning-artifacts/prfaq-game-note-py.md`, verdict:
forged). Scope decisions locked upstream are repeated here only where readers
need the boundary; the full rationale lives in those documents' memlogs.

## 1. Vision

A learner should be able to run one command, see `Hello, World!`, read the
entire program in a single sitting, and understand all of it. That is the whole
product: the canonical hello world, done properly — invocation, output, and exit
code, all working, all tested, all explainable.

The program also proves the pipeline that produced it: a hello world that
behaves exactly as documented shows the machinery behind it can be trusted with
anything bigger. When `note.txt` changes, `main.py` evolves with it.

## 2. Target User

### 2.1 Jobs To Be Done

- Functional: print a greeting from a terminal with predictable output and exit codes.
- Learning: absorb the complete Python CLI pattern — entry point, argparse, exit codes, tests — from one readable file.
- Contextual: reproducible via `uv run python main.py` on any machine with uv, including Windows PowerShell.
- Meta (for the builder): prove the note-driven pipeline produces a working, tested artifact.

### 2.2 Non-Users (v1)

- Users wanting multi-name, colored, internationalized, or plugin-extensible CLI behavior.
- Users wanting an installable PyPI package with a console-script entry point.

### 2.3 Key User Journeys

- **UJ-1. Ada runs the CLI for the first time.**
  - **Persona + context:** a beginner with a cloned repo and `uv sync` already run.
  - **Entry state:** terminal at project root, no prior interaction.
  - **Path:** types `uv run python main.py` → sees `Hello, World!` → tries `--name Ada` → sees `Hello, Ada!` → reads `main.py` top to bottom.
  - **Climax:** every line of the file has a reason she can name.
  - **Resolution:** she can predict what `--version` and a bad flag will do before running them.
  - **Edge case:** she passes an empty `--name ""` — still gets `Hello, World!`, output stays canonical.

## 3. Glossary

- **CLI** — command-line interface; the program's interaction surface.
- **`--name`** — optional flag accepting a single value; default `World`; empty/whitespace falls back to `World`; repeated flags are last-one-wins (single-value).
- **`--version`** — optional flag printing a version string and exiting 0 (argparse `action="version"`).
- **Canonical output** — the exact string `Hello, {name}!` on stdout; the golden-string test target.
- **Exit code** — process exit status: `0` success, `2` bad arguments (argparse default).
- **`main(argv)`** — function returning the exit code; testable without subprocess.
- **`hello(name)`** — pure function returning the greeting string.

## 4. Features

### 4.1 Command-line Greeting

**Description:** The CLI greets the user by name, defaulting to the canonical
`Hello, World!`. Behavior is deterministic: no network, no file writes, no
color; output ASCII-safe for Windows PowerShell. Realizes UJ-1.

**Functional Requirements:**

#### FR-1: Print canonical greeting on bare run

The user can run `uv run python main.py` and receive `Hello, World!` on stdout
with exit code 0. Realizes UJ-1.

**Consequences (testable):**
- Bare invocation prints exactly `Hello, World!` followed by a newline.
- Process exits with status 0.
- Output is written to stdout, nothing to stderr.

**Out of Scope:**
- Any output beyond the greeting (banners, logos, color).

#### FR-2: Accept a custom name

The user can pass `--name <value>` and receive `Hello, <value>!` on stdout with
exit code 0. Empty or whitespace values fall back to `World`. Realizes UJ-1.

**Consequences (testable):**
- `--name Ada` prints exactly `Hello, Ada!`.
- `--name ""` and `--name "   "` print exactly `Hello, World!`.
- Repeated `--name` flags produce the last value (single-value semantics).

#### FR-3: Report the version

The user can pass `--version` and receive a version string on stdout with exit
code 0. The version comes from a module-level `__version__` constant; `--version`
also takes precedence over any name. Realizes UJ-1.

**Consequences (testable):**
- `--version` prints a non-empty version string (format `%(prog)s <version>`).
- `--version` exits 0.
- `--version --name Ada` prints the version and ignores the name.

**Feature-specific NFRs:**
- The version constant is the single source of truth (flat project: package
  metadata unavailable — see addendum).

#### FR-4: Exit non-zero on bad arguments

The user can pass an unknown flag or malformed arguments and receive exit code 2
(argparse convention), with a usage message on stderr. Realizes UJ-1.

**Consequences (testable):**
- `--bogus-flag` prints a usage/error message to stderr and exits 2.
- No traceback is printed for argument errors.

## 5. Non-Goals (Explicit)

- **Not** a multi-name, repeated-flag, or subcommand CLI in v1.
- **Not** colored, rich, or animated output (no `colorama`, `rich`, `click`, `typer`).
- **Not** an installable package; no PyPI publishing, no console-script entry point.
- **Not** a file-reader, stdin-echo, or farewell variant — the note says hello world.
- **Not** a teaching-pack feature set (`--lang`, `--repeat`, `--caps`, env-var
  greeting) — each is deferred and gated: it ships only when `note.txt` asks for it.

## 6. MVP Scope

### 6.1 In Scope

- stdlib `argparse` CLI; `--name` (single, default `World`); `--version`.
- Pure `hello(name: str) -> str` + `main(argv: list[str] | None = None) -> int`.
- Exit codes 0/2; ASCII-safe, deterministic output.
- 2–3 test assertions (bare run golden string, custom name, version); ruff-clean.
- `main.py` stays ~30 lines, readable in one sitting.

### 6.2 Out of Scope for MVP

- Teaching-pack extensions (`--repeat`, `--caps`, `--lang`, env-var greeting) —
  deferred v2, gated on `note.txt`. *(emotionally load-bearing: they are the
  most-requested next features; flag for revisit if the note evolves)*
- PyPI packaging, color/rich output, subcommands, repeated `--name` — deferred v2+.

## 7. Success Metrics

**Primary**
- **SM-1**: Bare run prints exactly `Hello, World!` and exits 0; `uv run pytest` passes. Validates FR-1, FR-2, FR-3, FR-4.

**Secondary**
- **SM-2**: `main.py` remains ≤ ~30 lines and readable in one sitting (a reviewer can explain every line without the docs). Validates FR-1–FR-4 (scope discipline).

**Counter-metrics (do not optimize)**
- **SM-C1**: Feature count / extensibility breadth — must NOT be maximized; the read-in-one-sitting property is the product, and each added flag erodes it. Counterbalances SM-2.

## 8. Open Questions

1. None blocking. Follow-ups: whether the version string should carry a
   `v` prefix (`v0.1.0` vs `0.1.0`) — decided at build time, one line.
2. Future: whether repeated `--name` joins the teaching pack when the note evolves.

## 9. Assumptions Index

- Inline `[ASSUMPTION]` tags: none manufactured; the stdlib-vs-framework choice
  was confirmed by deep-recon, and the version-source decision by research claim
  [13] + flat-project constraint (see addendum).

---

## Cross-Cutting NFRs

- **Determinism:** identical input → identical output; no network, no file
  writes, no time-dependent behavior. (Drives FR-1–FR-4.)
- **Portability:** runs on Windows PowerShell and POSIX shells via `uv run
  python main.py`; output ASCII-safe. (Drives FR-1.)

## Constraints and Guardrails

- **Dependency policy:** zero runtime dependencies (stdlib only); dev dependency
  on `pytest` remains the sole addition. Flat project — `[tool.uv] package =
  false` must stay (removing it breaks `uv sync`).
- **Tooling:** all commands via `uv run ...`; never bare `python`/`pytest`/`ruff`.

## API Contracts / Public Surface

- **Public surface:** `main.py` CLI only — `uv run python main.py [--name <v>] [--version]`.
- **Breaking-change policy:** v1 scope is a contract; flag-level behavior changes
  (e.g. semantics of a `--name` value, version output format) are breaking until
  v1 is deemed frozen by the note pipeline.

## Versioning and Deprecation Policy

- `__version__` constant increments deliberately on user-visible change; no
  deprecation machinery in v1 (scope too small). Revisit if the teaching pack lands.

## Language / Runtime Targets and Dependency Policy

- Python 3.12+ (project env provisioned at 3.14.3 by uv); stdlib only at runtime.
- type hints on all signatures; `snake_case`, `PascalCase` classes, `UPPER_SNAKE`
  constants; imports grouped stdlib/third-party/local; ruff defaults (line-length 88).