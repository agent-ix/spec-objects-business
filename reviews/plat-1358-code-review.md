---
id: SR-024
title: "Code review — PR #57 aggregate_root emits rows (PLAT-1358)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-business; tests/test_relationships.py (PR #57, git diff origin/main...HEAD at 1ab2a15)"
review_set: subset
---
# SR-024: Code review — PR #57

## Summary

Ticket: PLAT-1358. The test helper `extract_relations` now passes the object
type's `dataSchema`, as `validate_document` does, so the TC-090 skeleton test
sees the same lowering as the real surface. TC-090 now expects one `relations`
entry per non-typed row, pairs `relationSources` one-to-one with `relations`,
and checks that the `aggregate_root` skeletons (`aggregate_root.md` and
`aggregate_root.sysml.md`) lower `placed emits event_001` into `emits`.

Red check: with a pytest plugin that strips `dataSchema` from every
`extract_semantic` request (the old behaviour, where the `emits` row lands in
`relations`), TC-090 fails at the `actual_relations` assertion on
`aggregate_root.md`. With the branch as is, `tests/test_relationships.py`
passes (10 passed, quire 0.54.0).

`TYPED_VERBS` is the right filter: `emits` and `persists` are the only typed
relation keys any of the five table-bearing record schemas declare.

## Verdict

**Clean.** The test change is correct and fails against the old behaviour.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | low | No findings (placeholder) | - | correct-requirement-no-evidence |

## Gates Run

- `poetry run pytest tests/test_relationships.py -o addopts=""`: 10 passed (quire 0.54.0).
- Red check (dataSchema stripped): TC-090 fails on `aggregate_root.md`.
