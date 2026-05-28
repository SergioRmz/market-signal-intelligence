# Event Contract Validation

## Purpose

Define the lightweight validation approach for the base `AssetEvent` contract and sample files.

## Local Commands

Run from the repository root:

```bash
scripts/validation/check-foundation-artifacts.sh
```

This command checks required artifact paths, sample counts, JSON parseability, required `AssetEvent` fields, source categories, and invalid sample rule mappings.

## Evidence Format

Pull requests must include:

- Command executed.
- Pass/fail result.
- Count of valid samples.
- Count of invalid samples.
- Invalid sample to violated rule ID mapping.

## Failure Handling

- Missing required artifact: add the artifact or update the manifest through a spec change.
- Invalid JSON: fix the sample file.
- Invalid sample without rule mapping: update `docs/validation/sample-rule-mapping.md`.
- Contract mismatch: update the sample or propose a contract version change.

## Guardrails

Validation must not require deployed services, cloud resources, event brokers, application runtime components, or network access.
