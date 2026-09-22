---
id: US-001
title: "Declare business object types against semantic-core"
type: US
relationships:
  - target: "ix://agent-ix/spec-objects-business/StR-001"
    type: "traces_to"
---
# US-001: Declare business object types against semantic-core

## Story

**As a** maintainer of the business object module
**I want** every business object type (domain, entity, value object, aggregate root, nested entity, repository, event, state machine, process, enumeration) to carry a real structural contract expressed in the shared semantic-core grammar
**So that** spec authors write one typed `## Properties` table per object, reviewers and generators read one declaration record per object, and the same record validates identically in Quire, Quoin, and the compiler.

The story is stated from the maintainer's perspective and does not prescribe
the emitter, the file layout, or the extraction engine.

## Context

Today every object type in `manifest.yaml` carries `data_schema: {type: object}`,
which types nothing: an entity and an enumeration are indistinguishable to a
consumer, `## Properties` is free prose, and no cross-reference between two
objects is checked. The semantic-core grammar
(`agent-ix/filament-core-data#35`) and the semantic-module contract
(`agent-ix/quoin#293`, `agent-ix/quire-rs#388`) now exist and are merged; this
module is the first read-only fixture source for the downstream frontends
(`agent-ix/quire-contract-ir#52`, `agent-ix/filament-core-data#36`).

## Acceptance Examples (Illustrative)

These examples clarify the maintainer's expectations. They are illustrative
only, not test cases and not verification criteria.

### US-001-EX-1: An entity skeleton extracts to typed fields

- **Given** the `entity` skeleton with a `| Field | Type | Multiplicity | Constraints |` table
- **When** Quire extracts it under this module
- **Then** the record carries one `FieldDecl` per row, the identity row is flagged, and the record validates against the shipped `Entity.json`

### US-001-EX-2: A value object with an identity field is refused

- **Given** a value-object artifact whose table marks a row `identity`
- **When** Quire validates it
- **Then** validation fails naming the value-object schema, because a value object has no identity of its own

### US-001-EX-3: The module installs into Quoin

- **Given** the packaged module directory
- **When** an operator runs `quoin module install path:<dir>`
- **Then** the install succeeds, every exported schema digest matches, and the module is listed

## Options (Exploratory)

Approaches discussed: hand-authoring one JSON Schema per type; generating the
schemas from a TypeSpec package that imports `@agent-ix/semantic-core`;
deriving the schemas from the skeletons. Only the TypeSpec route keeps one
source for the grammar and its vocabulary; it is the route the authoring
contract on the ticket already names.

## Constraints (Contextual)

No corpus repository may be edited; existing `body_extraction` locators stay
as they are so current artifacts keep extracting; the change is advisory until
corpus promotion. This context is not binding here and is refined in the
functional and non-functional requirements.

## Dependencies (Contextual)

Upstream: semantic-core 0.3.0 on GitHub Packages, the module-manifest schema
with the `semantic` block, Quire 0.47.1 with `extract_semantic`. Downstream: the
frontends that read this module's skeletons as fixtures.

## Priority and Risk (Informative)

P1 on the Track A programme. The risk if unmet is that the downstream
frontends have no business-object fixture and the typed-properties migration
has no reference module.

## Notes (Informative)

Open question captured for later analysis: which sections beyond
`## Properties`, `## Invariants`, and `## Operations` the extraction engine
should read (`## Values`, `## Relationships`, states, steps). The schemas
declare those keys; extraction of them is an engine concern.

## Traceability (Informative)

Traces to [StR-001](../stakeholder/StR-001-module-activation.md); implemented
by [FR-002](../functional/FR-002-emitted-json-schemas.md),
[FR-003](../functional/FR-003-semantic-manifest-contract.md),
[FR-004](../functional/FR-004-role-schemas.md), and
[FR-005](../functional/FR-005-executable-skeletons.md).
