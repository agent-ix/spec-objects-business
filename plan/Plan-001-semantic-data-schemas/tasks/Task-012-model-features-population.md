---
id: Task-012
title: "FR-006 — model tables, the population type and manifest 0.4.0"
type: Task
status: in_progress
track: D
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-008
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-006
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-business/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-080
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-081
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-082
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-083
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-084
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-085
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-086
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-087
    type: verifies
---
# Task-012: FR-006 — model tables, the population type and manifest 0.4.0

## Scope

Declare every object-type model table quire-rs FR-075 extracts as a manifest
`table_row` locator, add the `population` object type, and bring the manifest to
0.4.0 against semantic-core 0.2.0 with `compatibility_posture: strict`.

## Subtasks

- [ ] **Locators.** The eight FR-006 model-table locators, full column lists until `agent-ix/filament-core-service#31` admits `optional_columns`.
- [ ] **Population.** `Population` and `PopulationMember` in `typespec/main.tsp`, regenerated schemas, the `population` object type with a required `Members` table, a skeleton, a positive fixture and a duplicate-type negative.
- [ ] **Clauses.** Every skeleton and fixture clause valid Quire per FR-006 (TC-084 Inspection).
- [ ] **Edges.** `specializes` declared in the manifest `edge_types` (TC-086).
- [ ] **Negatives.** One refusing fixture per model table, including process `## States` (TC-083).

## Deliverables

- `manifest.yaml` 0.4.0, 19 schemas, 14 skeletons, 20 negative fixtures
- Tests for TC-080..TC-083 and TC-085..TC-087

## Notes

- Inline guard expressions: `agent-ix/quire-rs#433`. Fence model alias:
  `agent-ix/quire-specification#84`. Extraction of `persists`, `source`,
  `owner`, `emits`: `agent-ix/quire-rs#435` and `agent-ix/spec-objects-business#9`.
