---
id: Plan-001
title: "spec-objects-business — semantic data schemas (issue #4)"
type: Plan
status: active
relationships:
  - target: ix://agent-ix/spec-objects-business/StR-001
    type: references
  - target: ix://agent-ix/spec-objects-business/US-001
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-business/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-business/IT-001
    type: references
  - target: ix://agent-ix/spec-objects-business/IT-002
    type: references
---
# Implementation Plan: semantic data schemas

## Requirements Summary

### Stakeholder Requirements
- [ ] **StR-001**: DDD specifications yield extractable graph entities; every business object carries one typed structural contract downstream frontends can read (VC-1..VC-3).

### User Stories
- [ ] **US-001**: Declare every business object type against the shared semantic-core grammar, so one declaration record per object validates identically in Quire, Quoin and the compiler.

### Functional Requirements
- [ ] **FR-001**: The manifest conforms to filament-core-service FR-035 at revision `a77f31e` and activates idempotently; the registered `data_schema` is the reference object as posted.
- [ ] **FR-002**: Emit one JSON Schema 2020-12 document per model from `typespec/main.tsp` with the official `@typespec/json-schema` emitter at a pinned toolchain; normalize `$id`/`$ref`; gate drift; package the schemas into the wheel and the npm tarball; version-embedded `$id` with an atomic bump procedure.
- [ ] **FR-003**: `manifest.yaml` at version 0.3.0 carries the quoin FR-070 `semantic` block and a reference-form `data_schema` (path + digest) per exported object type, with every 0.2.0 locator unchanged.
- [ ] **FR-004**: One role-distinct model per business object type — required, forbidden and item rules — with every grammar item by `$ref` to semantic-core 0.1.0 and no redeclaration.
- [ ] **FR-005**: Every skeleton is an executable typed fixture in the quoin FR-071/FR-072 Markdown forms, with three `sysml` alternates and eight negative fixtures; the semantic suite fails rather than skips when the engine is absent.

### Non-Functional Requirements
- [ ] **NFR-001**: Additive compatibility — the checked-in 0.2.0 skeleton set still validates at 0.3.0, every 0.2.0 locator definition is unchanged, and the untyped `properties` string is byte-identical.

### Integration Test Requirements
- [ ] **IT-001**: Activation roundtrip against a running filament-core-service at `a77f31e` or later.
- [ ] **IT-002**: `quoin module install path:<dir>` accepts the semantic contract and the prior module state is restored unconditionally.

## Dependency Graph

### Core dependency edges
- `FR-002 (toolchain half) -> FR-004`
  Reason: the models cannot be authored until `tsp compile` runs against `@agent-ix/semantic-core` 0.1.0 and the generator normalizes what it emits.
- `FR-004 -> FR-002 (emitted-set half)`
  Reason: FR-002-AC-1/AC-2/AC-3 assert the emitted file set, its `$id`s and its `$ref`s, none of which exist before FR-004 declares the models. The spec resolves the apparent cycle by splitting FR-002 into an enablement half (generator, drift gate, packaging) that precedes FR-004 and an emitted-set half that follows it; FR-002 `depends_on` FR-004 in the frontmatter.
- `FR-002 (emitted set) + FR-001 -> FR-003`
  Reason: the manifest references the emitted files by path and digest, and the 0.3.0 manifest must still be an FR-035-valid manifest.
- `FR-003 + FR-004 -> FR-005`
  Reason: a skeleton validates only once the archetype loads with its schema, and the negative fixtures pin refusals the FR-004 rules define.
- `FR-005 -> FR-003 (added locators)`
  Reason: the `required: false` locators the manifest gains exist to assert sections the skeletons introduce, so the section lands before its locator.
- `FR-003 + FR-005 -> NFR-001`
  Reason: the compatibility metrics compare 0.2.0 locators and skeletons against the finished 0.3.0 manifest and its loader behaviour.
- `FR-003 -> IT-002`
  Reason: the Quoin install exercises the finished `semantic` block and digests.
- `FR-003 -> FR-001 / IT-001 (re-verification)`
  Reason: the manifest changed, so activation must be re-verified against the pinned service revision.

### Shared dependencies
- **The generator** (`scripts/generate-schemas.mjs`) is the single writer of
  `spec_objects_business/schemas/` and of `manifest.yaml`'s `data_schema.digest`
  values. It is needed by FR-002, FR-003, FR-004 and NFR-001; it is extracted as
  Task-001 and no other task writes those bytes.
