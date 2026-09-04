---
id: Task-011
title: "Gate — Entity, ValueObject and Event end-to-end through the real validator"
type: Task
status: not_started
track: Gate
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-031
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-032
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-034
    type: verifies
---
# Task-011: Gate — three types end-to-end

## Scope

Validate the one assumption the other seven types are built on: that the item-rule
encoding survives the round trip from TypeSpec decorators through the official emitter
to a real 2020-12 validator, with the schemas sealed.

## Subtasks

- [ ] **Measure.** For `Entity`, `ValueObject` and `Event` only: emit, then validate the positive record and every named negative against the emitted file.
- [ ] **Pass criteria.** `Entity` accepts a one-identity-field record and refuses the same record with the flag removed and the record with no `fields`; `ValueObject` accepts a no-identity record and refuses one identity field and any `relations`; `Event` accepts a `Timestamp` field with no identity field and refuses a non-`Timestamp`-only record, an identity field, and `operations`.
- [ ] **If it fails.** Investigate in this order: whether `@minContains(0) @maxContains(0)` emits the "exactly zero" encoding at all; whether the validator honours two `contains` predicates over one array through `allOf`; whether `unevaluatedProperties: {not: {}}` interacts with a `$ref` sibling as expected. Do not author the remaining seven types against an encoding that failed here, and do not weaken a rule to make the gate pass.

## Deliverables

- A green run of the three types' positive and negative record fixtures
- A recorded note in the plan log stating which encodings were confirmed

## Notes

- This gate exists because the identity and occurrence rules are the only thing that
  makes the ten roles distinct, and none of the three mechanisms they rest on has been
  prototyped in this repository.
- Unblocks: Task-003, and the authoring of the remaining seven types' rules.
