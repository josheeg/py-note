# Dimension 1 — Landscape & maturity (CLI parsing approaches)

**Round 1 — breadth-first mapping of the Python CLI-parsing landscape.**
Run inline (subagent harness unavailable), same budgets: 8 sources/dimension.

## Claims

- **claim**: argparse is the default recommended stdlib module for implementing basic
  command line applications in Python; the stdlib docs point to a "Choosing an argument
  parsing library" guide for the broader landscape.
  - source: https://docs.python.org/3/library/argparse.html
  - publisher: Python Software Foundation (official docs)
  - pub_date: rolling (live docs)
  - accessed: 2026-09-22
  - confidence: high
  - class: landscape
- **claim**: the argparse tutorial is described in official docs as "the recommended
  command-line parsing module".
  - source: https://docs.python.org/3/howto/argparse.html
  - publisher: Python Software Foundation (official docs)
  - pub_date: rolling (live docs)
  - accessed: 2026-09-22
  - confidence: high
  - class: landscape
- **claim**: the mainstream third-party CLI frameworks (Click, Typer) are built **on top
  of** argparse rather than replacing argument parsing wholesale — the stdlib module is
  the base layer of the ecosystem.
  - source: https://typer.tiangolo.com/alternatives/
  - publisher: Typer project (official docs)
  - pub_date: rolling
  - accessed: 2026-09-22
  - confidence: high
  - class: landscape
- **claim**: argparse has been actively improving in recent CPython releases — better,
  more helpful error messages in 3.12 and colorized help/error output plus suggestions
  in 3.14 — so it is not a frozen/churning legacy module.
  - source: https://docs.python.org/3.14/whatsnew/3.14.html (+ 3.12 whatsnew)
  - publisher: Python Software Foundation (official docs)
  - pub_date: rolling (3.14 current)
  - accessed: 2026-09-22
  - confidence: medium (single source family for 3.14 colorization specifics)
  - class: ecosystem
- **claim** (counterpoint, low trust): "Never use argparse for new greenfield projects" —
  a pro-Typer comparison blog post.
  - source: https://johal.in/comparison-click-vs-typer-vs-argparse-2026-python
  - publisher: Johal (personal blog, marketing register)
  - pub_date: 2026-04-29
  - accessed: 2026-09-22
  - confidence: low
  - class: landscape

## Leads worth chasing
- The stdlib "Choosing an argument parsing library" guide (linked from the argparse
  library page) — the canonical decision page; worth quoting directly in synthesis.

## Looked for and not found
- A credible primary/secondary source arguing argparse is *unsuitable* for simple CLIs
  (the only hit was the low-confidence blog above, in marketing register).