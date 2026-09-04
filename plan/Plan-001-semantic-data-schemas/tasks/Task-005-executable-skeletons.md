---
id: Task-005
title: "FR-005 — executable skeletons, sysml alternates and negative fixtures"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-business/US-001
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-050
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-051
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-052
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-053
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-054
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-055
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-056
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-057
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-059
    type: verifies
---
# Task-005: FR-005 — executable skeletons, sysml alternates and negative fixtures

## Scope

Rewrite the ten skeletons as the module's executable positive fixtures in the quoin
FR-071/FR-072 Markdown forms, add three `sysml` alternates, and add the eight negative
fixtures that pin what the schemas and the engine refuse.

## Subtasks

- [ ] **Typed `## Properties`.** One table with the header exactly `Field | Type | Multiplicity | Constraints` on `entity`, `nested_entity`, `value_object`, `aggregate_root`, `event`, `process`, and on `state_machine` where it declares context fields.
- [ ] **Three alternates.** `entity.sysml.md`, `aggregate_root.sysml.md`, `value_object.sysml.md`: the same declarations as one ```sysml``` fence of `attribute` / `ref item` lines, under the table skeleton's `id` and `title`.
- [ ] **`## Invariants`.** Exactly seven skeletons, one `### <clauseId>` per clause, each owning exactly one ```ocl``` fence. `domain`, `repository`, `enumeration` carry none.
- [ ] **`## Operations`.** `repository` and `state_machine` (and any type that declares operations): one `### <name>` per operation, an optional param table, a `Returns:` line where a value is returned, optional `Pre:`/`Post:` naming clause ids declared in the same artifact.
- [ ] **Frontmatter.** `object: <type name>` beside `type: <type name>` in every skeleton, because Quire runs the semantic layer on the `object:` archetype. Every `title` an `Identifier`, distinct across the skeletons, outside the `KernelScalar` names.
- [ ] **Kernel sections kept.** `## Values`, `## Bounded Context`, `## Schema`, `## States & Transitions`, `## Workflow`, `## Members`, `## Parent` with the heading, columns and fence language the manifest asserts; where a kernel section and a typed section describe the same facts the typed section is the authority and the kernel section a derived view.
- [ ] **Eight negatives** under `tests/fixtures/negative/`, each with an `expect:` code: value object with an identity row, entity without one, event without a `Timestamp` row, domain with a `## Properties` table, repository whose `## Operations` declares none (`semantic.record-invalid`); both forms in one Properties section (`semantic.properties-both-forms`); `Post:` naming an undeclared clause (`semantic.dangling-clause-ref`); a non-`Identifier` `Type` token (`semantic.invalid-type-token`).

## Deliverables

- Ten rewritten skeletons plus three alternates under `spec_objects_business/skeletons/`
- Eight fixtures under `tests/fixtures/negative/`
- Tests for TC-050..TC-057 and TC-059

## Notes

- FR-005-AC-1 runs under `validate_document` against the module; FR-005-AC-3 runs under
  `extract_semantic` with a bundle index built from the skeleton frontmatter. They are
  different resolution paths — assert each under its own.
- A negative fixture must fail for its own reason: assert the failing schema path or
  diagnostic detail, not the code alone, since five of the eight surface as
  `semantic.record-invalid`.
- FR-005-CON-1: skeletons and negatives live in this repository only. No corpus
  repository and no vendored quoin/quire fixture is touched.
- Unblocks: Task-006, Task-008.
