---
id: SR-013
title: "Code review — PLAT-160 entity/state_machine references vocabulary (#52)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-business; spec_objects_business/manifest.yaml, tests/test_manifest.py, spec/functional/FR-007-relationships-table.md, spec/tests.md"
review_set: subset
---
# SR-013: Code review — PLAT-160 references vocabulary (#52)

## Summary

Ticket: PLAT-160 (gaps 2 and 3). Reviewed `git diff origin/main...HEAD` of
branch `plat-160-object-links` at 9c84174: two `allowed_links.references`
edits in the manifest (`entity` gains `value_object`; `state_machine` gains
`entity` and `aggregate_root`), one new trace-tagged test, one new AC
(FR-007-AC-11) and one new test-plan row (TC-110).

Gates run in a scratch worktree with the repo's own Poetry environment
(quire wheel 0.52.1) and `npm ci` for the pinned TypeSpec toolchain:
full `pytest` 235 passed, 7 skipped (env-gated integration), 4 xfailed,
coverage 100%; `ruff` and `black` clean; `schemas-check` 20 schemas match.
`test_relationships.py` and `test_model_tables.py`, which the coder could not
run, are green. Reverting only the manifest to `origin/main` makes the new
test fail at the `value_object` assertion, so the test is not vacuous.

Behaviour probe (not part of the suite): the `entity-relationships.md`
positive fixture with its `references aggregate_root_001` row retargeted to
`value_object_001`, extracted with the bundle index, lowers `available` on the
PR manifest and is refused `semantic.invalid-model-cell` / `target-not-allowed`
on the `origin/main` manifest. The entity half of the change does what the
ticket asked through the `## Relationships` table.

No JSON-schema or skeleton change is needed: `allowed_links` is manifest
vocabulary, not part of any record schema, and TC-090 requires that no
skeleton carry frontmatter `relationships`.

## Verdict

**PASS with one low finding.** The code change is correct and minimal; the
one finding is that the new test asserts only list membership.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | low | TC-110 asserts only that the manifest lists contain the new tokens. Nothing in the suite exercises either new link through Quire: no fixture row `references value_object_*` on an entity (the probe above shows it works, but no test pins it), and no test authors a `state_machine` `references` edge at all. A cheap fix is a `references value_object_001` row in `tests/fixtures/positive/entity-relationships.md` (TC-091's composite list then gains one `False`). | tests/test_manifest.py:40-44 | correct-requirement-no-evidence |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (be03995): `tests/fixtures/positive/entity-relationships.md` gains the row `shared_terms \| references \| value_object_001 \| 0..*`, and TC-091's composite list becomes `[True, False, False, False, False]`. With only the manifest reverted to `origin/main`, TC-091 and TC-110 both fail, so the entity half is now pinned through Quire extraction. Full suite at be03995: 235 passed, 7 skipped, 4 xfailed, coverage 100%. The state_machine half has no Quire surface this module's tests can drive. FR-007 Behavior now states that the edge lives in frontmatter, where bundle-level checking is quire's concern. |
