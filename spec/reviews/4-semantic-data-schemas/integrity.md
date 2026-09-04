---
id: SR-003
title: "Integrity review of the #4 semantic data schemas spec"
type: SpecReview
analysis: integrity
scope: "spec/spec.md, spec/stakeholder/StR-001-module-activation.md, spec/usecase/US-001-declare-business-objects-against-semantic-core.md, spec/functional/FR-001-module-manifest-activates.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/integration/IT-001-manifest-activation-roundtrip.md, spec/integration/IT-002-quoin-module-install.md, spec/tests.md"
review_set: all
---
# SR-003: Integrity review of the #4 semantic data schemas spec

## Summary

Integrity gate (completeness, consistency, atomicity/testability) over the
twelve artifacts that deliver `agent-ix/spec-objects-business#4`, grounded
against the upstream contract: `semantic-core` `main.tsp` (filament-core-data),
quoin FR-070..FR-075, quire-rs FR-069..FR-072, the quoin `module-ok` fixture,
and the current `spec_objects_business/manifest.yaml` (0.2.0) and skeletons.
The spec is well structured and traceable at the FR/AC level, and the Test
Matrix has a row for every AC and NFR metric. The gate does not pass: one high
finding (FR-004's required `fields`/`operations` keys contradict NFR-001's
"zero errors for 0.2.0 artifacts" once Quire validates the declaration record,
which `validate_document` does unconditionally), nine mediums (an emitter
feasibility gap in FR-004, a nine-vs-ten object-type contradiction in
`spec.md`, three uncovered constraints behind a "no gaps" claim, an AC that
undercounts its own Behavior, an enumeration `## Values` form that diverges
from the upstream `EnumValue` mapping, an activation story that ignores the
reference-form `data_schema`, unspecified npm.ix/Node resolution, a
developer-path-bound IT, an undeclared Quire dependency with a skip escape,
and a stakeholder layer that never states the #4 need), and nine lows.

## Verdict

**Not ready for `spec-to-plan`.** Resolve FND-120 (a design decision, likely
an ADR plus an upstream ticket on quire-rs#388) and FND-121 (emitter
mechanism) before tasking FR-004; the remaining mediums are one-line spec
edits or new AC/TC rows. Once FND-120..FND-130 are dispositioned the matrix
can be regenerated and the plan started.

## Traceability Matrix

Completeness deliverable: US -> FR -> StR -> verification. "StR (direct)" is
the frontmatter relationship; "(via US)" means the only StR link is transitive.

| US | FR | StR | Verification (AC/CON -> TC) | Gap |
|---|---|---|---|---|
| — | FR-001 | none in frontmatter; tests.md asserts StR-001 | AC-1..4 -> TC-001..004; IT-001 | FND-130 |
| US-001 | FR-002 | StR-001 (via US) | AC-1..6 -> TC-010..015; CON-3 -> TC-016; CON-1, CON-2 -> none | FND-123 |
| US-001 | FR-003 | StR-001 (via US) | AC-1..6 -> TC-020..027; CON-1 -> TC-020 (equality only); CON-2 -> TC-023; IT-002 -> TC-070 | FND-134 |
| US-001 | FR-004 | StR-001 (via US) | AC-1..10 -> TC-030..039; CON-1 -> TC-040; CON-2 -> TC-038; TC-041 -> AC-1 (no nested-entity AC) | FND-123 |
| US-001 | FR-005 | StR-001 (via US) | AC-1..7 -> TC-050..056; CON-2 -> TC-051, TC-057; CON-1 -> none | FND-123 |
| — | NFR-001 (constrains FR-003, FR-005; not FR-004) | — | 4 metrics -> TC-060..063 | FND-120 |
| StR-001-VC-1 | — | — | TC-005 (Inspection) | — |
| StR-001-VC-2 | — | — | TC-006 (Manual; names templates the module does not ship) | FND-130 |

Every NFR is scoped (NFR-001 lists manifest, schemas, skeletons) but is
referenced by FR-003 and FR-005 only; FR-004 owns the schemas the NFR
measures and carries no relationship to it.

## Hidden Assumption Probes

| FR | Pattern | Result |
|---|---|---|
| FR-002 | Delegates to external CLIs (`node`, `tsp`) | No NFR declares the Node minimum, detection, or the error when absent (FND-127) |
| FR-002 | Depends on a registry-scoped package (`@agent-ix/semantic-core` on npm.ix) | Resolution mechanism with no `.npmrc` and a committed lockfile is unspecified (FND-127) |
| FR-002 | Generation command | Build (`make schemas`) and check (`--check`) modes are both specified; no interactive mode needed. OK |
| FR-003 | Lookup over multiple consumers (Quoin install, Quire load) | Tie-break not needed; both reject. The Quoin half of CON-1 is untested (FND-134) |
| FR-003 | Declares mapping names | `typed-table`, `sysml-fence`, `ocl-clause` are defined nowhere upstream (FND-131) |
| FR-004 | Depends on emitter capability | Negative and dual `contains` item rules have no stated TypeSpec expression under FR-002-CON-1 (FND-121) |
| FR-005 | Depends on a package version not yet released (Quire 0.46.0; quire-rs is at v0.45.0) | Pin undeclared; skip clause hides the absence (FND-129) |
| FR-001 | Calls an external service with a changed payload | Reference-form `data_schema` on activation is unaddressed; filament-core-service#23 open (FND-126) |

## Failure Domain Check

- Extension failures: the schemas are sealed (`unevaluatedProperties: {not: {}}`), so a future extractor key not listed in FR-004 fails every record; FR-004 lists the forward-compatible optional keys explicitly. OK.
- Identity keys: `identity: true` on `FieldDecl` is the only identity marker; FR-004 defines it once. Skeleton `id`/`title` as resolution keys are under-specified (FND-132).
- Evaluation purity: FR-002-CON-3 (deterministic emission) and FR-002-AC-4 (check mode) cover the build; the manifest digest rewrite's textual/structural mode is not (FND-137).
- Topological robustness: FR-004-AC-10 covers the unresolved-token edge; the legacy-artifact edge is where the spec breaks (FND-120).

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-120 | high | FR-004 makes `fields` (six types) and `operations` (repository, state_machine) required; Quire validates the declaration record unconditionally, so a legacy-form 0.2.0 artifact (no typed table, `fields` unavailable) fails `semantic.record-invalid` at `error`, contradicting NFR-001's zero-error metric and the advisory merge gate | FR-004, NFR-001, FR-003, FR-005 | wrong-requirement |
| FND-121 | medium | FR-004's item rules (Event: >=1 `Timestamp` field AND 0 identity fields; Entity/ValueObject: >=1 / 0 identity fields) need `contains` plus `minContains`/`maxContains`, and Event needs two `contains` predicates on one array (`allOf`); FR-002-CON-1 forbids anything but the official emitter and no decorator path is stated | FR-004, FR-002-CON-1 | missing-requirement |
| FND-122 | medium | `spec.md` says "nine tier-2 business ObjectTypes" in Purpose, In Scope, and System Description; the manifest, FR-003, and FR-004 declare ten | spec.md, FR-003, FR-004 | wrong-requirement |
| FND-123 | medium | `tests.md` claims "every acceptance criterion, named constraint, and NFR metric maps to at least one test case" and "Coverage Gaps: None", but FR-002-CON-1, FR-002-CON-2, and FR-005-CON-1 have no TC row and are omitted from the FR rows; TC-041 (nested entity) traces to FR-004-AC-1, which does not describe nested-entity rules, because FR-004 has no nested-entity AC | tests.md, FR-002, FR-004, FR-005 | correct-requirement-no-evidence |
| FND-124 | medium | FR-005-AC-4 states `clauses` `available` "for `aggregate_root`" only, while FR-005 Behavior mandates `## Invariants` on seven types; the Behavior's "requires or admits clauses" list also omits domain and enumeration, which FR-004 admits | FR-005, FR-004 | wrong-requirement |
| FND-125 | medium | FR-005 pins the enumeration `## Values` as a `Value \| Description` table "exactly as the manifest asserts", while quoin FR-071 defines the `EnumValue[]` mapping over a bullet list (`- value — doc`); the divergence is not recorded as a decision | FR-005, quoin FR-071 | wrong-requirement |
| FND-126 | medium | FR-001 and IT-001 are unchanged from 0.2.0: activation posts `manifest.yaml` alone, but the 0.3.0 manifest's `data_schema` references `schemas/<Model>.json`, which is not in the payload; filament-core-service accepts the form (FR-035-AC-14) but resolution is filament-core-service#23 (open); the spec is silent on the minimum service revision and on what IT-001-SC-03 "declared attributes" means for `data_schema` | FR-001, IT-001, FR-003 | missing-requirement |
| FND-127 | medium | FR-002 resolves `@agent-ix/semantic-core` from npm.ix through a committed `package-lock.json` with FR-002-CON-2 forbidding `.npmrc`; the resolution mechanism is unstated, semantic-core sits in `dependencies` (a runtime dep of a Markdown module for every npm consumer), and no NFR declares the Node/`tsp` minimum or the error when absent | FR-002 | missing-requirement |
| FND-128 | medium | IT-002 and FR-003-AC-5 bind the test to `/home/peter/dev/quoin` (`make build && npm i -g .`), `/home/peter/dev/spec-objects-business/...`, and "main at or after commit `3e842ce`"; the integration test is not reproducible outside one workstation and is Demonstration-only | IT-002, FR-003-AC-5 | wrong-requirement |
| FND-129 | medium | FR-005 requires a Quire wheel ">=0.46.0 with `extract_semantic`" (quire-rs is at v0.45.0), `pyproject.toml` declares no Quire dependency, and the skip-on-missing clause lets FR-003-AC-4, FR-005-AC-1..5, and NFR-001 evidence disappear silently | FR-005, FR-003, NFR-001 | missing-requirement |
| FND-130 | medium | The stakeholder layer never states the #4 need: StR-001 is the 0.2.0 activation need, StR-001-VC-2 validates "templates" the module does not ship, FR-001 has no StR/US relationship in frontmatter though `tests.md` asserts StR-001 -> FR-001, and FR-002..FR-005 reach StR-001 only through US-001 | StR-001, FR-001, US-001, tests.md | missing-requirement |
| FND-131 | low | FR-003 fixes `mappings: [typed-table, sysml-fence, ocl-clause]`; quoin FR-070 names no mapping vocabulary and the vendored schema admits any string, and mapping (d) (`data_schema` by digest, FR-073) is absent from the list | FR-003 | missing-requirement |
| FND-132 | low | FR-005 asserts a skeleton's `title` "(an `Identifier`)"; four current titles are not (`Order Management`, `Order Lifecycle`, `Order Fulfilment`, `Order state vocabulary`) and ids such as `entity-001` are not either; no requirement makes titles Identifiers | FR-005 | missing-requirement |
| FND-133 | low | FR-002-AC-1 "exactly the ten object-type models plus the support models the source declares" is circular; FR-004 Outputs already enumerates the six support files | FR-002-AC-1, FR-004 | wrong-requirement |
| FND-134 | low | FR-003-CON-1 duplicates FR-003-AC-6 (unknown-key refusal) and its "both consumers" Quoin half has no test: TC-020 checks block equality, TC-027/TC-070 never inject a `foo` key | FR-003, tests.md | correct-requirement-no-evidence |
| FND-135 | low | FR-003 Behavior "the module maintainer SHALL correct the manifest ... rather than relax the contract" is an obligation on a person, not observable system behaviour | FR-003 | wrong-requirement |
| FND-136 | low | The event skeleton carries two payload authorities: the `## Schema` JSON fence (kept as "wire representation") and the new `## Properties` typed table; no rule states agreement or precedence | FR-005, FR-004 | missing-requirement |
| FND-137 | low | FR-002 "edit `manifest.yaml` only at `data_schema.digest`" against a manifest that uses YAML anchors and comments: a structural rewrite drops both; whether FR-003-AC-3's baseline comparison is byte- or structure-level is unstated | FR-002, FR-003-AC-3 | missing-requirement |
| FND-138 | low | NFR-001's statement is universal ("every artifact that validated against 0.2.0") but the measurement samples one legacy entity skeleton; the other nine 0.2.0 skeleton forms (bullet-list repository operations, prose aggregate members, ...) are unsampled | NFR-001 | correct-requirement-no-evidence |
| FND-139 | low | Small consistency items: `spec.md` `depends_on: []` beside four `depends_on` relationships; FR-001 cites FR-026-AC-1 and FR-034 without links; IT-001-SC-01 has no TC; US-001-EX-2 (value object with identity refused) maps to TC-053 instead of TC-032/TC-054 | spec.md, FR-001, IT-001, tests.md | wrong-requirement |

## Finding Details

### FND-120 (high) — required record keys versus legacy artifacts

Evidence. FR-004's table requires `fields` on entity, nested_entity,
value_object, aggregate_root, event, process and `operations` on repository
and state_machine (with `minItems` 1). quire-rs FR-070 sets `fields`
`unavailable` (`legacy-form`) for a bullet-list or free-column Properties
section and the record then carries no `fields` key (FR-004 Inputs: "any key
absent when its section is absent"). `validate_document`
(`quire-rs/src/validate_document.rs`, `semantic.record-invalid`) validates
`record.declaration_record()` against the resolved schema whenever the
archetype has a data validator, with no availability gate. Every 0.2.0
skeleton is a legacy form (`entity.md`, `value_object.md` use bullet lists;
`repository.md` bullet operations with no `### <name>`), so each yields one
`semantic.legacy-properties-form` warning **and** one
`semantic.record-invalid` error. NFR-001 targets 0 errors and 1 warning for
exactly that fixture; the ticket's merge gate is "advisory-only until corpus
promotion".

Proposed fix. Decide and record (ADR): (a) keep FR-004's required keys and
require Quire to skip record validation when any declaration kind is
`unavailable`/`missing`/`not_applicable` in a legacy artifact (a quire-rs#388
change, to be filed and referenced from FR-004 and NFR-001), or (b) drop
`required` from every type and carry the "must have >=1 field" rule as an
`available`-only rule enforced by the extractor, keeping the schema
additive. Under either option add NFR-001 as a `constrains` relationship on
FR-004 and extend the NFR-001 fixture set to the repository and aggregate
legacy skeletons.

### FND-121 (medium) — emitter expressibility of the item rules

FR-004 Outputs names `IdentityField`/`OccurrenceField` as "open marker
schemas used by `contains`" but never states the TypeSpec decorators. In
`@typespec/json-schema` 1.15.0 `@contains`, `@minContains`, and
`@maxContains` apply once per property; "0 identity fields" needs
`@contains(IdentityField) @minContains(0) @maxContains(0)`, and Event needs
that **and** `@contains(OccurrenceField)` on the same `fields` array, which
JSON Schema only admits through `allOf`. FR-002-CON-1 forbids a custom
emitter and hand edits, so the only route is `@extension("allOf", ...)`.
State the decorator recipe per rule in FR-004 Behavior (or relax Event to one
predicate and move the other to the extractor), and add an AC that the
recipe uses official decorators only.

### FND-122 (medium) — nine versus ten

`spec.md` lines 45, 79 (and Purpose) say nine; `manifest.yaml` declares ten
object types (`nested_entity` is the tenth), FR-003 lists ten exports, FR-004
ten models. Replace "nine" with "ten" and list them once. Outside the spec
but the same defect: `pyproject.toml` and `package.json` descriptions list
eight (no `nested_entity`, no `enumeration`).

### FND-123 (medium) — matrix completeness claim

Add TC rows of type Inspection for FR-002-CON-1 (official emitter only, no
hand edits), FR-002-CON-2 (no `.npmrc`/`file:`/`link:`/upper bound), and
FR-005-CON-1 (no corpus or vendored-fixture edit), and list them in the FR
rows. Add FR-004-AC-11 for nested_entity (local identity validates,
`relations` fails, `owner` accepted) and retarget TC-041 to it. Then the
Overview and Coverage Gaps statements become true.

### FND-124 (medium) — FR-005-AC-4 undercounts Behavior

Rewrite AC-4 to enumerate `clauses` `available` for the seven types Behavior
mandates (`entity`, `nested_entity`, `value_object`, `aggregate_root`,
`event`, `state_machine`, `process`) and `not_applicable` for `domain`,
`enumeration`, `repository`; fix the Behavior bullet to "requires or is
mandated here to author clauses" or include domain/enumeration.

### FND-125 (medium) — enumeration Values form

quoin FR-071: "An enumeration SHALL be an artifact of the `enumeration`
object type whose `## Values` list maps to `EnumValue[]` (`- value — doc`)".
FR-005 keeps the `Value | Description` table because the 0.2.0
`values_table` locator must survive (NFR-001). Record the divergence as an
ADR (table stays, bullet mapping deferred to the engine ticket) or ask quoin
to admit the table form; do not leave it implicit.

### FND-126 (medium) — activation with reference-form `data_schema`

`filament-core-service` `origin/main` validates the `semantic` block and
reference form (FR-035-AC-13..15) and stores `data_schema` as posted
(`filament_core_client.py:56`); resolving the reference into a snapshot is
`agent-ix/filament-core-service#23` (open). FR-001 should state the minimum
service revision (post-CR-003) and IT-001-SC-03 should say what the
registered `data_schema` is expected to be (the reference object, verbatim)
until #23 lands; otherwise FR-001-AC-4 has two valid readings.

### FND-127 (medium) — npm.ix, lockfile, and toolchain preconditions

State how `npm ci` reaches npm.ix without a repo `.npmrc` (registry flag or
environment, per the ecosystem rule), whether `package-lock.json` may carry
npm.ix resolved URLs (the ecosystem rule says stable builds only), move
`@agent-ix/semantic-core` to `devDependencies` (it is a build input, not a
runtime need of the published Markdown module), and add an NFR naming the
Node minimum for TypeSpec 1.15.0 and the error when `node`/`tsp` is absent.

### FND-128 (medium) — IT-002 portability

Replace the absolute paths with `<quoin checkout>` / `<module dir>` and pin
Quoin by released version (the first release containing FR-070/073/075)
rather than a commit; keep the path form only in the Test Procedure's
example. FR-003-AC-5 should say "a Quoin at or above `<version>`".

### FND-129 (medium) — undeclared Quire dependency and the skip escape

Declare `quire` (>= the first wheel with `extract_semantic`; today's tag is
v0.45.0, so 0.46.0 is a forecast, not a fact) as a dev dependency in
`pyproject.toml`, and change the skip clause: skipping is acceptable
locally, but the CI job that produces the FR-003/FR-005/NFR-001 evidence
must fail, not skip, when the function is missing.

### FND-130 (medium) — stakeholder layer

Add StR-002 (or a VC-3 on StR-001) stating the #4 need in stakeholder terms:
one typed structural contract per business object that the downstream
frontends (quire-contract-ir#52, filament-core-data#36) can consume
read-only. Fix StR-001-VC-2 ("templates" -> "skeletons and schemas") and
add `traces_to`/`implements` relationships from FR-001 to StR-001 so the
`tests.md` StR row matches the frontmatter.

### Lows

- FND-131: cite the source of the mapping names or define them in FR-003 and add `digest-reference` (FR-073).
- FND-132: add "Every skeleton `title` SHALL be an `Identifier`" to FR-005 and rename the four titles.
- FND-133: replace with "the ten object-type models and the six support models of FR-004 Outputs (16 files)".
- FND-134: fold FR-003-CON-1 into AC-6 or add a Quoin-side TC injecting `foo`.
- FND-135: move the maintainer obligation to Rationale or a boundary Constraint on the module (not a person).
- FND-136: state that the event `## Schema` fence is a derived view of the typed table, or add an AC that its `required` set equals the table's field names.
- FND-137: specify a textual digest rewrite (anchors and comments preserved) and that the AC-3 comparison is structural.
- FND-138: scope NFR-001 to "the checked-in 0.2.0 skeleton set" and sample every type, or narrow the Statement.
- FND-139: set `spec.md` `depends_on` to the four targets or drop the empty key; link FR-026/FR-034; add a TC for IT-001-SC-01; retarget the US-001-EX-2 row.

## Dispositions

| Finding | Disposition |
|---|---|
| FND-120 | Applied: see failure-domain.md FND-100. No schema relaxed; the engine defect is `agent-ix/quire-rs#391` and NFR-001-AC-2 is a named expected failure. NFR-001 now carries a `constrains` relationship to FR-004 and its fixture set is the whole checked-in 0.2.0 skeleton set. |
| FND-121 | Applied: FR-004 Behavior states the decorator recipe (`@contains(IdentityField)`, `@contains(IdentityField) @minContains(0) @maxContains(0)`, and the event occurrence rule as an `@extension("allOf", …)` clause over `OccurrenceField.json`), all official-emitter decorators, satisfying FR-002-CON-1. |
| FND-122 | Applied: `spec.md` says ten in Purpose, In Scope and System Description. |
| FND-123 | Applied: TC-017, TC-018, TC-058 added for the three `Inspection` constraints; FR-004-AC-11 added and TC-041 retraced; the FR rows list the full TC ranges. |
| FND-124 | Applied: FR-005 Behavior names exactly seven Invariants-bearing skeletons and states that `domain`, `repository`, `enumeration` carry none; FR-005-AC-4 enumerates the availability matrix to match. |
| FND-125 | Applied: FR-005 Behavior records the divergence and names `agent-ix/quoin#335` as where the `EnumValue[]` mapping is decided; the `Value \| Description` table stays because NFR-001 forbids changing the 0.2.0 locator. |
| FND-126 | Applied: FR-001 Behavior and IT-001-SC-03 state that while `agent-ix/filament-core-service#23` is open the registered `data_schema` is the reference object as posted; FR-001-AC-4 reads against that value, and the minimum service revision is pinned. |
| FND-127 | Applied: `@agent-ix/semantic-core` moved to `devDependencies` (it is a build input; the published artifact is Markdown and JSON), FR-002 Inputs names Node 20, FR-002 Behavior fails naming the required Node version or the missing `tsp`, and FR-002-CON-4 states the npm.ix resolution discipline. |
| FND-128 | Applied: IT-002 uses `<checkout>` paths and states the Quoin build by repository and commit with the reason no release can be named. |
| FND-129 | Applied: see dependency.md FND-141. The skip escape is gone; the CI-visible failure is the gate. |
| FND-130 | Applied: StR-001 gains VC-3 (one typed structural contract per business object, consumable read-only by the downstream frontends) with TC-075; StR-001-VC-2 reads "skeletons and schemas"; FR-001 gains a `traces_to` StR-001 relationship so the `tests.md` StR row matches the frontmatter. |
| FND-131 | Recorded, no change. See dependency.md FND-147: the mapping names have no registry to be checked against, and the digest reference is a manifest form rather than a Markdown authoring mapping. |
| FND-132 | Applied: see failure-domain.md FND-102. |
| FND-133 | Applied: FR-002-AC-1 enumerates the seventeen files by name. |
| FND-134 | Applied: FR-003-CON-1 is scoped to Quire's loader refusal (verified by FR-003-AC-6) and states Quoin's refusal as the neighbour's obligation, assumed and evidenced only by IT-002's clean install. |
| FND-136 | Applied: see failure-domain.md FND-101 — the typed table is the authority, the `## Schema` fence a derived view. |
| FND-135 | Applied: the FR-003 maintainer obligation is restated as a module obligation ("this module SHALL correct its own manifest or schemas rather than relax …"). |
| FND-137 | Applied at implementation: the generator rewrites `data_schema.digest` textually, so YAML anchors and comments survive; FR-002 Behavior already scopes its manifest writes to those values, and the FR-003-AC-3 locator comparison is structural (parsed YAML), which the baseline test asserts. |
| FND-138 | Applied: NFR-001's Statement is narrowed to the population it measures (the checked-in 0.2.0 skeleton set) and the measurement is widened from the entity skeleton to all ten. |
| FND-139 | Applied in part: FR-026/FR-034 stay unlinked (they are filament-core-service ids cited in prose, and `ix://` links to them are already carried by FR-001's Dependencies); `spec.md` keeps `depends_on: []` because that key is the module-dependency list, a different axis from the requirement-lineage `relationships`. The US-001-EX-2 row is illustrative, not a trace target, and the matrix row it appears in lists TC-050, TC-053 and TC-070 as the story's coverage, which is unchanged. IT-001-SC-01 is an environment precondition with no separable test. |
