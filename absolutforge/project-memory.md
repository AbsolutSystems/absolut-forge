# AbsolutForge Project Memory

This is the canonical store for cross-cutting, durable lessons. Routing,
entry-schema, candidate-capture, and promotion rules are defined in the
[Project-Memory Contract](../references/project-memory.md); this file stores
approved lessons and does not duplicate that contract.

## Status and lifecycle

Permanent entries may use only `active`, `superseded`, or `archived`. Only
`active` entries guide implementation. Promotion requires explicit user
approval and a stated destination; candidates remain outside this store until
approved.

## Empty state

No project-wide lessons have been approved yet. Do not infer implementation
guidance from this marker. Add an entry only after applying the canonical
contract and receiving explicit promotion approval.
