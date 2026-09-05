# AbsolutForge maintainer guidance

Keep `skills/` as the single host-agnostic behavioral source of truth. Put host-specific mechanics in `references/claude-tools.md`, `references/codex-tools.md` and `references/opencode-tools.md`. Keep artifact schemas in `references/artifact-contracts.md`; skills link to them instead of duplicating canonical templates.

The public `build` entrypoint selects one of two internal implementation strategies at Ready: `autonomous` or `planned` (standard for new starts; delegated only for legacy resume). Explicit strategy overrides apply before Build start; resumes preserve recorded strategy and methodology. Never switch strategy after Build start unless the human explicitly abandons the active build and restarts from a clean committed Ready baseline.

Run bundled Python validators that import `yaml` through `UV_CACHE_DIR=/private/tmp/absolutforge-uv-cache rtk uv run --with pyyaml python <validator> ...`. Do not treat a direct-run `ModuleNotFoundError: yaml` as a validation result or report it as a project failure; rerun the validator with the isolated `uv` dependency first.
