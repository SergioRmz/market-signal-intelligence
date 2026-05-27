<!--
Sync Impact Report
- Version change: template -> 1.0.0
- Modified principles:
  - Placeholder Principle 1 -> I. Non-Advisory Educational Scope
  - Placeholder Principle 2 -> II. Traceable and Reproducible Intelligence
  - Placeholder Principle 3 -> III. Contract-First Event-Driven Design
  - Placeholder Principle 4 -> IV. Evidence-Backed AI Analysis
  - Placeholder Principle 5 -> V. Simplicity and Foundation-First Delivery
- Added sections:
  - Operational Constraints and Technology Standards
  - Delivery Workflow and Quality Gates
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
  - ⚠ pending: .specify/templates/commands/*.md (directory not present)
- Follow-up TODOs:
  - None
-->

# BMV Signal Intelligence Platform Constitution

## Core Principles

### I. Non-Advisory Educational Scope
The platform MUST operate as an educational and technical market intelligence system
for Mexican equities. The platform MUST NOT issue financial advice, portfolio
allocations, or buy/sell/hold recommendations. Every user-facing analytical output
MUST include a clear disclaimer that content is not investment advice. Rationale:
this boundary protects users, clarifies product intent, and reduces compliance risk.

### II. Traceable and Reproducible Intelligence
All data transformations, indicators, and analytical results MUST be traceable to
their sources and reproducible from versioned inputs, code, and configuration.
Pipelines MUST record provenance metadata, processing timestamps, and deterministic
parameters so another engineer can recreate the same result. Rationale: reproducible
workflows are required for auditability, debugging, and scientific credibility.

### III. Contract-First Event-Driven Design
Inter-service communication and event flows MUST be defined by explicit contracts
(schemas, versioning rules, and compatibility expectations) before implementation.
Event-driven components MUST be testable through contract and integration tests.
Interfaces MUST prefer stable, documented boundaries over implicit coupling.
Rationale: explicit contracts reduce regressions and enable safe evolution.

### IV. Evidence-Backed AI Analysis
Any AI-generated analysis MUST include: source references, generation timestamp,
model name, provider name, confidence indicator, latency metric, prompt version,
and a non-investment-advice disclaimer. AI outputs MUST be grounded in verifiable
inputs and MUST NOT present unsupported claims as facts. Rationale: transparent AI
metadata enables trust, review, and responsible downstream use.

### V. Simplicity and Foundation-First Delivery
The project MUST avoid overengineering and introduce complexity only when justified
by validated requirements. Do not introduce production-grade Kafka topology, AWS
deployment, RAG systems, autonomous agents, or multi-provider LLM orchestration
before deterministic ingestion, transformation, validation, and serving pipelines
are operating and tested. Rationale: foundation-first delivery reduces risk, cost,
and operational burden while preserving iteration speed.

## Operational Constraints and Technology Standards

- Backend APIs and data workflows MUST use Python with FastAPI.
- Dashboard and user-facing web interface MUST use Next.js.
- Event streaming during local development MAY use Kafka, but only after deterministic
  pipeline baselines are established and validated.
- Cloud deployment, when initiated, MUST prioritize low-cost AWS serverless services
  and incremental adoption aligned with measured usage.
- Data usage MUST respect licensing, attribution, and jurisdictional constraints for
  Mexican market data sources.

## Delivery Workflow and Quality Gates

- Every feature plan MUST pass a constitution check for non-advisory scope,
  traceability, reproducibility, contract clarity, and testability.
- Specifications that include AI outputs MUST define required evidence metadata
  fields and acceptance scenarios for disclaimer presence.
- Task plans MUST include contract tests, integration tests for event flows, and
  validation steps for provenance and reproducibility.
- Pull requests MUST document compliance with these principles and include evidence
  for any exception approved through governance.

## Governance

This constitution supersedes conflicting local conventions for this repository.
Amendments require: (1) a written proposal, (2) explicit rationale and impact
analysis, and (3) updates to affected templates and workflow artifacts.

Versioning policy for this constitution follows semantic versioning:
- MAJOR: incompatible principle removals or redefinitions.
- MINOR: new principle or materially expanded mandatory guidance.
- PATCH: clarifications and non-semantic refinements.

Compliance review is required in planning, specification, task generation, and pull
request review. Any waiver MUST be documented with scope, owner, expiration, and a
remediation plan.

**Version**: 1.0.0 | **Ratified**: 2026-05-26 | **Last Amended**: 2026-05-26
