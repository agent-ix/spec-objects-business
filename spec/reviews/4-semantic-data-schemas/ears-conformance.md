---
id: SR-008
title: "EARS review of the semantic data schemas"
type: SpecReview
analysis: ears-conformance
scope: "StR-001, FR-001..FR-005, NFR-001"
review_set: all
---
# EARS conformance review

## Summary

The 66 SHALL-bearing statements of issue #4 (StR-001 Stakeholder Need; FR-001
through FR-005 Description, Behavior and Constraint cells; NFR-001 Statement)
plus the ten unmodalled rows of the FR-004 per-type table were read for EARS
pattern, single `shall`, named subject and concrete response. Quire 0.31.0
(engine 0.46.0) reports 19/19 documents grammar-clean with zero `[ears:*]`
findings, with `--summary` and with `--strict`; every unwanted-behaviour
obligation that is stated uses `If … then … SHALL`, and no statement uses an
`On`/`Upon`/`After`/`During` trigger. The defects below are semantic: two
contradictions that leave what gets built undecidable (which skeletons carry
`## Invariants`; what record a legacy-form artifact yields against a schema
that requires `fields`), one table of ten obligations with no governing
`SHALL`, four obligations whose only verification covers a different
population than the statement names, obligations placed on external systems,
compound Descriptions, and a family of `Where …` state clauses and non-actor
subjects the grammar does not flag. FR-001 predates this issue and is noted
for completeness only.

## Verdict

