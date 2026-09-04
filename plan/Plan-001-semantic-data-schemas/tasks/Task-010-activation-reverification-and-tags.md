---
id: Task-010
title: "FR-001/StR-001 — activation re-verification and trace tags"
type: Task
status: done
track: B
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-business/StR-001
    type: references
  - target: ix://agent-ix/spec-objects-business/IT-001
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-001
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-002
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-003
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-004
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-005
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-006
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-075
    type: verifies
---
# Task-010: FR-001/StR-001 — activation re-verification and trace tags

## Scope

The manifest changed, so re-verify that it is still an FR-035-valid manifest and still
activates; and make every test in this repository bind to the matrix.

## Subtasks

- [ ] **TC-001.** `quire.validate_manifest` accepts the 0.3.0 manifest against the vendored FR-035 schema at revision `a77f31e`.
- [ ] **Trace tags.** Every test landed on this branch, and the pre-existing tests in `tests/test_basic.py`, `tests/test_manifest.py` and `tests/test_skeletons_and_validate.py`, carry the repository's declared trace-tag form so `quire coverage` binds their TC rows. Today the census is 13 symbols, 0 tagged.
- [ ] **TC-002..TC-004 (environment-gated).** Activation, re-activation and registry reads against a running filament-core-service at `a77f31e` or later; the registered `data_schema` of each exported type is the reference object as posted, while `agent-ix/filament-core-service#23` is open.
- [ ] **TC-005, TC-006, TC-075 (stakeholder demonstrations).** Activation registers the declared contents; a generator produces an artifact that validates against the shipped skeletons and schemas; every object type carries a typed schema a fixture reader can consume, with an entity and an enumeration record distinguishable by schema alone.

## Deliverables

- Trace tags across the whole `tests/` tree
- Tests/rows for TC-001..TC-006 and TC-075

## Notes

- TC-002..TC-004 stay environment-gated and their status column says so; that is
  pre-existing debt from issue #1, not this issue's.
- Do not mark an environment-gated row green from a local run against a stale service.
