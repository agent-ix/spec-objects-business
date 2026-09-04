---
id: TM-001
title: "spec-objects-business Test Matrix"
type: TestMatrix
relationships:
  - target: "ix://agent-ix/spec-objects-business/FR-001"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/FR-002"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/FR-003"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/FR-005"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/NFR-001"
    type: covers
---
# Test Matrix

## Overview

This matrix is the verification contract for the module: the manifest
activation requirement (FR-001, issue #1 era) and the issue #4 semantic data
schemas (US-001, FR-002..FR-005, NFR-001, IT-002). Coverage is complete when
every acceptance criterion, named constraint, and NFR metric maps to at least
one test case. Rows are `🚧` until a tagged test asserts them.

## Test Matrix Rules

1. Every acceptance criterion and named constraint has at least one test case.
2. Both Properties forms (typed table, `sysml` fence) and every object type are tested.
3. Item-rule boundaries are tested at their allowed and refused edges (zero versus one identity field, empty versus one-item arrays).
4. Every named refusal (digest mismatch, unknown key, both forms, dangling clause, non-Identifier token) has a failing fixture.
5. Availability states (`available`, `not_applicable`, `missing`) are tested per declaration kind.
6. Legacy artifacts, the empty record, and unresolved tokens are covered as edge cases.

## Requirements Traceability

### Stakeholder Requirement Coverage

| Stakeholder Req | Trace to US/FR | Test/Validation | Coverage Status |
|---|---|---|---|
| StR-001 | US-001, FR-001..FR-005 | TC-005, TC-006, TC-075 | 🚧 |

### User Story Coverage

| User Story | Acceptance Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| US-001 | US-001-EX-1..3 (illustrative) implemented by FR-002..FR-005 | TC-050, TC-053, TC-070 | 🚧 |

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| FR-001 | FR-001-AC-1..4 | TC-001..TC-004 | 🚧 |
| FR-002 | FR-002-AC-1..9, FR-002-CON-1..5 | TC-010..TC-019, TC-071..TC-074 | 🚧 |
| FR-003 | FR-003-AC-1..6, FR-003-CON-1..2 | TC-020..TC-027 | 🚧 |
| FR-004 | FR-004-AC-1..11, FR-004-CON-1..2 | TC-030..TC-041 | 🚧 |
| FR-005 | FR-005-AC-1..8, FR-005-CON-1..2 | TC-050..TC-059 | 🚧 |

### Non-Functional Requirement Coverage

| Non-Functional Req | Verification Method | Evidence/Test Cases | Status |
|---|---|---|---|
| NFR-001 | Test (NFR-001-AC-1..4: locator baseline diff, legacy skeleton validation) | TC-060..TC-063 | 🚧 |

### Integration Test Coverage

| Integration Test | Success Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| IT-001 | IT-001-SC-01..04 | TC-002..TC-004 | 🚧 |
| IT-002 | IT-002-SC-01..06 | TC-070 | 🚧 |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---|---|---|---|---|---|
| TC-001 | Manifest validates against the vendored FR-035 module-manifest schema through `quire.validate_manifest` | Unit | P0 | FR-001-AC-1 | 🚧 |
| TC-002 | Activation against a clean filament-core returns 200 | Integration | P1 | FR-001-AC-2 | 🚧 needs a running filament-core |
| TC-003 | Re-activation is a content-hash no-op | Integration | P1 | FR-001-AC-3 | 🚧 needs a running filament-core |
| TC-004 | Every declared contribution appears in the registry tables | Integration | P1 | FR-001-AC-4 | 🚧 needs a running filament-core |
| TC-005 | Module activation registers the declared contents | Demonstration | P2 | StR-001-VC-1 | 🚧 needs a running filament-core |
| TC-006 | Generators produce valid artifacts from the shipped skeletons and schemas | Manual | P2 | StR-001-VC-2 | 🚧 |
| TC-010 | Emitted set equals the ten object-type models plus the declared support models; `toolchain.json` records compiler and emitter 1.15.0 | Unit | P0 | FR-002-AC-1 | 🚧 |
| TC-011 | Every shipped schema declares the 2020-12 `$schema` and the `$id` matching its file name under the 0.3.0 base | Unit | P0 | FR-002-AC-2 | 🚧 |
| TC-012 | Every `$ref` resolves to a shipped sibling or semantic-core 0.1.0 | Unit | P0 | FR-002-AC-3 | 🚧 |
| TC-013 | `make schemas-check` exits zero on the committed tree and non-zero naming a mutated schema or digest | Integration | P1 | FR-002-AC-4 | 🚧 |
| TC-014 | A `@jsonSchema` base version differing from the manifest version fails the generator naming both | Integration | P1 | FR-002-AC-5 | 🚧 |
| TC-015 | The built wheel contains every exported schema file | Integration | P1 | FR-002-AC-6 | 🚧 |
| TC-016 | Two generator runs over one source are byte-identical | Integration | P1 | FR-002-CON-3 | 🚧 |
| TC-017 | The build uses the official `@typespec/json-schema` emitter only and no emitted file is hand-edited | Inspection | P2 | FR-002-CON-1 | 🚧 |
| TC-018 | No `.npmrc`, no `file:`/`link:` dependency, exact toolchain pins in `package.json` | Inspection | P2 | FR-002-CON-2 | 🚧 |
| TC-019 | `package-lock.json` resolves every package from npmjs except `@agent-ix/semantic-core` (npm.ix) | Unit | P2 | FR-002-CON-4 | 🚧 |
| TC-020 | The `semantic` block equals the nine admitted keys and `exports` equals the ten types | Unit | P0 | FR-003-AC-1, FR-003-CON-1 | 🚧 |
| TC-021 | Every exported type's `data_schema` is the reference form whose file hashes to the recorded digest | Unit | P0 | FR-003-AC-2 | 🚧 |
| TC-022 | Every 0.2.0 locator is unchanged against the checked-in baseline | Unit | P0 | FR-003-AC-3 | 🚧 |
| TC-023 | Every added locator is `required: false` | Unit | P1 | FR-003-AC-3, FR-003-CON-2 | 🚧 |
| TC-024 | `quire.Registry.load_from` lists all ten archetypes | Integration | P0 | FR-003-AC-4 | 🚧 |
| TC-025 | `validate_document` on every skeleton reports no `semantic.*` load failure | Integration | P0 | FR-003-AC-4 | 🚧 |
| TC-026 | An unknown `semantic` key and an altered digest are each refused by the loader naming the key or path | Integration | P1 | FR-003-AC-6 | 🚧 |
| TC-027 | `quoin module install path:` succeeds, lists the module, and the prior entry is restored | Manual | P1 | FR-003-AC-5 | 🚧 |
| TC-030 | Each of the ten schemas differs from every other in a required, forbidden, or item rule; none is `type: object` only | Unit | P0 | FR-004-AC-1 | 🚧 |
| TC-031 | Entity: identity record validates; identity flag removed fails; no `fields` fails | Integration | P0 | FR-004-AC-2 | 🚧 |
| TC-032 | Value object: no-identity record validates; one identity fails; `relations` fails | Integration | P0 | FR-004-AC-3 | 🚧 |
| TC-033 | Aggregate root: identity plus one clause validates; no `clauses` fails | Integration | P0 | FR-004-AC-4 | 🚧 |
| TC-034 | Event: `Timestamp` field and no identity validates; no `Timestamp` fails; identity fails; `operations` fails | Integration | P0 | FR-004-AC-5 | 🚧 |
| TC-035 | Repository: one operation validates; `fields` fails; empty `operations` fails | Integration | P0 | FR-004-AC-6 | 🚧 |
| TC-036 | State machine: one operation validates with `states` and `transitions`; a transition without `trigger` fails | Integration | P1 | FR-004-AC-7 | 🚧 |
| TC-037 | Process: identity record validates with `steps`; a step outside `StepKind` fails | Integration | P1 | FR-004-AC-8 | 🚧 |
| TC-038 | Empty record validates for Domain and Enumeration only; `fields` on either fails | Integration | P0 | FR-004-AC-9, FR-004-CON-2 | 🚧 |
| TC-039 | Placeholder `unresolved` target is accepted by the schema and reported by the extractor; a bare token is refused | Integration | P1 | FR-004-AC-10 | 🚧 |
| TC-040 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core | Unit | P1 | FR-004-CON-1 | 🚧 |
| TC-041 | Nested entity: local identity validates; `relations` fails; `owner` accepted | Integration | P1 | FR-004-AC-11 | 🚧 |
| TC-050 | Every skeleton (ten plus three alternates) validates with no error | Integration | P0 | FR-005-AC-1 | 🚧 |
| TC-051 | Table and `sysml` skeletons extract to identical normalized fields with the recorded forms | Integration | P0 | FR-005-AC-2, FR-005-CON-2 | 🚧 |
| TC-052 | Under the skeleton bundle index every skeleton extracts with zero errors and zero unresolved tokens | Integration | P0 | FR-005-AC-3 | 🚧 |
| TC-053 | Availability states per skeleton (fields, clauses, operations) match the type's declared set | Integration | P1 | FR-005-AC-4 | 🚧 |
| TC-054 | Every negative fixture fails with its `expect:` code and the eight named cases exist | Integration | P0 | FR-005-AC-5 | 🚧 |
| TC-055 | Every skeleton's H2 set is asserted by the manifest and includes every required heading | Unit | P1 | FR-005-AC-6 | 🚧 |
| TC-056 | Every skeleton is placeholder-free with non-empty asserted sections | Unit | P2 | FR-005-AC-7 | 🚧 |
| TC-057 | A Properties section holding both a table and a fence is refused at the second form | Integration | P1 | FR-005-CON-2 | 🚧 |
| TC-058 | No corpus repository or vendored fixture is edited by the change (diff over the branch) | Inspection | P2 | FR-005-CON-1 | 🚧 |
| TC-059 | Skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` in every skeleton frontmatter | Unit | P1 | FR-005-AC-8 | 🚧 |
| TC-060 | Zero 0.2.0 locators changed | Unit | P0 | NFR-001-AC-1 | 🚧 |
| TC-061 | Every checked-in 0.2.0 skeleton validates under 0.3.0 with zero errors | Integration | P0 | NFR-001-AC-2 | 🚧 expected failure, blocked on quire-rs#391 (record validated as `{}`) |
| TC-062 | Each legacy-form 0.2.0 skeleton yields exactly one `semantic.legacy-properties-form` warning | Integration | P1 | NFR-001-AC-3 | 🚧 |
| TC-063 | Each legacy skeleton's `properties` string is identical under 0.2.0 and 0.3.0 | Integration | P1 | NFR-001-AC-4 | 🚧 |
| TC-070 | Quoin install roundtrip with state restore | Manual | P1 | IT-002-SC-01..IT-002-SC-06, FR-003-AC-5 | 🚧 needs a Quoin built from quoin main ≥ `3e842ce` (no release carries it) |
| TC-071 | The packed npm tarball contains `manifest.yaml` and a sibling `schemas/<Model>.json` per export | Integration | P1 | FR-002-AC-7 | 🚧 |
| TC-072 | A coordinated version bump re-emits every `$id`/`$ref` at the new version with matching digests; bumping one half of the pair fails the check | Integration | P1 | FR-002-AC-8, FR-002-CON-5 | 🚧 |
| TC-073 | `make schemas-check` names a stale committed schema with no emitted counterpart and writes nothing | Integration | P1 | FR-002-AC-9 | 🚧 |
| TC-074 | No acceptance test hard-codes the `$id` version segment; each reads it from the manifest `version` | Unit | P2 | FR-002-CON-5 | 🚧 |
| TC-075 | Every object type ships a typed schema a fixture reader can consume; an entity and an enumeration record are distinguishable by schema alone | Demonstration | P2 | StR-001-VC-3 | 🚧 |

## Test Environment

Every `Integration` row that names Quire runs against the Quire wheel FR-005
Inputs pins, provisioned by `make dev-quire`. That wheel is not on any index
this repository may commit a dependency against (`internal-pypi` serves 0.33.0
at most); `agent-ix/quire-rs#392` is the blocking issue. The suite **fails**
rather than skips when `extract_semantic` is absent, so no row here can be
reported green without the engine under test. The one exception is TC-061, an
explicit expected failure while `agent-ix/quire-rs#391` is open.

Rows over the record keys the extractor does not populate (`members`,
`vocabulary`, `owner`, `emits`, `persists`, `source`, `states`, `transitions`,
`steps`, `values`, `relations`) are verified against hand-built records, not
extracted ones — TC-036, TC-037, TC-041 in particular — and their tests say
so; they are schema evidence, not extraction evidence.

## Coverage Gaps

Every criterion, constraint, and metric above has a row. Two evidence-plan
artifacts are absent and are carried by the plan, not by this matrix: no
`SuiteRegistry` document declares a producer for the `Unit`, `Integration`,
`Snapshot`, and `Manual` evidence kinds, and no `Inspections` document exists
to discharge the `Inspection`/`Manual`/`Demonstration` rows (TC-005, TC-006,
TC-017, TC-018, TC-027, TC-058, TC-070, TC-075). Rows remain `🚧` until the
implementation lands a tagged test for them.
