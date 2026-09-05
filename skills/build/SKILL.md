---
name: build
description: "Explicitly implement an accepted Feature Brief, selecting autonomous or planned execution once at Ready and preserving recorded strategy on resume. Use only when the user invokes AbsolutForge build."
---

# Build

Accept the canonical Feature Brief path and optional `--strategy=autonomous` or `--strategy=planned`. Read [runtime common](../../runtime/common.md). At Ready, follow [Build strategy selection](../../references/artifact-contracts.md#build-strategy-selection): inspect accepted intent and relevant repository evidence, default to autonomous, and choose planned only for concrete benefits that repay its overhead. A valid explicit override wins. Reject unknown or repeated options before mutation. Announce the choice and concise reason without asking for confirmation; persist it in the Build-start checkpoint before implementation.

At Building, read recorded Build strategy and methodology first; do not select again. A matching override is allowed; reject a conflicting override before mutation. Missing methodology means standard for planned or not applicable for autonomous; missing strategy or contradictory evidence requires reconciliation, never inference from task size or artifact presence. Preserve historical evidence without backfilling selection fields. Draft requires accepted Ready intent; In Review routes to Review/Ship as eligible; Shipped is closed.

Load only the selected [autonomous runtime](../../runtime/autonomous.md) or [planned runtime](../../runtime/planned.md), plus the matching active-host mechanics in `../../references/`. Continue that strategy within this invocation; internal routing requires no second skill invocation or approval. Do not preload the other runtime or compile a plan to decide whether planning is needed.

For recorded planned/delegated state, load `../../references/planned-delegated-contract.md` and the active host fixed-executor mechanics before implementation; never convert, substitute or take over. Legacy tdd requires a compatible older release or explicit clean Ready restart. Strategy overrides never change recorded methodology.

Follow the selected runtime's complete start/resume, verification, ownership, checkpoint and final handoff rules. Read verification doctrine at autonomous start or planned compilation, and for uncertain obligations/exemptions; artifact sections at start and final delivery; planned contract for compilation, frontier repair, PC changes or ownership/completion ambiguity; harness syntax for the resolved Review continuation. Never switch strategy or methodology after Build start without explicit abandonment and restart from a clean committed Ready baseline.
