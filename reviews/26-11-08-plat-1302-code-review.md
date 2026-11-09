---
id: SR-010
title: "Code review — PR #51 single-extent population, guardExpression, operationExpressions"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-business; spec_objects_business/manifest.yaml, spec_objects_business/schemas/, spec_objects_business/skeletons/population.md, typespec/main.tsp, tests/ (PR #51, git diff origin/main...HEAD at 3b7dc2b)"
review_set: subset
---
# SR-010: Code review — PR #51

## Summary

Ticket: PLAT-1302 (primary) and the spec-objects-business half of PLAT-1305.
Reviewed the whole PR diff against `origin/main` and measured it against
quire-rs `origin/main` (71a1f97, crate 0.53.0) and the installed Python
engine wheel `quire` 0.53.0 (same version as quire-rs main). The wheel was
driven directly with `quire.validate_document("population", <module>, text)`
over extracted copies of the module at `origin/main` and at the PR head, and
over two variants of the PR head (no `required` on `Population.json`; that
plus no `extent` frontmatter locator). The installed `quire` CLI 0.36.2
(engine 0.50.2) could not be used: it registers no archetype from this
repository's module source at either `origin/main` or the PR head
("unknown type 'population'"), so all engine evidence is from the wheel.

The expression shapes (`Expression`, `ExpressionSlot`, `OperationExpression`,
`Transition.guardExpression`) match quire-rs `schemas/output/semantic-v1.schema.json`
`$defs.expression` / `$defs.operationExpression` key for key (`kind` const
`expression`, `text` minLength 1, `sourceSpan`, sealed; `operation`
identifier, `slot` `pre|post`, `expression`, sealed). The TypeSpec source and
the emitted JSON agree. The old `Type | Extent` shape is gone from every
authored skeleton, fixture and test; only the skeleton comment and FR-006
mention it, as the refused form.

## Verdict

**NOT MERGEABLE** — FND-001 is a reproduced regression: with
`Population.json` requiring `extent`, the engine refuses the population
skeleton and the population positive fixture with `semantic.record-invalid`,
so TC-025 and TC-085 fail on the PR head. Removing `required: [extent]` makes
both validate (measured). FND-002 is a redundant manifest locator that
doubles the missing-extent error.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | high | `Population.json` makes `extent` required, but the engine validates the data schema against `SemanticExtraction::declaration_record()` (quire-rs `src/semantic/surface.rs:384-460`), which carries only `fields`, `clauses`, `relations`, `operations`, `featureOrder`, systems keys and typed relations, never `model.population`. Every population artifact is therefore refused: engine 0.53.0 returns `semantic.record-invalid: declaration record fails the resolved data schema at extent: "extent" is a required property` for `skeletons/population.md` and `tests/fixtures/positive/population-members.md`. TC-025 (skeleton validation) and TC-085 (`assert result["is_valid"]`) fail. Without `required` both validate and the missing/invalid `extent` cases are still refused by the engine itself (`semantic.invalid-model-cell`). TC-038's `not ok(population, {"members": [member]})` asserts the wrong contract. | spec_objects_business/schemas/Population.json:22-24, typespec/main.tsp:321, tests/test_role_schemas.py:238 | wrong-requirement |
| FND-002 | medium | The new `extent` `frontmatter_field` locator is redundant. quire-rs FR-075 Behavior: "`extent` is a population feature, declared by the object type's `population` table locator"; `src/semantic/model.rs:1179-1200,1896-1932` reads frontmatter `extent` itself. Measured: removing the locator leaves the skeleton and fixtures valid and still refuses a missing or invalid `extent`; keeping it makes a missing `extent` report two errors (`[population] required 'extent' (frontmatter_field(extent)) is missing` plus `semantic.invalid-model-cell`). | spec_objects_business/manifest.yaml:500-504 | wrong-requirement |

## Gates Run

Not an aggregate gate. Engine probe only: `quire.validate_document` (wheel
0.53.0) over the three population documents at `origin/main`, PR head, and
two PR-head variants. `test_role_schemas` could not be re-run (semantic-core
0.3.3 package not installed locally); its oracles were checked by reading.

## Dispositions

Round 1, checked against fix commit c25ddc6.

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | `Population.json` no longer carries `required` (`extent?` in `typespec/main.tsp`); engine 0.53.0 now validates the population skeleton and positive fixture, and TC-025, TC-083 and TC-085 pass (system python3, quire wheel 0.53.0). TC-038 now asserts `ok(population, {"members": [member]})`. |
| FND-002 | fixed | The `extent` `frontmatter_field` locator is removed from `manifest.yaml`; the engine still refuses a missing or invalid `extent` through the `population` table locator. |
