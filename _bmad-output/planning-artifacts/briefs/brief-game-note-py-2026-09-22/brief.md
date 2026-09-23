---
title: 'Product Brief: python cli hello world'
status: draft
created: '2026-09-22'
updated: '2026-09-22'
---

# Product Brief: python cli hello world

## Executive Summary

The project exists to turn a note — `a python cli hello world program` — into a
real, runnable artifact through the BMad method pipeline. The first product is a
minimal, zero-dependency Python CLI that prints `Hello, {name}!`, defaulting the
name to `World` so a bare run produces the canonical `Hello, World!`.

This is deliberately the smallest *complete* CLI: invocation, output, exit code.
It serves two masters at once — it is the canonical learning vehicle for Python
CLI development (argparse, entry points, venv, tests, lint), and it is the demo
target of the note-driven loop this repository exists to prove. Every choice
below is made so the barrier to the next iteration stays near zero: when
`note.txt` changes, downstream skills evolve `main.py` off a clean, documented
baseline.

Why now: the idea is seed-worthy but not yet code. A hello world is the
universal first deliverable, and shipping one cleanly is what makes the pipeline
trustworthy before it is asked to carry anything bigger.

## The Problem

`note.txt` holds an idea with no runnable artifact behind it. The repository has
scaffolding, a venv, and a lint/test toolchain, but no program that does
anything. Until `main.py` runs, the pipeline has demonstrated process but not
product.

Who feels this: the human learner who wants one obvious command, one obvious
output, and zero surprises; and the pipeline itself, which needs a concrete,
plan-able surface for the downstream stages (PRD → UX → spec → architecture →
stories). The cost of the status quo is deferred learning and an unproven loop.

## The Solution

A single-file CLI: `uv run python main.py` prints `Hello, World!`; `--name Ada`
prints `Hello, Ada!`; `--version` prints a version and exits 0. Bad arguments
exit 2 (argparse default). Output is ASCII-safe for PowerShell, deterministic,
and free of side effects — no network, no file writes, no color. The
implementation is two functions: a pure `hello(name: str) -> str` and a
`main(argv: list[str] | None = None) -> int` returning the exit code, so tests
run without subprocesses.

The user experiences a tool that behaves exactly as expected, every time —
documented, testable, and explainable in one sitting.

## What Makes This Different

- **Zero dependencies.** Stdlib argparse only; the supply-chain surface is nil
  and the teachable core is unobscured. [ASSUMPTION: no third-party framework
  adds enough value at this scale — confirmed by deep-recon, which found
  Click/Typer are layers *over* argparse, not replacements for it.]
- **Canonical output contract.** `Hello, {name}!` is a golden-string test
  target; empty or whitespace names fall back to `World`, so the bare run is
  always canonical and deterministic.
- **Pure function core.** `hello()`/`main()` split keeps tests fast and
  subprocess-free — the dominant testable-CLI pattern in the ecosystem.
- **Pipeline fidelity.** The product is intentionally boring; its job is to be
  the reliable demo target of the note-driven loop, with extensions gated on
  `note.txt` changing.

## Who This Serves

- **Primary — the human learner.** Wants one obvious command, one obvious
  output, a single clean pattern to absorb (argparse + `main(argv)` + tests).
  Success: runs `uv run python main.py`, sees `Hello, World!`, reads the whole
  program and understands all of it.
- **Secondary — the pipeline.** Downstream skills need a real but tiny surface
  to plan against. Success: the PRD→build stages proceed without re-litigating
  scope decisions already locked here.

## Success Criteria

- Bare run prints exactly `Hello, World!` and exits 0.
- `--name Ada` prints `Hello, Ada!`; empty/whitespace name falls back to `World`.
- `--version` prints a version and exits 0; unknown/bad args exit 2.
- `uv run pytest` passes the 2–3-assertion suite; `uv run ruff check .` is
  clean.
- `main.py` remains readable in one sitting (~30 lines) and extends naturally
  when `note.txt` changes.

## Scope

**In (first version):** stdlib argparse; `--name` (single value, default
`World`, last-one-wins); `--version` via a module-level version constant
(deep-recon resolved the flat-project metadata gap: `package = false` means
`importlib.metadata.version()` cannot work, so the constant is the source of
truth); exit codes 0/2; the pure `hello()`/`main(argv)` structure; 2–3 tests;
ASCII-safe output.

**Explicitly out:** repeated `--name`, `--repeat`, `--caps`, `--lang`, env-var
greetings, color/rich output, PyPI packaging, subcommands. Each is a deferred
teaching-pack option (brainstorm direction C) that enters only when `note.txt`
asks for it. Notably rejected during the forge stage: `sys.argv`-only main (no free
`--help`/`--version`, less teachable) and a positional name argument (breaks the
bare-run canonical output).

## Vision

If this succeeds, the hello world is the first of many deliverables the
note-driven pipeline turns out — the pattern proven on the smallest example,
trusted for larger notes. In the near term it can grow into the teaching pack
(`--lang`, `--repeat`, `--caps`) that demonstrates a menu of Python CLI concepts
as `note.txt` evolves. The meta-goal is a loop the user can point at and say:
*I write the idea; the machine builds and keeps the program in sync.*