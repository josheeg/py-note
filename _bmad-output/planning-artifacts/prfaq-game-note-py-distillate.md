---
title: "PRFAQ Distillate: game-note-py"
type: llm-distillate
source: "prfaq-game-note-py.md"
created: "2026-09-22"
purpose: "Token-efficient context for downstream PRD creation"
---

# PRFAQ Distillate: game-note-py

## Verified Product Core (locked in forge + brief + research, do not relitigate)

- **Product:** minimal, zero-dependency Python CLI printing `Hello, {name}!`; bare run must print canonical `Hello, World!`.
- **Entry point:** `uv run python main.py`. No importable package (flat project; `[tool.uv] package = false` — do NOT introduce src/ layout).
- **CLI:** stdlib `argparse` only; `--name` single value, default `World`, last-one-wins; `--version` flag via module-level `__version__` constant (flat project means `importlib.metadata.version()` cannot work — constant is the honest source of truth, bumped deliberately, revisit only if real packaging is adopted).
- **Structure:** pure `hello(name: str) -> str` + `main(argv: list[str] | None = None) -> int` returning exit code — tests run without subprocesses (captured via capsys/pytest.raises).
- **Edge behavior:** empty/whitespace `--name` falls back to `World` (keeps output canonical).
- **Exit codes:** `0` success, `2` bad args (argparse default). No color, no network, no file writes; ASCII-safe output (Windows PowerShell default codepage safe).
- **Quality gates:** `uv run pytest` passes (2-3 assertions: bare run golden string, custom --name, --version); `uv run ruff check .` clean; ruff defaults (line length 88, 4-space indent); type hints on every signature; imports grouped stdlib/third-party/local; catch specific exceptions, never bare except.
- **`main.py` should stay ~30 lines / readable in one sitting** — "read-in-one-sitting" is the artifact's core property; scope discipline protects it.

## Rejected Framings (why, for PRD consistency)

- `print("Hello, World!")` one-liner alone — teaches printing only; gives downstream nothing to plan.
- `sys.argv`-only main — no free `--help`/`--version`, not the teachable norm (argparse is stdlib-recommended; Click/Typer are layers on top of argparse, skill transfers upward).
- Positional name argument — breaks the bare-run canonical-output contract.
- Teaching-pack extensions (`--repeat`, `--caps`, `--lang`, env-var greeting, color/rich output, PyPI packaging, repeated `--name`, subcommands) — **all deferred and gated: they ship only when `note.txt` asks for them.** Document as out-of-scope in PRD; do not let them creep in.
- "Humbled Hello World" / "Hello, World!" as press headlines — unclear or self-referential; final headline "Hello, World, Done Properly".

## Requirements Signals

- **Primary user:** human learner — one obvious command, one obvious output, zero surprises, whole file understandable in one sitting.
- **Secondary user:** the planning pipeline itself — needs a real-but-tiny surface to plan against (PRD→build proceeds without relitigating locked scope).
- **Stakes:** this is the pipeline's first real deliverable; it must demonstrably work (tested code, decision trail) to defeat the "process theater" indictment — the next note build is the definitive proof.
- **Windows/PowerShell is first-class**, not an afterthought (ASCII-safe output).
- Golden-string test target: exact `Hello, {name}!` output.
- Version string: seen in `--version` output; format `%(prog)s <version>` argparse `action="version"`; constant `__version__` in main.py.

## Technical Constraints (research-grounded, verified 2026-09-22)

- argparse `_VersionAction` prints to stdout and calls `parser.exit()` → exit code 0 (verified against CPython source).
- Exit convention 0/2/1 per Python docs (0 success, 2 usage error, 1 generic).
- `[tool.uv] package = false` — script-only project; removing breaks `uv sync` (hatchling can't find package dir).
- ruff defaults: line-length 88, indent 4; config-free project (no `[tool.ruff]` block needed).
- Staleness re-check of research claims: 2026-10-01 (version-class claims [2][5][6] earliest).
- `uv run ...` mandatory for all commands (never bare python/pytest/ruff — they miss the venv).

## Resource & Timeline Estimates

- ~30 lines for `main.py`; dev effort negligible for a single iteration (minutes-to-hour scale for an agent build).
- Timeline governed by pipeline iteration cadence (note change → re-run), not a calendar.
- Maintenance burden: near zero by construction (stdlib-only, self-contained, tests alongside).

## Open Questions / Unknowns (non-blocking)

- None blocking. Accepted weakness: single-value `--name` last-one-wins (multi-name extension parked in teaching-pack).
- Version-constant revisit condition: only if project adopts real packaging.

## Verdict Findings (actionable for PRD)

- **Forged in steel:** canonical output contract; zero-dependency constraint; pure hello()/main() testable structure; documented exit codes 0/2; note-gated scope discipline ("say no is the feature").
- **Needs more heat:** teaching-pack extensions intentionally under-specified — keep them that way until note.txt demands.
- **Cracks:** one process-shaped risk (pipeline-theater perception) — evidence-based defense already exists (tested code, decision trail); next note build converts it to demonstrable loop. No launch blockers.
- **Recommended next step (per verdict):** PRD creation using this PRFAQ + distillate; mirror the note-gated out-of-scope discipline in the PRD.