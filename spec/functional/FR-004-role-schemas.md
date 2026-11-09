---
id: FR-004
title: "Give every business object type a role-distinct declaration schema"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
---
# FR-004: Give every business object type a role-distinct declaration schema

## Description

The TypeSpec source SHALL declare one model per business object type whose
emitted schema validates that type's declaration record
`{ fields?, relations?, clauses?, operations?, … }` with type-specific
required keys, forbidden keys, and item rules, so that no type is a
placeholder and each DDD role refuses the records that violate its own
rules; full pairwise disjointness is not claimed, because the keys that
would separate a minimal entity from a nested entity or a process (`owner`,
`steps`) are not yet populated by the extractor.

## Inputs

- semantic-core grammar models: `FieldDecl`, `RelationDecl`,
  `OperationDecl`, `ClauseRef`, `EnumValue`, `Identifier`, `SemanticId`,
  `KernelScalar`.
- The declaration record Quire assembles per artifact: `fields` from
  `## Properties`, `clauses` from `## Invariants`, `operations` from
  `## Operations` (quire-rs FR-070/FR-071), with any key absent when its
  section is absent.

## Outputs

- Eleven object-type models, each emitted as `schemas/<Model>.json`, sealed
  (`unevaluatedProperties: {not: {}}`).
- Support models emitted as sibling files: `IdentityField`, `OccurrenceField`,
  and `OccurrenceTypeRef` (open marker schemas used by `contains`), `Term`,
  `Transition`, `ProcessStep`, `PopulationMember`, and the `StepKind` enum.

## Behavior

Each model SHALL enforce its row of the following table. "Identity field"
means a `FieldDecl` with `identity: true`; "occurrence field" a `FieldDecl`
whose `type.target` is `Timestamp`. Both readings are semantic-core
reader conventions (the flag is set only by a bare `identity` keyword in a
Constraints cell and is absent, not `false`, otherwise; the kernel scalar is
the bare token `Timestamp`), so a semantic-core release that renders
`identity: false` or namespaces kernel scalars is a breaking change to these
schemas and SHALL be handled by a manifest version bump, not by widening a
rule. Where a row admits "≥ 1 identity field", two or more identity rows are
admitted: a composite key is a legitimate declaration and no rule forbids it.

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
| process | `Process` | `fields` | `steps: ProcessStep[]`, `clauses`, `operations`, `emits: SemanticId[]` | `fields` has ≥ 1 item and ≥ 1 identity field (the correlation key); `relations` forbidden |
| enumeration | `Enumeration` | none | `values: EnumValue[]`, `clauses` | `fields` and `operations` forbidden |
| population | `Population` | none | `members: PopulationMember[]`, `extent`, `clauses` | `extent`, when present, is `closed` or `open`; `fields` and `operations` forbidden: a population declares which instances exist together, not data |
| variant_set | `VariantSet` | none | `variants: VariantDecl[]`, `clauses` | `fields` and `operations` forbidden; see [FR-010](./FR-010-variant-set-and-graph.md) |
| graph | `Graph` | none | `clauses` | `fields`, `operations`, `states` and `transitions` forbidden; see [FR-010](./FR-010-variant-set-and-graph.md) |

