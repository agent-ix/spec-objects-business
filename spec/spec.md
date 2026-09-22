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

- The Module manifest (`spec_objects_business/manifest.yaml`) and the eleven tier-2
  business ObjectTypes it contributes for DDD modelling.
- The functional requirement that the manifest activates idempotently against
  `filament-core-service`, and the integration test that verifies it.
- The semantic-module contract (issue #4): a TypeSpec source importing
  `@agent-ix/semantic-core` 0.3.0, the emitted JSON Schema per object type
  shipped under `spec_objects_business/schemas/`, the manifest `semantic`
  block with reference-form `data_schema`, and the skeletons rewritten as
  executable typed fixtures with negative counterparts.
- The object-type model tables (values, states, transitions, steps, members,
  vocabulary) declared as manifest `table_row` locators, and the mapping
  tokens for generalization, abstract types, field presence, subsetting,
  redefinition, and operation effect frames, which Quire extracts as the
  manifest directs and refuses where the manifest is silent.

### Out of Scope

- The behaviour of `filament-core-service` itself, referenced here only by the
  relationship to its manifest schema (FR-035).
- Deployment topology and cluster infrastructure, which live in the operating
  environment rather than this specification.
- Generated-language fixtures (Rust, TypeScript, Python) for the business
  types: produced by the TypeSpec frontend and compiler core
  (`agent-ix/filament-core-data#19`) and published only behind the promotion
  gate (`agent-ix/quoin#290`); the semantic-core language packages are
  `agent-ix/filament-core-data#11`. None is produced or faked here.
- Extraction of the record keys no model table declares from Markdown; the
  schemas declare them as optional so the engine can fill them without a
  schema change. Repository `persists`, event `source`, nested-entity
  `owner`, and aggregate/process `emits` are `agent-ix/quire-rs#435`, and the
  module's locators and skeleton sections for them are
  `agent-ix/spec-objects-business#9`. `relations` are extracted from the
  FR-007 `## Relationships` table.
- Inline Quire expressions in a transition `Guard` or an operation's
  `Pre:`/`Post:` lines (`agent-ix/quire-rs#433`); today those name
  clause ids only.
- Checking `quire` fence expressions mechanically: `agent-ix/quire-spec-language#133`.
  Clause validity is an Inspection (FR-006-AC-8) until that checker exists.
- Naming what a module load refused: `agent-ix/quire-rs#221` (an unknown
  manifest key empties the model silently) and `agent-ix/quire-rs#394` (a
  `data_schema` digest mismatch drops the object type with no diagnostic).
  FR-003-AC-6's "naming the key or the path" half is blocked on them and is
  carried as an explicit expected failure.
- Record validation of a legacy-form artifact that declares `object:`:
  `agent-ix/quire-rs#391` (the engine validates an `unavailable` record as
  `{}`, so a legacy form errors even under `legacy_forms: warning`).
  NFR-001-AC-2 itself holds — no 0.2.0 artifact carries `object:` — and the
  defect is carried as an explicit expected failure beside it rather than
  worked around by relaxing a schema.
- Publishing the Quire 0.46.0 wheel to an index a repository may commit
  against: `agent-ix/quire-rs#392`. `internal-pypi` serves 0.33.0 at most and
  no `quire-rs` tag carries the semantic layer, so this module provisions the
  wheel with a documented `make dev-quire` target and its semantic tests fail
  rather than skip when the engine is absent (FR-005). Declaring `quire` as a
  committed dev dependency waits on that issue.
- Resolving a reference-form `data_schema` into a stored snapshot at
  activation: `agent-ix/filament-core-service#23`. Until it lands the service
  stores the reference verbatim, which is what FR-001-AC-4 and IT-001-SC-03
  assert.
- Editing any corpus repository or vendored fixture; the legacy-form sweep and
  corpus promotion (`agent-ix/quoin#291`).
- Application database schema generation: none is produced by these schemas.

## System Overview

### System Description

`spec-objects-business` is a Python package that publishes a Filament Module
manifest declaring eleven tier-2 ObjectTypes for business / DDD modelling. The
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
role-distinct schema; FR-005 makes the skeletons executable fixtures; FR-006
declares the object-type model tables the engine extracts; FR-007 declares the
`## Relationships` table and the edge verbs its rows use; FR-008 declares each
object type's semantic IR construct; FR-009 fixes the underscore object id. NFR-001 states
where the contract is additive and why the model-table sections are strict. Integration tests in
`integration/` verify the activation and Quoin-install boundaries; the third
external boundary, the Quire engine (loader, extraction, record surface), has
no IT artifact of its own — the FR-003 and FR-005 test harness is this
module's Quire contract test, and the wheel version is pinned once in FR-005
Inputs. The Test Matrix in `tests.md` records every criterion's test case.

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
  clauses and operations, extraction surface) and FR-075 (model features).
