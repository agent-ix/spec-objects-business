---
id: Task-013
title: "FR-007 — the Relationships table and manifest 0.5.0"
type: Task
status: in_progress
track: D
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-012
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-007
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-business/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-089
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-090
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-091
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-092
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-093
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-094
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-095
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-096
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-097
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-098
    type: verifies
---
# Task-013: FR-007 — the Relationships table and manifest 0.5.0

## Scope

Declare the quoin FR-104 `## Relationships` table on the object types whose
record admits `relations` (`entity`, `aggregate_root`), declare every
`allowed_links` verb in `edge_types`, and bring the manifest to 0.5.0.
Issue `agent-ix/spec-objects-business#9`, relations half; the `persists`,
`source`, `owner` and `emits` half waits on `agent-ix/quire-rs#435`.

## Subtasks

- [ ] **Mapping.** `relationships` in `semantic.mappings`; manifest and `@jsonSchema` base 0.5.0 with regenerated schemas and digests.
- [ ] **Locators.** The `relationships` `table_row` locator on `entity` and `aggregate_root` (TC-089).
- [ ] **Edges.** The fifteen domain verbs in `edge_types`, identical to `agent-ix/spec-artifacts-iso` (TC-089).
- [ ] **Skeletons.** A `## Relationships` table in both `aggregate_root` skeletons (TC-090).
- [ ] **Fixtures.** An entity positive fixture (TC-091) and unknown-verb, inverse-verb, target-not-allowed and bad-multiplicity negatives (TC-092).
- [ ] **Breaking scope.** Header-only (TC-093), sealed-type table (TC-094), list-form and prose-only sections (TC-095), and the no-bundle-index target limit (TC-096); NFR-001 declares the module-wide break.
- [ ] **Typed keys.** The `relationships` locator on `process` and `repository`, `emits` on the `Process` record, TC-097 as a per-type expected failure on `agent-ix/quire-rs#435` (typed key, `relationSources`, header-only), and TC-098 pinning today's `semantic.record-invalid` blocker.

## Deliverables

- `manifest.yaml` 0.5.0, 19 schemas, 14 skeletons, 26 negative fixtures, 7 positive fixtures
- Tests for TC-089..TC-098 (TC-097 an expected failure on `agent-ix/quire-rs#435`, TC-098 the blocker it flips), run against a Quire wheel at `agent-ix/quire-rs` `44df254` or later

## Notes

- Validation goes through `validate_document(..., bundle_package="agent-ix/spec-objects-business")`; without a bundle package the table is `unavailable` (`no-bundle-package`).
- The Python surface loads this module alone, so a verb the manifest does not declare is `unknown-verb`; that is why `edge_types` carries every `allowed_links` verb.
