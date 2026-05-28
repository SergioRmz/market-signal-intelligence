<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
specs/001-project-foundation/plan.md
<!-- SPECKIT END -->

# Agent Instructions

## Repository Scope

This repository is the BMV Signal Intelligence Platform foundation. Work in this phase is limited to documentation, contracts, sample data, validation guidance, and repository scaffolding.

Do not add runtime application behavior in this feature. Specifically, do not implement ingestion logic, Kafka topology, AWS deployment automation, AI analysis, RAG workflows, autonomous agents, or dashboard code.

## Required Reading Order

1. `.specify/memory/constitution.md`
2. `specs/001-project-foundation/spec.md`
3. `specs/001-project-foundation/plan.md`
4. `specs/001-project-foundation/tasks.md`
5. `docs/foundation/artifact-manifest.md`

## Contribution Guardrails

- Keep all financial content educational and non-advisory.
- Preserve traceability for source policies, contracts, and samples.
- Treat `contracts/events/asset-event.schema.json` as the contract boundary for future event work.
- Update validation evidence when contract or sample files change.
- Keep scaffolding empty or documentation-only unless a future feature explicitly authorizes runtime code.

## Review Expectations

- Confirm every changed artifact is listed in `docs/foundation/artifact-manifest.md` or justified by a task.
- Confirm invalid samples map to rule IDs in `docs/validation/sample-rule-mapping.md`.
- Confirm local validation instructions in `docs/validation/event-contract-validation.md` remain reproducible from a clean clone.
