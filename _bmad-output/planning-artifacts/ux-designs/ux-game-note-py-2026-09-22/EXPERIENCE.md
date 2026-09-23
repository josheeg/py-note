---
name: python cli hello world
status: final
sources:
  - {planning_artifacts}/prds/prd-game-note-py-2026-09-22/prd.md
updated: '2026-09-22'
---

# EXPERIENCE — python cli hello world

> CLI product. Single surface: the terminal. No GUI form-factor; DESIGN.md
> (visual identity) is intentionally lean — the terminal's defaults are the
> spec. This spine owns the behavioral contract: command shape, output,
> states, and accessibility.

## Foundation

Form-factor is a **single-surface command-line program**, invoked as
`uv run python main.py`. No UI system — the terminal's own conventions
(Windows PowerShell and POSIX shells) are the interaction platform. DESIGN.md
documents the visual discipline; this spine owns how it behaves.

## Information Architecture

| Surface (command form) | Reached from | Purpose |
|---|---|---|
| Bare run | `uv run python main.py` | Canonical greeting — UJ-1 |
| Named run | `--name <value>` | Greeting with a custom name — UJ-1 |
| Version query | `--version` | Report the program version — FR-3 |
| Help | `-h` / `--help` | Usage + option documentation *(argparse default)* |
| Error | unknown flag / malformed args | Explain bad input, exit 2 — FR-4 |

The command has no navigation hierarchy: it is five top-level forms of one
program, each mutually independent. `--version` and `--help` take precedence
over `--name` (argparse action ordering).

→ Composition reference: none — no mocks appropriate for an 80-column stdout
surface. DESIGN.md is the visual spec.

## Voice and Tone

Micropcopy. The brand is "exactly what you asked for, nothing added"
(DESIGN.md.Brand & Style).

| Do | Don't |
|---|---|
| `Hello, World!` | `Hello, world!` / `Greetings, human!` / `Welcome!` |
| `Hello, Ada!` | `Hello Ada!` / `Hi there Ada!!` |
| `main.py 0.1.0` (argparse version format) | `v0.1.0` / fancy version banners |
| usage: `main.py [-h] [--name NAME] [--version]` (argparse) | Custom help prose, taglines |
| error: unrecognized arguments: `--bogus` (argparse, stderr) | "Oops! Something went wrong" / tracebacks |

One voice rule: **the output is the output.** No exclamation beyond the
greeting's own `!`, no encouragement, no decoration. The greeting's `!` is the
only punctuation in the product's vocabulary.

## Component Patterns

Behavioral. Visual rules live in DESIGN.md.Components.

| Component | Use | Behavioral rules |
|---|---|---|
| Greeting | stdout on success | Exactly `Hello, {name}!` + newline. `name` = provided value, else `World`; empty/whitespace falls back to `World`. |
| Version | stdout with `--version` | `main.py <version>` via argparse `action="version"`. Exits 0. Takes precedence over `--name`. |
| Help | stdout with `-h`/`--help` | Argparse defaults. Exits 0. |
| Error | stderr on bad args | Argparse `error:` + message + usage hint. Exits 2. No `main.py` traceback. |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| Success (bare) | stdout | `Hello, World!` — the canonical golden string. Exit 0. |
| Success (named) | stdout | `Hello, {value}!`. Exit 0. |
| Success (empty name) | stdout | `--name ""`/whitespace → falls back to `World`. Exit 0. Output stays canonical. |
| Version requested | stdout | Version line; **climax of UJ-1's learnability** — predicts output without running. Exit 0. |
| Error (unknown flag) | stderr | Argparse error + usage, exit 2. |
| Error (missing value) | stderr | `--name` without value → argparse error + usage, exit 2. |

## Interaction Primitives

- **Single flag, single value:** `--name` accepts exactly one value;
  repeated flags are last-one-wins (argparse default, FR-2).
- **Immediate exit:** every form is one-shot — no prompts, no stdin reads,
  no interactive loop, no waiting.
- **Determinism:** identical inputs → identical stdout, stderr, and exit code.
  No network, no file writes, no time dependence.
- **Banned:** interactive prompts, spinner/progress output, stdin echo,
  color output, and any output that changes between runs.

## Accessibility Floor

Behavioral. Contrast lives in DESIGN.md (no color → no contrast dependency).

- **ASCII-only output** — renders in any terminal, any text-to-speech reader,
  any capture pipeline. Unicode or ANSI escapes would break this.
- **No color dependence** — information is never conveyed by color, bold, or
  blink (none are used at all). Legible on any theme.
- **One line, predictable position** — the greeting is always the sole stdout
  line; screen-reader and automation users always know where the answer is.
- **Predictable exit codes** — 0 success / 2 bad args (argparse); scriptable
  and CI-safe without parsing text.
- **Errors on stderr, data on stdout** — separation preserves pipe/redirect
  correctness (`uv run python main.py > out.txt` captures only the greeting).

## Key Flows

### Flow 1 — Ada learns the CLI by running it (UJ-1)

1. Ada opens a terminal at the project root after `uv sync`.
2. Runs `uv run python main.py`.
3. Sees `Hello, World!` and her shell prompt on the next line.
4. Runs `uv run python main.py --name Ada`.
5. Sees `Hello, Ada!` — the name flag makes sense immediately.
6. Runs `uv run python main.py --version` to confirm the version exists.
7. **Climax:** she can predict, before running them, what `uv run python
   main.py --name ""` (→ `Hello, World!`) and `--bogus` (→ error, exit 2)
   will do. The program is fully learned.

Failure: unknown flag → argparse error on stderr + exit 2; she reads the
usage hint and retries. The failure is the teacher (FR-4, UJ-1).