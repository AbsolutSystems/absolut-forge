# AbsolutForge maintainer guidance

Keep `skills/` as the single host-agnostic behavioral source of truth. Put host-specific mechanics in `references/claude-tools.md`, `references/codex-tools.md` and `references/opencode-tools.md`. Keep artifact schemas in `references/artifact-contracts.md`; skills link to them instead of duplicating canonical templates.

A Ready Feature Brief has exactly two first-class implementation strategies: `build` (autonomous) and `build-planned` (planned/delegated). Never switch strategy after Build start unless the human explicitly abandons the active build and restarts from a clean committed Ready baseline.
