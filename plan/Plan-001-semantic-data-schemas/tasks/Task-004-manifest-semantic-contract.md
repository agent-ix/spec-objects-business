---
id: Task-004
title: "FR-003 — manifest 0.3.0, semantic block and reference-form data_schema"
type: Task
status: not_started
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-003
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/Task-007
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-020
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-021
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-022
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-024
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-026
    type: verifies
---
# Task-004: FR-003 — manifest 0.3.0, semantic block and reference-form data_schema

## Scope

Turn `manifest.yaml` into a semantic module: version 0.3.0, the quoin FR-070 `semantic`
block, and a reference-form `data_schema` per exported object type — without changing
a single 0.2.0 locator.

## Subtasks

- [ ] **`semantic` block.** Exactly the nine admitted keys: `contract_version: 1.0.0`, `semantic_core: 0.1.0`, `package: agent-ix/spec-objects-business`, `exports` (the ten object-type names), `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, ocl-clause]`, `compatibility_posture: additive`, `legacy_forms: warning`.
- [ ] **Reference-form `data_schema`.** `{ schema: schemas/<Model>.json, digest: sha256:<hex> }` on every exported type, the digest written by the generator over the shipped bytes. No inline `data_schema` survives.
- [ ] **Version.** `version: 0.3.0`, bumped together with the `@jsonSchema` base in one commit.
- [ ] **Locator preservation.** Every 0.2.0 locator keeps its `from`, heading, `language`, `required`, `multiple` and `assert` facets, compared structurally against the checked-in baseline from Task-007. The `properties` string locator on `entity` and `value_object` stays exactly where it is.
- [ ] **Loader verification.** `quire.Registry.load_from([module dir])` lists all ten archetypes with no `ArchetypeLoadFailure`; a copy whose `semantic` block gains `foo` is refused naming `foo`; a copy with an altered digest is refused naming the path.

## Deliverables

- `spec_objects_business/manifest.yaml` at 0.3.0
- Tests for TC-020, TC-021, TC-022, TC-024, TC-026

## Notes

- One refused schema fails every object type of the module (quire-rs FR-069), which is
  why all ten digests are regenerated together and why a partial edit is never valid.
- The manifest-schema revision all three consumers judge against is
  filament-core-service `a77f31e`; a consumer vendoring an older copy is that
  consumer's skew defect, not a change here.
- This task is the only writer of the `semantic` block, the version and the
  `data_schema` values. Task-006 is the only writer of the added locators.
- Unblocks: Task-005, Task-006, Task-009, Task-010's re-verification half.