- **The Quire test harness** (module registry construction, `validate_document`,
  `extract_semantic`, the hard-fail-on-missing-engine rule) is needed by FR-003,
  FR-004, FR-005 and NFR-001; it is extracted as Task-007.
- **The 0.2.0 baseline** (a checked-in copy of the 0.2.0 `body_extraction` and of the
  ten 0.2.0 skeletons) is needed by FR-003-AC-3 and by all four NFR-001 criteria; it
  is captured once in Task-007 and read by Task-004 and Task-008.

### Cross-cutting constraints
- `NFR-001` applies to every write to `manifest.yaml`'s `body_extraction` and to the
  skeleton rewrite: a locator may be added (`required: false`) but never changed.
- `FR-002-CON-1` (official emitter only, no hand-edited emitted file) applies to every
  byte under `spec_objects_business/schemas/`.
- `FR-002-CON-2`/`CON-4` (no `.npmrc`, no `file:`/`link:`, exact pins, npm.ix only for
  `@agent-ix/semantic-core`) apply to `package.json` and `package-lock.json`.
- `FR-005-CON-1` (no corpus repository and no vendored fixture edited) applies to the
  whole branch and is checked as a diff inspection.

### The seams

The module already ships `spec_objects_business/manifest.yaml` (0.2.0, ten object
types, `data_schema: {type: object}` on every one) and ten skeletons under
`spec_objects_business/skeletons/`. This plan adds `typespec/main.tsp` and
`scripts/generate-schemas.mjs` beside the existing `scripts/stage-npm.mjs`, which
already stages `schemas/` for the npm tarball and needs no change; `pyproject.toml`'s
`include` list gains `schemas/*.json`. The existing `tests/test_skeletons_and_validate.py`
holds the skeleton/locator parity assertions and the "quire is intentionally NOT a
dependency" skip that FR-005 replaces with a hard failure.

## Test Plan

### Unit Tests
- [ ] **TC-001** (FR-001-AC-1): the manifest validates through `quire.validate_manifest` against the vendored FR-035 schema.
- [ ] **TC-010** (FR-002-AC-1): the emitted set equals the seventeen files `toolchain.json` lists, with compiler and emitter 1.15.0 recorded.
- [ ] **TC-011** (FR-002-AC-2): every shipped schema declares the 2020-12 `$schema` and an `$id` under the base whose version segment is read from `manifest.yaml`.
- [ ] **TC-012** (FR-002-AC-3): every `$ref` resolves to a shipped sibling or to semantic-core 0.1.0.
- [ ] **TC-019** (FR-002-CON-4): `package-lock.json` resolves every package from npmjs except `@agent-ix/semantic-core`.
- [ ] **TC-020** (FR-003-AC-1, FR-003-CON-1): the `semantic` block equals the nine admitted keys and `exports` equals the ten object-type names.
- [ ] **TC-021** (FR-003-AC-2): every exported type's `data_schema` is the reference form and the referenced file hashes to the recorded digest.
- [ ] **TC-022** (FR-003-AC-3): every 0.2.0 locator is unchanged against the checked-in baseline.
- [ ] **TC-023** (FR-003-AC-3, FR-003-CON-2): every locator added after 0.2.0 is `required: false`.
- [ ] **TC-030** (FR-004-AC-1): the ten object-type schemas differ pairwise in a required, forbidden or item rule; none is `type: object` only.
- [ ] **TC-040** (FR-004-CON-1): no module schema redeclares a semantic-core model; every grammar item is a `$ref`.
- [ ] **TC-055** (FR-005-AC-6): every skeleton's H2 set is asserted by the manifest and includes every `required: true` heading.
- [ ] **TC-056** (FR-005-AC-7): every skeleton is placeholder-free with non-empty asserted sections.
- [ ] **TC-059** (FR-005-AC-8): skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` in every frontmatter.
- [ ] **TC-060** (NFR-001-AC-1): zero 0.2.0 locator definitions changed.
- [ ] **TC-074** (FR-002-CON-5): no test hard-codes the `$id` version segment.

### Integration Tests
- [ ] **TC-013** (FR-002-AC-4): `make schemas-check` exits zero on the committed tree and non-zero naming a mutated schema or digest.
- [ ] **TC-014** (FR-002-AC-5): a `@jsonSchema` base version differing from the manifest version fails the generator naming both.
- [ ] **TC-015** (FR-002-AC-6): the built wheel contains every exported schema file.
- [ ] **TC-016** (FR-002-CON-3): two generator runs over one source are byte-identical.
- [ ] **TC-024** (FR-003-AC-4): `quire.Registry.load_from` lists all ten archetypes.
- [ ] **TC-025** (FR-003-AC-4): `validate_document` on every skeleton reports no `semantic.*` load failure.
- [ ] **TC-026** (FR-003-AC-6): an unknown `semantic` key and an altered digest are each refused by the loader naming the key or the path.
- [ ] **TC-031..TC-039, TC-041** (FR-004-AC-2..AC-11, FR-004-CON-2): the per-type positive and negative record fixtures — entity identity, value-object identity refusal, aggregate clauses, event occurrence, repository operations, state-machine transitions, process steps, the empty record, the unresolved placeholder, nested-entity `owner`.
- [ ] **TC-050** (FR-005-AC-1): every skeleton (ten plus three alternates) validates with no error.
- [ ] **TC-051** (FR-005-AC-2, FR-005-CON-2): table and `sysml` skeletons extract to identical normalized fields with the recorded forms.
- [ ] **TC-052** (FR-005-AC-3): under the skeleton bundle index every skeleton extracts with zero errors and zero unresolved tokens.
- [ ] **TC-053** (FR-005-AC-4): availability states per skeleton match the type's declared set.
- [ ] **TC-054** (FR-005-AC-5): every negative fixture fails with its `expect:` code and the eight named cases exist.
- [ ] **TC-057** (FR-005-CON-2): a Properties section holding both a table and a fence is refused at the second form.
- [ ] **TC-071** (FR-002-AC-7): the packed npm tarball ships `manifest.yaml` beside `schemas/<Model>.json`.
- [ ] **TC-072** (FR-002-AC-8, FR-002-CON-5): a coordinated version bump re-emits every `$id`/`$ref` with matching digests; half a bump fails the check.
- [ ] **TC-073** (FR-002-AC-9): `make schemas-check` names a stale committed schema and writes nothing.

### Verification (NFRs)
- [ ] **TC-061** (NFR-001-AC-2): every checked-in 0.2.0 skeleton validates under 0.3.0 with zero errors — an explicit expected failure while `agent-ix/quire-rs#391` is open.
- [ ] **TC-062** (NFR-001-AC-3): each legacy-form 0.2.0 skeleton yields exactly one `semantic.legacy-properties-form` warning.
- [ ] **TC-063** (NFR-001-AC-4): each legacy skeleton's `properties` string is byte-identical under 0.2.0 and 0.3.0.

