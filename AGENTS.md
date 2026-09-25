<!-- bmad:context -->
<!-- Verified 2026-09-24 against local filesystem; no Git SHA available because this directory is not a Git repository. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## py

BMAD/OpenCode tooling workspace for the `py` installation, not an application source tree. It contains generated BMAD v6.12.0 configuration and skill sources; planning and implementation artifacts belong under `_bmad-output/`, and project knowledge is configured for `docs/` (currently absent).

## Policy

- Treat `_bmad/config.toml`, `_bmad/config.user.toml`, `_bmad/core/config.yaml`, and `_bmad/bmm/config.yaml` as installer-managed; do not hand-edit them. Put durable team overrides in `_bmad/custom/` and personal overrides in `_bmad/custom/*.user.toml`.
- Treat `_bmad/render/` as generated output and `.opencode/commands/` plus `.agents/skills/` as installed tooling; use BMAD override files for durable behavior changes.
- Do not commit `.opencode/node_modules/`, `.opencode/package.json`, or `.opencode/package-lock.json`; `.opencode/.gitignore` lists them.

## Where things are

- Central BMAD config and resolver helpers: `_bmad/config.toml`, `_bmad/config.user.toml`, `_bmad/scripts/`.
- Installed skills and OpenCode wrappers: `.agents/skills/`, `.opencode/commands/`.
- Durable customizations: `_bmad/custom/`; generated render snapshots: `_bmad/render/`; planning and implementation artifacts: `_bmad-output/`.

## Running and verifying

- Run installed Python helpers through `uv run`; resolver and render scripts require Python >=3.11, while `_bmad/scripts/memlog.py` declares >=3.8.
- Resolve central config with `uv run _bmad/scripts/resolve_config.py --project-root .`; resolve a skill customization with `uv run _bmad/scripts/resolve_customization.py --skill <skill-dir> --project-root . --key workflow`.
- Render an installed skill with `uv run _bmad/scripts/render_skill.py --project-root . --skill <skill-dir>`; output belongs under `_bmad/render/`.
- No application build, test, or lint command is defined here; do not invent one. This directory is not a Git repository, so do not rely on `git diff`, `git log`, or commit provenance.

## Conventions that differ from defaults

- Central config merges `_bmad/config.toml`, `_bmad/config.user.toml`, `_bmad/custom/config.toml`, then `_bmad/custom/config.user.toml`; skill customization merges its installed `customize.toml`, team override, then user override.
- Write memlog state only through `_bmad/scripts/memlog.py`; `.memlog.md` is append-only and has no hand-edit/delete workflow.
- Use English for agent communication and generated documents, as configured in `_bmad/config.user.toml`.

<!-- /bmad:context -->
