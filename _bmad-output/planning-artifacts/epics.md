---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
status: final
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-game-note-py-2026-09-22/prd.md
  - _bmad-output/planning-artifacts/architecture/architecture-game-note-py-2026-09-22/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/ux-designs/ux-game-note-py-2026-09-22/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-game-note-py-2026-09-22/EXPERIENCE.md
  - _bmad-output/specs/spec-game-note-py/SPEC.md
---

# game-note-py - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for game-note-py, decomposing the requirements from the PRD, UX Design, Architecture, and the canonical SPEC into implementable stories.

## Requirements Inventory

### Functional Requirements

- FR-1: On bare run (`uv run python main.py`), print exactly `Hello, World!` + newline on stdout, exit 0, nothing on stderr.
- FR-2: On `--name <value>`, print exactly `Hello, <value>!` on stdout, exit 0; empty/whitespace values fall back to `World`; repeated `--name` flags are last-one-wins.
- FR-3: On `--version`, print `main.py <version>` on stdout, exit 0, taking precedence over `--name`; version comes from the module-level `__version__` constant.
- FR-4: On unknown flag or missing `--name` value, print argparse `error:` + usage on stderr and exit 2 with no traceback; on `-h`/`--help`, print usage on stdout and exit 0.

### NonFunctional Requirements

- NFR-1: Zero runtime dependencies — stdlib `argparse` only; `pytest` is the sole dev dependency.
- NFR-2: Flat project — `[tool.uv] package = false` is non-negotiable (removing it breaks `uv sync`); forces module-level `__version__` as the version source.
- NFR-3: Deterministic ASCII output — no color, ANSI, Unicode, network, or file writes; stdout carries data, stderr carries errors; exit codes are 0 (success) or 2 (bad args) only.
- NFR-4: Readable in one sitting — `main.py` stays ~30 lines.
- NFR-5: Python 3.12+; type hints on every function signature; all commands via `uv run` (never bare `python`/`pytest`/`ruff`).
- NFR-6: Portability — runs identically on Windows PowerShell and POSIX shells.

### Additional Requirements

- AR-1: `main.py` is the only production module; no package directory, no importable package (AD-1).
- AR-2: Functional core / imperative shell — `hello(name: str) -> str` is pure (no I/O); greeting canonicalization is exactly `f"Hello, {name.strip() or 'World'}!"`; all I/O (argparse, print, exit codes) lives in `main(argv: list[str] | None = None) -> int` (AD-2).
- AR-3: `argparse` owns all CLI parsing, constructed with `prog="main.py"`; no manual `sys.argv` scanning (AD-3).
- AR-4: Module-level `__version__` is the single version authority, wired to argparse `action="version"` with format `'%(prog)s <version>'` (AD-4).
- AR-5: Success returns 0 with data on stdout only; every error path exits 2 via argparse `SystemExit` with usage on stderr only; no tracebacks escape (AD-5).
- AR-6: Tests colocated in `tests/test_main.py`, capsys-based, never subprocess (AD-2, AD-5).
- AR-7: pytest added as dev dependency via `uv add --dev pytest` at build time (Stack).

### UX Design Requirements

- UX-DR1: Output is the output — exactly one ASCII line per surface; no banners, decoration, color, ANSI, or Unicode anywhere (DESIGN Brand & Style, Do's/Don'ts).
- UX-DR2: Greeting component — exact `Hello, {name}!` on stdout; name = provided value else `World`; empty/whitespace falls back to `World` (DESIGN Components; EXPERIENCE Component Patterns).
- UX-DR3: Version component — `main.py <version>` on stdout via argparse `action="version"`, exits 0, takes precedence over `--name` (DESIGN Components; EXPERIENCE Voice & Tone).
- UX-DR4: Help component — argparse-default usage on stdout, exits 0, no custom branding or ASCII art (DESIGN Components).
- UX-DR5: Error component — argparse `error:` + message + usage hint on stderr, exits 2, no traceback (DESIGN Components; EXPERIENCE State Patterns).
- UX-DR6: One-shot forms — no prompts, no stdin reads, no interactive loop, no waiting (EXPERIENCE Interaction Primitives).
- UX-DR7: Predictable exit codes (0/2) and strict stream separation (data stdout, errors stderr) — scriptable and CI-safe without parsing text (EXPERIENCE Accessibility Floor).

### FR Coverage Map

| Requirement | Epic | Story |
| --- | --- | --- |
| FR-1 | Epic 1 | 1.1 (canonical greeting) |
| FR-2 | Epic 1 | 1.2 (custom `--name`) |
| FR-3 | Epic 1 | 1.3 (`--version`) |
| FR-4 | Epic 1 | 1.4 (errors/help) |
| NFR-1..6 | Epic 1 | 1.1 (zero deps + flat), cross-cutting |
| AR-1..7 | Epic 1 | 1.1 (layout/core-shell/argparse), 1.3 (version source), 1.5 (tests) |
| UX-DR1..7 | Epic 1 | cross-cutting (all stories) |

## Epic List

1. **Epic 1: A faithful, tested hello-world CLI** — deliver `main.py` + `tests/test_main.py` that satisfy every SPEC capability, pinned by the architecture decisions. *(Single epic: the feature altitude and readable-in-one-sitting constraint make one cohesive build the correct decomposition; stories below are ratable work units, not feature silos.)*

---

## Epic 1: A faithful, tested hello-world CLI

