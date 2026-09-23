# Dimension 2 — Architecture patterns in practice (well-formed CLI structure)

**Round 1 — patterns for flag parsing, --version, exit codes, and testability.**
Run inline (subagent harness unavailable), same budgets.

## Claims

- **claim**: canonical argparse pattern for `--version` is the built-in `version` action
  with a `version=` string containing `%(prog)s` substitution —
  `parser.add_argument('--version', action='version', version='%(prog)s 2.0')`
  prints e.g. `PROG 2.0` and exits.
  - source: https://docs.python.org/3/library/argparse.html
  - publisher: Python Software Foundation (official docs)
  - pub_date: rolling
  - accessed: 2026-09-22
  - confidence: high
  - class: version
- **claim**: the argparse `_VersionAction` implementation prints the version string to
  **stdout** and then calls `parser.exit()` — i.e. `--version` exits 0, not 2.
  - source: https://github.com/python/cpython/blob/main/Lib/argparse.py (class
    `_VersionAction.__call__`)
  - publisher: CPython (source of record)
  - pub_date: rolling (main branch)
  - accessed: 2026-09-22
  - confidence: high
  - class: version
- **claim**: Unix convention for CLI exit status, restated in the Python docs: 0 for
  success, **2 for command-line syntax errors**, 1 for all other errors.
  - source: https://docs.python.org/3/library/sys.html (`sys.exit`)
  - publisher: Python Software Foundation (official docs)
  - pub_date: rolling
  - accessed: 2026-09-22
  - confidence: high
  - class: patterns
- **claim**: established test pattern for argparse CLIs is to structure the CLI as a
  `main(argv=None)` function (parser built inside, `parse_args` on provided argv) and
  test with `capsys` (capture stdout) + `pytest.raises(SystemExit)`.
  - source: https://til.simonwillison.net/pytest/pytest-argparse
  - publisher: Simon Willison (TIL, practitioner account)
  - pub_date: 2022-01-08
  - accessed: 2026-09-22
  - confidence: medium (single practitioner source, but consistent with CLI
    test-pattern folklore and with FERAL-verified assertion of exit code 2 on
    parse errors)
  - class: patterns
- **claim**: alternative test pattern — monkeypatching `sys.argv` before calling the
  main entry — exists but is the weaker pattern (global state mutation vs passing argv).
  - source: Stack Overflow (argparse testing answers), e.g.
    https://stackoverflow.com/questions/18160078 (pattern class)
  - publisher: Stack Overflow (community)
  - pub_date: n/a (rolling thread)
  - accessed: 2026-09-22
  - confidence: medium
  - class: patterns

## Leads worth chasing
- `parser.exit()` default status confirms 0; `parser.error()` (used on parse failure)
  exits with status 2 — consistent with the sys-docs convention; cross-referenced in
  synthesis and aligned with a FERAL integration test asserting exit 2 on bad args.

## Looked for and not found
- Any source recommending a command/subcommand structure for a single-greeting CLI
  (scope argues decisively against subparsers for this decision — noted for synthesis).