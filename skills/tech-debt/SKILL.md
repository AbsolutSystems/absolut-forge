---
name: tech-debt
description: "Explicitly perform a static read-only evidence-backed technical-debt audit of a repository or bounded repository-relative path and route findings to discuss, debug, or watch."
disable-model-invocation: true
---

# Tech Debt

Inspect only the requested repository/path. Run no application commands and change no files. Ground every finding in concrete source evidence and explain impact.

Prioritize findings that create correctness, maintainability, security/data, testability or architecture risk. Exclude subjective style preferences and speculative problems without evidence.

Route remediation:

- `discuss` when fixing requires product/architecture/scope decisions;
- `debug` for a concrete failure with unambiguous expected behavior;
- `WATCH` for evidence-backed debt that is not currently worth changing.

Do not create Feature Briefs, plans, maps, reviews or commits.