**Goal:** Ada runs one command, sees `Hello, World!`, reads the whole program in one sitting, and can predict its behavior before running it — invocation, output, and exit code all working, tested, and explainable. Realizes UJ-1; satisfies SPEC CAP-1..4 under AD-1..AD-5.

**FRs covered:** FR-1, FR-2, FR-3, FR-4
**NFRs:** NFR-1..6 (zero deps, flat project, deterministic ASCII, ~30 lines, type hints/`uv run`, portability)
**Additional:** AR-1..7 (flat layout, core/shell split, argparse-only, version single-source, exit/stream contract, capsys tests, pytest dev dep)
**UX-DRs:** UX-DR1..7 (output-is-the-output, exact components, one-shot forms, exit/stream predictability)

### Story 1.1: Canonical greeting on bare run

As a beginner learner,
I want to run one command and see the canonical `Hello, World!` greeting,
So that I immediately have a working, explainable first artifact.

**Acceptance Criteria:**

**Given** a repository with `uv sync` already run,
**When** I run `uv run python main.py`,
**Then** stdout is exactly `Hello, World!` followed by a newline
**And** the process exits with status 0, nothing is written to stderr.

**Given** the pure/shell split mandated by AD-2,
**When** `hello()` is called with no arguments (default `World`),
**Then** it returns the exact string `"Hello, World!"` without printing or touching `sys`
**And** `main(argv)` is the only place argparse, print, and exit codes live.

**Given** the flat-project constraint (AD-1, NFR-2),
**When** I inspect the project,
**Then** there is no package directory and `[tool.uv] package = false` is preserved
**And** `pytest` is declared as the sole dev dependency (`uv add --dev pytest`).

### Story 1.2: Custom greeting with `--name`

As a beginner learner,
I want to personalize the greeting with `--name <value>`,
So that I learn the flag pattern that makes the CLI mine.

**Acceptance Criteria:**

**Given** a value `Ada`,
**When** I run `uv run python main.py --name Ada`,
**Then** stdout is exactly `Hello, Ada!` followed by a newline, exit 0, nothing on stderr.

**Given** an empty or whitespace-only value (`--name ""` or `--name "   "`),
**When** the program runs,
**Then** the name falls back to `World` and stdout is exactly `Hello, World!` (canonical output preserved).

**Given** repeated `--name` flags,
**When** the program runs,
**Then** the last value wins (single-value semantics, argparse default).

**Given** AD-2 canonicalization,
**When** `hello()` receives a name with surrounding whitespace,
**Then** it strips it and returns `f"Hello, {name.strip() or 'World'}!"` — one deterministic normalization.

### Story 1.3: Version reporting with `--version`

As a beginner learner,
I want to query the program version,
So that I can confirm what I'm running and predict the flag's output before trying it (UJ-1 climax).

**Acceptance Criteria:**

**Given** a module-level `__version__` constant (AD-4 single-source),
**When** I run `uv run python main.py --version`,
**Then** stdout is exactly `main.py <version>` (argparse `action="version"`, format `'%(prog)s <version>'`), exit 0
**And** the version text comes from the constant, never from package metadata (unavailable under flat `package = false`).

**Given** `--version` combined with `--name Ada`,
**When** the program runs,
**Then** the version is printed and the name is ignored (`--version` precedence).

**Given** a capsys test invoking `main(["--version"])`,
**When** the parser output is captured,
**Then** the program name is deterministically `main.py` (parser constructed with `prog="main.py"`, AD-3) — identical in CLI and test contexts.

### Story 1.4: Errors and help

As a beginner learner,
I want well-formed feedback when I mistype or ask for help,
So that the program teaches me the correct usage instead of crashing (FR-4).

**Acceptance Criteria:**

**Given** an unknown flag (`--bogus-flag`),
**When** the program runs,
**Then** an argparse `error:` message plus usage hint is written to stderr, exit status 2, no traceback.

**Given** `--name` with no value,
**When** the program runs,
**Then** argparse reports the missing argument on stderr, exit status 2, no traceback.

**Given** `-h` or `--help`,
**When** the program runs,
**Then** argparse usage + options are written to stdout, exit status 0.

**Given** AD-5's stream contract,
**When** any error path executes,
**Then** data goes to stdout only, errors go to stderr only, and outputs remain deterministic ASCII (UX-DR1, UX-DR5, UX-DR7).

### Story 1.5: Test suite, contract verification, and one-sitting readability

As a beginner learner,
I want the golden strings, exit codes, and edge cases locked by tests,
So that the documented behavior is provably true (SM-1) and the file stays readable (SM-2).

**Acceptance Criteria:**

**Given** the full contract (CAP-1..4),
**When** `uv run pytest` runs,
**Then** all assertions pass: golden string (bare), custom name, empty/whitespace fallback, last-one-wins, `--version` (stdout + exit 0), unknown flag and missing value (stderr + exit 2 via `pytest.raises(SystemExit)`), and help (stdout + exit 0).

**Given** the test strategy pinned by AD-2/AD-5 (AR-6),
**When** tests exercise `main()`,
**Then** they use capsys to capture I/O and `pytest.raises(SystemExit)` for error paths — never `subprocess`.

**Given** SM-2 / NFR-4 / AD-1,
**When** `main.py` is reviewed,
**Then** it is ~30 lines, readable in one sitting, every line explainable without the docs, type hints on all signatures, and `uv run ruff check .` is clean (NFR-5).

**Given** UX-DR1 and UX-DR6,
**When** help and error output are inspected,
**Then** nothing is printed beyond the documented components (no decoration, color, ANSI, or interactive prompts).