---
id: SR-014
title: "Gap analysis — PLAT-160 entity/state_machine references vocabulary (#52)"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-objects-business; spec/functional/FR-007-relationships-table.md, spec/tests.md, spec_objects_business/manifest.yaml, tests/test_manifest.py"
review_set: subset
---
# SR-014: Gap analysis — PLAT-160 references vocabulary (#52)

## Summary

Ticket: PLAT-160. Planless, diff-scoped gap analysis of PR #52. Plan
completion: not assessed.

Spec to test: FR-007-AC-11 is new, and `quoin matrix --repo .` reports it
`tagged` by TC-110 (`tests/test_manifest.py`). TC-110 has a row in
`spec/tests.md` naming FR-007-AC-11. No id collides with open PR #51: #51
deletes FR-007-AC-10 and TC-098 and adds no FR-007 AC or TC-110, so after both
land FR-007 holds AC-1..9 and AC-11.

Test to code: the test fails on the `origin/main` manifest and passes on the
PR manifest. Code to spec: both manifest edits are owned by FR-007-AC-11; no
unowned change.

Surface check: `state_machine` declares no `relationships` locator, its
record schema has no `relations`, and FR-007 Behavior refuses a
`## Relationships` table on it with `semantic.record-invalid`. The only place
a state machine can author `references` to its subject is frontmatter
`relationships`, which Quire checks against `allowed_links` at bundle level
(`disallowed-edge-target`, warning tier). In the quire CLI 0.36.2 OKF run,
that check emitted nothing even for a negative control
(`state_machine` → `value_object`), so this review could not show the
state_machine half working end to end. That is a tooling observation, not a
defect in this PR.

## Verdict

**CONDITIONAL.** The AC→TC trace is complete and real. Two spec-side gaps:
AC-11 has no Behavior statement behind it and does not say where a state
machine authors the new edge, and the hand-maintained FR-007 summary row is
now stale.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-007-AC-11 has no Behavior `SHALL` behind it. Every other FR-007 AC traces to a Behavior bullet, and FR-006 backs its own `allowed_links` AC (FR-006-AC-7) with one. FR-007's statement and Behavior cover only the `## Relationships` table, and they bar `state_machine` from authoring that table. So the state_machine half of AC-11 describes an edge that can only be written in frontmatter `relationships`, which FR-007 Behavior calls the artifact-graph surface where no domain relationship is declared. Add a Behavior bullet that states both admissions and says a state machine names its subject through a frontmatter `references` relationship, checked against `allowed_links` at bundle level. | spec/functional/FR-007-relationships-table.md:83 | missing-requirement |
| FND-002 | low | The FR-007 summary row in `spec/tests.md` still reads `FR-007-AC-1..10 \| TC-089..TC-098` and omits AC-11 and TC-110. Open PR #51 rewrites the same row to `AC-1..9 \| TC-089..TC-097`. That rewrite does not textually conflict with this PR, so whichever lands second leaves the row silently omitting AC-11. The computed `quoin matrix` already shows AC-11 → TC-110, so the hand-maintained range adds nothing: either update it in the PR that lands second or delete the range columns and let the matrix own it. | spec/tests.md:68 | wrong-requirement |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-003 | low | The new FR-007 Behavior bullet says "SHALL be able to refer" and "SHALL be able to name". `quire validate` flags the line `[ears:vague-response] vague response verb 'be able to'` and `[ears:non-singular]`. The behaviour is right, but the wording is not a verifiable response. "`entity.allowed_links.references` SHALL admit `value_object`" and "`state_machine.allowed_links.references` SHALL admit `entity` and `aggregate_root`" state the same thing checkably. | spec/functional/FR-007-relationships-table.md:64 | wrong-requirement |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Round 1 (be03995): FR-007 Behavior gains a bullet. It states both admissions and says a `state_machine` link to its subject "is written in frontmatter `references` (the artifact-graph surface), never in a `## Relationships` table". AC-11 now has a Behavior statement and a named surface. The bullet's wording is FND-003. |
| FND-002 | fixed | Round 1 (be03995): the FR-007 summary row's AC and TC range cells are blank, so the row no longer claims a stale range, and `quoin matrix` remains the authority (FR-007-AC-11 tagged). A trial merge with #51's head 77b5256 conflicts on this row and on the FR-007 AC table. The resolution is #51's AC-9 text with AC-10 removed, plus #52's AC-11 row; and `\| FR-007 \| \| \| ✅ AC-6 asserts that a line is reported; the table line is `agent-ix/quire-rs#440` \|`. |
