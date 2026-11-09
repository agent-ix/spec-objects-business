---
id: SR-023
title: "Spec review — PR #55 FR-012 and FR-004 optional section keys"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-business; spec/functional/FR-012-optional-sections-optional-keys.md, spec/functional/FR-004-role-schemas.md (Behavior, table rows, AC-4, AC-9, CON-2 removal), spec/spec.md, spec/tests.md TC-033, TC-038, TC-122, TC-123 (PR #55)"
review_set: subset
---
# SR-023: Spec review — PR #55

## Summary

Ticket: PLAT-277 (finding F1). This review covers:

- new FR-012: statement, Inputs, Outputs, Behavior, CON-1, AC-1..3 and Dependencies
- FR-004: the Behavior sentence, the five table rows, AC-4, AC-9 and the removal of CON-2
- the spec.md overview sentence
- tests.md: the TC-033, TC-038, TC-122 and TC-123 rows and the coverage rows

These were read against FR-008 and against how the FR-008 `construct:` is
consumed downstream:

- quire-rs `origin/main` `src/semantic/context.rs`
  `ConstructReferences::from_construct`
- filament-core-data `origin/main`
  `crates/extraction-frontend/src/constructs.rs` `shape()`

Clean parts:

- FR-012's statement is a single EARS-style SHALL NOT. Its Outputs name the
  five relaxed types and the three kept types, which matches the manifest
  locators.
- FR-012-AC-1..3 are testable and each can fail.
- FR-004's new Behavior sentence ("a key is required only where the type's
  manifest locator for it is required ... an item rule applies to a key
  whenever it is present") is consistent with the table and the schemas.
- Removing FR-004-CON-2 is correct. The new rule falsified it, and FR-004-AC-9
  now states the new partition.
- `quoin validate` reports no repository QA findings.

How the construct is consumed:

- Quire reads only the construct's `references` (`from_construct`). It never
  reads `members` or `rules`, so `quire validate` does not enforce a construct
  at document level.
- filament-core-data's extraction frontend does enforce them, one artifact at
  a time, when it lowers to IR. `shape()` refuses with `ARTIFACT_NOT_LOWERED`:
  - "it declares no invariant, and the construct requires one" under `min_clauses`
  - "it declares no identity field, and the construct is identified by one" under `identity_field_required`
  - an occurrence-field count other than one, under `occurrence_field_required`
  - "it declares no operation, and the construct requires one" under `min_operations`

## Verdict

**NOT MERGEABLE as written: one medium finding.** FND-001 is a spec
contradiction. The fix is a short FR-012 note or an owner decision on the
direction. FND-002 is low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | medium | FR-012 Behavior says "the absence of `fields`, `clauses` or `operations` is a valid declaration, not a defect" and that `construct:` declarations "stay as they are". FR-008's constructs still declare `fields` and `clauses` required, and the rules `identity_field_required`, `min_clauses`, `occurrence_field_required` and `min_operations`, for `aggregate_root`, `nested_entity`, `event`, `state_machine` and `process`. filament-core-data's extraction frontend (`constructs.rs` `shape()`) enforces these per artifact and refuses to lower exactly the documents FR-012 now calls valid (ARTIFACT_NOT_LOWERED). Quire reads only the construct `references`, so the refusal moves from `quire validate` to FCD lowering. FR-004's row still gives the reason "the root exists to enforce invariants". The spec now states two incompatible validity rules for one declaration. Either scope FR-012 to the record layer and state that FCD lowering still refuses these declarations under the FR-008 rules, or, for types whose construct needs the member, choose the other F1 option and make the locator `required: true`. The PLAT-277 thread still lists that direction as an open design decision. The bullet "Locators and `construct:` declarations stay as they are" is a change note, not a target-state requirement, and should go either way. | spec/functional/FR-012-optional-sections-optional-keys.md:41-43, spec/functional/FR-008-construct-declarations.md:57-63, spec/functional/FR-004-role-schemas.md:61 | wrong-requirement |
| FND-002 | low | For `state_machine`, the relaxation can never be reached by a document. `transitions` is a required locator with `min_rows: 1`, and every trigger must name a declared operation (`semantic.unknown-trigger`). A `state_machine` document without `## Operations` is always refused: the probe on the skeleton gives three `unknown-trigger` errors. FR-012's claim that the absence of `operations` is a valid declaration is therefore never true for this type, although FR-012-AC-1 passes on a hand-built record. Making the `state_machine` `operations` locator `required: true`, and keeping `StateMachine.operations` required, would describe the real contract. Otherwise FR-012 should say that the trigger rule makes the section required in practice. | spec/functional/FR-012-optional-sections-optional-keys.md:24-25, spec/functional/FR-012-optional-sections-optional-keys.md:41-42, spec_objects_business/manifest.yaml:383-386 | wrong-requirement |

## Gates Run

- `quoin validate` (quoin 0.29.1): repository QA gates, no findings.
- `quire validate --scope .` on FR-004, FR-012 and tests.md: FR-004 and FR-012 are clean. tests.md fails at line 140 (TC-085). That row is unchanged by this PR and fails identically on `origin/main`, so it is out of scope here.
