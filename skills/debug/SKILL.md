---
name: debug
description: "Diagnose a concrete failure and, when explicitly requested, make one bounded direct fix. Use for errors, failing tests, crashes or regressions; diagnosis may auto-trigger but edits require explicit fix intent."
---

# Debug

Work from observable evidence: reproduce, isolate the violated invariant, test a focused hypothesis, confirm root cause. Do not propose a fix before sufficient evidence.

For diagnosis-only, change no files. For an explicit fix with unambiguous expected behavior, make the smallest root-cause correction and focused regression verification. If the fix changes product behavior, public contract, security/data handling, migration, material cost or requires major architecture judgment, route to `discuss` instead.

When invoked inside an active feature, respect its recorded Build strategy and planned methodology and append relevant failure/verification evidence without taking ownership from its matching builder. A fix there follows `../../references/verification-doctrine.md`: pin the defect with a regression test, or record the exemption and its reason in that stage's evidence. Under delegated methodology, diagnosis may run here but every source or test correction returns to `build`, which preserves its fixed executor. Under legacy `tdd`, limit this skill to diagnosis and require a compatible older builder or explicit abandonment/restart for edits. Never weaken, skip or delete an existing test to reach green.
