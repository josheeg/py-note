---
title: 'Technical research: python cli hello world'
type: 'technical'
topic: 'python cli hello world'
decision: 'Confirm the forged Minimal+ CLI spec (argparse, --name default World, --version, zero deps, pure-function structure, flat uv project) against current Python CLI practice'
source: 'deep-recon native run'
status: complete
preset: 'standard'
validation: 'normal'
claims_verified: 6
claims_unverified: 0
created: '2026-09-22'
updated: '2026-09-22'
---

# Technical research: python cli hello world

**Decision this research serves:** Confirm the forged Minimal+ CLI spec (argparse, `--name` default World, `--version`, zero deps, pure-function structure, flat uv project) against current Python CLI practice.

## Executive summary

**Verdict: the forged Minimal+ spec is confirmed in every particular — adopt as-is.**
None of the three research dimensions produced a reason to change the spec; two
dimensions added positive confirmation, one resolved the only flagged weak point.

Three findings drive this:

1. **argparse is the current baseline for simple Python CLIs, not a legacy choice.**
   Official docs recommend it as the default stdlib module for basic CLIs [1], the
   mainstream frameworks (Click, Typer) are built *on top of* it [8], and it keeps
   improving (better errors in 3.12, colorized help in 3.14) [9]. The only
   "never argparse" source found is a low-confidence April-2026 blog written in a
   marketing register, targeting feature-heavy CLIs [10].
2. **The forged structure is the ecosystem's dominant testable pattern.** A pure
   `hello(name)` + `main(argv=None)` with capsys/SystemExit tests is the norm [4];
   `--version` via `action='version'` prints to stdout and exits 0 [2]; bad args exit
   2 per both argparse behavior and Unix convention [3].
3. **The flat project's `--version` needs a static constant — confirmed inherent.**
   `package = false` means no installed metadata, so `importlib.metadata.version()`
   cannot work [5][13]. The forge's one surviving weak point ("version source of truth
   unwedged") is resolved: a module-level `__version__` constant; it can switch to
   metadata only if the project later becomes a package.

Biggest caveat: research validated the *shape* against current practice, not the
product decision itself — that rests on the forge and note scope. Recommendations
binding downstream: architecture spine (argparse constraint, `__version__` source of
truth, testability contract), PRD input (exit-code contract), brief (feasibility: zero
runtime deps confirmed).

---

## 1. Argument parsing landscape & maturity

**Claim [1] (verified, high):** argparse is the stdlib-default recommended module for
implementing basic command-line applications; the official library reference calls it
"the default recommended standard library module for implementing basic command line
applications" and defers broader choices to a "Choosing an argument parsing library"
guide [1]. The official tutorial is likewise introduced as "the recommended
command-line parsing module" [7].

**Claim [1]-supporting (high):** argparse is not a niche choice — mainstream
third-party frameworks stack *on top of it*: Typer's own docs situate Click/Typer as
higher-level layers over argparse rather than replacements [8]. A single low-trust
counterpoint ([10], personal blog, marketing register) argues "never use argparse for
new greenfield projects" in favor of Typer; it is the only source found taking that
stance and is outweighed by the official-docs position for a two-flag greeting CLI.

**Ecosystem note (medium):** argparse is actively maintained, not frozen — Python 3.12
improved its error messages and 3.14 colorizes help/error output with suggestions [9].
Not load-bearing for the decision; no ledger claim.

## 2. Architecture patterns in practice

**Claim [2] (verified, high):** the canonical `--version` implementation is argparse's
built-in `version` action with a `version=` string supporting `%(prog)s` substitution:
`parser.add_argument('--version', action='version', version='%(prog)s 2.0')` prints to
**stdout** and exits **0** — confirmed in the CPython source where `_VersionAction`
writes to `_sys.stdout` and calls `parser.exit()` [2]. Empirical check: the same
mechanics hold in this workspace's Python 3.14 runtime [14].

**Claim [3] (verified, high):** exit-code convention that argparse follows: 0 =
success; **2 = command-line syntax errors**; 1 = all other errors — restated by the
official `sys` docs [3]. `--version` (a successful path) therefore exits 0, while bad
arguments exit 2; both are testable assertions.

**Claim [4] (verified, high):** the dominant testable-CLI pattern is a `main(argv=None)`
function that builds the parser internally and parses the provided argv, tested with
`capsys` plus `pytest.raises(SystemExit)` [4]. The alternative — monkeypatching
`sys.argv` before invoking the entry point — exists but mutates global state and is
the weaker pattern [11]. This directly validates the forged pure-function structure
(`hello(name: str) -> str` + `main(argv: list[str] | None = None) -> int`).

