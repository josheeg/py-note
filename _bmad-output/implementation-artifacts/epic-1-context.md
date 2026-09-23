# Epic 1 Context: A faithful, tested hello-world CLI

<!-- Generated from planning artifacts. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Ada runs one command, sees `Hello, World!`, reads the whole program in one sitting, and can predict its behavior before running it — invocation, output, and exit code all working, tested, and explainable. Realizes UJ-1; satisfies SPEC CAP-1..4 under AD-1..AD-5.

## Stories

- 1.1: Canonical greeting on bare run
- 1.2: Custom greeting with `--name`
- 1.3: Version reporting with `--version`
- 1.4: Errors and help
- 1.5: Test suite, contract verification, and one-sitting readability

## Requirements & Constraints

The CLI must produce exactly `Hello, World!` on stdout with exit 0 and nothing on stderr when run without arguments. The `--name` flag personalizes the greeting, defaulting to `World` when no name is provided or when the value is empty or whitespace. The `--version` flag reports the program version as `main.py <version>`, exits 0, and takes precedence over `--name`. Invalid arguments and missing `--name` values produce error feedback on stderr with exit 2 and no tracebacks. The implementation uses only stdlib `argparse` with no runtime dependencies. The project maintains a flat layout with `[tool.uv] package = false` and no package directory. Output is deterministic ASCII — no color, ANSI, Unicode, network, or file writes. The program stays readable in approximately 30 lines. All function signatures include type hints; the project uses Python 3.12+ and all commands run via `uv run`. A pure `hello(name: str) -> str` function computes the greeting with deterministic canonicalization, stripping whitespace and falling back to `World` for empty values. All I/O (argument parsing, printing, exit codes) is confined to the `main()` entry point. The argparse parser uses `prog="main.py"` for deterministic version and usage text. The version string comes from a module-level `__version__` constant wired to argparse `action="version"`. Error paths exit with code 2 via argparse, writing usage to stderr only with no tracebacks. The test suite uses capsys for I/O capture and `pytest.raises(SystemExit)` for error paths, never subprocess. Exit codes are 0 for success and 2 for bad arguments, with strict stream separation (data on stdout, errors on stderr) for CI/scriptability.

## Technical Decisions

Functional core / imperative shell pattern separates the pure `hello(name: str) -> str` function from the I/O `main(argv)` entry point. argparse is the exclusive CLI parsing module, constructed with `prog="main.py"` for deterministic version and usage output. Module-level `__version__` constant is the single version authority wired to argparse `action="version"`. The project uses a flat layout with `[tool.uv] package = false` and no package directory, forcing module-level version as the only authoritative source. Greeting canonicalization follows exactly `f"Hello, {name.strip() or 'World'}!"` — strip whitespace first, then fallback to `World` for empty/whitespace values. Test strategy uses capsys-based tests colocated in `tests/test_main.py`, never subprocess invocations. Exit code contract is 0 for success, 2 for bad arguments, with strict stream separation (stdout for data, stderr for errors). No runtime dependencies beyond stdlib `argparse`; `pytest` is the sole dev dependency added via `uv add --dev pytest`.

## UX & Interaction Patterns

The program outputs exactly one ASCII line per surface with no banners, color, ANSI, Unicode, or decoration. The `--name` flag personalizes the greeting; empty or whitespace values fall back to `World` while preserving canonical output. The `--version` flag takes precedence over `--name` via argparse inherent behavior. The `-h`/`--help` flag provides usage documentation on stdout, exiting 0. Unknown flags and missing `--name` values produce argparse `error:` messages on stderr, exiting 2 with no traceback. All forms are one-shot — no prompts, no stdin reads, no interactive loops, no waiting. Exit codes are predictable: 0 for success, 2 for bad arguments. Strict stream separation (data on stdout, errors on stderr) enables CI-safe scripting and redirection. Help and error text follows argparse conventions without custom branding, taglines, or ASCII art. Output renders legibly on any terminal theme (Windows PowerShell or POSIX) because it uses ASCII-only content with no color dependence.

## Cross-Story Dependencies

The test suite validates all documented behavior across the other stories in the epic. The pure `hello()` core function is the foundation for greeting behavior, used by `main()` and tested across stories 1.1–1.4. The argparse configuration is shared across all CLI invocation forms (bare run, `--name`, `--version`, help, errors). The version source (`__version__` constant) and flat-project constraint apply across multiple stories. All stories cross-cut with the UX design constraints (output-is-the-output, one-shot forms, predictable exit codes, stream separation).