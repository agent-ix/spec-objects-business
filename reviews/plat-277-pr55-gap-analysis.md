---
id: SR-022
title: "Gap analysis — PR #55 FR-012 and FR-004 acceptance criteria to tests"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-business; FR-012-AC-1..3, FR-012-CON-1, FR-004-AC-4, FR-004-AC-9 and tests/test_role_schemas.py TC-033, TC-038, TC-122, TC-123 (PR #55)"
review_set: subset
---
# SR-022: Gap analysis — PR #55

## Summary

Ticket: PLAT-277 (finding F1). This review compares `quire matrix --scope .`
against the PR's tests. Plan completion: not assessed.

The following criteria are tagged and asserted:

- FR-012-AC-1 and FR-012-AC-2, by TC-122. It tests absent keys on all six
  (type, key) pairs, and present-but-invalid keys on each relaxed type.
- FR-012-AC-3, by TC-123. It derives the set of types with a required key
  from the emitted JSON, and reads the three locators from the manifest.
- FR-004-AC-4, by TC-033. An aggregate root with no `clauses` validates, and
  one with `clauses: []` fails.
- FR-004-AC-9, by TC-038. It loops over every object type.

No production code lacks an owning requirement: the schemas trace to FR-004
and FR-012. No stub or coverage inflation was found.

## Verdict

**Covered; two low findings.** One trace tag is missing. One gap remains
between FR-012's document-level purpose and its record-level tests.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | low | `quire matrix` reports FR-012-CON-1 as untagged. tests.md lists it in the FR-012 coverage row (✅) and in TC-123's Traces To, but `test_only_types_with_a_required_source_section_still_require_a_key` is tagged `TC-123, FR-012-AC-3` only. The test body does assert CON-1. Add `FR-012-CON-1` to the trace marker. | tests/test_role_schemas.py:402, spec/tests.md:76, spec/tests.md:172 | correct-requirement-no-evidence |
| FND-002 | low | FR-012's Description is about documents: a document that satisfies every mandatory locator is not refused as `semantic.record-invalid`. Every FR-012 test validates hand-built records against the schema. They rest on the assumption that the extractor omits a key when its section is absent. No committed test validates a document with the optional section removed. The PR body's probe was not committed. A rerun of that probe in this review confirmed the behaviour under quire 0.54.0, so this is a regression gap, not a defect. One `validate_document` case per relaxed type would close it, for example a skeleton with the section removed. | tests/test_role_schemas.py:376-397, spec/functional/FR-012-optional-sections-optional-keys.md:17-20 | correct-requirement-no-evidence |

## Gates Run

- `quire matrix --scope .`: FR-012-AC-1..3 tagged; FR-012-CON-1 untagged.
- `pytest tests/` (quire 0.54.0): 270 passed, 7 skipped, 2 xfailed.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-003 | low | TC-123 covers FR-012-AC-2 ("each of those skeletons with the required section removed is refused"), but it removes only `Properties` (or `Operations`). It never removes `aggregate_root` `## Invariants`, which FR-012-AC-1 makes required. No test covers a required section that is present but holds only `### ` subsections. That is the case SR-023 FND-003 shows is now refused, and such a test would have exposed it. | tests/test_skeletons_semantic.py:324-347, spec/functional/FR-012-optional-sections-optional-keys.md:60 | correct-requirement-no-evidence |

## Dispositions

Round 1, checked against fix commit baff077.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | TC-122 is now tagged `TC-122, FR-012-AC-1, FR-012-AC-3, FR-012-CON-1`. `quire matrix` reports FR-012-CON-1 as tagged. |
| FND-002 | fixed | Fixed by the change of direction. TC-123 now runs `validate_document` on each skeleton with its required section removed and asserts a refusal that names the missing section. |
| FND-003 | fixed | Round 2, fix commit f763ce3. TC-123 now removes `aggregate_root` `## Invariants` as well as Properties, and a new TC-123 case (FR-012-AC-3) validates a `state_machine` whose `## Operations` holds only `###` subsections. |