## 3. Implementation reality: uv flat project + ruff + pytest

**Claim [5] (verified, high):** with `[tool.uv] package = false` (as in this project's
pyproject.toml), the project package is *not* built or installed into the environment,
so `importlib.metadata.version()` can never resolve for this project [5]. Consequently the
forged `--version` must use a static version string — the standard pattern for
script-only projects, and precisely the friction the `importlib-metadata-argparse-version`
ecosystem solves for *installed* packages [13]. The forge's "version string source of
truth unwedged for flat project" weak point is therefore resolved: a module constant.

**Claim [6] (verified, high):** ruff defaults with no `[tool.ruff]` section are
`line-length = 88`, `indent-width = 4` ("Same as Black") [6][12] — matching the
project's existing convention and the forged spec. `capsys`/`SystemExit` pattern needs
no plugin; pytest is a dev-only dependency, consistent with zero runtime deps.

## Cross-dimension insights

- **The decision's core verdict is over-determined.** All three dimensions point the
  same way: argparse is the baseline the ecosystem builds on [1][8], the testable
  `main(argv)` shape is the norm [4], and the flat-uv constraint forces the exact
  `--version` design the forge already locked (static string) [5]. No dimension
  produced a reason to deviate from the Minimal+ spec.
- **The only churn is one layer up.** The stdlib base is stable and improving [9];
  the framework competition (Click vs Typer) lives above argparse and is irrelevant to
  a two-flag greeting CLI [8][10].
- **Version-metadata friction is the one real constraint discovered.** The forge flagged
  "version-string source of truth unwedged" as a surviving weak point; research confirms
  it is *inherent* to `package = false` — there is no installed metadata to read from
  [5][13]. Resolution: module-level constant, trivially testable.

## Contrary evidence

Red-team pass was off for this run (`validation: normal`, `red_team: off`), so no
adversarial hunt ran. One counter-claim surfaced during acquisition and is carried here
for transparency: a personal blog (April 2026, written in a marketing register) argues
"never use
argparse for new greenfield projects" in favor of Typer/Click [10]. Weighed against the
official docs' recommendation [1], the ecosystem base-layer fact [8], and this
decision's scope (two flags, zero deps), it does not survive — recorded as low
confidence in the appendix and reflected in Recommendation 1's "at this scale" qualifier.

## Recommendations

Each bound to the confirmed decision downstream, with the confidence basis named:

1. **Keep argparse, stdlib only** — confirmed idiomatic for a hello-world-grade CLI;
   third-party frameworks are overhead at this scale [1][8][10]. **Confidence: high.**
2. **`--version` via `action='version'` with a module-level `__version__` constant** —
   prints to stdout, exits 0, works in a flat non-installed project (the only viable
   source of truth under `package = false`) [2][5][13]. **Confidence: high.** Feeds:
   architecture spine (constraint on source-of-truth), PRD input.
3. **`main(argv: list[str] | None = None) -> int` + pure `hello(name)` + capsys tests** —
   the dominant testable pattern; `pytest.raises(SystemExit)` asserts exit codes
   [4][11]. **Confidence: high.** Feeds: architecture spine, implementation.
4. **Exit 0 on success (incl. `--version`/`--help`); exit 2 on bad args** — argparse
   native behavior matching the sys-docs convention [2][3]. **Confidence: high.**
   Feeds: PRD input.
5. **Zero runtime deps; pytest as the only dev dependency** — no plugin needed for
   capsys [4]. **Confidence: high.** Feeds: brief (feasibility).
6. **Keep ruff defaults (line-length 88)** — already the repo convention, confirmed the
   ruff default [6][12]. **Confidence: high.** Feeds: architecture constraint.

## Open questions

- **When does the flat project graduate from a `__version__` constant?** If the note
  grows the project to a distributable package, the metadata source of truth changes
  (`importlib.metadata.version()` becomes available); the constant remains the right
  answer until then [5][13]. Not blocking — tracked for the architecture step.
- **Where the argparse ergonomics ceiling sits** for this codebase — nothing in this
  run's scope suggests subcommands/groups are coming; if the CLI grows past a few
  flags and commands, Click/Typer re-enters the tradeoff [8][10]. Flagged as a
  roadmap risk, not a present requirement.

## Source appendix

