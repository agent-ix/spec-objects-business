---
id: SR-017
title: "Spec review — PR #53 FR-010 and FR-003/004/005/007 changes"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-business; spec/functional/FR-010-record-key-owners.md, FR-003, FR-004, FR-005, FR-007, spec/spec.md, spec/tests.md TC-111..TC-117 (PR #53)"
review_set: subset
---
# SR-017: Spec review — PR #53

## Summary

Ticket: PLAT-240. Reviewed new FR-010 (statement, Behavior, CON-1, AC-1..6,
Dependencies), the FR-003, FR-004, FR-005 and FR-007 edits, the spec.md
out-of-scope bullet, and tests.md TC-111..TC-117, against quoin `origin/main`
FR-121, FR-122 and FR-123 (its "Downstream, spec-objects-business" list) and
quire-rs `origin/main` FR-081 and FR-075.

Clean parts: every FR-123 downstream item is taken up: `owner` dropped and
left to the bundle, `ubiquitous_language` kept as display prose,
`Process.states` added, `record-sections` named with an event `## Source`,
aggregate membership authored once, and `Domain.members` replaced by
`relations` and a `## Relationships` locator. FR-003 names the new token and
its owner. FR-004's domain row also corrects the pre-existing `clauses`
entry that `Domain.json` never declared. FR-007's locator, AC-1, AC-6 and
skeleton statements now include `domain`. The spec.md bullet matches.
`quoin validate --strict` reports no findings. The FR-008 construct
declarations (`domain` `members: required`, `nested_entity` `owner:
required`) are out of scope for this PR as briefed.

## Verdict

**NOT MERGEABLE as written** — FR-010 assigns population `members` and
`extent` to a source that never fills the record (FND-001), which contradicts
FR-010's own statement and quoin FR-123-AC-8. FR-010-AC-3 does not require
the inline-code form the reader needs (FND-002), and its Dependencies cite a
quire-rs requirement that does not exist (FND-003). FND-004 and FND-005 are
low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-010 Behavior names quire-rs FR-075 as the owner of `population` `members` and `extent`, and the statement says no declared key is "left without a source an extractor can read". FR-075 fills only `model.population` (`{ extent, extentSpan, members }`), which the declaration record never carries (SR-012 FND-001). quoin FR-123 and FR-123-AC-8 list `population` `members` as unmapped, and quire-rs FR-081 (`record.rs` `owner()`: `(Some("domain" \| "population"), "members")` is `Unmapped`) never copies it. `extent` is in no owned list, so under the module-wide `record-sections` token a `## Extent` section would be read into `extent`, giving it a second authored form beside frontmatter. Either list `population` `members` and `extent` as unmapped (and drop them from `Population.json` as `Domain.members` was dropped), or raise the missing mapping with quoin FR-123 / quire-rs FR-081. | spec/functional/FR-010-record-key-owners.md:48, spec/functional/FR-010-record-key-owners.md:24-25 | wrong-requirement |
| FND-002 | medium | FR-010 Behavior and FR-010-AC-3 say the `## Source` section "holds one inline id". quoin FR-121 and quire-rs FR-081 read a scalar key only from "a body of exactly one inline-code value"; any other body is `semantic.feature-not-extractable`. Two readers can take "inline id" as bare text, and the PR's skeleton and TC-113 did (SR-015 FND-001). State the form as one inline-code id (`` `aggregate_root_001` ``). | spec/functional/FR-010-record-key-owners.md:52, spec/functional/FR-010-record-key-owners.md:68 | wrong-requirement |
| FND-003 | medium | FR-010 Dependencies cites "quire-rs FR-121 reader, lane P-PLAT-101". quire-rs has no FR-121; the reader is quire-rs FR-081 (`spec/functional/FR-081-record-sections-extraction.md`), merged on quire-rs main in PLAT-1370 (#626) after the 0.54.0 release, and it does copy model entries to record keys and read `## Source`. The sentence should name quire-rs FR-081 and say the gap is the installed release, not a missing reader. | spec/functional/FR-010-record-key-owners.md:76 | wrong-requirement |
| FND-004 | low | tests.md keeps hand-maintained ranges that each new FR must bump: the intro's "FR-002..FR-010" and the coverage row's "FR-010-AC-1..6" / "TC-111..TC-117", plus a TC-117 row whose only content is that an Inspection passed. Coverage is computed by `quoin matrix`; these ranges guard nothing and drift. TC-117 is also filed out of order, before TC-106. | spec/tests.md:33, spec/tests.md:73, spec/tests.md:160 | wrong-requirement |
| FND-005 | low | FR-005 lists `## Parent` as a case "where a typed section and a kernel section describe the same declarations" while saying in the same parenthesis that no key mirrors it. With `owner` gone there is no typed counterpart, so `## Parent` no longer belongs in that bullet. | spec/functional/FR-005-executable-skeletons.md:66 | wrong-requirement |

## Gates Run

`quoin validate --strict` (quoin 0.29.1; quire 0.36.2, engine 0.50.2): no
findings.
