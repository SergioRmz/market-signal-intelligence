<!--
Sync Impact Report
- Version change: 1.0.0 -> 2.0.0
- Modified principles:
 - I. Non-Advisory Educational Scope -> I. Functional Market Intelligence Scope
 - IV. Evidence-Backed AI Analysis (removed mandatory non-investment-advice product scope clarification)
 - V. Simplicity and Foundation-First Delivery -> V. Incremental Complexity Delivery
- Modified sections:
 - Operational Constraints: opened scope from Mexican-only to multi-market
 - Delivery Workflow and Quality Gates: removed and product scope clarification checks
- Added sections:
 - None
- Removed sections:
 - None
- Rationale: The platform is a functional market intelligence system, not an educational
 demo. Scope is multi-market (BMV is the first market, not the only one). Disclaimers
 are not mandated in every output. Tone reflects professional engineering, not timidity.
- Follow-up TODOs:
 - Propagate rename and scope changes across README, AGENTS, specs, docs, and schemas.
-->

# Market Signal Intelligence Platform Constitution

## Core Principles

### I. Functional Market Intelligence Scope
The platform is a functional market intelligence system for multi-market assets.
It captures, transforms, and serves structured market data with traceable provenance.
The platform does not issue personalized financial advice, portfolio allocations,
or buy/sell/hold recommendations — this is a product boundary, not a product scope clarification.
Analytical outputs present evidence, indicators, and structured observations.
Rationale: the system demonstrates real engineering capability applied to real
market data. Product scope is defined by what the system does, not by what it
apologetically says it does not do.

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
model name, provider name, confidence indicator, latency metric, and prompt version.
AI outputs MUST be grounded in verifiable inputs and MUST NOT present unsupported
claims as facts. Rationale: transparent AI metadata enables trust, review, and
responsible downstream use.

### V. Incremental Complexity Delivery
The project MUST introduce complexity only when justified by validated requirements.
Each layer — ingestion, transformation, validation, serving, analysis — MUST be
operating and tested before the next layer adds dependency on it. Production-grade
infrastructure (Kafka, AWS, RAG, autonomous agents, multi-provider orchestration)
MUST be justified by a concrete use case, not adopted speculatively. Rationale:
incremental delivery with justified complexity reduces risk and cost while
preserving iteration speed and architectural integrity.

## Operational Constraints and Technology Standards

- Backend APIs and data workflows MUST use Python with FastAPI.
- Dashboard and user-facing web interface MUST use Next.js.
- Event streaming during local development MAY use Kafka, but only after deterministic
 pipeline baselines are established and validated.
- Cloud deployment, when initiated, MUST prioritize low-cost AWS serverless services
 and incremental adoption aligned with measured usage.
- Data usage MUST respect licensing, attribution, and jurisdictional constraints for
 each governed market data source.

## Delivery Workflow and Quality Gates

- Every feature plan MUST pass a constitution check for scope clarity, traceability,
 reproducibility, contract clarity, and testability.
- Specifications that include AI outputs MUST define required evidence metadata
 fields and acceptance scenarios for metadata completeness.
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

**Version**: 2.0.0 | **Ratified**: 2026-05-26 | **Last Amended**: 2026-06-18
