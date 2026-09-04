---
type: master-requirements
name: spec-objects-business
org: agent-ix
component_type: filament-module
implementation_language: python
tags:
  - filament-module
  - ddd
  - object-types
depends_on: []
standards_alignment:
  - iso-iec-ieee-29148
relationships:
  - target: "ix://agent-ix/filament-core-service/FR-035"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/quire-rs/FR-069"
    type: "depends_on"
    cardinality: "1:1"
security_critical: false
---
# Master Requirements Specification

## Purpose

This document specifies the requirements for `spec-objects-business`, a Filament
Module that contributes tier-2 business ObjectTypes for DDD modelling. DDD-driven
specs need extractable graph entities for domains, entities, value objects,
aggregates, repositories, events, processes, and state machines; this module
ships those ObjectTypes (with their templates and schemas) so that authors,
reviewers, and agent generators share one authoritative definition of what the
module activates against `filament-core`.

## Scope

### In Scope

- The Module manifest (`spec_objects_business/manifest.yaml`) and the nine tier-2
  business ObjectTypes it contributes for DDD modelling.
- The functional requirement that the manifest activates idempotently against
  `filament-core-service`, and the integration test that verifies it.
- The semantic-module contract (issue #4): a TypeSpec source importing
  `@agent-ix/semantic-core` 0.1.0, the emitted JSON Schema per object type
  shipped under `spec_objects_business/schemas/`, the manifest `semantic`
  block with reference-form `data_schema`, and the skeletons rewritten as
  executable typed fixtures with negative counterparts.

### Out of Scope

- The behaviour of `filament-core-service` itself, referenced here only by the
  relationship to its manifest schema (FR-035).
- Deployment topology and cluster infrastructure, which live in the operating
  environment rather than this specification.
- Generated-language fixtures (Rust, TypeScript, Python) for the business
  types: owned by `agent-ix/filament-core-data#11` and `#36`, not produced or
  faked here.
- Extraction of the declared-but-not-yet-extracted keys (`values`,
  `members`, `owner`, `states`, `transitions`, `steps`, `emits`, `persists`,
  `source`, `vocabulary`) from Markdown: an engine concern owned by
  `agent-ix/quire-rs` (FR-070/FR-071 read `Properties`, `Invariants`, and
  `Operations` only); the schemas declare the keys as optional so the engine
  can fill them without a schema change.
- Editing any corpus repository or vendored fixture; the legacy-form sweep and
  corpus promotion (`agent-ix/quoin#291`).
- Application database schema generation: none is produced by these schemas.

## System Overview

### System Description

`spec-objects-business` is a Python package that publishes a Filament Module
manifest declaring nine tier-2 ObjectTypes for business / DDD modelling. The
manifest is activated against `filament-core-service` over its HTTP API, which
registers the declared archetypes, object types, grammars, and artifact types.

### Intended Users

The Filament platform (which activates and serves the contributed ObjectTypes),
spec authors (who model domains using them), and agent CLI generators such as
`minijinja-cli` (which produce artifacts from the shipped templates and schemas).

## Requirements Architecture

The requirement classes that make up this specification trace from the
stakeholder need for extractable DDD graph entities (`stakeholder/`) through
the maintainer's story of declaring those types against semantic-core
(`usecase/`) to the functional requirements (`functional/`): FR-001 activates
the manifest against `filament-core`; FR-002 emits the schemas; FR-003
declares the semantic contract in the manifest; FR-004 fixes each type's
role-distinct schema; FR-005 makes the skeletons executable fixtures. NFR-001
bounds the change to additive compatibility. Integration tests in
`integration/` verify the activation and Quoin-install boundaries. The Test
Matrix in `tests.md` records every criterion's test case.

## References

- ISO/IEC/IEEE 29148 — Requirements engineering.
- This module's source repository and `manifest.yaml`.
- `filament-core-service` FR-035 (Module Manifest Schema), the upstream
  specification this module's manifest conforms to.
- `agent-ix/filament-core-data` FR-031..FR-034 (semantic-core grammar,
  scalars, JSON Schema projection, lowering) and ADR-0005 (TypeSpec source).
- `agent-ix/quoin` FR-070..FR-075 (semantic-module contract, mappings,
  `data_schema` by digest, legacy forms, package manifests).
- `agent-ix/quire-rs` FR-069..FR-072 (contract at load, typed Properties,
  clauses and operations, extraction surface).