### Environment-gated and inspection rows
- [ ] **TC-002..TC-004** (FR-001-AC-2..AC-4, IT-001): activation, re-activation and registry reads against a running filament-core-service at `a77f31e` or later.
- [ ] **TC-005, TC-006, TC-075** (StR-001-VC-1..VC-3): the stakeholder demonstrations.
- [ ] **TC-017** (FR-002-CON-1), **TC-018** (FR-002-CON-2), **TC-058** (FR-005-CON-1): inspections over the emitter path, the packaging surface, and the branch diff.
- [ ] **TC-027, TC-070** (FR-003-AC-5, IT-002-SC-01..SC-06): the Quoin install roundtrip with unconditional state restore.

## Remaining Work

### Track A: Critical Path (serial)
- **A1 = Task-001** TypeSpec toolchain, generator and drift gate — Hard; exit: `make schemas` compiles an empty-but-valid source and `make schemas-check` exits zero on the committed tree and non-zero on any mutation, stale file, or half-bumped version.
- **A2 = Task-002** The ten role-distinct models and six support models — Hard; exit: each type accepts the records its role admits and refuses the records its role forbids, with every grammar item resolved by `$ref` to semantic-core.
- **Gate = Task-011** Three types end-to-end — measures whether the emitter's `contains`/`minContains`/`maxContains` recipe and `unevaluatedProperties` survive the real validator for `Entity`, `ValueObject` and `Event`; pass: all three accept their positive record and refuse their identity/occurrence negatives. If it fails, the item-rule encoding is wrong and the remaining seven types must not be authored against it.
- **A3 = Task-003** Emitted set, `toolchain.json`, digests and packaging — Medium; exit: seventeen schema files ship in the wheel and the npm tarball with digests the manifest agrees with.
- **A4 = Task-004** Manifest 0.3.0, `semantic` block, reference-form `data_schema` — Medium; exit: Quire's loader lists all ten archetypes and refuses an unknown key or an altered digest.
- **A5 = Task-005** Skeleton rewrite, three `sysml` alternates, eight negative fixtures — Hard; exit: every skeleton validates clean under the module and every negative fails for its named reason.
- **A6 = Task-006** Added `required: false` locators for the sections the skeletons introduced — Easy; exit: every new section is asserted by the manifest and no existing artifact is invalidated.

