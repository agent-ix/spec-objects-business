---
id: SR-001
title: "Base review of the issue #4 semantic data schemas specification"
type: SpecReview
analysis: base
scope: "spec/spec.md, spec/stakeholder/StR-001, spec/usecase/US-001, spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/integration/IT-001..IT-002, spec/tests.md"
review_set: all
---
# Base review of the issue #4 semantic data schemas specification

## Summary

Checklist review (id formats, story and requirement quality, the six coverage
rules, cross-references) of the specification authored for
`agent-ix/spec-objects-business#4`. Ids are well-formed and sequential per
class (StR-001, US-001, FR-001..FR-005, NFR-001, IT-001..IT-002, TM-001,
TC-001..TC-070 in blocks); every FR links its US; `quire validate` over
`spec/**/*.md` reports zero errors and zero grammar warnings after the
authoring pass. Three gaps were found in coverage bookkeeping (constraint rows
verified by inspection had no matrix row; one TC traced to a criterion it does
not assert; FR-001's verification cells use uncatalogued method names) and
are dispositioned below.

## Verdict

**CONDITIONAL** — no high finding; the four mediums are bookkeeping fixes
applied before planning (see Dispositions).

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | Constraints FR-002-CON-1, FR-002-CON-2, and FR-005-CON-1 are verified by `Inspection` but have no row in `## Test Case Summary`, so coverage rule 1 (every named constraint has a TC) is not met for them. Add `Inspection`-typed rows TC-017, TC-018, TC-058. Escape cause: correct-requirement-no-evidence. | spec/tests.md, FR-002, FR-005 |
| FND-002 | medium | TC-041 (nested-entity item rules) traces to FR-004-AC-1, which asserts pairwise schema distinctness, not the nested-entity rules; the nested-entity row of the FR-004 table has no criterion of its own. Add FR-004-AC-11 and retrace TC-041. Escape cause: missing-requirement. | FR-004, spec/tests.md TC-041 |
| FND-003 | medium | FR-001's Verification cells read `Schema Test` and `Integration Test`, which `quire coverage` reports as `uncatalogued-verification-method` (neither a catalog id nor a class); the class value `Test` is the declared form. Pre-existing wording; corrected here since the matrix now depends on those rows. Escape cause: wrong-requirement. | FR-001-AC-1..4 |
| FND-004 | low | US-001 carries illustrative examples (US-001-EX-1..3) rather than Given/When/Then acceptance criteria; this follows the `spec-artifacts-iso` US skeleton, which keeps verification out of stories, so the checklist item "≥ 2 acceptance criteria" is satisfied by the examples plus the FR criteria they lead to. No change. | US-001 |
| FND-005 | low | No FR carries an `## Options` section; the design choice (TypeSpec over hand-authored schema) is recorded in US-001 Options and the ticket's authoring contract, so an FR-level options table would repeat it. No change. | FR-002..FR-005 |
| FND-006 | low | FR-001 still says "conforms to FR-035 v1.0.0" while the `semantic` block was admitted by FR-035 CR-003; the manifest schema version string is unchanged (`manifest_version: 1.0.0`), so the statement remains true. No change. | FR-001 |
| FND-008 | medium | `quire coverage` reports `section-matches-nothing` for NFR-001: the `nfr-acceptance-criterion` declaration mints trace targets from `## Acceptance Criteria` only, so the four Measurement metrics mint nothing and TC-060..TC-063 trace to the bare requirement id. Add an `## Acceptance Criteria` table (NFR-001-AC-1..4, one per metric) and retrace the four rows. Escape cause: correct-requirement-no-evidence. | NFR-001, spec/tests.md TC-060..TC-063 |
| FND-007 | low | The matrix's `TC-002..TC-004` and `TC-006` rows depend on a running `filament-core` or a human and are marked `🚧` with a note; they predate this issue and remain outside the automated gate. Recorded so the gap analysis does not read them as this issue's debt. | spec/tests.md |

## Coverage Rules

1. Coverage: every AC has ≥ 1 TC after FND-001/FND-002 are applied (FR-002: 6 AC + 3 CON; FR-003: 6 AC + 2 CON; FR-004: 11 AC + 2 CON; FR-005: 7 AC + 2 CON; NFR-001: 4 metrics; FR-001: 4 AC; StR-001: 2 VC).
2. Option permutation: both Properties forms × the three alternate-form types (TC-051), all ten types (TC-030..TC-041, TC-050).
3. Constraint boundary: zero/one identity field, empty/one-item arrays, zero/one Timestamp field (TC-031..TC-038).
4. Error path: digest mismatch, unknown key, both forms, dangling clause, non-Identifier token, missing required section (TC-013, TC-026, TC-054, TC-057).
5. State transition: availability states `available`/`not_applicable`/`missing` per kind (TC-053).
6. Edge case: empty record, legacy artifact, unresolved placeholder (TC-038, TC-039, TC-061..TC-063).

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Applied: TC-017, TC-018, TC-058 added as `Inspection` rows. |
| FND-002 | Applied: FR-004-AC-11 added; TC-041 retraced. |
| FND-003 | Applied: FR-001 cells changed to `Test`. |
| FND-008 | Applied: NFR-001 gained `## Acceptance Criteria` with NFR-001-AC-1..4; TC-060..TC-063 retraced. |
| FND-004..FND-007 | Recorded, no change. |
