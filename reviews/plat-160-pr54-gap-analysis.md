---
id: SR-019
title: "Gap analysis — PR #54 FR-011 against tests and module data"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-business; spec/functional/FR-011-variant-set-and-graph.md, FR-010-AC-1, tests/test_variant_set_and_graph.py, tests/test_record_key_owners.py, spec_objects_business/ (PR #54 diff vs origin/main 0aa44f8)"
review_set: subset
---
# SR-019: Gap analysis — PR #54

## Summary

Ticket: PLAT-160. Planless. Plan completion: not assessed. Mapped FR-011-AC-1..4
to TC-118..TC-121 and their tagged tests in
`tests/test_variant_set_and_graph.py`, and checked the edited FR-003, FR-004,
FR-005, FR-008 and FR-010 tests against their ACs. `quoin validate --strict`
reports no findings. Every new AC has a tagged test that can fail.

Bindings checked: TC-118 to FR-011-AC-1, TC-119 to FR-011-AC-2, TC-120 to
FR-011-AC-3, TC-121 to FR-011-AC-4, TC-099 to FR-008-AC-1, TC-038 to
FR-004-AC-9, TC-111 to FR-010-AC-1. All are bound to the right criterion. No
module data is left without an owning requirement.

## Verdict

**Mergeable on the test side once the two medium gaps are closed.** TC-119,
TC-120 and TC-121 assert their ACs fully. TC-118 does not pin the `graph`
reference targets (FND-001), and TC-111's allowed-key table was widened past
the FR-010 owner list it traces to (FND-002).

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-011 Behavior fixes the `graph` references to seven types; TC-118 asserts only that `{event, process, entity, graph}` is a subset. Removing `value_object`, `enumeration` or `aggregate_root` from the manifest, or adding an eighth type, still passes. The `variant_set` half asserts equality. | tests/test_variant_set_and_graph.py:41-43 | correct-requirement-no-evidence |
| FND-002 | medium | TC-111 traces FR-010-AC-1 ("every top-level key ... is in the owner list above"). The PR adds `"variant_set": {"variants", "clauses"}` to its `ALLOWED_KEYS`, but FR-010 Behavior's owner list does not name `variants` or any FR-011 source. The test passes because it now checks a list the AC does not state. | tests/test_record_key_owners.py:43 | correct-requirement-no-evidence |

## Gates Run

`quoin validate --strict` (quoin 0.29.1; quire 0.36.2, engine 0.50.2): no findings.

## Dispositions

Round 1, checked against fix commit c12d7d8 (head 715eb3e).

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | TC-118 now asserts `graph` `references` equals the seven-type list. |
| FND-002 | fixed | FR-010 Behavior's owner list now names `variants` of `variant_set` (FR-011, read by FR-081), so TC-111's `ALLOWED_KEYS` matches the AC. |
