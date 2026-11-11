---
id: SR-026
title: "Gap analysis — PR #57 FR-007-AC-2 and AC-9 to tests (PLAT-1358)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-business; FR-007-AC-2, FR-007-AC-9, tests/test_relationships.py TC-090, TC-097 (PR #57)"
review_set: subset
---
# SR-026: Gap analysis — PR #57

## Summary

Ticket: PLAT-1358. Plan completion: not assessed. The computed matrix
(`quire matrix --scope .`) binds FR-007-AC-2 to TC-090 and FR-007-AC-9 to
TC-090 and TC-097. FR-007-AC-2 is fully asserted by TC-090. For FR-007-AC-9,
the process and repository clauses are asserted by TC-097. TC-090 asserts the
`aggregate_root` skeleton's `emits` lowering, but only with a non-typed row
alongside it.

## Verdict

**One medium coverage gap.** The `aggregate_root` clauses of FR-007-AC-9 are
only partly asserted.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-007-AC-9 now covers an `aggregate_root` artifact with the single row `placed emits event_001 0..1` and its header-only form ("the typed key present and empty"). No test asserts either one. TC-097's parametrization (`TYPED_KEY_ROWS`) lists only `process` and `repository`. TC-090 checks only the skeleton, which also has a `references` row and never goes header-only. Under quire 0.54.0 the engine gives `emits` [event_001], `relations` [] and `relationSources` [] for the single row, and `emits` [] for header-only, both `available`. So the test can be written today. Add an `aggregate_root` case to TC-097 that expects `relationSources` [] rather than one entry. TC-097's `typed_key_document` appends a second `## Relationships` section to the skeleton, so this case needs the skeleton's table replaced, not appended to. This goes with SR-025 FND-001's AC-9 rewording. | tests/test_relationships.py:386-394, tests/test_relationships.py:421-460, spec/functional/FR-007-relationships-table.md:85 | correct-requirement-no-evidence |

## Gates Run

- `quire matrix --scope .`: FR-007-AC-2 and FR-007-AC-9 are `tagged`.
- Probe script (scratchpad, not committed) through `validate_document` and `extract_semantic` with `dataSchema`, on the aggregate_root skeleton with its table replaced: single emits row and header-only are both valid and `available`.
