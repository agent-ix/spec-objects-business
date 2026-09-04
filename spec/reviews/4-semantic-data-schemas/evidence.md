---
id: SR-005
title: "Evidence review of the #4 semantic data schemas spec set"
type: SpecReview
analysis: evidence
scope: "spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/stakeholder/StR-001, spec/integration/IT-001, IT-002, spec/tests.md"
review_set: all
---
# SR-005: Evidence review of the #4 semantic data schemas spec set

## Summary

Every `Verification` cell in FR-001..FR-005, every `Validation` cell in the
constraint and StR tables, every NFR-001 `Method` cell, and every Test Matrix
`Type` was checked against the declared catalog in
`spec-artifacts-process/manifest.yaml` (33 method ids across the classes
`Test`, `Analysis`, `Inspection`, `Demonstration`; matrix `Type` vocabulary
`Unit | Integration | E2E | Property | Fuzz | Benchmark | Static | Compile |
Snapshot | Manual | Eval | Inspection | Analysis | Demonstration`).
`quoin advise` was run over the 37 obligations `quire coverage --json` derives
(33 acceptance criteria, 4 NFR-001 measurement rows): 1 mismatch, 4
uncatalogued, 0 inconclusive. Context: agent-ix/spec-objects-business#4.

What the engine found on its own: the four FR-001 cells (`Schema Test`,
`Integration Test`) are strings no catalog entry or class declares, so quire
reports `uncatalogued-verification-method` for them and nothing can say what
discharging them means; FR-003-AC-5 is authored `Demonstration` against a
criterion with an executable exit-code oracle. What judgement adds: the
`Inspection`/`Manual` rows have no inspections registry to be discharged
through and no suite registry exists at all, so four matrix rows and three
`Inspection` constraints currently have no evidence path; StR-001's own prose
says its criteria are demonstrated, while its table and matrix row say
`Inspection`; and the advisor's `performance-benchmarking` for NFR-001 and
`dast`/`iast`/`demonstration` for two FR criteria are rule misfires the author
should not follow. The evidence store is empty (binding census: 13 Python test
symbols, 0 tagged, 0 of 81 rows backed), so every row is honestly `🚧` and no
evidence-derived characteristic (`fault-detection-*`) can mint yet.

## Verdict

**Revise before the matrix is treated as the verification contract.** The
spec set is close: 29 of 33 acceptance criteria carry a declared class and the
advisor agrees with them. The blocking items are the four uncatalogued FR-001
cells (FND-160, FND-161) and the missing discharge path for every non-symbol
row (FND-164). The remaining findings are method refinements the author can
accept or decline in the `Verification` cell, which is the obligation's method
(quire-rs FR-053).

