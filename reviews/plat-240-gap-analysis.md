---
id: SR-016
title: "Gap analysis — PR #53 FR-010 acceptance criteria to tests"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-business; FR-010-AC-1..6, FR-010-CON-1, FR-004-AC-11, FR-007-AC-1, AC-2, AC-6 and tests/test_record_key_owners.py, tests/test_role_schemas.py, tests/test_relationships.py (PR #53)"
review_set: subset
---
# SR-016: Gap analysis — PR #53

## Summary

Ticket: PLAT-240. Plan completion: not assessed. `quoin matrix --json`
(quoin 0.29.1) shows FR-010-AC-1..6 each tagged by one test in
`tests/test_record_key_owners.py` (TC-111..TC-116) and FR-010-CON-1 as an
Inspection with no symbol, as declared. The changed FR-004-AC-11 (TC-041)
and FR-007-AC-1, AC-2, AC-6 tests (TC-089, TC-090, TC-094) now cover
`domain` as a relation-bearing type and assert the `owner` refusal. All pass
on quire 0.54.0. The accepted limitation holds: record-key extraction of
`values`, `states`, `transitions`, `steps`, `members`, `vocabulary` and
`source` is schema evidence only. No stubs, no skipped new tests.

## Verdict

**MERGEABLE with fixes** — two weak oracles: TC-111 does not test the
per-type part of FR-010-AC-1 and carries an unused owner map, and TC-116's
name claims an extraction it does not check. The TC-113 bare-id oracle is
SR-015 FND-001.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | TC-111 checks each schema's keys against one flat set, so `members` passes on any object type. FR-010 Behavior admits `members` only on `population` and `aggregate_root`, and the test pins only that `domain` lacks it, so an `Enumeration.json` or `Event.json` that declared `members` would pass FR-010-AC-1. The `KEY_OWNERS` dict values (owner strings such as `"quoin FR-071"`) are never asserted: they are informational values kept as data, which the value test deletes. Make the allowed set per object type and keep only the key set. | tests/test_record_key_owners.py:26-62 | correct-requirement-no-evidence |
| FND-002 | low | `test_domain_relationships_skeleton_extracts_its_contains_rows` (TC-116) asserts only that the skeleton validates and that the Markdown rows say `contains`; it never reads an extracted `relations`. The name overclaims; FR-010-AC-6 asks only for validation, and TC-090 checks the extraction row for row. | tests/test_record_key_owners.py:127-139 | correct-requirement-no-evidence |

## Gates Run

`quoin matrix --json`, and `pytest` with the existing quire 0.54.0 venv
(242 passed, 7 skipped, 2 xfailed).

## Dispositions

Round 1, checked against fix commit e6834e9.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | `KEY_OWNERS` and its unused owner strings are gone; TC-111 asserts `keys <= ALLOWED_KEYS[name]` per object type, with `members` only on `aggregate_root` and `population`. |
| FND-002 | fixed | TC-116 is renamed `test_domain_skeleton_validates_and_authors_contains_relationships`, matching what it asserts. |
