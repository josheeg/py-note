---
title: "PRD Addendum: python cli hello world"
created: '2026-09-22'
updated: '2026-09-22'
---

# PRD Addendum

## Rejected alternatives (with rationale)

- **`sys.argv`-only main** — read args manually. Rejected (forge): no free
  `--help`/`--version`, no argparse validation, less teachable; every project
  hand-rolls a different variant. argparse is the stdlib-recommended module.
- **Positional name argument** (`uv run python main.py Ada`) — rejected (forge):
  breaks the bare-run canonical `Hello, World!` contract and teaches a worse
  pattern than an optional flag.
- **Frameworks (Click / Typer / rich / colorama)** — rejected (forge + deep-recon):
  they are layers *over* argparse, add a dependency surface of zero value at this
  scale, and obscure the teachable core. Confirmed by research: Click/Typer are
  alternative APIs atop argparse, not replacements for its mechanism.

## Options considered

- **Version source of truth** — `importlib.metadata.version()` vs module constant.
  Decided: module-level `__version__` constant. Rationale: `[tool.uv] package =
  false` means the project is never installed as a package, so metadata is
  unavailable (research claim [13] documents the friction); the constant is the
  honest single source of truth. Revisit condition: only if the project adopts
  real packaging. Format `%(prog)s <version>` per argparse `_VersionAction`
  (prints to stdout, exits 0, verified against CPython source).
- **`--name` repeated flags** — last-one-wins (argparse default) accepted this
  iteration; multi-greeting is a parked teaching-pack extension.
- **Empty/whitespace `--name`** — explicit fallback to `World` keeps the
  canonical-output contract and the golden-string test stable (forge crack #1).

## Mechanism/transport notes (for architecture)

- Test strategy: pure `hello()` returns the string; `main(argv)` returns the exit
  code — capture via `capsys` + `pytest.raises(SystemExit)`; never spawn a
  subprocess in tests.
- The `--version` argparse action writes to stdout and exits 0 — tests must
  expect `SystemExit(0)` and capture stdout, not assert on return.

## Sizing data

- `main.py` target: ~30 lines. Test file: 2–3 assertions. Dev effort per
  iteration: minutes; governed by pipeline cadence, not calendar.

## In-depth persona

- **Ada (learner)** — primary user. One obvious command, one obvious output, zero
  surprises. Success = run, see `Hello, World!`, read the whole file and
  understand all of it. Windows PowerShell is her likely shell; ASCII-safe output
  is a hard requirement she will never name but will immediately notice if broken.