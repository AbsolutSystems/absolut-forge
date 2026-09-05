---
name: build-planned
description: "Explicitly implement an accepted Ready Feature Brief through a durable task graph, bounded workers, and verified Review handoff. New starts use standard methodology; legacy delegated builds resume with fixed-executor restrictions. Use only when the user invokes AbsolutForge build-planned."
---

# Build — Planned Strategy

Use this entrypoint only with the canonical Feature Brief path. Read [runtime common](../../runtime/common.md), then the [planned runtime](../../runtime/planned.md), and the matching active-host mechanics in `../../references/`. Those documents own compilation, task capsules, worker boundaries, start/resume checks, verification, evidence, and handoff.

`Ready` starts planned Build with standard methodology only. A `Building` Brief resumes here only when its recorded strategy is planned. For recorded `delegated`, lazily load `../../references/planned-delegated-contract.md` and the active host's fixed-executor mechanics before implementation; preserve every restriction and never convert it. Recorded legacy `tdd` requires a compatible older release or an explicit clean Ready restart. Route autonomous state to `build`.

When compiling a new plan, read the planned contract and verification doctrine as required by the planned runtime; also read the relevant artifact-contract sections at Build start and final delivery-gate verification. Follow the runtime's full remaining triggers, including the planned contract for frontier reconstruction, PC changes, ownership, or completion ambiguity; doctrine for uncertain obligations or exemptions; and the harness contract when producing the final Review continuation. The runtime specifies the required resolved Brief/Review paths and copy-ready final handoff.