Counts: 0 high, 5 medium, 7 low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|----|----------|---------|------|--------------|
| FND-160 | medium | FR-001-AC-1 is authored `Schema Test`, which is neither a catalog method id nor a class (`uncatalogued-verification-method`). Recommend `unit-testing` (Unit): `quire.validate_manifest` against the vendored FR-035 schema is one component against a fixed oracle, which is what TC-001 already types it as. `contract-testing` (published-interface, cross-repo-boundary) is the stronger reading if the schema is fetched from filament-core-service rather than vendored; judgement, not a rule match. | FR-001-AC-1, TC-001 | wrong-requirement |
| FND-161 | medium | FR-001-AC-2, AC-3, AC-4 are authored `Integration Test`, an uncatalogued string (3 rows). The intended method is `integration-testing` (Integration): two components across a real HTTP boundary, matching IT-001 and TC-002..TC-004. The advisor recommended `bdd-spec-by-example`/`unit-testing` on the `example` shape only because the statements carry no `cross-component` characteristic it can read; that recommendation is set aside by judgement. AC-3 is idempotence-shaped (re-POST, same hash) and could also be held as a `property-based-testing`/`metamorphic-testing` relation, but one integration run discharges the criterion as written. | FR-001-AC-2, FR-001-AC-3, FR-001-AC-4, IT-001, TC-002, TC-003, TC-004 | wrong-requirement |
| FND-162 | medium | FR-003-AC-5 is the advisor's one mismatch: authored `Demonstration`, recommended `unit-testing`/`bdd-spec-by-example` (example). The criterion has an executable oracle (exit code 0, `quoin module` listing contains the name, prior entry restored), and IT-002 writes it as a five-step CLI procedure with recorded state. Recommend `integration-testing` (Integration) with a fixture that records and restores the installed entry. As authored, its matrix rows TC-027 and TC-070 are `Manual`, a `no_source_symbol` type, so the criterion can never be backed by a tag, and the pinned precondition (Quoin built from `/home/peter/dev/quoin`) is machine-specific. If the author keeps `Demonstration`, the row must be discharged through an inspections registry, which does not exist (FND-164). | FR-003-AC-5, IT-002, TC-027, TC-070 | correct-requirement-no-evidence |
| FND-163 | medium | StR-001-VC-1 is authored `Inspection` and its matrix row TC-005 is typed `Inspection`, but the StR's own text says "Satisfaction is judged by demonstrating both outcomes against a running `filament-core` instance", and the same outcome is already an executable integration criterion (FR-001-AC-4 via TC-004). `Inspection` is for `judgement-required, no-executable-oracle`; this has an oracle. Recommend `demonstration` (Demonstration) for the stakeholder-facing validation, tracing to TC-004 as the observed run, or drop TC-005 and let TC-004 carry both ids. VC-2 (`Demonstration`, TC-006 `Manual`) is consistent with the catalog (`demonstration` produces `Manual` evidence). | StR-001-VC-1, StR-001-VC-2, TC-005, TC-006, TC-004 | wrong-requirement |
| FND-164 | medium | No evidence-plan artifacts exist: quire reports `declaration 'suite' declares archetype 'SuiteRegistry', which no document has` and `declaration 'inspection' declares archetype 'Inspections', which no document has`. Four matrix rows are `no_symbol_rows` (TC-005 Inspection, TC-006 Manual, TC-027 Manual, TC-070 Manual) and three constraints are `Inspection` (FR-002-CON-1, FR-002-CON-2, FR-005-CON-1) with no matrix row at all. Every one of these needs the inspections registry to be discharged, and every Integration/Unit row needs a suite to produce its evidence kind (IT-001 in particular needs an Integration suite that says where the running filament-core comes from). This is a gap in the plan, not in the spec. | TC-005, TC-006, TC-027, TC-070, FR-002-CON-1, FR-002-CON-2, FR-005-CON-1, IT-001 | correct-requirement-no-evidence |
| FND-165 | low | NFR-001-M-1..M-4 are authored `Test` (class). The advisor recommends `performance-benchmarking` on `quantified-threshold`, which is a rule misfire: the targets are `0`, `1`, `identical`, not latency or throughput. Judgement: M-1 (0.2.0 locators unchanged) and M-4 (`properties` string identical) are `stable-output` comparisons against a checked-in baseline, so `golden-approval-testing` (Snapshot); M-2 and M-3 (legacy skeleton under 0.3.0 yields 0 errors, exactly 1 `semantic.legacy-properties-form` warning) exercise Quire against the module, so `integration-testing` (Integration), matching TC-061..TC-063. TC-060 is typed `Unit`; `Snapshot` is the honest type for a baseline diff. Separately, the NFR has no `## Acceptance Criteria` section, so the `nfr-acceptance-criterion` declaration mints nothing from it (`section-matches-nothing`); the obligations come from the Measurement table only. | NFR-001, TC-060, TC-061, TC-062, TC-063 | wrong-requirement |
| FND-166 | low | FR-002-CON-3 (two runs over one source are byte-identical) is authored `Test` and TC-016 is typed `Integration`. The property is `stable-output` over a serialization, which is `golden-approval-testing` (Snapshot) or, as a relation between two executions, `metamorphic-testing` (Property). Either is more specific than the class and names the evidence kind the suite must produce. | FR-002-CON-3, TC-016 | wrong-requirement |
| FND-167 | low | FR-004-AC-2..AC-9 are typed `Integration` in the matrix (TC-031..TC-038, TC-041) although each validates an in-memory record against one shipped schema file with a JSON Schema library: a single component against a fixed expected result, which is `unit-testing` (Unit). The advisor's `property-based-testing` for these comes from the `universal` catch-all (quire reports `catch-all-universal` for all 6 documents), and the criteria are written as explicit positive/negative fixtures, so `unit-testing` is the judgement; `bdd-spec-by-example` adds nothing here. FR-004-AC-10 (extractor reports `semantic.unresolved-type`) genuinely crosses into Quire and stays `Integration`. | FR-004-AC-2, FR-004-AC-3, FR-004-AC-4, FR-004-AC-5, FR-004-AC-6, FR-004-AC-7, FR-004-AC-8, FR-004-AC-9, TC-031, TC-032, TC-033, TC-034, TC-035, TC-036, TC-037, TC-038, TC-041 | wrong-requirement |
| FND-168 | low | FR-002-CON-2 (no `.npmrc`, no `file:`/`link:` dependency, no upper bound beyond the exact pin) is authored `Inspection`, but every clause has an executable oracle over `package.json` and the tree. Recommend `unit-testing` (Unit) or a `Static` check so it gets a matrix row and a symbol; `Inspection` is right for FR-002-CON-1 (no custom emitter, no hand-edited file) and FR-005-CON-1 (no corpus repo edited), which are judgement over authored intent. | FR-002-CON-2, FR-002-CON-1, FR-005-CON-1 | wrong-requirement |
| FND-169 | low | The `Functional Requirement Coverage` table in `spec/tests.md` uses the header `Coverage Status` while the module configures `traceability.status.column: Status`; quire reports `status-column-matches-nothing` and skipped status classification for that table, so a complete-but-unbacked requirement row could not be checked for a status lie. The per-test `Test Case Summary` table does carry `Status` and was classified (0 status lies, all rows `🚧`). Rename the column or the configuration; the engine will not guess. | TM-001 | correct-requirement-no-evidence |
| FND-170 | low | Advisor residue recorded as judgement, not verdict: FR-004-AC-10 was recommended `demonstration` on `stakeholder-acceptance` and FR-005-AC-7 was recommended `dast`/`iast`/`sast`/`negative-abuse-testing` on `security`; both are characteristic misreads of the statement text (a schema accepting a placeholder token; a skeleton having no placeholder token), and the authored `Test` stands. FR-004-AC-9 (`{}` validates for Domain/Enumeration and fails elsewhere) matched `input-validation` and `negative-abuse-testing` is a defensible refinement, but `unit-testing` over the paired fixtures discharges it. No obligation was inconclusive. | FR-004-AC-10, FR-005-AC-7, FR-004-AC-9 | wrong-requirement |
| FND-171 | low | The evidence store is empty: binding census walked 13 Python evidence symbols in `tests/` and found 0 carrying any declared trace-tag form (`pytest-trace-marker`, `python-trace-line`, `python-comment-id`, `python-docstring-id`; example `test_manifest_path_points_to_packaged_manifest` at `tests/test_basic.py:4`), so `coverage.backed` is 0 of 81 with a `hollow-denominator` warning and every row is `🚧`. That is honest, not a lie, but it means no `fault-detection-unmeasured`/`fault-detection-failed` characteristic can mint and `mutation-testing`/`concolic-execution` were correctly recommended for nothing. Tag the existing FR-001 tests when the matrix is implemented. | TM-001, FR-001-AC-1 | correct-requirement-no-evidence |

