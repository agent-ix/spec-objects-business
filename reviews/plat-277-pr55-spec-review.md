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

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-003 | high | A required `section_body` locator reads only the text directly under its heading, so `required: true` refuses a section that holds only `### ` subsections as "required '<key>' (section_body(<H>)) is empty", even when it declares the very member the construct requires. FR-012 Behavior turns this quirk into an authoring rule ("a required section SHALL carry at least one line of prose before its first subsection"), and the PR edits a positive fixture to comply. Under quire 0.54.0, measured against main's manifest and then this branch's manifest, these documents validate on main and are refused on the branch: quire-specification FR-231 and FR-234 (`state_machine` Operations), filament-core-data's own extraction-frontend fixture SM_001 (Operations), and the `aggregate_root` and `state_machine` skeletons with only the intro line removed. filament-core-data's AR_001 also hits the new Invariants refusal. This refuses valid declarations, which is the opposite of what F1 is for. The intended contract (the schema requires the key wherever the construct requires the member) already held on main: the schemas there require `fields`, `clauses` and `operations` for these types, and FR-012-CON-1/AC-3 with TC-122 now pin that. Keep FR-012's construct rule and TC-122, revert the five locator flips and the fixture line, and drop the prose-line Behavior. A document that really lacks the member is then still refused, as `semantic.record-invalid ... is a required property`. | spec_objects_business/manifest.yaml:229-233, spec_objects_business/manifest.yaml:273, spec_objects_business/manifest.yaml:338, spec_objects_business/manifest.yaml:386, spec_objects_business/manifest.yaml:431, spec/functional/FR-012-optional-sections-optional-keys.md:43-45, tests/fixtures/positive/state_machine-declared-model.md:44 | wrong-requirement |
| FND-004 | low | The FR-012 rewrite left stale text. spec/functional/index.md still titles FR-012 "Require a declaration key only when its source section is required", and spec.md says "FR-012 keeps a declaration key optional where its source section is"; both contradict the new FR-012. The file slug `optional-sections-optional-keys` now names the reverse rule. `quire validate` also reports EARS warnings on FR-012's statement (more than one `shall`, no subject) and on CON-1 (two `shall`s). | spec/functional/index.md:21, spec/spec.md:120, spec/functional/FR-012-optional-sections-optional-keys.md:19-26, spec/functional/FR-012-optional-sections-optional-keys.md:53 | wrong-requirement |

## Dispositions

Round 1, checked against fix commit baff077.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | Fixed by the change of direction. typespec/main.tsp and the schemas are byte-equal to main, so the schemas again require what the FR-008 construct requires. FR-012 now states that the record layer follows the construct, and the "stay as they are" bullet is gone. The new locator approach is a separate defect, recorded as FND-003. |
| FND-002 | fixed | Fixed by the change of direction. StateMachine.json requires `operations` again, and the `state_machine` `operations` locator is `required: true`. |
