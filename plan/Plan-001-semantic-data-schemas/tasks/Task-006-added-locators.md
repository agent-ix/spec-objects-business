---
id: Task-006
title: "FR-003/FR-005 — required:false locators for the sections the skeletons introduced"
type: Task
status: done
track: A
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-005
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-023
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-025
    type: verifies
---
# Task-006: FR-003/FR-005 — the added locators

## Scope

Add one `required: false` `section_body` locator per `## Properties`, `## Invariants`
and `## Operations` section the rewritten skeletons introduced, so every section a
skeleton carries is asserted by the manifest while every existing artifact stays valid.

## Subtasks

- [ ] **Add the locators.** One per introduced section, on the object type that introduced it, every one `required: false`.
- [ ] **Assert the rule.** Every locator absent at 0.2.0 is `required: false` (TC-023); no 0.2.0 locator is touched.
- [ ] **Re-run the loader.** `validate_document` on every skeleton reports no `semantic.*` load failure (TC-025).
- [ ] **Regenerate.** The manifest changed, so re-run `make schemas-check` — the digests are over the schema bytes, not the manifest, but the check must stay green.

## Deliverables

- `spec_objects_business/manifest.yaml` locator additions
- Tests for TC-023 and TC-025

## Notes

- The section lands before its locator by design (the FR-003/FR-005 cycle the
  dependency review found is broken this way), so this task runs after Task-005.
- Unblocks: Task-008.
