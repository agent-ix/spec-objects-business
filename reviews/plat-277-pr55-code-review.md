---
id: SR-021
title: "Code review — PR #55 optional section keys (PLAT-277 F1)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-business; typespec/main.tsp, spec_objects_business/schemas/{NestedEntity,AggregateRoot,Event,StateMachine,Process}.json, spec_objects_business/skeletons/{aggregate_root,state_machine}.md, tests/test_role_schemas.py (PR #55, git diff origin/main...HEAD at b751066)"
review_set: subset
---
# SR-021: Code review — PR #55

## Summary

Ticket: PLAT-277 (finding F1). The TypeSpec change makes `fields` optional on
`NestedEntity`, `Event` and `Process`, `fields` and `clauses` optional on
`AggregateRoot`, and `operations` optional on `StateMachine`. Every decorator
(`@minItems`, `@contains`, `@minContains`/`@maxContains`) stays on the
property, so each item rule still applies when the key is present. The
regenerated JSON differs from main only in the removed `required` arrays.
`node scripts/generate-schemas.mjs --check` reports "27 schema(s) match the
committed output".

Locators were checked against `manifest.yaml`. Each relaxed key is fed only
by a `required: false` locator:

- `properties` (to `fields`) on `nested_entity`, `aggregate_root`, `event` and `process`
- `invariants` (to `clauses`) on `aggregate_root`
- `operations` on `state_machine`

The keys that stay required are fed by `required: true` locators:

- `entity` and `value_object` `properties`
- `repository` `operations`

The diff touches no locator and no `construct:`.

Tests assert both directions. TC-122 checks that `{}` validates for each
relaxed type and that a present empty or rule-breaking key still fails. TC-033
now admits an aggregate root with no `clauses` and refuses one with
`clauses: []`. TC-038 derives the set of types that accept the empty record.
TC-123 checks that only the three types fed by a required locator still list
a required key. None of these is ceremony: each asserts schema behaviour or a
schema-to-locator consistency rule, the exact defect F1 measured.

An engine probe was run on the skeletons with quire 0.54.0, with the optional
section removed:

- `aggregate_root` without `## Invariants` validates. So does `aggregate_root`
  without `## Properties`.
- `nested_entity`, `event` and `process` without `## Properties` validate.
- `entity` without `## Properties` is still refused, by both the locator and
  `record-invalid`. So is `repository` without `## Operations`.
- `state_machine` without `## Operations` is refused by
  `semantic.unknown-trigger` (see SR-023 FND-002).

## Verdict

**Code correct; one low finding.** The schema and test changes do what the PR
says. The construct-versus-schema question belongs to the spec and is recorded
in SR-023 FND-001.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | low | The `aggregate_root` skeleton comment now contradicts itself. It says `## Invariants` is "optional; the `clauses` it feeds are not required by AggregateRoot.json" and then "the root exists to enforce invariants, so it declares at least one". A reader cannot tell whether an aggregate root may omit invariants. The comment should say the section may be omitted at the record layer, and that the FR-008 construct (`min_clauses`) still requires a clause for IR lowering (SR-023 FND-001). | spec_objects_business/skeletons/aggregate_root.md:11-12 | wrong-requirement |

## Gates Run

- `node scripts/generate-schemas.mjs --check`: 27 schemas match.
- `pytest tests/` (venv spec-objects-business-Dc60l5v7, quire 0.54.0): 270 passed, 7 skipped, 2 xfailed, coverage 100%.
- Skeleton probe via `quire.validate_document`, with the optional section removed, as listed above.
