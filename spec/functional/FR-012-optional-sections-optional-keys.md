---
id: FR-012
title: "Require a declaration key only when its source section is required"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-006"
    type: "depends_on"
---
# FR-012: Require a declaration key only when its source section is required

## Description

An object type's declaration schema SHALL NOT require a record key whose source
section the same module's manifest locator marks optional (`required: false`),
so that a document satisfying every mandatory locator is not refused as
`semantic.record-invalid` for a key it was allowed to omit.

## Inputs

- The manifest locators `properties` and `invariants` of `nested_entity`,
  `aggregate_root`, `event` and `process`, and `operations` of `state_machine`,
  all `required: false`.
- The declaration record Quire assembles per artifact, which omits a key whose
  section is absent ([FR-004](./FR-004-role-schemas.md) Inputs).

## Outputs

- `NestedEntity`, `AggregateRoot`, `Event`, `StateMachine` and `Process` list no
  required key.
- `Entity`, `ValueObject` and `Repository` still require `fields` or
  `operations`: their `properties` and `operations` locators are `required: true`.

## Behavior

- A key made optional here keeps every item rule it had: `minItems`, `contains`
  and the `Event` occurrence-field rule apply to the key whenever it is present.
- The absence of `fields`, `clauses` or `operations` is a valid declaration, not
  a defect.
- Locators and `construct:` declarations stay as they are.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-012-CON-1 | A schema SHALL require a record key only where a required manifest locator feeds it: `Entity` and `ValueObject` through `properties`, `Repository` through `operations`. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | A record lacking `fields` (`NestedEntity`, `AggregateRoot`, `Event`, `Process`), `clauses` (`AggregateRoot`) or `operations` (`StateMachine`) validates against that type's schema. | Test |
| FR-012-AC-2 | A present key is still checked: an empty `clauses` or `fields` array, an `Event` without an occurrence field, a `Process` without an identity field, or an empty `operations` array fails. | Test |
| FR-012-AC-3 | Exactly `Entity.json`, `ValueObject.json` and `Repository.json` still list a required key, and the `properties` locators of the first two and the `operations` locator of the third are `required: true`. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-006](./FR-006-model-table-locators.md)
