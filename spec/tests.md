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
  - target: "ix://agent-ix/spec-objects-business/FR-008"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/FR-009"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/FR-010"
    type: covers
  - target: "ix://agent-ix/spec-objects-business/FR-011"
    type: covers
---
# Test Matrix

## Overview

This matrix is the verification contract for the module: the manifest
activation requirement (FR-001, issue #1 era) and the issue #4 semantic data
schemas, model tables, relationships, construct declarations and object ids (US-001, FR-002..FR-010, IT-002). Coverage is complete when
every acceptance criterion and named constraint maps to at least
one test case. Rows are `🚧` until a tagged test asserts them; `quoin validate --strict` reports no findings on this branch, and the rows still `🚧` are the ones whose evidence needs an environment this repository cannot provision (a running `filament-core-service`, a Quoin with the semantic installer).

## Test Matrix Rules

1. Every acceptance criterion and named constraint has at least one test case.
2. Both Properties forms (typed table, `sysml` fence) and every object type are tested.
3. Item-rule boundaries are tested at their allowed and refused edges (zero versus one identity field, empty versus one-item arrays).
4. Every named refusal (unknown key, both forms, dangling clause, non-Identifier token, undeclared model form, unknown state, trigger, or step kind, unknown or inverse relationship verb, disallowed relationship target, malformed relationship multiplicity, list-form Relationships section, Relationships table on a type without `relations`) has a failing fixture.
5. Availability states (`available`, `not_applicable`, `missing`) are tested per declaration kind.
6. Legacy artifacts, the empty record, and unresolved tokens are covered as edge cases.

## Requirements Traceability

### Stakeholder Requirement Coverage

| Stakeholder Req | Trace to US/FR | Test/Validation | Status |
|---|---|---|---|
| StR-001 | US-001, FR-001..FR-005 | TC-005, TC-006, TC-075 | 🚧 VC-1/VC-2 need a running filament-core |

### User Story Coverage

| User Story | Acceptance Criteria | Test Cases | Status |
|---|---|---|---|
| US-001 | US-001-EX-1..3 (illustrative) implemented by FR-002..FR-005 | TC-050, TC-053, TC-070 | 🚧 TC-070 needs a Quoin with the semantic installer |

### Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Status |
|---|---|---|---|
| FR-001 | FR-001-AC-2..4 | TC-002..TC-004 | 🚧 AC-2..AC-4 need a running filament-core |
| FR-002 | FR-002-AC-2..4, FR-002-AC-6, FR-002-AC-7, FR-002-AC-9, FR-002-CON-1..4 | TC-011..TC-013, TC-015..TC-019, TC-071, TC-073 | ✅ |
| FR-003 | FR-003-AC-1..2, FR-003-AC-4..6, FR-003-CON-1 | TC-020, TC-021, TC-024..TC-027 | ✅ AC-5 is a Demonstration; AC-6's naming half is an expected failure |
| FR-004 | FR-004-AC-1..12, FR-004-CON-1..2 | TC-030..TC-041, TC-042 | ✅ |
| FR-005 | FR-005-AC-1..8, FR-005-CON-1..2 | TC-050..TC-059 | ✅ |
| FR-006 | FR-006-AC-1..8, FR-006-CON-1 | TC-080..TC-088 | 🚧 CON-1 (TC-088) is an expected failure blocked on filament-core-service#31; AC-8 is an Inspection |
| FR-007 | FR-007-AC-1..9, AC-11 | TC-089..TC-097, TC-110 | ✅ AC-6 asserts that a line is reported; the table line is `agent-ix/quire-rs#440` |
| FR-008 | FR-008-AC-1, AC-3, AC-5..7 | TC-099, TC-101, TC-106, TC-108, TC-109 | ✅ AC-1 holds `population` without a construct while filament-core-data#174 is open |
| FR-009 | FR-009-AC-1..3 | TC-103..TC-105 | ✅ |
| FR-010 | FR-010-AC-1..6, FR-010-CON-1 | TC-111..TC-117 | ✅ CON-1 is an Inspection; the engine's record-key extraction is quire-rs's to prove |
| FR-011 | FR-011-AC-1..4 | TC-118..TC-121 | ✅ |

### Integration Test Coverage

| Integration Test | Success Criteria | Test Cases | Coverage Status |
|---|---|---|---|
| IT-001 | IT-001-SC-01..04 | TC-002..TC-004 | 🚧 needs a running filament-core |
| IT-002 | IT-002-SC-01..06 | TC-070 | 🚧 needs a Quoin with the semantic installer |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---|---|---|---|---|---|
| TC-002 | Activation against a clean filament-core returns 200 | Integration | P1 | FR-001-AC-2 | 🚧 needs a running filament-core |
| TC-003 | Re-activation is a content-hash no-op | Integration | P1 | FR-001-AC-3 | 🚧 needs a running filament-core |
| TC-004 | Every declared contribution appears in the registry tables | Integration | P1 | FR-001-AC-4 | 🚧 needs a running filament-core |
| TC-005 | Module activation registers the declared contents | Demonstration | P2 | StR-001-VC-1 | 🚧 needs a running filament-core |
| TC-006 | Generators produce valid artifacts from the shipped skeletons and schemas | Manual | P2 | StR-001-VC-2 | 🚧 |
| TC-011 | Every shipped schema declares the 2020-12 `$schema` and the `$id` matching its file name | Unit | P0 | FR-002-AC-2 | ✅ |
| TC-012 | Every `$ref` resolves to a shipped sibling or the declared semantic-core bundle | Unit | P0 | FR-002-AC-3 | ✅ |
| TC-013 | `make schemas-check` exits zero on the committed tree and non-zero naming a mutated schema | Integration | P1 | FR-002-AC-4 | ✅ |
| TC-015 | The built wheel contains every exported schema file | Integration | P1 | FR-002-AC-6 | ✅ |
| TC-016 | Two generator runs over one source are byte-identical | Integration | P1 | FR-002-CON-3 | ✅ |
| TC-017 | The build uses the official `@typespec/json-schema` emitter only and no emitted file is hand-edited | Inspection | P2 | FR-002-CON-1 | ✅ |
| TC-018 | No `.npmrc`, no `file:`/`link:` dependency | Inspection | P2 | FR-002-CON-2 | ✅ |
| TC-019 | `package-lock.json` resolves every package from npmjs except `@agent-ix/semantic-core` (GitHub Packages) | Unit | P2 | FR-002-CON-4 | ✅ |
| TC-020 | The `semantic` block equals the nine admitted keys and `exports` equals every object type | Unit | P0 | FR-003-AC-1, FR-003-CON-1 | ✅ |
| TC-021 | Every exported type's `data_schema` is the reference form | Unit | P0 | FR-003-AC-2 | ✅ |
| TC-024 | `quire.Registry.load_from` lists every archetype | Integration | P0 | FR-003-AC-4 | ✅ |
| TC-025 | `validate_document` on every skeleton reports no `semantic.*` load failure | Integration | P0 | FR-003-AC-4 | ✅ |
| TC-026 | An unknown `semantic` key is refused by the loader; the refusal names the key or path | Integration | P1 | FR-003-AC-6 | ✅ refusal verified; the naming half is an expected failure blocked on quire-rs#221 |
| TC-027 | `quoin module install path:` succeeds, lists the module, and the prior entry is restored | Manual | P1 | FR-003-AC-5 | 🚧 |
| TC-030 | Each schema differs from every other in a required, forbidden, or item rule; none is `type: object` only | Unit | P0 | FR-004-AC-1 | ✅ |
| TC-031 | Entity: identity record validates; identity flag removed fails; no `fields` fails | Integration | P0 | FR-004-AC-2 | ✅ |
| TC-032 | Value object: no-identity record validates; one identity fails; `relations` fails | Integration | P0 | FR-004-AC-3 | ✅ |
| TC-033 | Aggregate root: identity plus one clause validates; no `clauses` fails | Integration | P0 | FR-004-AC-4 | ✅ |
| TC-034 | Event: `Timestamp` field and no identity validates; no `Timestamp` fails; identity fails; `operations` fails | Integration | P0 | FR-004-AC-5 | ✅ |
| TC-035 | Repository: one operation validates; `fields` fails; empty `operations` fails | Integration | P0 | FR-004-AC-6 | ✅ |
| TC-036 | State machine: one operation validates with `states` and `transitions`; a transition without `trigger` fails; a transition `guardExpression` validates, a malformed one fails, and `guard` with `guardExpression` fails | Integration | P1 | FR-004-AC-7 | ✅ |
| TC-037 | Process: identity record validates with `steps` and `emits`; a step outside `StepKind` fails | Integration | P1 | FR-004-AC-8 | ✅ |
| TC-038 | Empty record validates for Domain, Enumeration, Population, VariantSet, and Graph only; `fields` on any of them fails; a population `extent` outside `closed`/`open` fails; population `members` (type only) validate only against Population | Integration | P0 | FR-004-AC-9, FR-004-CON-2 | ✅ |
| TC-039 | Placeholder `unresolved` target is accepted by the schema and reported by the extractor; a bare token is refused | Integration | P1 | FR-004-AC-10 | ✅ |
| TC-040 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core | Unit | P1 | FR-004-CON-1 | ✅ |
| TC-041 | Nested entity: local identity validates; `relations` and `owner` fail | Integration | P1 | FR-004-AC-11 | ✅ |
| TC-042 | Each of the five operation-bearing role schemas validates `operationExpressions` entries; a bad `slot` or a missing `expression` fails; `Repository` refuses the key | Integration | P1 | FR-004-AC-12 | ✅ |
| TC-050 | Every skeleton (every type plus three alternates) validates with no error | Integration | P0 | FR-005-AC-1 | ✅ |
| TC-051 | Table and `sysml` skeletons extract to identical normalized fields with the recorded forms | Integration | P0 | FR-005-AC-2, FR-005-CON-2 | ✅ |
| TC-052 | Under the skeleton bundle index every skeleton extracts with zero errors and zero unresolved tokens | Integration | P0 | FR-005-AC-3 | ✅ |
| TC-053 | Availability states per skeleton (fields, clauses, operations) match the type's declared set | Integration | P1 | FR-005-AC-4 | ✅ |
| TC-054 | Every negative fixture fails with its `expect:` code under the module's bundle package and the twenty-six named cases, including the six FR-007 relationship negatives by name, exist | Integration | P0 | FR-005-AC-5 | ✅ |
| TC-055 | Every skeleton's H2 set is asserted by the manifest and includes every required heading | Unit | P1 | FR-005-AC-6 | ✅ |
| TC-056 | Every skeleton is placeholder-free with non-empty asserted sections | Unit | P2 | FR-005-AC-7 | ✅ |
| TC-057 | A Properties section holding both a table and a fence is refused at the second form | Integration | P1 | FR-005-CON-2 | ✅ |
| TC-058 | No corpus repository or vendored fixture is edited by the change (diff over the branch) | Inspection | P2 | FR-005-CON-1 | ✅ |
| TC-059 | Skeleton titles are distinct `Identifier`s outside `KernelScalar`, and `object` equals `type` in every skeleton frontmatter | Unit | P1 | FR-005-AC-8 | ✅ |
| TC-070 | Quoin install roundtrip with state restore | Manual | P1 | IT-002-SC-01..IT-002-SC-06, FR-003-AC-5 | 🚧 needs a Quoin with the semantic installer |
| TC-071 | The packed npm tarball contains `manifest.yaml` and a sibling `schemas/<Model>.json` per export | Integration | P1 | FR-002-AC-7 | ✅ |
| TC-073 | `make schemas-check` names a stale committed schema with no emitted counterpart and writes nothing | Integration | P1 | FR-002-AC-9 | ✅ |
| TC-080 | The `table_row` locators whose first column is a model-table key are exactly the eight FR-006 declares, with their sections, columns within the table's set, `required` flags, and `min_rows: 1` | Unit | P0 | FR-006-AC-1 | ✅ |
| TC-088 | Every model-table locator declares `assert.optional_columns` — an explicit expected failure while `agent-ix/filament-core-service#31` is open | Unit | P1 | FR-006-CON-1 | 🚧 blocked on filament-core-service#31 |
| TC-081 | Each model-table skeleton extracts one model entry per table row, in row order, with no error or refusal | Integration | P0 | FR-006-AC-2 | ✅ |
| TC-082 | The declared-model fixture extracts supertypes, `abstract`, field presence, subsets, redefines, one operation frame with its `Modifies:`, `Creates:` and `Deletes:` lines, its `pre`/`post` lines, and the transition guard and emits | Integration | P0 | FR-006-AC-3 | ✅ |
| TC-083 | Each model-table negative fixture fails with its `expect:` code and every declared model-table locator has one | Integration | P0 | FR-006-AC-4 | ✅ |
| TC-084 | Every skeleton and fixture `quire` fence is valid Quire (qualified enum values, `present()` on `0..1` fields only, declared fields, names that state the check, invariants that hold in every state) and every `Emits`/`Consumes`/`Creates:`/`Deletes:` name resolves; mechanical check is `agent-ix/quire-spec-language#133` | Inspection | P1 | FR-006-AC-8 | ✅ |
| TC-085 | The population fixture validates and extracts one member per `## Members` row with its type, plus the population's frontmatter `extent`; a repeated `Type` and a retired `Type | Extent` table are refused | Integration | P0 | FR-006-AC-6 | ✅ |
| TC-086 | The manifest declares `specializes` as a structural edge with inverse `generalizes`, admitted by every field-bearing type | Unit | P1 | FR-006-AC-7 | ✅ |
| TC-087 | Skeleton clauses are `quire` with no advisory; no skeleton carries `ocl` or a model-section diagram, and its operation contract lines are `Pre:`/`Post:` (the `state_machine` skeleton writes a `Post:` line) | Integration | P1 | FR-006-AC-5 | ✅ |
| TC-089 | `semantic.mappings` includes `relationships`; only `domain`, `entity`, `aggregate_root`, `process` and `repository` declare the `relationships` locator, with no `min_rows`; `edge_types` declares `specializes` and the fifteen domain verbs with their spec-artifacts-iso category and inverse, covering every `allowed_links` verb | Unit | P0 | FR-007-AC-1 | ✅ |
| TC-090 | Each skeleton `## Relationships` table validates under the bundle package and lowers one relation per row, in row order, with verb, category, `composite`, `ix://` target and multiplicity; no frontmatter domain relationship and no `specializes` row | Integration | P0 | FR-007-AC-2 | ✅ |
| TC-091 | The entity relationships fixture validates and lowers every non-`specializes` entity verb, `composite` only for `contains` | Integration | P0 | FR-007-AC-3 | ✅ |
| TC-092 | The unknown-verb, inverse-verb, target-not-allowed and bad-multiplicity fixtures each fail with exactly one `semantic.invalid-model-cell` at line 21 on both surfaces, their reason, `availability.relations` `unavailable` with `entry-errors: lines 21`, and no relation; the inverse-verb message names `aggregates` and `aggregate_root_001` | Integration | P0 | FR-007-AC-4 | ✅ |
| TC-093 | A header-only Relationships table validates and extracts `available` with empty `relations` | Integration | P0 | FR-007-AC-5 | ✅ |
| TC-094 | Only `Entity`, `AggregateRoot` and `Domain` declare `relations`; a Relationships table on `value_object`, populated or header-only, fails with one `semantic.record-invalid` naming `relations` as unexpected (a line is reported; the table line is `agent-ix/quire-rs#440`) | Integration | P0 | FR-007-AC-6 | ✅ |
| TC-095 | A list-form Relationships section fails with `semantic.feature-not-extractable` at the list line; a prose-only section warns `semantic.relationships-no-block` at the heading | Integration | P0 | FR-007-AC-7 | ✅ |
| TC-096 | Through `validate_document`, a row targeting another artifact (`aggregate_root_999`) validates with one `semantic.unresolved-target` advisory at the row (`agent-ix/quoin#557`) | Integration | P1 | FR-007-AC-8 | ✅ |
| TC-097 | Per type, a process `emits` row and a repository `persists` row validate and lower into `emits` and `persists` with the qualified target, not `relations`, with every row in `relationSources` and non-lossy availability; header-only extracts the typed key empty, with the object type's data schema on the extraction request | Integration | P1 | FR-007-AC-9 | ✅ |
| TC-099 | Exactly the ten construct kinds declare `construct:`, and `population` none while filament-core-data#174 is open | Unit | P0 | FR-008-AC-1 | ✅ |
| TC-101 | Per kind, `references` name only roles an object type of the manifest carries, never `*` or a type name | Unit | P0 | FR-008-AC-3 | ✅ |
| TC-103 | `ObjectFrontmatter.json` carries the segmented document id pattern; every object type references that frontmatter schema and has a required id locator without a second regex | Unit | P0 | FR-009-AC-1 | ✅ |
| TC-104 | `ObjectFrontmatter.json` accepts underscore and QSpec style hyphenated ids, refuses malformed ids, every skeleton and fixture frontmatter validates, and a composed `FR` artifact with `object: enumeration` accepts `FR-271` | Integration | P0 | FR-009-AC-2 | ✅ |
| TC-105 | Every skeleton validates with its current id and a well-formed hyphenated id, while a repeated hyphen is refused by its frontmatter schema | Integration | P0 | FR-009-AC-3 | ✅ |
| TC-111 | Every top-level key of every record schema has an owner, none declares `owner` or `ubiquitous_language`, `Domain` declares `relations` and no `members`, `Process` declares `states` | Unit | P0 | FR-010-AC-1 | ✅ |
| TC-112 | `Process` `states` validate and a value-less entry fails; `Domain` `relations` validate and `members` or `ubiquitous_language` fail | Unit | P0 | FR-010-AC-2 | ✅ |
| TC-113 | The manifest names `record-sections`, `event` declares the optional `source` locator, and the event skeleton `## Source` holds one inline id of an `aggregate_root` skeleton | Unit | P0 | FR-010-AC-3 | ✅ |
| TC-114 | `nested_entity` `## Parent` stays a required prose locator and no skeleton authors `## Owner`, `## Emits` or `## Persists` | Unit | P0 | FR-010-AC-4 | ✅ |
| TC-115 | The `aggregate_root` skeleton has a `## Members` table and no `aggregates` or `contains` Relationships row | Unit | P0 | FR-010-AC-5 | ✅ |
| TC-116 | The `domain` skeleton validates under the bundle package with `contains` Relationships rows | Integration | P0 | FR-010-AC-6 | ✅ |
| TC-117 | FR-010-CON-1: no quire-rs or quoin fixture is copied into the repository | Inspection | P1 | FR-010-CON-1 | ✅ |
| TC-106 | The manifest `roles:` registry declares `aggregate-member` and `composite-owner`, each with a description, and each type carries the roles its references admit | Unit | P0 | FR-008-AC-5 | ✅ |
| TC-108 | `event`'s `construct:` declares `immutable: true`; every other of the ten kinds' `construct:` lacks the key | Unit | P0 | FR-008-AC-6 | ✅ |
| TC-109 | Each QSpec FR-208 refusal this module's record schema can express fails validation, and the same record without the refused form passes: an operation on `ValueObject`/`Event`; a `clauses` key or a non-empty operation `pre`/`post` on `Repository`; a `fields`, `operations` or `clauses` key on `Domain`; and no `repository` or `domain` `allowed_links` admits `specializes` | Unit | P0 | FR-008-AC-7 | ✅ |
| TC-110 | `entity` `references` admits `value_object`; `state_machine` `references` admits `entity` and `aggregate_root` | Unit | P0 | FR-007-AC-11 | ✅ |
| TC-118 | The manifest exports `variant_set` and `graph` with their `allowed_links` and reference-form `data_schema` | Unit | P0 | FR-011-AC-1 | ✅ |
| TC-119 | The `variants` locator declares the `Variant`, `Payload`, `Description` table; the skeleton and fixture validate and the list form is refused | Integration | P0 | FR-011-AC-2 | ✅ |
| TC-120 | The `graph` locator is a required mermaid block; the skeleton and fixture validate and prose alone is refused | Integration | P0 | FR-011-AC-3 | ✅ |
| TC-121 | `VariantSet.json` and `Graph.json` accept the empty record, `clauses`, and (VariantSet) `variants`; both refuse `fields`, `operations`, `states` and `transitions` | Unit | P1 | FR-011-AC-4 | ✅ |
| TC-075 | Every object type ships a typed schema a fixture reader can consume; an entity and an enumeration record are distinguishable by schema alone | Demonstration | P2 | StR-001-VC-3 | ✅ |

## Test Environment

Every `Integration` row that names Quire runs against the Quire wheel FR-005
Inputs pins, a dev dependency resolved from `internal-pypi` by `poetry install`.
The suite **fails**
rather than skips when `extract_semantic` is absent, so no row here can be
reported green without the engine under test. The exception is TC-088, an
explicit expected failure while `agent-ix/filament-core-service#31` is open.
A Relationships table whose columns do not match the locator assert reports that
assert error twice (`agent-ix/quire-rs#441`); FR-007 tests pin no such error list.

Rows over the declaration-record keys (`members`, `vocabulary`,
`emits`, `persists`, `source`, `states`, `transitions`, `steps`, `values`,
`relations`) are verified against hand-built records — TC-036, TC-037, TC-041
and TC-112 in particular — and their tests say so; they are schema evidence. The
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