## Method recommendations per obligation

Only obligations whose authored method should change or be sharpened are
listed; the 29 acceptance criteria authored `Test` whose advisor
recommendation is a `Test`-class method (`unit-testing`,
`property-based-testing`, `bdd-spec-by-example`) match at class level and
need no edit.

| Obligation | Authored | Advisor | Recommended | Basis |
|---|---|---|---|---|
| FR-001-AC-1 | Schema Test (uncatalogued) | unit-testing, bdd-spec-by-example | `unit-testing` | judgement; `contract-testing` if the schema is fetched, not vendored |
| FR-001-AC-2 | Integration Test (uncatalogued) | unit-testing, bdd-spec-by-example | `integration-testing` | judgement: real HTTP boundary |
| FR-001-AC-3 | Integration Test (uncatalogued) | unit-testing, bdd-spec-by-example | `integration-testing` | judgement; idempotence relation noted |
| FR-001-AC-4 | Integration Test (uncatalogued) | property-based-testing | `integration-testing` | judgement: registry reads after activation |
| FR-003-AC-5 | Demonstration | unit-testing, bdd-spec-by-example (mismatch) | `integration-testing` | rule + judgement: exit-code oracle, state restore is fixture work |
| StR-001-VC-1 | Inspection | not an obligation (VC table) | `demonstration` | StR prose: "judged by demonstrating" |
| NFR-001-M-1, M-4 | Test | performance-benchmarking (misfire) | `golden-approval-testing` | judgement: baseline diff, stable-output |
| NFR-001-M-2, M-3 | Test | performance-benchmarking (misfire) | `integration-testing` | judgement: Quire validates the legacy skeleton |
| FR-002-CON-3 | Test | not an obligation (constraint) | `golden-approval-testing` or `metamorphic-testing` | judgement: two runs byte-identical |
| FR-002-CON-2 | Inspection | not an obligation (constraint) | `unit-testing` | judgement: executable oracle over the tree |
| FR-004-AC-2..AC-9 | Test | property-based-testing (universal catch-all) | `unit-testing` | judgement: explicit paired fixtures against one schema |

