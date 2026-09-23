---
name: 'game-note-py'
type: architecture-spine
purpose: build-substrate    # build-substrate (default) · discussion · report · deck
altitude: feature           # initiative (keeps features) · feature (keeps epics) · epic (keeps stories)
paradigm: 'functional core / imperative shell: pure hello() core, argparse main() shell'
scope: 'the python cli hello world — main.py and its tests'
status: final               # draft · final
created: '2026-09-22'
updated: '2026-09-22'
binds: []                   # capability / unit IDs governed (from the driving spec; at epic altitude, also the inherited parent AD ids)
sources: []
companions: []
---

# Architecture Spine — game-note-py

## Design Paradigm

Functional core / imperative shell: the pure `hello(name: str) -> str` function is
side-effect-free and deterministic; `main(argv)` is the single I/O boundary —
argparse parsing, printing, and exit codes live only there. This is the smallest
durable shape: it is what makes the CLI testable without subprocesses and keeps
the output contract (CAP-1..4) enforceable by unit test.

## Invariants & Rules

### AD-1 — Single-file flat layout

- **Binds:** all production code
- **Prevents:** introducing a `src/` layout or package dir that breaks `uv sync` (hatchling cannot find a package dir under flat `[tool.uv] package = false`)
- **Rule:** `main.py` is the only production module; no package directory, no importable package.

### AD-2 — Pure core / I/O shell separation

- **Binds:** CAP-1, CAP-2 (greeting behavior); test strategy
- **Prevents:** side effects or output formatting leaking into the pure function; tests forced into subprocess invocation
- **Rule:** `hello(name: str) -> str` performs no I/O, no prints, no `sys` access — it computes and returns the greeting string. Greeting canonicalization is exactly `f"Hello, {name.strip() or 'World'}!"` (strip first; empty/whitespace-after-strip falls back to `World`) — one deterministic normalization. All I/O (argparse, `print`, exit codes) stays inside `main(argv: list[str] | None = None) -> int`.

### AD-3 — argparse owns all CLI parsing

- **Binds:** CAP-1..CAP-4 (all invocation forms)
- **Prevents:** hand-rolled `sys.argv` scanning, divergent parsing implementations, and manual exit-code handling
- **Rule:** `main.py` uses stdlib `argparse` exclusively — the parser is constructed with `prog="main.py"` (deterministic version/usage text in every invocation context, real CLI or capsys test); `--name` (single value, last-one-wins), `--version`, `-h`/`--help`, and error messages/usage all come from argparse. No manual `sys.argv` parsing anywhere.

### AD-4 — Version single-source

- **Binds:** CAP-3
- **Prevents:** `importlib.metadata.version()` attempts (breaks under flat `package = false`) and version-string drift between `--version` output and the constant
- **Rule:** module-level `__version__` constant is the only version authority; wired to argparse `action="version"` with format `'%(prog)s <version>'`. `--version` precedence over `--name` is inherent to argparse.

### AD-5 — Exit-code & stream contract

- **Binds:** CAP-4; MOAT (must-only-allowed-terms) output rules
- **Prevents:** custom exit codes, traceback leaks to the user, and stdout/stderr mixing
- **Rule:** success returns 0 with data on stdout only; every error path exits 2 via argparse `SystemExit` with usage on stderr only; no tracebacks escape. Output is deterministic ASCII — no color, ANSI, Unicode, network, or file writes (print-based output is the permitted CLI exception to logging).

## Consistency Conventions

| Concern | Convention |
| --- | --- |
| Naming (entities, files, interfaces, events) | `hello` (function), `main` (entry), `__version__` (module constant); snake_case per AGENTS.md |
| Code size & structure | `main.py` stays ~30 lines readable in one sitting (SPEC Constraint + SM-2); tests colocated in `tests/test_main.py` |
| Data & formats (ids, dates, error shapes, envelopes) | Greeting canonicalizes per AD-2: `f"Hello, {name.strip() or 'World'}!"` (ASCII); version format `%(prog)s <version>` with parser `prog="main.py"`; error surface = argparse `error:` + usage, stderr |
| State & cross-cutting (mutation, errors, logging, config, auth) | Stateless — no global mutable state, no config files, no env-var reads (env-var greeting is a note-gated non-goal); errors are argparse's, never raised; no logging module (print-only CLI) |

## Stack

| Name | Version |
| --- | --- |
| Python | 3.12+ (venv runs 3.14.3) |
| argparse | stdlib (none — zero runtime deps per SPEC Constraints) |
| pytest | dev dependency, added via `uv add --dev pytest` at build |

## Structural Seed

```text
game-note-py/
  main.py          # hello() + main() + __version__ (the CLI)
  tests/
    test_main.py   # capsys-based tests, never subprocess
  pyproject.toml   # flat, package = false
```

## Capability → Architecture Map

| Capability / Area | Lives in | Governed by |
| --- | --- | --- |
| CAP-1 (canonical greeting) | `main.py` → `hello()` + `main()` print | AD-1, AD-2, AD-3, AD-5 |
| CAP-2 (custom `--name`) | `main.py` → argparse `--name` + `hello()` | AD-2, AD-3 |
| CAP-3 (`--version`) | `main.py` → `__version__` + argparse `action="version"` | AD-3, AD-4 |
| CAP-4 (errors/help, exit 0/2) | `main.py` → argparse error/help paths, `main()` return | AD-3, AD-5 |
| Testability | `tests/test_main.py` (capsys, no subprocess) | AD-2, AD-5 |

## Deferred

- **Repeated `--name` semantics** — argparse default is last-one-wins, already compliant; richer multi-value semantics are note-gated.
- **Teaching pack** (`--repeat`, `--caps`, `--lang`, env-var greeting) — note-gated non-goals; each ships only when `note.txt` asks.
- **Color/decoration, packaging, console-script, subcommands** — locked non-goals per SPEC Non-goals; revisit only via note.txt change.