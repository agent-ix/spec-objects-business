---
id: SR-025
title: "Spec review — PR #57 FR-007 aggregate_root emits lowering (PLAT-1358)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-business; spec/functional/FR-007-relationships-table.md (Behavior bullet, AC-2, AC-9), spec/tests.md TC-090 (PR #57)"
review_set: subset
---
# SR-025: Spec review — PR #57

## Summary

Ticket: PLAT-1358. The new FR-007 Behavior bullet and FR-007-AC-2 were read
against quire-rs `spec/functional/FR-076-relationships-extraction.md`
(Outputs, AC-16, AC-18, AC-21, CR-193 note) and against quire 0.54.0.

Clean parts:

- The Behavior bullet ("a row with verb `emits` SHALL lower into `emits` only
  and every other row into `relations`, with one `relationSources` entry per
  `relations` entry") matches quire-rs FR-076 Outputs: "Where the schema
  declares both `relations` and a typed key, `relationSources` stays aligned
  with `relations` and carries no typed row", and FR-076-AC-18. The asymmetry
  with `process`/`repository` (typed-only types, where `relationSources`
  carries every row) is intended upstream, so there is no engine bug.
- FR-007-AC-2 matches the engine and quire-rs.
- `domain` and `entity` schemas declare no typed key, so "every row SHALL lower
  into `relations`" is still true for them.
- The TC-090 row now lists FR-007-AC-9, and `quire matrix` binds
  FR-007-AC-2 and FR-007-AC-9 to the TC-090 test with no outside-row warning.

## Verdict

**NOT MERGEABLE as written: one high finding.** FR-007-AC-9 contradicts
FR-007-AC-2 and the Behavior bullet for `aggregate_root`.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | high | FR-007-AC-9 adds the `aggregate_root` artifact to a sentence whose shared predicate is that each artifact extracts "no `relations`, one `relationSources` entry carrying the row's `Name`, `Verb`, `Target`, and `Multiplicity` cells and its line". For `aggregate_root` that is false. quire-rs FR-076 (Outputs and AC-18) says `relationSources` carries no typed row when the schema declares `relations`. Measured under quire 0.54.0, an aggregate_root with only `placed emits event_001 0..1` extracts `emits` [event_001], `relations` [] and `relationSources` []. FR-007-AC-2 and the Behavior bullet in the same PR say there is no `relationSources` entry, so the spec contradicts itself. "extract `emits` and `persists` respectively" also no longer maps three subjects onto two keys. Fix: take `aggregate_root` out of the shared clause and give it its own sentence: `emits` holds the qualified target, there is no `relations` entry and no `relationSources` entry, availability is `available` and not lossy, and header-only extracts `emits` []. | spec/functional/FR-007-relationships-table.md:85 | wrong-requirement |

## Gates Run

- `quire validate --scope .` (quire 0.40.0, engine 0.56.0) on FR-007 and tests.md: FR-007 has no structural errors, only EARS warnings in unchanged lines. tests.md fails at line 140 (TC-085, an unescaped `|` in "`Type | Extent`"). That line is unchanged and fails the same way on `origin/main`, so this PR did not introduce it.
- `quire matrix --scope .`: FR-007-AC-2 tagged by tests/test_relationships.py:186; FR-007-AC-9 tagged by :186 and :425.
