---
name: python cli hello world
status: final
description: Terminal-native greeting CLI. ASCII-only, zero color, zero decoration — the visual identity IS the absence of decoration. Surface is the user's terminal (Windows PowerShell or POSIX); the program adds nothing to it.
---

# DESIGN — python cli hello world

## Brand & Style

The product's visual identity is *restraint as identity*. A hello-world CLI
renders on the user's terminal — a surface the program does not own. The brand
promise is "exactly what you asked for, nothing added": one line of output,
ASCII-only, no color codes, no banners, no spinners. The absence of decoration
is the feature; it is what makes the output canonical and the program readable.

No colors, typography, spacing, elevation, or shape tokens are defined. The
terminal's own defaults are the spec — the program must render correctly on the
widest possible terminal configuration (white-on-black, black-on-white, any
ANSI palette, Windows PowerShell's default console). Emitting any ANSI escape,
color code, or Unicode glyph would *break* that contract.

## Colors

None. The program emits no color codes and renders no color-dependent content.
Output must be legible on any terminal theme because it uses neither theme's
color. This is a hard constraint, not an omission: a colored greeting would
violate FR-1's canonical-output contract.

## Typography

No font control. The program relies on the terminal's monospace font and never
attempts to re-flow, pad, or decorate output. The single output line
(`Hello, {name}!`) is short enough to never wrap at standard terminal widths.

## Layout & Spacing

No layout language. Output is exactly one line ending in one newline,
terminated by the shell prompt. No leading blank lines, no trailing blank
lines, no alignment padding. Help text follows argparse's standard two-space
indentation for options, rendered to the terminal's width.

## Elevation & Depth

None. A CLI has no elevation model; depth is conveyed by the shell's own
prompt hierarchy, not by the program.

## Shapes

None. No graphical elements, borders, or box-drawing characters. ASCII
characters only, and only the ones the canonical outputs require.

## Components

- **Greeting line** — `Hello, {name}!` on stdout. The only user-facing success
  component. Never wrapped in quotes, brackets, or decoration.
- **Version line** — `%(prog)s {__version__}` on stdout (argparse
  `action="version"`). Flat, unadorned, predictable.
- **Help text** — argparse-generated `usage:` + options list on stdout.
  Conventional layout; no custom branding, no ASCII art.
- **Error text** — argparse-generated `error:` + message + `usage:` hint on
  stderr. Single message line; no exclamation, no embellishment.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Emit exactly the canonical output, nothing else | Add banners, ASCII art, separators, or "welcome" flair |
| Output only ASCII characters | Emit ANSI color codes, emoji, box-drawing, or Unicode |
| Let the terminal's own font/theme render | Emit width-padding, centering, or font-control escapes |
| One line in, one line out, shell prompt resumes | Print spinners, progress, or "done" celebratory text |
| Keep help/error text to argparse conventions | Invent custom branding, taglines, or mascots |