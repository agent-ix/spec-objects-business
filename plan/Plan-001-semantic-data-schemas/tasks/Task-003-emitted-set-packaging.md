---
id: Task-003
title: "FR-002 — emitted set and packaging"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-011
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-010
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-011
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-012
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-015
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-071
    type: verifies
---
# Task-003: FR-002 — emitted set and packaging

## Scope

The emitted-set half of FR-002: run the generator over the finished models, commit the
seventeen schema files it produces, and make them ship in both distribution channels.

## Subtasks

- [ ] **Generate and commit.** `make schemas` produces `spec_objects_business/schemas/` with the ten object-type models plus `IdentityField`, `OccurrenceField`, `OccurrenceTypeRef`, `Term`, `Transition`, `ProcessStep` and `StepKind`. No output digest and no `toolchain.json` is written.
- [ ] **Assert the shipped bytes.** Every schema declares the 2020-12 `$schema` and an `$id` matching its file name under the base whose version segment is read from `manifest.yaml`; every `$ref` names a shipped sibling or semantic-core 0.1.0 and nothing else.
- [ ] **Wheel packaging.** `pyproject.toml` `include` gains `spec_objects_business/schemas/*.json` for both sdist and wheel.
- [ ] **npm packaging.** Confirm `scripts/stage-npm.mjs` stages `schemas/` beside `manifest.yaml` (it already lists it in `PAYLOAD`) and that `package.json` `files` ships it; assert over a real `npm pack` tarball.

## Deliverables

- `spec_objects_business/schemas/*.json`, committed
- `pyproject.toml` include entry
- Tests for TC-010, TC-011, TC-012, TC-015, TC-071

## Notes

- The manifest references these files by path only; no digest is recorded.
- Unblocks: Task-004.
