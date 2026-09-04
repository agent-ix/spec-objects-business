---
id: FR-005
title: "Make every skeleton an executable typed fixture"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-071"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-072"
    type: "depends_on"
---
# FR-005: Make every skeleton an executable typed fixture

## Description

Every skeleton under `spec_objects_business/skeletons/` SHALL author its
declarations in the quoin FR-071/FR-072 Markdown forms (typed `## Properties`
table by default, `## Invariants` clause fences, `## Operations`
subsections) and validate through Quire against this module, accompanied by
negative fixtures that fail for a named reason, so that the skeletons are the
module's executable positive fixtures and the negatives pin what the schemas
refuse.

## Inputs

- The rewritten skeletons `skeletons/<type>.md` (one per object type) and the
  alternate-form skeletons `skeletons/entity.sysml.md`,
  `skeletons/aggregate_root.sysml.md`, `skeletons/value_object.sysml.md`.
- Negative fixtures `tests/fixtures/negative/<type>-<case>.md`, each with
  frontmatter `expect:` naming the diagnostic code or reason the fixture must
  produce.
- The Quire wheel (0.46.0 or later) exposing `extract_semantic`,
  `validate_document`, and `Registry`.

## Outputs

- A validation result per skeleton with no error and no `semantic.record-invalid`.
- A semantic record per skeleton whose `fields`, `clauses`, and `operations`
  availability match the type's required set.

## Behavior

- Each skeleton with a `fields` requirement (`entity`, `nested_entity`, `value_object`, `aggregate_root`, `event`, `process`) SHALL author `## Properties` as one table with the header exactly `Field | Type | Multiplicity | Constraints`.
- Where the `state_machine` skeleton declares context fields, it SHALL use the same typed table.
- The `entity`, `aggregate_root`, and `value_object` alternate skeletons SHALL author the same declarations as one ```` ```sysml ```` fence of `attribute <name> : <Type>[<mult>] { <constraints> }` and `ref item <name> : <Type>[<mult>]` lines.
- Each alternate skeleton SHALL share the table skeleton's frontmatter `id` and `title`, so the two extract to identical normalized `FieldDecl[]`.
- Each skeleton whose type requires or admits `clauses` (`entity`, `nested_entity`, `value_object`, `aggregate_root`, `event`, `state_machine`, `process`) SHALL author `## Invariants` with one `### <clauseId>` per clause, each owning exactly one ```` ```ocl ```` fence.
- Each skeleton whose type requires `operations` (`repository`, `state_machine`) SHALL author `## Operations` with one `### <name>` per operation, an optional `| Param | Type | Multiplicity | Constraints |` table, a `Returns:` line where the operation returns a value, and `Pre:`/`Post:` lines naming clause ids declared in the same artifact.
- Where `entity`, `aggregate_root`, `value_object`, or `process` declares operations, it SHALL use the same `## Operations` form.
- Every `Type` cell that names another skeleton SHALL use that skeleton's frontmatter `title` (an `Identifier`), so that under a bundle index built from the skeletons every non-kernel token resolves to `ix://agent-ix/spec-objects-business/type/<Title>` with no `semantic.unresolved-type` finding.
- Every skeleton SHALL keep every H2 heading whose manifest locator is `required: true` for its type.
- No skeleton SHALL carry an H2 heading the manifest does not assert.
- The `enumeration`, `domain`, `event`, `state_machine`, and `process` skeletons SHALL keep their kernel sections (`## Values` with `Value | Description`, `## Bounded Context`, the `## Schema` JSON fence as the wire representation of the declared payload, `## States & Transitions`, `## Workflow`) exactly as the manifest asserts them.
- Each negative fixture SHALL fail `validate_document` with an error whose message carries the fixture's `expect:` code, covering at least: a value object with an identity row, an entity without an identity row, an event without a `Timestamp` row, a domain with a `## Properties` table, a repository without operations, a `## Properties` section carrying both a table and a fence, an operation whose `Post:` names an undeclared clause, and a `Type` token that is not an `Identifier`.
- If the installed Quire wheel lacks `extract_semantic`, then the semantic tests SHALL skip with a message naming the missing function rather than pass vacuously.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-005-CON-1 | The module SHALL keep the skeletons and negatives in this repository only, editing no corpus repository and no vendored quoin/quire fixture. | Boundary | Inspection |
| FR-005-CON-2 | A skeleton SHALL carry one Properties form; the alternate form is a separate file, never a second block in the same artifact. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | Every skeleton file (ten types plus three alternates) passes `validate_document` against this module with `is_valid` true and no `semantic.record-invalid` error. | Test |
| FR-005-AC-2 | For `entity`, `aggregate_root`, and `value_object`, the table and `sysml` skeletons extract to identical normalized `fields` with `fieldsForm` `table` and `fence` respectively. | Test |
| FR-005-AC-3 | Under a bundle index built from the skeleton frontmatter, every skeleton extracts with zero `error` diagnostics and zero `semantic.unresolved-type` findings, and every non-kernel `type.target` starts with `ix://agent-ix/spec-objects-business/type/`. | Test |
| FR-005-AC-4 | Each skeleton's `availability` states match its type: `fields` `available` for the six field-bearing types, `operations` `available` for `repository` and `state_machine`, `clauses` `available` for `aggregate_root`, and `not_applicable` where the section is absent. | Test |
| FR-005-AC-5 | Every negative fixture fails validation with an error message containing its `expect:` code, and at least the eight cases listed in Behavior are present. | Test |
| FR-005-AC-6 | Every skeleton's H2 set equals a subset of the headings the manifest asserts for its type and includes every `required: true` heading. | Test |
| FR-005-AC-7 | The skeleton for each of the ten types has no placeholder token and every asserted section body is non-empty. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md); quoin FR-071/FR-072 (`ix://agent-ix/quoin/FR-071`, `ix://agent-ix/quoin/FR-072`); quire-rs FR-070/FR-071/FR-072
- **Downstream**: `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` consume the skeletons read-only