Grammar: pass (engine clean in both modes). Semantics: fail on two highs
(FND-220, FND-221) that need a wording decision before FR-005 and NFR-001 are
implementable; the six mediums degrade traceability or leave an obligation
unverified; the lows are wording.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-220 | high | FR-005 `Each skeleton whose type requires or admits clauses (entity, nested_entity, value_object, aggregate_root, event, state_machine, process) SHALL author ## Invariants …` names seven types, but per the FR-004 table only `aggregate_root` *requires* `clauses` and all ten types *admit* them (`domain`, `repository`, `enumeration` are omitted), and FR-005-AC-4 then says `clauses available for aggregate_root` and `not_applicable where the section is absent` — which reads as six of those seven skeletons carrying no `## Invariants`. Two implementers would ship different skeleton sets and different AC-4 expectations. State the exact list once (Behavior and AC-4 agree) and drop `requires or admits`. | FR-005, FR-004 | wrong-requirement |
| FND-221 | high | NFR-001 `SHALL keep every artifact that validated against 0.2.0 validating against 0.3.0 with at most warning-level semantic findings` (metric: legacy-form entity skeleton, 0 errors) collides with FR-004 `Entity` (`fields` required, ≥ 1 identity field) and FR-005 `no semantic.record-invalid`: no statement in this module or in quoin FR-074 says what declaration record a legacy-form `## Properties` yields (`fields` absent? empty? unvalidated?) or whether that record is validated against the type schema at all. If it is, the legacy entity fails `Entity.json` with an error and NFR-001 is unsatisfiable; if it is not, FR-004 Inputs (`any key absent when its section is absent`) does not cover a section that is present in a legacy form. Add one statement: `While a ## Properties section is in a legacy form, Quire SHALL <not assemble fields / not validate the record / …>`, and cite it from NFR-001. | NFR-001, FR-004, FR-005 | missing-requirement |
| FND-222 | medium | FR-005 `Each skeleton whose type requires operations (repository, state_machine) SHALL author ## Operations with … Pre:/Post: lines naming clause ids declared in the same artifact` leaves the optionality of `Pre:`/`Post:` unstated (the param table is marked `optional`, `Returns:` is conditioned on a return value, the `Pre:`/`Post:` lines are neither), while the Invariants bullet (FND-220) excludes `repository` from the skeletons that declare clauses; a repository skeleton therefore cannot satisfy both bullets as written. State `Pre:`/`Post:` as optional (`where the operation has a precondition …`) or add `repository` to the Invariants list. | FR-005 | wrong-requirement |
| FND-223 | medium | FR-004 Behavior introduces its per-type table with `The per-type contract;` and no modal: the ten rows that carry the FR's core obligations (required keys, forbidden keys, item rules) are not requirement statements, so nothing obliges the schema to enforce a row and the ACs trace to prose the engine does not count. In the same FR, the Description `the ten DDD roles are told apart by the shape of their records rather than by name alone` and FR-004-CON-2 `the two open-required types (Domain, Enumeration) are distinguished by their forbidden and optional keys` overclaim: FR-004-AC-9 itself states that `{}` validates against both `Domain.json` and `Enumeration.json`, so the two are not told apart by shape for the empty record. Add `Each model SHALL enforce its row of the following table` and restate CON-2 as what actually differs (`a record carrying values fails Domain; a record carrying members or vocabulary fails Enumeration`). | FR-004 | wrong-requirement |
| FND-224 | medium | FR-002 `When any emitted file differs from the committed output, a committed file is stale, toolchain.json differs, or a manifest digest differs from the shipped bytes, the check SHALL exit non-zero naming each such file` states an unwanted condition with `When` (four disjuncts; should be `If … then`), and `a committed file is stale` is undefined — presumably a committed `schemas/*.json` with no emitted counterpart — and is the one disjunct FR-002-AC-4 does not exercise (AC-4 changes one byte of a shipped schema and one digest). Define stale and add the extra-file case to AC-4. | FR-002 | correct-requirement-no-evidence |
| FND-225 | medium | FR-002 `The npm staging script SHALL copy schemas/ beside manifest.yaml, so the npm tarball ships the schemas the manifest references` names an actor that appears nowhere in Inputs (only `scripts/generate-schemas.mjs` is named) and has no acceptance criterion: FR-002-AC-6 covers the wheel only, so the npm tarball obligation is unverified. Name the script and add an AC over the packed tarball. | FR-002 | correct-requirement-no-evidence |
| FND-226 | medium | FR-003-CON-1 `The semantic block SHALL contain no key outside the admitted list; an unknown key is rejected by both consumers` states the rejection by Quoin and Quire as a fact, not an obligation, and FR-003-AC-6 tests Quire's loader only while FR-003-AC-5 demonstrates a successful `quoin module install` only; Quoin's rejection of an unknown key or a wrong digest is never exercised. Either state the Quoin rejection as `If … then Quoin SHALL reject …` with an AC, or scope CON-1 to Quire. | FR-003 | correct-requirement-no-evidence |
| FND-227 | medium | NFR-001 Statement packs two obligations with `while` (`SHALL keep every artifact … validating …, while the untyped properties string and every 0.2.0 locator yield stay byte-identical`), and both quantifiers outrun their measurement: `every artifact that validated against 0.2.0` is measured on one checked-in legacy entity skeleton, and `every 0.2.0 locator yield … byte-identical` is measured on the `properties` string only (the metric `0.2.0 locators changed = 0` compares locator definitions, not their yields). Split the Statement and either widen the Verification to every 0.2.0 skeleton and every locator yield or narrow the quantifiers to what is measured. | NFR-001 | correct-requirement-no-evidence |
| FND-228 | low | Obligations placed on systems this module does not build: FR-001 `Re-activation SHALL be a no-op` (filament-core's behaviour; also a nominalised event as subject — `When the manifest is re-activated with an unchanged content hash, filament-core SHALL …`), FR-003 `When the install has completed, quoin module SHALL list spec-objects-business` (Quoin), FR-004 `… a reference to an undeclared type is the placeholder … and reported by the extractor rather than silently accepted` (quire-rs; FR-004-AC-10 depends on it). Restate each as this module's obligation (`the manifest SHALL activate such that …`) or as a stated dependency assumption. | FR-001, FR-003, FR-004 | wrong-requirement |
| FND-229 | low | FR-001 (pre-dates this issue) uses the generic subject `The system SHALL publish …` in a module repository where `the system` could be the module, the package, or filament-core, and its Description packs conformance to FR-035 and idempotent activation into one `SHALL`. Name the module and let Behavior carry the two obligations. | FR-001 | wrong-requirement |
| FND-230 | low | Compound Descriptions the engine reads as one `SHALL`: FR-002 (emit per-type schemas + from a semantic-core import + official emitter + pinned toolchain + output directory, with `any drift … fails the build` as a `so that` clause that is really the FR-002 check obligation), FR-003 (carry the `semantic` block + reference by path and digest + `while every existing extraction locator keeps its meaning`, the last being a compatibility obligation restated in Behavior), FR-005 (author in FR-071/072 forms + validate through Quire + `accompanied by negative fixtures`, the last with a different subject). Behavior atomises all of them; reduce each Description to one summary `SHALL`. | FR-002, FR-003, FR-005 | wrong-requirement |
| FND-231 | low | Non-canonical state and condition keywords the grammar does not flag: `Where …` opens five state clauses (FR-003 `Where a skeleton gains a ## Properties …`, FR-004 `Where a key is declared but the current extractor does not populate it …`, FR-005 `Where the state_machine skeleton declares context fields`, `Where entity, aggregate_root, value_object, or process declares operations`, and FR-003's `Where` cousin `so the section is asserted …`); FR-002 `When no $id is relative, …` and `When nothing differs, …` are conditions (the complements of `If … then` branches), not events. Use `While …` for states and `If … then …` for the complements. | FR-002, FR-003, FR-004, FR-005 | wrong-requirement |
| FND-232 | low | Non-actor subjects: FR-004-CON-2 `A record that satisfies no required key SHALL fail every type …` (the schema rejects; `satisfies no required key` should read `carries none of the required keys`), FR-002-CON-3 `Emission SHALL be deterministic` (the generator), FR-003 `the object type SHALL gain a matching required: false section_body locator` (the manifest declares it), FR-003 `If Quoin or Quire rejects the manifest, then the module maintainer SHALL correct the manifest or schemas … rather than relax …` (a human process rule inside an FR, verifiable only by review). Name the generator, schema or manifest as subject; move the maintainer rule to a constraint with `Inspection` or to an ADR. | FR-002, FR-003, FR-004 | wrong-requirement |
| FND-233 | low | FR-004 `Every fields, params, clauses, and operations item SHALL be validated by $ref to the semantic-core 0.1.0 model` omits the `RelationDecl` carriers (`relations`, `members`, `owner`), so a copied `RelationDecl` definition would not violate the statement while FR-004-CON-1 intends otherwise; and two table parentheticals state rules no schema can express and no AC tests: nested_entity `≥ 1 identity field (local to the owner)` and state_machine `operations has ≥ 1 item (each transition command)` (is a transition whose `trigger` names no operation invalid?). Add `relations` to the `$ref` list and either state the parenthetical rules as extractor obligations or drop them. | FR-004 | wrong-requirement |
| FND-234 | low | FR-005 `Each alternate skeleton SHALL share the table skeleton's frontmatter id and title, so the two extract to identical normalized FieldDecl[]` states the consequence backwards: sharing `id`/`title` does not cause identical extraction, identical declarations do, and the identity is the obligation FR-005-AC-2 tests (the shared `id` also gives the module two skeleton files with one id, which the statement should acknowledge as intended). FR-005 `… SHALL keep their kernel sections (… the ## Schema JSON fence as the wire representation of the declared payload …) exactly as the manifest asserts them` is vague in two places: the manifest asserts headings, not bodies (`exactly` is unmeasurable), and `as the wire representation of the declared payload` implies a consistency between the event's `## Schema` fence and its `## Properties` table that no statement obliges and no AC tests. | FR-005 | wrong-requirement |
| FND-235 | low | StR-001 `… require that DDD-driven specifications SHALL yield extractable graph entities …` puts the obligation on the specifications (documents do not yield; the module's manifest and Quire's extractor do), and the Validation Criteria cite `StR-001-AC-1` and `StR-001-AC-2`, identifiers that exist nowhere in the document (its rows are `StR-001-VC-1`/`VC-2`). Reword to `the module SHALL make … extractable` and fix the self-references. | StR-001 | wrong-requirement |

## Result

| Check | Result |
|---|---|
| Explicit subject | Pass with notes (FND-228, FND-229, FND-232, FND-235) |
| Canonical trigger/state wording | Pass on the engine lexicon; five `Where …` state clauses and two condition-as-`When` bullets noted (FND-224, FND-231) |
| Atomic primary obligation | Fail in the FR-002/FR-003/FR-005 Descriptions and the NFR-001 Statement (FND-227, FND-230); pass in Behavior bullets and Constraint cells |
| Modal consistency | Fail in FR-004: ten table rows carry obligations with no modal (FND-223) |
| Unwanted-behaviour response stated | Pass for the six `If … then … SHALL` statements; fail for the FR-002 check trigger (FND-224) and the undefined legacy-form record (FND-221) |
| Statement vs verification population | Fail (FND-224, FND-225, FND-226, FND-227) |
| Tool grammar validation | Pass: 19/19 documents, zero `[ears:*]` findings, `--strict` exit 0 |

## Dispositions

| Finding | Disposition |
|---|---|
| FND-220 | Applied: FR-005 Behavior states the exact list once ("Exactly seven skeletons … SHALL author `## Invariants`", with `domain`, `repository`, `enumeration` carrying none as a separate statement) and FR-005-AC-4 enumerates the matching availability matrix. |
| FND-221 | Applied without a wording workaround: the legacy-form record question is an engine defect, filed as `agent-ix/quire-rs#391` and named in `spec.md`, NFR-001 Verification and the TC-061 status; the criterion stands and its test is an expected failure rather than the schema being relaxed. |
| FND-222 | Applied: `Pre:`/`Post:` are stated as optional, with the note that the repository skeleton declares no clauses and so writes none. |
| FND-223 | Applied: FR-004 Behavior opens with "Each model SHALL enforce its row of the following table", and FR-004-CON-2 is restated as what actually differs. |
| FND-224 | Applied: the check trigger is `If … then`, "stale" is defined (a committed file under `schemas/` with no emitted counterpart in this run), and FR-002-AC-9 exercises that disjunct with TC-073. |
| FND-225 | Applied: `scripts/stage-npm.mjs` is named in FR-002 Inputs and Behavior, and FR-002-AC-7 with TC-071 verifies the packed tarball. |
| FND-226 | Applied: see integrity.md FND-134 — CON-1 is scoped to Quire. |
| FND-227 | Applied: NFR-001's Statement is split into two obligations, the artifact quantifier is narrowed to the checked-in 0.2.0 skeleton set (and the measurement widened to all ten), and the locator-yield quantifier is narrowed to the `properties` string with the other yields stated as unmeasured. |
| FND-228 | Applied in part: FR-001 re-states its obligations as the module's ("the manifest SHALL activate such that …"), and FR-004's extractor claim is scoped to quire-rs FR-070. FR-003's `quoin module` lines stay as they are and are labelled contract checks under scope-boundary.md FND-204. |
| FND-229 | Applied: FR-001's Description names the module and defers conformance and idempotency to Behavior as separate obligations. |
| FND-230 | Recorded, partly applied: FR-001's Description is reduced to one obligation. FR-002, FR-003 and FR-005 keep summary Descriptions with their obligations atomised in Behavior, which the engine reports clean; splitting the summary sentence further would repeat Behavior without adding a testable obligation. |
| FND-231 | Recorded, no change. The engine reports zero `[ears:*]` findings on these statements in `--strict`; the `Where …` state clauses read naturally and every one is discharged by a Behavior obligation with its own subject. |
| FND-232 | Applied for FR-003 (the maintainer obligation is now the module's) and FR-004-CON-2 (restated). FR-002-CON-3 keeps "Emission SHALL be deterministic" as a constraint on the artifact, which is what the constraint table states. |
| FND-233 | Applied: `relations`, `members`, `owner`, `values` and `states` are added to the `$ref` list; the nested-entity locality and state-machine parentheticals are restated as reader rules that the schema does not express (failure-domain.md FND-104, FND-106). |
| FND-234 | Applied: the alternate-skeleton statement no longer claims sharing `id`/`title` causes identical extraction, and "exactly as the manifest asserts them" is replaced by "with the heading, table columns, and fence language the manifest asserts". |
| FND-235 | Applied: StR-001's Stakeholder Need places the obligation on the module, and the VC rows no longer cite non-existent `StR-001-AC-*` ids. |
