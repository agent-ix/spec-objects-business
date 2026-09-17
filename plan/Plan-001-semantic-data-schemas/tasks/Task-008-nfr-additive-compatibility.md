---
id: Task-008
title: "NFR-001 — additive-compatibility verification"
type: Task
status: done
track: C
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-006
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/Task-007
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-060
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-061
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-062
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-063
    type: verifies
---
# Task-008: NFR-001 — additive-compatibility verification

## Scope

Prove that 0.3.0 is additive over 0.2.0 for the population the NFR measures: the
checked-in 0.2.0 skeleton set and every 0.2.0 locator definition.

## Subtasks

- [ ] **TC-060.** Every 0.2.0 `body_extraction` locator is present at 0.3.0 with identical facets, compared structurally against the frozen baseline. Zero changed.
- [ ] **TC-061.** Every checked-in 0.2.0 skeleton validates under 0.3.0 with zero error findings — an explicit expected failure while `agent-ix/quire-rs#391` is open, because the engine validates the declaration record of a legacy-form artifact as `{}` and `Entity.json` requires `fields`. Name the issue in the marker; do not relax the schema and do not turn the criterion into a skip.
- [ ] **TC-062.** Each 0.2.0 skeleton carrying a legacy-form `## Properties` yields exactly one `semantic.legacy-properties-form` warning.
- [ ] **TC-063.** Each such skeleton's extracted `properties` string is byte-identical under 0.2.0 and 0.3.0.

## Deliverables

- Tests for TC-060..TC-063 against the frozen baseline

## Notes

- The criterion stands and the test is red-by-declaration; that is the honest state
  while the engine defect is open. If TC-061 starts passing, `agent-ix/quire-rs#391`
  has landed — remove the expected-failure marker and the blocked note in `tests.md`
  in the same change.
- `legacy_forms: warning` is the manifest posture; nothing here promotes a legacy form
  to an error.