- `Term` SHALL be `{ term: string (minLength 1), doc: string }`.
- `Transition` SHALL be `{ from: Identifier, to: Identifier, trigger: Identifier, guard?: ClauseRef, guardExpression?: Expression, emits?: SemanticId }`, with `guard` and `guardExpression` mutually exclusive (a not-both-present constraint in `Transition.json`).
- `PopulationMember` SHALL be `{ type: TypeRef }`, sealed: a member carries no multiplicity. The population's one `extent` (`PopulationExtent`, the closed set `closed`, `open`) is authored as frontmatter and checked by the engine (`semantic.invalid-model-cell` when missing or invalid); the declaration record the engine builds omits it, so `Population.json` declares it optional.
- `Expression` SHALL be `{ kind: "expression", text: string (minLength 1), sourceSpan: SourceLocus }`, sealed: an inline Quire expression carried opaquely, as quire-rs FR-071 and FR-075 emit it.
- `OperationExpression` SHALL be `{ operation: Identifier, slot: pre | post, expression: Expression }`, sealed. `Entity`, `NestedEntity`, `AggregateRoot`, `StateMachine`, and `Process` SHALL each admit an optional `operationExpressions: OperationExpression[]` beside `operations`, because `OperationDecl.pre` and `post` carry clause references only. `Repository` admits none: its operations carry no contract. `operation` names an `operations[].name` of the same record, a reader rule JSON Schema does not express.
- `ProcessStep` SHALL be `{ name: Identifier, kind: StepKind, consumes?: SemanticId[], emits?: SemanticId[], doc?: string }` with `StepKind` the closed set `command`, `event`, `decision`, `compensation`, `wait`.
- Every `fields`, `params`, `clauses`, `operations`, `relations`, `members`, `owner`, `values`, and `states` item SHALL be validated by `$ref` to the semantic-core model, never by a copied definition.
- The TypeSpec source SHALL express the item rules through the official emitter's decorators over open marker models: `@contains(IdentityField)` for "≥ 1 identity field", `@contains(IdentityField) @minContains(0) @maxContains(0)` for "0 identity fields", and, because JSON Schema admits one `contains` per array, the event occurrence rule as an `@extension("allOf", …)` clause whose `contains` references `OccurrenceField.json` (a marker whose `type.target` is `Timestamp`); the generator normalizes that relative `$ref` per FR-002.
- Every cross-reference a declaration makes (`type.target`, `RelationDecl.target`, `emits`, `persists`, `source`, `Transition.emits`, `ProcessStep.consumes`/`emits`) SHALL be a `SemanticId` or `KernelScalar` per semantic-core, so a bare token is rejected by the schema; resolution against the bundle, and the placeholder `ix://<org>/<repo>/unresolved/<Token>` with its `semantic.unresolved-type` finding, exist today for `type.target` only (quire-rs FR-070) and for the other keys once `agent-ix/quoin#335` publishes their mapping.
- Each schema SHALL describe the declared shape only, never a runtime occurrence (an entity row, an emitted event instance), which is why `Event` carries no identity field and no `eventId`: occurrence identity belongs to the runtime record, not the declaration.
- Where a key is declared but the current extractor does not populate it (`members`, `vocabulary`, `owner`, `emits`, `persists`, `source`, `states`, `transitions`, `steps`, `values`) — and likewise `relations` — the key SHALL be optional, so a record produced by today's extractor validates and a future extractor can fill it without a schema change.
- The test suite SHALL verify every criterion over a key the extractor does not populate against a hand-built JSON record rather than an extracted one, naming that limitation in the test itself, so that no row claims extraction evidence it does not have; the extraction path for those keys is `agent-ix/quoin#335` (mapping) and its quire-rs successor.
- A `Transition` SHALL name a `states[].value` of the same record in `from` and in `to`, and an `operations[].name` of the same record in `trigger`. JSON Schema cannot express either rule, so both are reader rules stated here for the extractor that first populates `states` and `transitions`; neither is claimed as a schema refusal.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-004-CON-1 | No model SHALL redeclare a semantic-core model or scalar; the module namespace contributes archetype shapes only (semantic-core NFR-014 kernel discipline). | Architecture | Test |
| FR-004-CON-2 | The empty record `{}` SHALL fail every type whose required set is non-empty and pass only `Domain`, `Enumeration`, and `Population`, which are distinguished from each other by their optional keys alone. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | Each shipped object-type schema differs from every other in at least one required, forbidden, or item rule listed in the table; a schema with only `type: object` is absent. | Test |
| FR-004-AC-2 | An entity record with one identity field validates against `Entity.json`; the same record with the identity flag removed fails; a record with no `fields` fails. | Test |
| FR-004-AC-3 | A value-object record without identity fields validates against `ValueObject.json`; the same record with one identity field fails; a record carrying `relations` fails. | Test |
| FR-004-AC-4 | An aggregate-root record with an identity field and one clause validates; the same record without `clauses` fails. | Test |
| FR-004-AC-5 | An event record with a `Timestamp` field and no identity field validates against `Event.json`; a record whose only fields are non-`Timestamp` fails; a record with an identity field fails; a record with `operations` fails. | Test |
| FR-004-AC-6 | A repository record with one operation and no fields validates; a record with `fields` fails; a record with an empty `operations` array fails. | Test |
| FR-004-AC-7 | A state-machine record with one operation validates, with `states` and `transitions` accepted when present; a transition missing `trigger` fails; a transition carrying a `guardExpression` expression record validates, and a transition carrying both `guard` and `guardExpression` fails; one whose expression lacks `text` or has a `kind` other than `expression` fails. | Test |
| FR-004-AC-8 | A process record with an identity field validates, with `steps` and `emits` accepted when present; a step whose `kind` is outside `StepKind` fails. | Test |
| FR-004-AC-9 | Empty records `{}` validate against `Domain.json`, `Enumeration.json`, `Population.json`, `VariantSet.json`, and `Graph.json` and fail against every other type; a domain, enumeration, or population record with `fields` fails; a population record with `extent` outside `closed`/`open` fails, and a `members` list of population members, each carrying only `type`, validates only against `Population.json`; a member carrying `extent` fails. | Test |
| FR-004-AC-10 | A `type.target` of `ix://agent-ix/spec-objects-business/unresolved/Mystery` is accepted by the schema (it is a `SemanticId`) and reported by the extractor as `semantic.unresolved-type`; a bare `Mystery` string is rejected by the schema. | Test |
| FR-004-AC-11 | A nested-entity record with one identity field validates against `NestedEntity.json`, with `owner` accepted when present; a record carrying `relations` fails. | Test |
| FR-004-AC-12 | An entity, nested-entity, aggregate-root, state-machine, or process record carrying `operationExpressions` entries `{ operation, slot, expression }` with `slot` `pre` or `post` validates against its own schema; an entry with `slot` outside `pre`/`post`, or one missing `expression`, fails; `Repository.json` refuses `operationExpressions`. | Test |

## Dependencies

- **Upstream**: semantic-core FR-031 (`ix://agent-ix/filament-core-data/FR-031`)
- **Build**: [FR-002](./FR-002-emitted-json-schemas.md) emits these models
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md); `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` read these schemas as fixtures
