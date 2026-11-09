---
id: SR-011
title: "Gap analysis — PR #51 acceptance criteria to tests"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-business; FR-004-AC-7, FR-004-AC-9, FR-004-AC-12, FR-004-CON-2, FR-006-AC-6 and tests/test_role_schemas.py, tests/test_model_tables.py (PR #51)"
review_set: subset
---
# SR-011: Gap analysis — PR #51

## Summary

Ticket: PLAT-1302 (primary), PLAT-1305. Plan completion: not assessed.
Manual AC-to-test pass over the criteria the PR adds or edits; `quoin
matrix` was not used because the change is confined to five criteria and
their tagged tests were read directly.

Bindings checked: TC-036 → FR-004-AC-7 (correct), TC-038 → FR-004-AC-9 and
FR-004-CON-2 (correct binding, wrong contract, see SR-010 FND-001),
TC-042 → FR-004-AC-12 (correct), TC-085 → FR-006-AC-6 (correct for the
fixture half). Oracle strength: every new negative in TC-036 and TC-042 is
one mutation of a record the same test first asserts valid (missing `text`,
`kind: clause`, empty `text`; `slot: during`, missing `expression`), and the
types are sealed, so each fails for its intended reason; the positive
assertions would fail if the key were not declared.

## Verdict

**CONDITIONAL** — the criteria are traced, but FR-004-AC-12 tests one of the
five types FR-004 names, and FR-006-AC-6's new duplicate-type clause and
FR-006's retired-table refusal are not asserted by the AC-6 test. TC-085
itself fails on the PR head (SR-010 FND-001).

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-004 says `Entity`, `NestedEntity`, `AggregateRoot`, `StateMachine` and `Process` SHALL each admit `operationExpressions`; FR-004-AC-12 and TC-042 assert `Entity` only. Dropping the key from any of the other four TypeSpec models would pass every test. | spec/functional/FR-004-role-schemas.md:73, spec/functional/FR-004-role-schemas.md:105, tests/test_role_schemas.py:333 | correct-requirement-no-evidence |
| FND-002 | low | FR-006-AC-6 now also claims "the duplicate-type negative fixture is refused with `semantic.duplicate-model-entry`", but TC-085 (`test_the_population_fixture_extracts_one_member_per_row`) does not assert it; only TC-083, tagged FR-006-AC-4, does. FR-006 Behavior's "a `Type \| Extent` table is refused" has no fixture or test in this repo. | spec/functional/FR-006-model-table-locators.md:65, spec/functional/FR-006-model-table-locators.md:93, tests/test_model_tables.py:331 | correct-requirement-no-evidence |

## New findings (disposition pass 2)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-003 | high | TC-097 (FR-007-AC-9) stays a strict `xfail` although the behaviour it waits for works on quire 0.53.0. `extract_document` sends no `dataSchema`, so the engine has no FR-076 typed relation keys and leaves the row in `relations`. With the object type's own schema passed as `dataSchema`, both TC-097 cases pass (measured on a scratch copy: process `emits` and repository `persists` each hold the qualified target, `relations` absent, `relationSources` and non-lossy availability as asserted) and the TC-098 pin fails. AC-9 is therefore reported as an expected failure while the engine meets it. | tests/test_relationships.py:404-415, tests/test_relationships.py:418-428, tests/test_relationships.py:469-487 | correct-requirement-no-evidence |

## New findings (disposition pass 3)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-004 | medium | `extract_relations` omits `dataSchema` on purpose, with a comment saying that with one the engine lowers `emits` rows into their typed key and leaves them out of `relations`. TC-090 runs the `aggregate_root` skeleton through it and asserts every row, including `placed emits event_001`, lands in `relations`, as FR-007 says ("On `entity` and `aggregate_root` ... every row SHALL lower into `relations`"). Measured on quire 0.53.0: with `AggregateRoot.json` as `dataSchema`, which is what `validate_document` supplies, the `emits` row lowers into `emits: [ix://agent-ix/spec-objects-business/event_001]` and `relations` holds only `aggregates`, `contains`, `references`. The omission keeps TC-090 green by testing a request shape production never sends, and masks a contradiction between FR-007 and the engine for `aggregate_root` (entity is unaffected: it has no typed key). | tests/test_relationships.py:112-116, tests/test_relationships.py:201, spec/functional/FR-007-relationships-table.md:56 | correct-requirement-no-evidence |
| FND-005 | low | The plan still describes the removed criterion: `Task-013` lists `ix://agent-ix/spec-objects-business/TC-098` as a `verifies` relationship and its checklist and test list call TC-097 an expected failure and TC-098 the blocker it flips; `Plan-001` lines 170-171 and the Task-013 row (`TC-089…TC-098`) say the same. `quoin validate` reports no findings, so nothing catches the dangling target. | plan/Plan-001-semantic-data-schemas/tasks/Task-013-relationships-table.md:35, plan/Plan-001-semantic-data-schemas/tasks/Task-013-relationships-table.md:56, plan/Plan-001-semantic-data-schemas/plan.md:170 | correct-requirement-no-evidence |

## Dispositions

Round 1, checked against fix commit c25ddc6.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | FR-004-AC-12 now names all five types and TC-042 loops over `Entity`, `NestedEntity`, `AggregateRoot`, `StateMachine` and `Process`, asserting each base record valid and both negatives refused per type, plus the `Repository` refusal. |
| FND-002 | fixed | TC-085 now asserts the duplicate-type negative (`semantic.duplicate-model-entry`) and a retired `Type \| Extent` table built from the positive fixture (`semantic.feature-not-extractable`); FR-006-AC-6 names both. Passes on engine 0.53.0. |
| FND-003 | fixed | Round 3 (e166aec): `extract_document` passes the object type's schema as `dataSchema`, the TC-097 `xfail` is gone and TC-097 passes for both types on quire 0.53.0; AC-10 and TC-098 are deleted. |
| FND-004 | deferred | Deferred to PLAT-1358 by the code lead: pre-existing FR-007 / engine divergence for `aggregate_root` `emits` rows, outside this PR's scope. |
| FND-005 | fixed | Round 4 (0d5557a): Task-013 no longer lists TC-098 as a `verifies` target, and its checklist, deliverables, and the Plan-001 TC-097 line and Task-013 row (`TC-089…TC-097`) describe TC-097 as passing with the data schema; `git grep` finds no `TC-098` or `FR-007-AC-10` in spec/, plan/, or tests/. |
