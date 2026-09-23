# Review: Adversarial Divergence Hunt — architecture-game-note-py-2026-09-22

**Lens:** Construct two units one level down that each obey every AD to the letter yet still build incompatibly. Every pair found is a hole to close with a new or tightened AD. Also walk SPEC CAP-1..4 + success signal for AD coverage.

## Fix Tier

### F1 (MEDIUM) — Greeting canonicalization ambiguous: does `hello()` trim non-empty names?

- **Conflict pair:** two independent implementers of `main.py` — (A) treats CAP-2's "empty/whitespace values fall back to World" as *whitespace-only check only*: `--name "  Ada  "` → `Hello,   Ada  !` (no trim); (B) trims first: `--name "  Ada  "` → `Hello, Ada!`.
- **Why both obey every AD:** AD-2 Rule says "with empty/whitespace fallback to `World`" but never specifies trimming of *non-empty* names. AD-3 says fallback applied "inside `hello()`" but doesn't name the normalization. SPEC CAP-2 specifies only the whitespace-only → World case, silent on surrounding whitespace of real names.
- **Which breaks:** the shared-data shape (the exact greeting string) is undefined for the `"  Ada  "` input — a test asserting either behavior passes one implementer and fails the other.
- **Fix:** tighten AD-2 Rule to the exact canonicalization: greeting = `f"Hello, {name.strip() or 'World'}!"` — strip first, empty-after-strip falls back to World. One deterministic normalization, testable at any altitude.

### F2 (MEDIUM) — `%(prog)s` diverges between CLI and capsys test invocation

- **Conflict pair:** `main.py` vs `tests/test_main.py`. Under `uv run python main.py`, argparse `prog` defaults to basename(`sys.argv[0]`) = `main.py` → `--version` prints `main.py 0.1.0` (SPEC CAP-3 ✓). But a capsys test calling `main(["--version"])` runs under the pytest process — `sys.argv[0]` is the pytest runner, so the SAME code prints `pytest 0.1.0` (or the runner's basename).
- **Why both obey every AD:** AD-4 Rule says format `'%(prog)s <version>'` — both implementers comply literally; the divergence is inherent to `%(prog)s` resolving from `sys.argv[0]`, which the ADs never pin.
- **Which breaks:** the CAP-3 success criterion ("prints `main.py <version>`") is not invariant across invocation contexts; a test asserting the SPEC's exact string fails under capsys.
- **Fix:** bind `prog` explicitly — AD-3 Rule: the parser is constructed with `prog="main.py"` — making version output and usage text deterministic in every invocation context (real CLI, capsys unit test, any runner).

## Confirm Tier

- **Exit-code/stream handling** — success paths `return 0` from `main() -> int`; parse errors raise argparse `SystemExit(2)` which propagates out of `main()` unchecked (main never returns 2). Test contract = `pytest.raises(SystemExit)` + `code == 2` for error paths, `assert main([...]) == 0` for success. Consistent with addendum's capsys strategy; no custom error handler can diverge because AD-3 + AD-5 forbid manual parsing/exit handling. Confirmed — no fix.
- **CAP coverage walk:** CAP-1 → AD-1, AD-2, AD-3, AD-5; CAP-2 → AD-2, AD-3; CAP-3 → AD-3, AD-4; CAP-4 → AD-3, AD-5; success signal (readable one-sitting, green pytest) → AD-2 (capsys testability), AD-5 (stream/exit contract), conventions table (code-size row). Complete. Confirmed.

## Overall Verdict

Spine is sound at altitude; two tightenable rules (greeting canonicalization, explicit `prog`) are the only holes — both are one-line Rule tightenings, not new ADs.