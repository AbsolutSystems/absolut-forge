# One public Build entrypoint

## Decision

Expose one `build` command with two internal strategies, autonomous and planned. Select once from accepted intent and targeted repository evidence before the Build-start checkpoint. Default to autonomous; planned needs concrete benefits from independent work/dependencies, useful bounded delegation or durable multi-session recovery that repay its overhead. File count and generic complexity are insufficient. Do not compile a graph or load both execution runtimes just to select.

Accept optional `--strategy=autonomous` or `--strategy=planned`. Announce and record the selected strategy and concise reason without another confirmation. A valid explicit override takes precedence at Ready. Unknown or repeated options are refused before mutation.

At Building, recover recorded strategy and methodology without selecting again. Reject conflicting overrides; matching overrides cannot change methodology. Missing or contradictory strategy evidence requires reconciliation. Old starts without a selection rationale remain valid unchanged. Planned/delegated retains fixed-executor restrictions; legacy tdd remains unsupported. Review corrections and Save/Load handoffs use the same public command.

## Scope and compatibility

Remove the separate planned skill, UI descriptor and opencode command while retaining both execution runtimes and their verification, checkpoint and ownership contracts. Old planned invocations use `build` with the same Brief path; no accepted Brief or completed task history is migrated. Explicit strategy changes after start still require human abandonment and restart from a clean committed Ready baseline.

This supersedes the public two-command surface in the dual-build, lean-planned and token-efficient-runtime ADRs. Their internal execution strategies and delivery guarantees remain in effect. Existing Review reports cover their recorded revision only; this new implementation needs current delivery evidence and Review before lifecycle closeout.

## Verification

Distribution tests verify one public Build skill/host command, selected-runtime links, override and resume contracts, start-only selection evidence, and unchanged final evidence and legacy ownership sections. Existing fresh-process context tests and the pinned-baseline benchmark continue to exercise the actual current Build package. These checks validate the Markdown instruction product and local helper behavior; they do not claim live model routing or token-saving measurements.
