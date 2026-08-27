# Changelog

Wszystkie istotne zmiany w AbsolutForge są dokumentowane w tym pliku.
Format jest oparty na [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
a wersjonowanie projektu używa [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned

- Skill `build` z autonomiczną implementacją i warunkowym Execution Map.
- Pojedynczy niezależny `review` z klasyfikacją `BLOCKING` / `FOLLOW-UP`.
- Skill `ship` z Feature Record i Executive Summary HTML.
- Samodzielne skille `debug` i `tech-debt`.
- Testy behawioralne workflow na wspieranych modelach i harnessach.

## [0.1.0] — 2026-08-27

### Added

- Fundament prywatnego pilota dla Claude Code i Codexa z jednym współdzielonym,
  host-agnostycznym drzewem `skills/`.
- Cienkie manifesty pluginów Claude i Codex bez hooków, MCP, aplikacji ani
  globalnego wstrzykiwania kontekstu.
- Kanoniczne kontrakty Feature Brief, amendmentów, project memory oraz natywnych
  handoffów między etapami workflow.
- ADR-y opisujące wspólne drzewo skilli, explicit activation i opcjonalną
  konsultację Briefa między modelami.
- Explicit-only skill `discuss` z code-aware discovery, adaptacyjnym readiness
  frontier, użytecznym Draftem, pojedynczą akceptacją i niezmiennym baseline Ready.
- Opcjonalny explicit-only skill `consult` do niezależnego pressure-testu Briefa,
  z jedną ograniczoną paczką findings i mutacją wyłącznie po akceptacji człowieka.
- Natywne zabezpieczenia przed implicit invocation dla Claude i Codexa.
- Dokumentację produktu, architektury repo oraz raporty decyzji implementacyjnych
  dla ukończonych faz fundamentu i discovery.
- Deterministyczne testy kontraktowe oparte wyłącznie na Python standard library.

### Fixed

- Walidację Feature Briefów dopasowano do kanonicznego formatu heading-only
  Markdown; frontmatter pozostaje wymaganiem skilla, a nie Briefa.

### Verified

- 35 testów kontraktowych obejmujących AC-1–AC-15 dla Fazy 2.
- Poprawność deskryptorów JSON, strict Claude plugin validation, wspólnego drzewa
  skilli oraz symlinka `AGENTS.md` → `CLAUDE.md`.
- Canonical Codex validator pozostaje do uruchomienia w środowisku z PyYAML;
  zależności nie instalowano podczas prywatnego pilota.

[Unreleased]: https://github.com/AbsolutSystems/absolut-forge/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AbsolutSystems/absolut-forge/releases/tag/v0.1.0
