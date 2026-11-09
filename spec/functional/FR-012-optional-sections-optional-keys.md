---
id: FR-012
title: "Make a record key's source section required where its construct requires the key"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-008"
    type: "depends_on"
---
# FR-012: Make a record key's source section required where its construct requires the key

## Description

The module SHALL keep three layers of one contract in agreement: the object
type's `construct:` ([FR-008](./FR-008-construct-declarations.md)), the record
schema, and the manifest locator for the section that feeds the key. Where the
construct requires a member (`fields`, `clauses` or `operations`), the schema
SHALL require the key and the locator SHALL be `required: true`, so a document
missing the section is refused as a missing section rather than as an obscure
`semantic.record-invalid`. The downstream lowering to IR enforces the construct,
so the construct is the contract.

## Inputs

- The FR-008 construct table: `nested_entity`, `aggregate_root`, `event` and
  `process` require `fields`; `aggregate_root` also requires `clauses`;
  `state_machine` requires `operations`.
- The locators `properties` (the five types above except `state_machine`),
  `invariants` (`aggregate_root`) and `operations` (`state_machine`).

## Outputs

- Those locators are `required: true`. The schemas keep requiring `fields`,
  `clauses` and `operations` for them, unchanged.

## Behavior

- A `section_body` locator reads the text directly under its heading, so a
  required section SHALL carry at least one line of prose before its first
  subsection.
- A type whose construct does not require a member SHALL NOT have the schema
  require it; no object type of this module is in that state today.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-012-CON-1 | A record schema SHALL require a key only where its construct requires the member, and then the source locator SHALL be `required: true`. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-012-AC-1 | `nested_entity`, `event` and `process` `properties`, `aggregate_root` `properties` and `invariants`, and `state_machine` `operations` locators are `required: true`, and the matching schemas still require `fields`, `clauses` and `operations`. | Test |
| FR-012-AC-2 | Each of those skeletons with the required section removed is refused with a message naming the missing required section; the skeleton validates in the skeleton suite (TC-050). | Test |
| FR-012-AC-3 | Every schema key that is required is required by the type's construct. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-006](./FR-006-model-table-locators.md), [FR-008](./FR-008-construct-declarations.md)
