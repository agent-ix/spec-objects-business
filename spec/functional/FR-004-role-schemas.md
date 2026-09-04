---
id: FR-004
title: "Give every business object type a role-distinct declaration schema"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-002"
    type: "depends_on"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
---
# FR-004: Give every business object type a role-distinct declaration schema

## Description

The TypeSpec source SHALL declare one model per business object type whose
emitted schema validates that type's declaration record
`{ fields?, relations?, clauses?, operations?, … }` with type-specific
required keys, forbidden keys, and item rules, so that no type is a
placeholder and the ten DDD roles are told apart by the shape of their
records rather than by name alone.

## Inputs

- semantic-core 0.1.0 grammar models: `FieldDecl`, `RelationDecl`,
  `OperationDecl`, `ClauseRef`, `EnumValue`, `Identifier`, `SemanticId`,
  `KernelScalar`.
- The declaration record Quire assembles per artifact: `fields` from
  `## Properties`, `clauses` from `## Invariants`, `operations` from
  `## Operations` (quire-rs FR-070/FR-071), with any key absent when its
  section is absent.

## Outputs

- Ten object-type models, each emitted as `schemas/<Model>.json`, sealed
  (`unevaluatedProperties: {not: {}}`).
- Support models emitted as sibling files: `IdentityField` and
  `OccurrenceField` (open marker schemas used by `contains`), `Term`,
  `Transition`, `ProcessStep`, and the `StepKind` enum.

## Behavior

The per-type contract; "identity field" means a `FieldDecl` with
`identity: true`, "occurrence field" a `FieldDecl` whose `type.target` is
`Timestamp`.

| Object type | Model | Required keys | Optional keys | Item rules |
|---|---|---|---|---|
| domain | `Domain` | none | `members: RelationDecl[]`, `vocabulary: Term[]`, `clauses: ClauseRef[]` | `fields` and `operations` are forbidden: a domain declares a boundary, not data |
| entity | `Entity` | `fields` | `relations`, `clauses`, `operations` | `fields` has ≥ 1 item and ≥ 1 identity field |
| nested_entity | `NestedEntity` | `fields` | `owner: RelationDecl`, `clauses`, `operations` | `fields` has ≥ 1 item and ≥ 1 identity field (local to the owner); `relations` forbidden |
| value_object | `ValueObject` | `fields` | `clauses`, `operations` | `fields` has ≥ 1 item and 0 identity fields; `relations` forbidden |
| aggregate_root | `AggregateRoot` | `fields`, `clauses` | `relations`, `operations`, `members: RelationDecl[]`, `emits: SemanticId[]` | `fields` has ≥ 1 identity field; `clauses` has ≥ 1 item (the root exists to enforce invariants) |
| repository | `Repository` | `operations` | `clauses`, `persists: SemanticId[]` | `operations` has ≥ 1 item; `fields` forbidden |
| event | `Event` | `fields` | `clauses`, `source: SemanticId` | `fields` has ≥ 1 item, 0 identity fields, and ≥ 1 occurrence field; `operations` forbidden |
| state_machine | `StateMachine` | `operations` | `fields`, `states: EnumValue[]`, `transitions: Transition[]`, `clauses` | `operations` has ≥ 1 item (each transition command) |
| process | `Process` | `fields` | `steps: ProcessStep[]`, `clauses`, `operations` | `fields` has ≥ 1 item and ≥ 1 identity field (the correlation key); `relations` forbidden |
| enumeration | `Enumeration` | none | `values: EnumValue[]`, `clauses` | `fields` and `operations` forbidden |

- `Term` SHALL be `{ term: string (minLength 1), doc: string }`.
- `Transition` SHALL be `{ from: Identifier, to: Identifier, trigger: Identifier, guard?: ClauseRef, emits?: SemanticId }`.
- `ProcessStep` SHALL be `{ name: Identifier, kind: StepKind, consumes?: SemanticId[], emits?: SemanticId[], doc?: string }` with `StepKind` the closed set `command`, `event`, `decision`, `compensation`, `wait`.
- Every `fields`, `params`, `clauses`, and `operations` item SHALL be validated by `$ref` to the semantic-core 0.1.0 model, never by a copied definition.
- Every cross-reference a declaration makes (`type.target`, `RelationDecl.target`, `emits`, `persists`, `source`) SHALL be a `SemanticId` or `KernelScalar` per semantic-core, so a reference to an undeclared type is the placeholder `ix://<org>/<repo>/unresolved/<Token>` and reported by the extractor rather than silently accepted as a string.
- Each schema SHALL describe the declared shape only, never a runtime occurrence (an entity row, an emitted event instance), which is why `Event` carries no identity field and no `eventId`: occurrence identity belongs to the runtime record, not the declaration.
- Where a key is declared but the current extractor does not populate it (`members`, `vocabulary`, `owner`, `emits`, `persists`, `source`, `states`, `transitions`, `steps`, `values`), the key SHALL be optional, so a record produced by today's extractor validates and a future extractor can fill it without a schema change.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-004-CON-1 | No model SHALL redeclare a semantic-core model or scalar; the module namespace contributes archetype shapes only (semantic-core NFR-014 kernel discipline). | Architecture | Test |
| FR-004-CON-2 | A record that satisfies no required key SHALL fail every type whose required set is non-empty; the two open-required types (`Domain`, `Enumeration`) are distinguished by their forbidden and optional keys. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | Each of the ten shipped object-type schemas differs from every other in at least one required, forbidden, or item rule listed in the table; a schema with only `type: object` is absent. | Test |
| FR-004-AC-2 | An entity record with one identity field validates against `Entity.json`; the same record with the identity flag removed fails; a record with no `fields` fails. | Test |
| FR-004-AC-3 | A value-object record without identity fields validates against `ValueObject.json`; the same record with one identity field fails; a record carrying `relations` fails. | Test |
| FR-004-AC-4 | An aggregate-root record with an identity field and one clause validates; the same record without `clauses` fails. | Test |
| FR-004-AC-5 | An event record with a `Timestamp` field and no identity field validates against `Event.json`; a record whose only fields are non-`Timestamp` fails; a record with an identity field fails; a record with `operations` fails. | Test |
| FR-004-AC-6 | A repository record with one operation and no fields validates; a record with `fields` fails; a record with an empty `operations` array fails. | Test |
| FR-004-AC-7 | A state-machine record with one operation validates, with `states` and `transitions` accepted when present; a transition missing `trigger` fails. | Test |
| FR-004-AC-8 | A process record with an identity field validates, with `steps` accepted when present; a step whose `kind` is outside `StepKind` fails. | Test |
| FR-004-AC-9 | Empty records `{}` validate against `Domain.json` and `Enumeration.json` and fail against every other type; a domain or enumeration record with `fields` fails. | Test |
| FR-004-AC-10 | A `type.target` of `ix://agent-ix/spec-objects-business/unresolved/Mystery` is accepted by the schema (it is a `SemanticId`) and reported by the extractor as `semantic.unresolved-type`; a bare `Mystery` string is rejected by the schema. | Test |

## Dependencies

- **Upstream**: [FR-002](./FR-002-emitted-json-schemas.md); semantic-core FR-031 (`ix://agent-ix/filament-core-data/FR-031`)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md); `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` read these schemas as fixtures