## Suite plan implied

The methods above imply these evidence kinds, and no suite registry declares a
producer for any of them (FND-164):

- `Unit` (pytest over `spec_objects_business/`, `schemas/`, `manifest.yaml`): FR-001-AC-1, FR-002-AC-1..3, FR-003-AC-1..3, FR-004-AC-1..9, FR-004-CON-1, FR-005-AC-6..7, FR-002-CON-2.
- `Integration` (pytest with the Quire wheel and, for FR-001/IT-001, a running filament-core): FR-001-AC-2..4, FR-002-AC-4..6, FR-003-AC-4..6, FR-003-AC-5 (if retyped), FR-004-AC-10, FR-005-AC-1..5, FR-005-CON-2, NFR-001-M-2..3, IT-002.
- `Snapshot` (checked-in 0.2.0 baseline): NFR-001-M-1, M-4, FR-002-CON-3.
- `Manual` via an inspections registry: StR-001-VC-2, FR-002-CON-1, FR-005-CON-1, and FR-003-AC-5 / StR-001-VC-1 only if their authored method is kept.

## Diagnostics consulted

From `quire coverage --scope . --json` (engine 0.31.0): `uncatalogued-verification-method` x2 (`Schema Test`, `Integration Test`), `status-column-matches-nothing` (functional-coverage), `section-matches-nothing` (NFR-001 has no `Acceptance Criteria`), `archetype-matches-nothing` x2 (`SuiteRegistry`, `Inspections`), `no-symbol-bound` (13 Python symbols, 0 tagged), `hollow-denominator` (`coverage.backed`), `catch-all-universal` (6 of 6 documents). Duplicate* module-load noise ignored.

## Dispositions

| Finding | Disposition |
|---|---|
| FND-160 | Applied: FR-001-AC-1 is `Test`; TC-001 stays `Unit`. The catalog method id is not authored in the cell because every other criterion in this spec set uses the class form; the class is what `quire coverage` reads. |
| FND-161 | Applied: FR-001-AC-2..AC-4 are `Test`; TC-002..TC-004 stay `Integration`. |
| FND-162 | Recorded, declined for now. FR-003-AC-5 stays `Demonstration` because no released Quoin carries the semantic installer (`agent-ix/quoin` main `3e842ce`, no tag), so there is nothing a CI fixture could install; IT-002 makes the restore step unconditional and drops the developer path, which removes the parts of the finding that were about reproducibility. When a Quoin release carries FR-070/FR-073/FR-075 the criterion should be retyped `Test`/Integration. |
| FND-163 | Applied: StR-001-VC-1 is `Demonstration` and TC-005's matrix type changed from `Inspection` to `Demonstration`. |
| FND-164 | Recorded, carried to the plan, not to the spec — as the finding itself says. `tests.md` Coverage Gaps now names the two absent evidence-plan artifacts (`SuiteRegistry`, `Inspections`) and the eight rows that need them, so the gap is published rather than implied. Authoring those registries is process-artifact work outside issue #4's deliverables. |
| FND-165 | Recorded, no change to the method cells; NFR-001 gained the `## Acceptance Criteria` section the second half of the finding asks for (see base.md FND-008). The class form `Test` is kept for the four criteria; the finding's `Snapshot`/`Integration` refinement is a matrix `Type` question and TC-060 stays `Unit` because the baseline it diffs is a checked-in YAML fragment, not a rendered artifact. |
| FND-166 | Recorded, no change. TC-016 stays `Integration`: the two runs invoke the real generator and the real emitter. |
| FND-167 | Recorded, no change. TC-031..TC-038 and TC-041 stay `Integration` because they load the emitted schema files produced by the real toolchain rather than an in-repo fixture; the distinction the finding draws is real but does not change what the tests do. |
| FND-168 | Applied in part: FR-002-CON-2 keeps `Inspection` as its Validation class, but TC-018 now exists as a row and the implementation asserts it executably over `package.json` and the tree. FR-002-CON-1 and FR-005-CON-1 stay judgement-only (TC-017, TC-058). |
| FND-169 | Recorded, no change here. The `Coverage Status` header is the shape every other repo's matrix uses; renaming it is a `traceability.status.column` configuration question for the process module, not a change to this spec. |
| FND-170 | Recorded, no change; the authored `Test` stands, as the finding recommends. |
| FND-171 | Applied at implementation: every test landed for this issue carries the repo's trace-tag form so `quire coverage` binds the rows, and the pre-existing FR-001 tests are tagged with it. |
