# Scaffolding Boundaries

## Allowed Scaffolding

- Empty directories required by the artifact manifest.
- Documentation-only files explaining future boundaries.
- Contract schema files and sample payloads.
- Validation helper scripts that inspect files locally.

## Not Allowed In This Feature

- Runtime services.
- Data ingestion jobs.
- Kafka or event broker configuration.
- AWS infrastructure or deployment automation.
- AI/RAG pipelines or agent orchestration.
- Dashboard application code.

## Review Rule

If a file executes business behavior beyond local validation of repository artifacts, it is not allowed in this foundation feature.
