---
id: FR-012
title: "Require a record key in the schema exactly where its construct requires the member"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-008"
    type: "depends_on"
---
# FR-012: Require a record key in the schema exactly where its construct requires the member

## Description

Each record schema SHALL require a key exactly when the object type's
`construct:` ([FR-008](./FR-008-construct-declarations.md)) requires the matching
member, because the downstream lowering to IR enforces the construct.

## Inputs

- The FR-008 construct table: `entity`, `value_object`, `nested_entity`,
  `aggregate_root`, `event` and `process` require `fields`; `aggregate_root` also
  requires `clauses`; `repository` and `state_machine` require `operations`.
- The manifest locators `properties`, `invariants` and `operations`, which stay
  `required: false` where they are today: a `section_body` locator reads only the
  text directly under its heading, so making one required would refuse a valid
  document whose section holds only `###` subsections.

## Behavior

- The record validator SHALL refuse a document that lacks a member its construct
  requires, as `semantic.record-invalid ... is a required property`.
- The extractor SHALL count a section that holds only `###` subsections as present,
  because the locator stays optional and the record key comes from the subsections.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-012-CON-1 | The schema of an object type SHALL require a key only when the construct of that type requires the matching member. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | Every schema key that a record schema requires is a member its construct requires, and `NestedEntity`, `AggregateRoot`, `Event`, `Process` and `StateMachine` still require `fields`, `clauses` and `operations` respectively. | Test |
| FR-012-AC-2 | The `nested_entity`, `aggregate_root` and `event` skeletons without `## Properties`, and the `aggregate_root` skeleton without `## Invariants`, are refused with a `semantic.record-invalid` message naming the required property. | Test |
| FR-012-AC-3 | A `state_machine` whose `## Operations` section holds only `###` subsections, with no prose under the heading, validates. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-008](./FR-008-construct-declarations.md)
