# Dimension 3 — Implementation reality (uv flat project + ruff + pytest)

**Round 1 — does the forged "flat uv project, zero-deps, ruff-formatted, pytest" stack
hold up in current practice?**

## Claims

- **claim**: `[tool.uv] package = false` in pyproject.toml forces the project package
  *not* to be built and installed into the project environment. uv ignores the declared
  build system when interacting with the project (still respects explicit `uv build`).
  - source: https://docs.astral.sh/uv/concepts/projects/config/
  - publisher: Astral (uv official docs)
  - pub_date: rolling
  - accessed: 2026-09-22
  - confidence: high
  - class: version
- **claim** (verification, empirical): on THIS project, `uv sync` + `uv run python
  main.py` work with `package = false` and no installed distribution — consistent with
  the docs semantics (project scripts run from source, no package importable).
  - source: empirical — this workspace (`uv run python main.py` → `Hello, World!`)
  - publisher: n/a (local run)
  - pub_date: 2026-09-22
  - accessed: 2026-09-22
  - confidence: high
  - class: version
- **claim**: ruff default `line-length` is 88 and default `indent-width` is 4 ("Same as
  Black") — with no `[tool.ruff]` config in pyproject.toml these defaults apply.
  - source: https://docs.astral.sh/ruff/configuration/ (and astral-sh/ruff README,
    "default configuration is equivalent to ... line-length = 88")
  - publisher: Astral (ruff official docs + repo README)
  - pub_date: rolling
  - accessed: 2026-09-22
  - confidence: high
  - class: version
- **claim**: importing `importlib.metadata.version()` to power `--version` only works
  when the package is installed with metadata — which a `package = false` flat project
  is not. The standard fallback for script-only projects is a static version string
  (or a metadata wrapper that only resolves on demand); a small ecosystem exists purely
  to bridge this friction (e.g. `importlib-metadata-argparse-version`).
  - source: https://github.com/mondeja/importlib-metadata-argparse-version (README:
    "safe ... only when --version is passed", raised AttributeError otherwise) +
    https://docs.astral.sh/uv/concepts/projects/config/ (package=false semantics)
  - publisher: GitHub (maintainer README) + Astral docs
  - pub_date: rolling
  - accessed: 2026-09-22
  - confidence: high
  - class: version

## Leads worth chasing
- None material (all three stack claims confirmed primary-source).

## Looked for and not found
- Any evidence that ruff/pytest/uv require configuration beyond defaults for a single-
  file, zero-dependency CLI project; pytest `capsys` fixture is stdlib built-in, no
  plugin needed.