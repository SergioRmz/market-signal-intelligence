# Quickstart - Initial Project Foundation

## Purpose
Set up and validate the repository foundation artifacts defined in the specification without implementing runtime application behavior.

## 1) Confirm branch and feature context
```bash
git rev-parse --abbrev-ref HEAD
```
Expected branch: `001-project-foundation`.

## 2) Verify required artifact paths exist
Required paths:
- `README.md`
- `AGENTS.md`
- `docs/architecture/foundation-architecture.md`
- `docs/policies/allowed-sources.md`
- `contracts/events/asset-event.schema.json`
- `data/samples/asset-events/valid/`
- `data/samples/asset-events/invalid/`
- `docs/validation/event-contract-validation.md`

## 3) Validate sample set minimums
- At least 2 files under `data/samples/asset-events/valid/`
- At least 3 files under `data/samples/asset-events/invalid/`
- Each invalid sample must map to one or more documented rule IDs.

## 4) Run local contract checks (lightweight)
Use repository-local commands only (no deployed services, no cloud dependencies).

Command:
```bash
scripts/validation/check-foundation-artifacts.sh
```

Expected output includes `PASS foundation artifacts and samples validated`.

## 5) Record PR validation evidence
Include in PR description:
- Commands executed
- Pass/fail by sample group
- Invalid sample -> violated rule ID mapping

## Guardrails
- Do not add ingestion logic, Kafka topology, AI analysis pipelines, AWS deployment artifacts, RAG components, or dashboard runtime code.

## Validation Evidence

Latest local validation command:

```bash
scripts/validation/check-foundation-artifacts.sh
```

Latest observed result:

```text
PASS foundation artifacts and samples validated
```