### Track B: Parallel (independent agent, can start now)
- **B1 = Task-007** Test environment, provisioning and the 0.2.0 baseline — Medium; exit: the semantic suite fails loudly on a machine with no Quire and passes on one provisioned by `make dev-quire`; the 0.2.0 locators and skeletons are frozen as a fixture.
- **B2 = Task-010** FR-001 / StR-001 re-verification and trace tags — Easy; exit: the manifest still activates and every pre-existing test carries a trace tag that `quire coverage` binds.

### Track C: Post-critical-path
- **C1 = Task-008** NFR-001 additive-compatibility verification — Medium; exit: no 0.2.0 locator changed, the `properties` string is byte-identical, and the one blocked criterion is an expected failure naming its issue rather than a skip.
- **C2 = Task-009** IT-002 Quoin install demonstration — Medium; exit: the module installs, is listed, and the operator's prior module state is restored whether or not the install succeeded.

## Parallel Execution Summary

```
Track A  A1 ─── A2 ─── [Gate] ─── A3 ─── A4 ─── A5 ─── A6 ──┐
                                                            ├── C1
Track B  B1 ────────────────────────────────────┐           └── C2
         B2 ─────────────────────────(after A4)─┘
```

Track B starts immediately and independently of A1: neither the provisioning target
nor the 0.2.0 baseline touches the generator or the models. B2's re-verification half
waits on A4 because it re-posts the changed manifest. Track C begins once A6 lands.

## Task File Mapping

| Task     | Track | Owns (references)        | Verified by (verifies)                                  | Status      |
| -------- | ----- | ------------------------ | ------------------------------------------------------- | ----------- |
| Task-001 | A     | FR-002                   | TC-013, TC-014, TC-016, TC-017, TC-072, TC-073, TC-074   | not_started |
| Task-002 | A     | FR-004, US-001           | TC-030…TC-041                                            | not_started |
| Task-011 | Gate  | FR-004                   | TC-031, TC-032, TC-034                                   | not_started |
| Task-003 | A     | FR-002                   | TC-010, TC-011, TC-012, TC-015, TC-071                   | not_started |
| Task-004 | A     | FR-003                   | TC-020, TC-021, TC-022, TC-024, TC-026                   | not_started |
| Task-005 | A     | FR-005, US-001           | TC-050…TC-057, TC-059                                    | not_started |
| Task-006 | A     | FR-003, FR-005           | TC-023, TC-025                                           | not_started |
| Task-007 | B     | FR-005, FR-002           | TC-018, TC-019, TC-058                                   | not_started |
| Task-008 | C     | NFR-001                  | TC-060, TC-061, TC-062, TC-063                           | not_started |
| Task-009 | C     | FR-003, IT-002           | TC-027, TC-070                                           | not_started |
| Task-010 | B     | FR-001, StR-001, IT-001  | TC-001…TC-006, TC-075                                    | not_started |

## Coordination Rules

- **Single writer for the schemas.** Only the generator writes
  `spec_objects_business/schemas/` and `manifest.yaml`'s `data_schema.digest` values.
  No task hand-edits an emitted file (FR-002-CON-1); a wrong schema is fixed in
  `typespec/main.tsp` and regenerated.
- **Single writer for the manifest.** Task-004 owns the `semantic` block, the version
  and the reference-form `data_schema`; Task-006 owns the added locators. No other
  task edits `manifest.yaml`, so the digest rewrite never races a locator edit.
- **Freeze the 0.2.0 baseline first.** Task-007 captures the 0.2.0 `body_extraction`
  and the ten 0.2.0 skeletons before Task-004 or Task-005 changes anything; after that
  the baseline fixture is read-only.
- **Never relax to pass.** If a schema, a digest, or a locator makes a test red, the
  fix is in this module's source or an upstream ticket — never a widened rule, a
  dropped `required`, or a lowered gate.
- **No skip may stand in for evidence.** A missing Quire fails the suite. The only
  expected failure is TC-061, and it names `agent-ix/quire-rs#391`.
- **No corpus repository and no vendored fixture is edited** on this branch; Task-007
  checks it as a diff inspection (TC-058).
- **Merge sequencing.** A1 → A2 → Gate → A3 → A4 → A5 → A6, then C1 and C2. B1 merges
  whenever it is green; B2's re-verification half merges after A4.
