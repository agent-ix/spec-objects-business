---
id: SR-012
title: "Spec review — PR #51 FR-004 and FR-006 changes"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-business; spec/functional/FR-004-role-schemas.md, spec/functional/FR-006-model-table-locators.md, spec/spec.md, spec/tests.md (PR #51)"
review_set: subset
---
# SR-012: Spec review — PR #51

## Summary

Ticket: PLAT-1302 (primary), PLAT-1305. Reviewed the changed spec text
(FR-004 Population row, `Transition`, `PopulationMember`, `Expression`,
`OperationExpression` statements, FR-004-CON-2, FR-004-AC-7, AC-9, AC-12;
FR-006 Inputs, locator table, population Behavior line, AC-6; spec.md
out-of-scope bullet; tests.md TC-036, TC-038, TC-042, TC-085) against
quire-rs `origin/main` FR-075 and FR-071 and `semantic-v1.schema.json`.
The `Expression` and `OperationExpression` statements match semantic-v1
exactly. The spec.md bullet and the tests.md rows are consistent with the
FR edits.

## Verdict

**NOT MERGEABLE** — FR-004 states that the population data record requires
`extent`, which contradicts what quire-rs validates (FND-001); FR-006 states
a locator mechanism FR-075 does not use (FND-002) and still restricts a
`Guard` to a clause id although FR-004 now admits inline guard expressions
(FND-003).

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | high | FR-004's population row makes `extent` the required key of the `Population` data record, and FR-004-AC-9 / CON-2 follow it (`{}` no longer passes `Population.json`). quire-rs validates `data_schema` against the declaration record, which never carries `model.population`; FR-075 carries `extent` in `model.population` (`{ extent, extentSpan, members }`). The FR therefore specifies a record no engine produces and makes every population artifact invalid (SR-010 FND-001). The population row should list no required key, and AC-9 / CON-2 revert to `{}` passing `Population.json`. | spec/functional/FR-004-role-schemas.md:67, spec/functional/FR-004-role-schemas.md:88, spec/functional/FR-004-role-schemas.md:102 | wrong-requirement |
| FND-002 | medium | FR-006 says the population `extent` is "declared by an `extent` `frontmatter_field` locator beside the `population` table locator". quire-rs FR-075 says `extent` "is a population feature, declared by the object type's `population` table locator". The FR describes a mechanism the engine does not use and mandates a redundant locator (SR-010 FND-002). | spec/functional/FR-006-model-table-locators.md:65 | wrong-requirement |
| FND-003 | medium | FR-006 Behavior still says a transition's `Guard`, when present, "SHALL name an invariant clause", and line 73 still calls inline guard expressions future work (`agent-ix/quire-rs#433`, "Until then ..."). FR-004 now admits `guardExpression` because quire-rs FR-075 extracts a non-identifier `Guard` cell as an inline expression. The two FRs contradict each other on what a `Guard` cell may hold. | spec/functional/FR-006-model-table-locators.md:66, spec/functional/FR-006-model-table-locators.md:73, spec/functional/FR-004-role-schemas.md:70 | wrong-requirement |
| FND-004 | low | FR-075 says a transition carries `guard` or `guardExpression`, "never both"; FR-004's `Transition` statement and `Transition.json` admit both together with no stated reader rule. | spec/functional/FR-004-role-schemas.md:70, spec_objects_business/schemas/Transition.json:15-20 | missing-requirement |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-005 | low | The fix added "a retired `Type \| Extent` population table" to FR-006 Behavior's list of negative fixtures, which now names thirteen cases, but FR-006-AC-4 still says "each of the twelve negative fixtures in Behavior" and no negative fixture file with an `expect:` code exists for the retired table (it is synthesized inside TC-085). The list and AC-4 disagree on count and on what counts as a fixture. | spec/functional/FR-006-model-table-locators.md:76, spec/functional/FR-006-model-table-locators.md:91 | wrong-requirement |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-006 | high | The round-2 rewrite of FR-007-AC-10 says that until quire-rs#435 lands, the `process` and `repository` rows validate and extract "into `relations` with no `emits` or `persists` key". Measured on quire 0.53.0, that holds only for an extraction request with no `dataSchema`. `validate_document` passes the object type's data schema, lowers the rows into `emits` / `persists` (that is why the record now validates against the sealed `Process.json`), and `extract_semantic` with `dataSchema` returns `emits: [ix://agent-ix/spec-objects-business/event_001]` and `persists: [ix://agent-ix/spec-objects-business/aggregate_root_001]` with no `relations`. AC-10 states as engine behaviour a test-harness omission and locks it in through TC-098; by its own text AC-10 should be removed because AC-9 now passes. | spec/functional/FR-007-relationships-table.md:82, spec/tests.md:146, tests/test_relationships.py:469-487 | wrong-requirement |
| FND-007 | medium | FR-007-AC-6 now requires the `value_object` `relations` violation to be "reported at line 1" and drops the `agent-ix/quire-rs#440` reference. #440 is open and says the finding should name the Relationships table line; quire-rs `record_key_line` intends the Relationships row for `relations` and falls back to line 1 only because the unevaluated-property error path is `<root>`. The AC records a known engine defect as the requirement, and TC-094 asserts `line == 1` with no ticket cited, so the pin gives no hint why it may flip. | spec/functional/FR-007-relationships-table.md:78, spec/tests.md:142, tests/test_relationships.py:328-330 | wrong-requirement |

## Dispositions

Round 1, checked against fix commit c25ddc6.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | FR-004 population row now lists no required key with `extent` optional; CON-2 and AC-9 have `{}` passing `Population.json` again, and the `PopulationMember` statement says the engine owns the `extent` check and the declaration record omits it. |
| FND-002 | fixed | FR-006 now says the engine reads `extent` with the `population` table locator and refuses a missing or invalid value with `semantic.invalid-model-cell`; the separate locator wording is gone. |
| FND-003 | fixed | FR-006 Behavior now lets a `Guard` name an invariant clause "or hold an inline Quire expression", and the invariant line no longer calls inline expressions future work. |
| FND-004 | fixed | `Transition.json` carries `not: {required: [guard, guardExpression]}` (TypeSpec `@extension("not", ...)`); FR-004 states the exclusivity, AC-7 and TC-036 assert a transition with both fails. |
| FND-005 | fixed | Round 2 (4f0caf2): the FR-006 Behavior negative-fixture list again names twelve cases, matching FR-006-AC-4 and the twelve fixture files; the retired-table case stays under AC-6 / TC-085. |
| FND-006 | fixed | Round 3 (e166aec): AC-10 is deleted; FR-007 Behavior states that Quire lowers `emits`/`persists` rows when the request carries the data schema, as `validate_document` does, and that a request without it leaves them in `relations`; source/owner stay under quire-rs#435. FR-008 and spec/tests.md agree (FR-007-AC-1..9, TC-089..TC-097, TC-097 ✅, TC-088 the only expected failure named). Measured: true on quire 0.53.0. |
| FND-007 | fixed | Round 3 (e166aec): FR-007-AC-6 requires a line and names line 1 as the known gap `agent-ix/quire-rs#440`; TC-094 asserts only that an integer line ≥ 1 is reported and cites #440. |
