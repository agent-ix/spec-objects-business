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
  - target: "ix://agent-ix/spec-objects-business/FR-006"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/FR-007"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/NFR-001"
    type: covers
---
# Test Matrix

## Overview

This matrix is the verification contract for the module: the manifest
activation requirement (FR-001, issue #1 era) and the issue #4 semantic data
schemas, model tables and relationships (US-001, FR-002..FR-007, NFR-001, IT-002). Coverage is complete when
every acceptance criterion, named constraint, and NFR metric maps to at least
one test case. Rows are `🚧` until a tagged test asserts them; `quoin validate --strict` reports no findings on this branch, and the rows still `🚧` are the ones whose evidence needs an environment this repository cannot provision (a running `filament-core-service`, a Quoin built from main).

## Test Matrix Rules

1. Every acceptance criterion and named constraint has at least one test case.
2. Both Properties forms (typed table, `sysml` fence) and every object type are tested.
3. Item-rule boundaries are tested at their allowed and refused edges (zero versus one identity field, empty versus one-item arrays).
4. Every named refusal (digest mismatch, unknown key, both forms, dangling clause, non-Identifier token, undeclared model form, unknown state, trigger, or step kind, unknown or inverse relationship verb, disallowed relationship target, malformed relationship multiplicity, list-form Relationships section, Relationships table on a type without `relations`) has a failing fixture.
5. Availability states (`available`, `not_applicable`, `missing`) are tested per declaration kind.
6. Legacy artifacts, the empty record, and unresolved tokens are covered as edge cases.

## Requirements Traceability

### Stakeholder Requirement Coverage

| Stakeholder Req | Trace to US/FR | Test/Validation | Coverage Status |
|---|---|---|---|
| StR-001 | US-001, FR-001..FR-005 | TC-005, TC-006, TC-075 | 🚧 VC-1/VC-2 need a running filament-core |

### User Story Coverage

| User Story | Acceptance Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| US-001 | US-001-EX-1..3 (illustrative) implemented by FR-002..FR-005 | TC-050, TC-053, TC-070 | 🚧 TC-070 needs a Quoin built from main |

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| FR-001 | FR-001-AC-1..4 | TC-001..TC-004 | 🚧 AC-2..AC-4 need a running filament-core |
| FR-002 | FR-002-AC-1..9, FR-002-CON-1..5 | TC-010..TC-019, TC-071..TC-074 | ✅ |
| FR-003 | FR-003-AC-1..6, FR-003-CON-1..2 | TC-020..TC-027 | ✅ AC-5 is a Demonstration; AC-6's naming half is an expected failure |
| FR-004 | FR-004-AC-1..11, FR-004-CON-1..2 | TC-030..TC-041 | ✅ |
| FR-005 | FR-005-AC-1..8, FR-005-CON-1..2 | TC-050..TC-059 | ✅ |
| FR-006 | FR-006-AC-1..8, FR-006-CON-1 | TC-080..TC-088 | 🚧 CON-1 (TC-088) is an expected failure blocked on filament-core-service#31; AC-8 is an Inspection |
| FR-007 | FR-007-AC-1..9 | TC-089..TC-097 | 🚧 AC-9 (TC-097) is an expected failure blocked on quire-rs#435; AC-6 asserts the null line `agent-ix/quire-rs#440` fixes |

### Non-Functional Requirement Coverage

| Non-Functional Req | Verification Method | Evidence/Test Cases | Status |
|---|---|---|---|
| NFR-001 | Test (NFR-001-AC-1..4: locator baseline diff outside the declared model-table sections, legacy skeleton validation) | TC-060..TC-063 | ✅ |

### Integration Test Coverage

| Integration Test | Success Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| IT-001 | IT-001-SC-01..04 | TC-002..TC-004 | 🚧 needs a running filament-core |
| IT-002 | IT-002-SC-01..06 | TC-070 | 🚧 needs a Quoin built from main |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---|---|---|---|---|---|
| TC-001 | Manifest validates against the vendored FR-035 module-manifest schema through `quire.validate_manifest` | Unit | P0 | FR-001-AC-1 | ✅ |
| TC-002 | Activation against a clean filament-core returns 200 | Integration | P1 | FR-001-AC-2 | 🚧 needs a running filament-core |
| TC-003 | Re-activation is a content-hash no-op | Integration | P1 | FR-001-AC-3 | 🚧 needs a running filament-core |
| TC-004 | Every declared contribution appears in the registry tables | Integration | P1 | FR-001-AC-4 | 🚧 needs a running filament-core |
| TC-005 | Module activation registers the declared contents | Demonstration | P2 | StR-001-VC-1 | 🚧 needs a running filament-core |
| TC-006 | Generators produce valid artifacts from the shipped skeletons and schemas | Manual | P2 | StR-001-VC-2 | 🚧 |
| TC-010 | Emitted set equals the eleven object-type models plus the declared support models; `toolchain.json` records compiler and emitter 1.15.0 | Unit | P0 | FR-002-AC-1 | ✅ |
| TC-011 | Every shipped schema declares the 2020-12 `$schema` and the `$id` matching its file name under the manifest-version base | Unit | P0 | FR-002-AC-2 | ✅ |
| TC-012 | Every `$ref` resolves to a shipped sibling or semantic-core 0.2.0 | Unit | P0 | FR-002-AC-3 | ✅ |
| TC-013 | `make schemas-check` exits zero on the committed tree and non-zero naming a mutated schema or digest | Integration | P1 | FR-002-AC-4 | ✅ |
| TC-014 | A `@jsonSchema` base version differing from the manifest version fails the generator naming both | Integration | P1 | FR-002-AC-5 | ✅ |
| TC-015 | The built wheel contains every exported schema file | Integration | P1 | FR-002-AC-6 | ✅ |
| TC-016 | Two generator runs over one source are byte-identical | Integration | P1 | FR-002-CON-3 | ✅ |
| TC-017 | The build uses the official `@typespec/json-schema` emitter only and no emitted file is hand-edited | Inspection | P2 | FR-002-CON-1 | ✅ |
| TC-018 | No `.npmrc`, no `file:`/`link:` dependency, exact toolchain pins in `package.json` | Inspection | P2 | FR-002-CON-2 | ✅ |
| TC-019 | `package-lock.json` resolves every package from npmjs except `@agent-ix/semantic-core` (npm.ix) | Unit | P2 | FR-002-CON-4 | ✅ |
| TC-020 | The `semantic` block equals the nine admitted keys and `exports` equals the eleven types | Unit | P0 | FR-003-AC-1, FR-003-CON-1 | ✅ |
| TC-021 | Every exported type's `data_schema` is the reference form whose file hashes to the recorded digest | Unit | P0 | FR-003-AC-2 | ✅ |
| TC-022 | Every 0.2.0 locator outside the FR-006 model tables is unchanged against the checked-in baseline | Unit | P0 | FR-003-AC-3 | ✅ |
| TC-023 | Every added locator outside the FR-006 model tables is `required: false` | Unit | P1 | FR-003-AC-3, FR-003-CON-2 | ✅ |
| TC-024 | `quire.Registry.load_from` lists all eleven archetypes | Integration | P0 | FR-003-AC-4 | ✅ |
| TC-025 | `validate_document` on every skeleton reports no `semantic.*` load failure | Integration | P0 | FR-003-AC-4 | ✅ |
| TC-026 | An unknown `semantic` key and an altered digest are each refused by the loader; the refusal names the key or path | Integration | P1 | FR-003-AC-6 | ✅ refusal verified; the naming half is an expected failure blocked on quire-rs#221 and quire-rs#394 |
| TC-027 | `quoin module install path:` succeeds, lists the module, and the prior entry is restored | Manual | P1 | FR-003-AC-5 | 🚧 |
| TC-030 | Each of the eleven schemas differs from every other in a required, forbidden, or item rule; none is `type: object` only | Unit | P0 | FR-004-AC-1 | ✅ |
| TC-031 | Entity: identity record validates; identity flag removed fails; no `fields` fails | Integration | P0 | FR-004-AC-2 | ✅ |
| TC-032 | Value object: no-identity record validates; one identity fails; `relations` fails | Integration | P0 | FR-004-AC-3 | ✅ |
| TC-033 | Aggregate root: identity plus one clause validates; no `clauses` fails | Integration | P0 | FR-004-AC-4 | ✅ |
| TC-034 | Event: `Timestamp` field and no identity validates; no `Timestamp` fails; identity fails; `operations` fails | Integration | P0 | FR-004-AC-5 | ✅ |
| TC-035 | Repository: one operation validates; `fields` fails; empty `operations` fails | Integration | P0 | FR-004-AC-6 | ✅ |
| TC-036 | State machine: one operation validates with `states` and `transitions`; a transition without `trigger` fails | Integration | P1 | FR-004-AC-7 | ✅ |
| TC-037 | Process: identity record validates with `steps` and `emits`; a step outside `StepKind` fails | Integration | P1 | FR-004-AC-8 | ✅ |
| TC-038 | Empty record validates for Domain, Enumeration, and Population only; `fields` on any of them fails; population `members` validate only against Population | Integration | P0 | FR-004-AC-9, FR-004-CON-2 | ✅ |
| TC-039 | Placeholder `unresolved` target is accepted by the schema and reported by the extractor; a bare token is refused | Integration | P1 | FR-004-AC-10 | ✅ |
| TC-040 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core | Unit | P1 | FR-004-CON-1 | ✅ |
| TC-041 | Nested entity: local identity validates; `relations` fails; `owner` accepted | Integration | P1 | FR-004-AC-11 | ✅ |
| TC-050 | Every skeleton (eleven plus three alternates) validates with no error | Integration | P0 | FR-005-AC-1 | ✅ |
| TC-051 | Table and `sysml` skeletons extract to identical normalized fields with the recorded forms | Integration | P0 | FR-005-AC-2, FR-005-CON-2 | ✅ |
| TC-052 | Under the skeleton bundle index every skeleton extracts with zero errors and zero unresolved tokens | Integration | P0 | FR-005-AC-3 | ✅ |
| TC-053 | Availability states per skeleton (fields, clauses, operations) match the type's declared set | Integration | P1 | FR-005-AC-4 | ✅ |
| TC-054 | Every negative fixture fails with its `expect:` code under the module's bundle package and the twenty-six named cases, including the six FR-007 relationship negatives by name, exist | Integration | P0 | FR-005-AC-5 | ✅ |
| TC-055 | Every skeleton's H2 set is asserted by the manifest and includes every required heading | Unit | P1 | FR-005-AC-6 | ✅ |
| TC-056 | Every skeleton is placeholder-free with non-empty asserted sections | Unit | P2 | FR-005-AC-7 | ✅ |
| TC-057 | A Properties section holding both a table and a fence is refused at the second form | Integration | P1 | FR-005-CON-2 | ✅ |
| TC-058 | No corpus repository or vendored fixture is edited by the change (diff over the branch) | Inspection | P2 | FR-005-CON-1 | ✅ |
| TC-059 | Skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` in every skeleton frontmatter | Unit | P1 | FR-005-AC-8 | ✅ |
| TC-060 | Zero 0.2.0 locators changed outside the FR-006 model tables | Unit | P0 | NFR-001-AC-1 | ✅ |
| TC-061 | Each of the seven measured 0.2.0 skeletons validates under the current manifest with zero errors; a legacy form that declares `object:` is not an error | Integration | P0 | NFR-001-AC-2 | ✅ the criterion passes; the `object:`-declaring case is an expected failure on quire-rs#391 |
| TC-062 | Each legacy-form 0.2.0 skeleton yields exactly one `semantic.legacy-properties-form` warning | Integration | P1 | NFR-001-AC-3 | ✅ |
| TC-063 | Each legacy skeleton's `properties` string is identical under 0.2.0 and the current manifest | Integration | P1 | NFR-001-AC-4 | ✅ |
| TC-070 | Quoin install roundtrip with state restore | Manual | P1 | IT-002-SC-01..IT-002-SC-06, FR-003-AC-5 | 🚧 needs a Quoin built from quoin main ≥ `3e842ce` (no release carries it) |
| TC-071 | The packed npm tarball contains `manifest.yaml` and a sibling `schemas/<Model>.json` per export | Integration | P1 | FR-002-AC-7 | ✅ |
| TC-072 | A coordinated version bump re-emits every `$id`/`$ref` at the new version with matching digests; bumping one half of the pair fails the check | Integration | P1 | FR-002-AC-8, FR-002-CON-5 | ✅ |
| TC-073 | `make schemas-check` names a stale committed schema with no emitted counterpart and writes nothing | Integration | P1 | FR-002-AC-9 | ✅ |
| TC-074 | No acceptance test hard-codes the `$id` version segment; each reads it from the manifest `version` | Unit | P2 | FR-002-CON-5 | ✅ |
| TC-080 | The `table_row` locators whose first column is a model-table key are exactly the eight FR-006 declares, with their sections, columns within the table's set, `required` flags, and `min_rows: 1` | Unit | P0 | FR-006-AC-1 | ✅ |
| TC-088 | Every model-table locator declares `assert.optional_columns` — an explicit expected failure while `agent-ix/filament-core-service#31` is open | Unit | P1 | FR-006-CON-1 | 🚧 blocked on filament-core-service#31 |
| TC-081 | Each model-table skeleton extracts one model entry per table row, in row order, with no error or refusal | Integration | P0 | FR-006-AC-2 | ✅ |
| TC-082 | The declared-model fixture extracts supertypes, `abstract`, field presence, subsets, redefines, one operation frame, and the transition guard and emits | Integration | P0 | FR-006-AC-3 | ✅ |
| TC-083 | Each model-table negative fixture fails with its `expect:` code and every declared model-table locator has one | Integration | P0 | FR-006-AC-4 | ✅ |
| TC-084 | Every skeleton and fixture `quire` fence is valid Quire (qualified enum values, `present()` on `0..1` fields only, declared fields, names that state the check, invariants that hold in every state) and every `Emits`/`Consumes`/`Creates:`/`Deletes:` name resolves; mechanical check is `agent-ix/quire-spec-language#133` | Inspection | P1 | FR-006-AC-8 | ✅ |
| TC-085 | The population fixture validates and extracts one member per `## Members` row with its type and extent | Integration | P0 | FR-006-AC-6 | ✅ |
| TC-086 | The manifest declares `specializes` as a structural edge with inverse `generalizes`, admitted by every field-bearing type | Unit | P1 | FR-006-AC-7 | ✅ |
| TC-087 | Skeleton clauses are `quire` with no advisory; no skeleton carries `ocl`, `Pre:`/`Post:`, or a model-section diagram | Integration | P1 | FR-006-AC-5 | ✅ |
| TC-089 | `semantic.mappings` includes `relationships`; only `entity`, `aggregate_root`, `process` and `repository` declare the `relationships` locator, with no `min_rows`; `edge_types` declares `specializes` and the fifteen domain verbs with their spec-artifacts-iso category and inverse, covering every `allowed_links` verb | Unit | P0 | FR-007-AC-1 | ✅ |
| TC-090 | Each skeleton `## Relationships` table validates under the bundle package and lowers one relation per row, in row order, with verb, category, `composite`, `ix://` target and multiplicity; no frontmatter domain relationship and no `specializes` row | Integration | P0 | FR-007-AC-2 | ✅ |
| TC-091 | The entity relationships fixture validates and lowers every non-`specializes` entity verb, `composite` only for `contains` | Integration | P0 | FR-007-AC-3 | ✅ |
| TC-092 | The unknown-verb, inverse-verb, target-not-allowed and bad-multiplicity fixtures each fail with exactly one `semantic.invalid-model-cell` at line 21 on both surfaces, their reason, `availability.relations` `unavailable` with `entry-errors: lines 21`, and no relation; the inverse-verb message names `aggregates` and `aggregate-root-001` | Integration | P0 | FR-007-AC-4 | ✅ |
| TC-093 | A header-only Relationships table validates and extracts `available` with empty `relations` | Integration | P0 | FR-007-AC-5 | ✅ |
| TC-094 | Only `Entity` and `AggregateRoot` declare `relations`; a Relationships table on `value_object`, populated or header-only, fails with one `semantic.record-invalid` at `relations` (line null until `agent-ix/quire-rs#440`) | Integration | P0 | FR-007-AC-6 | ✅ |
| TC-095 | A list-form Relationships section fails with `semantic.feature-not-extractable` at the list line; a prose-only section warns `semantic.relationships-no-block` at the heading | Integration | P0 | FR-007-AC-7 | ✅ |
| TC-096 | Through `validate_document`, a row targeting another artifact (`aggregate-root-999`) validates with one `semantic.unresolved-target` advisory at the row (`agent-ix/quoin#557`) | Integration | P1 | FR-007-AC-8 | ✅ |
| TC-097 | A process `emits` row and a repository `persists` row validate and lower into `emits` and `persists`, not `relations` — an explicit expected failure while `agent-ix/quire-rs#435` is open | Integration | P1 | FR-007-AC-9 | 🚧 blocked on quire-rs#435 |
| TC-075 | Every object type ships a typed schema a fixture reader can consume; an entity and an enumeration record are distinguishable by schema alone | Demonstration | P2 | StR-001-VC-3 | ✅ |

## Test Environment

Every `Integration` row that names Quire runs against the Quire wheel FR-005
Inputs pins, provisioned by `make dev-quire`. That wheel is not on any index
this repository may commit a dependency against (`internal-pypi` serves 0.33.0
at most); `agent-ix/quire-rs#392` is the blocking issue. The suite **fails**
rather than skips when `extract_semantic` is absent, so no row here can be
reported green without the engine under test. The one exception is TC-061, an
explicit expected failure while `agent-ix/quire-rs#391` is open, TC-097, an explicit expected failure while `agent-ix/quire-rs#435` is open, and TC-088, an
explicit expected failure while `agent-ix/filament-core-service#31` is open.

Rows over the declaration-record keys (`members`, `vocabulary`, `owner`,
`emits`, `persists`, `source`, `states`, `transitions`, `steps`, `values`,
`relations`) are verified against hand-built records — TC-036, TC-037, TC-041
in particular — and their tests say so; they are schema evidence. The
extracted model tables are verified separately against the record's `model`
(TC-081..TC-083, TC-085), and the extracted `relations` against the `## Relationships` rows (TC-090..TC-096).

## Coverage Gaps

Every criterion, constraint, and metric above has a row. Two evidence-plan
artifacts are absent and are carried by the plan, not by this matrix: no
`SuiteRegistry` document declares a producer for the `Unit`, `Integration`,
`Snapshot`, and `Manual` evidence kinds, and no `Inspections` document exists
to discharge the `Inspection`/`Manual`/`Demonstration` rows (TC-005, TC-006,
TC-017, TC-018, TC-027, TC-058, TC-070, TC-075, TC-084). Rows remain `🚧` until the
implementation lands a tagged test for them.
