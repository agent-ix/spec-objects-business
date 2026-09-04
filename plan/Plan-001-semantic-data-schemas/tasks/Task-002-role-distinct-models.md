---
id: Task-002
title: "FR-004 — the ten role-distinct models and six support models"
type: Task
status: not_started
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-001
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-business/US-001
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-030
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-031
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-032
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-033
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-034
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-035
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-036
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-037
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-038
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-039
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-040
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-041
    type: verifies
---
# Task-002: FR-004 — the ten role-distinct models and six support models

## Scope

Declare in `typespec/main.tsp` one model per business object type whose emitted schema
validates that type's declaration record, plus the support models the item rules and
the optional keys need. No type may remain a placeholder.

## Subtasks

- [ ] **Ten object-type models.** `Domain`, `Entity`, `NestedEntity`, `ValueObject`, `AggregateRoot`, `Repository`, `Event`, `StateMachine`, `Process`, `Enumeration` — each sealed with `unevaluatedProperties: {not: {}}` and each carrying the required, optional and forbidden keys of the FR-004 table.
- [ ] **Support models.** `IdentityField`, `OccurrenceField`, `OccurrenceTypeRef` (open markers used by `contains`), `Term`, `Transition`, `ProcessStep`, and the `StepKind` closed enum.
- [ ] **Item rules through official decorators.** `@contains(IdentityField)` for "≥ 1 identity field"; `@contains(IdentityField) @minContains(0) @maxContains(0)` for "0 identity fields"; the event occurrence rule as an `@extension("allOf", …)` clause whose `contains` references `OccurrenceField.json`, because JSON Schema admits one `contains` per array.
- [ ] **Every grammar item by `$ref`.** `fields`, `params`, `clauses`, `operations`, `relations`, `members`, `owner`, `values` and `states` reference the semantic-core 0.1.0 model; nothing is copied (FR-004-CON-1).
- [ ] **Forward compatibility.** Every key the current extractor does not populate is optional, so today's records validate and a future extractor fills them without a schema change.
- [ ] **Record fixtures.** Positive and negative JSON records per type, validated against the emitted files with a 2020-12 validator.

## Deliverables

- `typespec/main.tsp` with sixteen models plus the `StepKind` enum
- `tests/` record fixtures and the TC-030..TC-041 assertions

## Notes

- FR-004 claims role-distinct *rules*, not pairwise record disjointness; do not add a
  discriminating required key to force disjointness — the keys that would separate a
  minimal entity from a nested entity or a process are the ones the extractor does not
  populate, which FR-004 requires to stay optional.
- Criteria over unpopulated keys (`owner`, `steps`, `states`, `transitions`,
  `relations`, `members`, `values`, `emits`, `persists`, `source`, `vocabulary`) are
  verified with hand-built records, and each such test must say so in its docstring:
  they are schema evidence, not extraction evidence.
- `Transition.from`/`to` naming a `states[].value` and `trigger` naming an
  `operations[].name` are reader rules the schema cannot express; state them, do not
  claim them as refusals.
- The identity flag and the bare `Timestamp` kernel token are semantic-core 0.1.0
  reader conventions; a change upstream is a breaking change handled by a version
  bump, not by widening a rule here.
- Unblocks: Task-011 (the gate), Task-003 (the emitted set), Task-005 (what the
  negatives pin).