| [1] | argparse is the default recommended stdlib CLI module; `--version` action docs | [docs.python.org/3/library/argparse.html](https://docs.python.org/3/library/argparse.html) | Python Software Foundation | rolling (live docs) | 2026-09-22 | high |
| [2] | `_VersionAction`: stdout + `parser.exit()` (exit 0) | [CPython Lib/argparse.py](https://github.com/python/cpython/blob/main/Lib/argparse.py) | CPython (source of record) | rolling (main) | 2026-09-22 | high |
| [3] | Exit-code convention: 2 for CLI syntax errors | [docs.python.org/3/library/sys.html](https://docs.python.org/3/library/sys.html) | Python Software Foundation | rolling | 2026-09-22 | high |
| [4] | capsys + `main(args)` + SystemExit test pattern | [til.simonwillison.net/pytest/pytest-argparse](https://til.simonwillison.net/pytest/pytest-argparse) | Simon Willison (TIL) | 2022-01-08 | 2026-09-22 | high |
| [5] | `package = false`: project not built/installed | [docs.astral.sh/uv/concepts/projects/config/](https://docs.astral.sh/uv/concepts/projects/config/) | Astral (uv docs) | rolling | 2026-09-22 | high |
| [6] | ruff defaults: line-length 88, indent-width 4 | [docs.astral.sh/ruff/configuration/](https://docs.astral.sh/ruff/configuration/) | Astral (ruff docs) | rolling | 2026-09-22 | high |
| [7] | argparse tutorial: "recommended command-line parsing module" | [docs.python.org/3/howto/argparse.html](https://docs.python.org/3/howto/argparse.html) | Python Software Foundation | rolling | 2026-09-22 | high |
| [8] | Click/Typer built on top of argparse | [typer.tiangolo.com/alternatives/](https://typer.tiangolo.com/alternatives/) | Typer project (official docs) | rolling | 2026-09-22 | high |
| [9] | Python 3.12/3.14 argparse error-message/color improvements | [docs.python.org/3.14/whatsnew/3.14.html](https://docs.python.org/3.14/whatsnew/3.14.html) | Python Software Foundation | rolling | 2026-09-22 | medium |
| [10] | "Never use argparse for new greenfield projects" (counterpoint) | [johal.in — Click vs Typer vs argparse](https://johal.in/comparison-click-vs-typer-vs-argparse-2026-python) | Johal (personal blog) | 2026-04-29 | 2026-09-22 | low |
| [11] | monkeypatch `sys.argv` as weaker alternative | [Stack Overflow argparse testing](https://stackoverflow.com/questions/18160078) | Stack Overflow (community) | rolling thread | 2026-09-22 | medium |
| [12] | ruff default config equivalent (`line-length = 88`) | [astral-sh/ruff README](https://github.com/astral-sh/ruff) | Astral (repo README) | rolling | 2026-09-22 | high |
| [13] | importlib.metadata version only works when installed; friction evidence | [mondeja/importlib-metadata-argparse-version](https://github.com/mondeja/importlib-metadata-argparse-version) | GitHub (maintainer README) | rolling | 2026-09-22 | medium |
| [14] | Empirical: uv run + argparse behavior on Python 3.14 in this workspace | local run (`uv run python main.py`) | n/a (workspace) | 2026-09-22 | 2026-09-22 | high |

## Staleness map

Computed 2026-09-22 from the claim ledger (`recon_kit.py staleness`, windows per the
technical pack: versions/compat ≤ 1 mo, ecosystem ≤ 6 mo, landscape ≤ 12 mo, patterns
≤ 2 yr):

| ref | claim | class | pub | re-check | stale |
|---|---|---|---|---|---|
| [1] | argparse stdlib default | landscape | 2026-09 | 2027-09-01 | no |
| [2] | `--version` prints stdout, exits 0 | version | 2026-09 | 2026-10-01 | no |
| [3] | syntax errors exit 2 | patterns | 2026-09 | 2028-09-01 | no |
| [4] | main(argv)+capsys test norm | patterns | 2026-09 | 2028-09-01 | no |
| [5] | package=false → static version string | version | 2026-09 | 2026-10-01 | no |
| [6] | ruff defaults line-length 88 | version | 2026-09 | 2026-10-01 | no |

**Earliest re-check: 2026-10-01** — the three version-class claims [2][5][6] (argparse
`--version` behavior, uv `package = false` semantics, ruff defaults) age fastest per
the 1-month freshness bar. A Refresh run in October will re-verify those three; the
patterns claims hold until 2028, the landscape claim until 2027.