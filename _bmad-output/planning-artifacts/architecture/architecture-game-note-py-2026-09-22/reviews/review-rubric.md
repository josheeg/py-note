## Review Rubric Walk — Architecture Spine `architecture-game-note-py-2026-09-22`

### Verify (confirmed valid)

- **AD-1 — Single-file flat layout:** Binds all production code; prevents `src/` layout or package dir that breaks `uv sync`. Confirmed enforceable: `[tool.uv] package = false` in `pyproject.toml` directly prohibits package dir, and AGENTS.md states "there is no importable package dir; do not introduce a `src/` layout." The rule is self-enforcing.

- **AD-2 — Pure core / I/O shell separation:** Binds CAP-1, CAP-2 (greeting behavior); test strategy. Rule — `hello(name: str) -> str` performs no I/O, no prints, no `sys` access; all I/O stays in `main(argv)`. The pure function is trivially testable without subprocess, and argparse/print/exit live only in the shell. Confirmed.

- **AD-3 — argparse owns all CLI parsing:** Binds CAP-1..CAP-4 (all invocation forms). Prevents hand-rolled `sys.argv` scanning, divergent parsing implementations, manual exit-code handling. Rule — `main.py` uses stdlib `argparse` exclusively: `--name` (single value, last-one-wins), `--version`, `-h`/`--help`, and error/usage all from argparse. The current `main.py` uses argparse exclusively. Confirmed.

- **AD-4 — Version single-source:** Binds CAP-3. Prevents `importlib.metadata.version()` attempts (breaks under flat `package = false`) and version-string drift. Rule — module-level `__version__` constant is the only version authority; wired to argparse `action="version"` with format `'%(prog)s <version>'`. `--version` precedence over `--name` is inherent to argparse. Confirmed.

- **AD-5 — Exit-code & stream contract:** Binds CAP-4; prevents custom exit codes, traceback leaks to the user, and stdout/stderr mixing. Rule — success returns 0 with data on stdout only; every error path exits 2 via argparse `SystemExit` with usage on stderr only; no tracebacks escape. Output is deterministic ASCII — no color, ANSI, Unicode, network, or file writes. The `main()` fall-through returns `None` → Python exit 0; argparse errors trigger `SystemExit(2)` with usage on stderr. Confirmed.

- **CAP → Architecture mapping:** All 4 capabilities mapped: CAP-1 → AD-1,AD-2,AD-3,AD-5; CAP-2 → AD-2,AD-3; CAP-3 → AD-3,AD-4; CAP-4 → AD-3,AD-5. Complete and non-contradictory.

- **Brownfield ratification:** `[tool.uv] package = false` in `pyproject.toml` ratifies AD-1's "no package dir" rule. AGENTS.md confirms "The package is flat — there is no importable package dir; do not introduce a `src/` layout." No contradictions.

- **Inherited invariants:** No parent spine present; the spine appropriately omits an "Inherited Invariants" section rather than incorrectly including one.

### Confirm (needs clarification — not a fix given scope)

- **Operational/environmental envelope not explicitly addressed:** The spine's scope is `"the python cli hello world — main.py and its tests"` at feature altitude. Deployment, environments, infra, and operations are not in the altitude's domain for this artifact. The rubric flags a whole dimension left silent as a finding, but the spine's explicit scope limits ownership. Noted as confirmed (silence is intentional given altitude/scope), not fixed.

- **AD-5 references "MOAT (must-only-allowed-terms) output rules":** The name "MOAT" is referenced upfront, and its practical definition is the deterministic ASCII + stderr-only + exit-0/2 rules in the AD-5 Rule section. The reference is consistent with the rule; no separate MOAT definition is needed within the spine.

### Fix (none required — spine is consistent with its stated altitude and scope)

- No fixes required. The spine correctly decides, defers, or opens every dimension it owns. The deferred section (repeated `--name`, teaching pack, color/decoration, packaging, console-script, subcommands) correctly notes note-gated non-goals. The capability→architecture map covers all spec CAPs. The brownfield codebase is ratified.