---
id: SR-015
title: "Code review — PR #53 record-key owners (quoin FR-123 downstream)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-objects-business; spec_objects_business/manifest.yaml, spec_objects_business/schemas/, spec_objects_business/skeletons/, typespec/main.tsp, tests/ (PR #53, git diff origin/main...HEAD at ab4d8f4)"
review_set: subset
---
# SR-015: Code review — PR #53

## Summary

Ticket: PLAT-240. Reviewed the manifest (`record-sections` token, event
`source` locator, domain `relationships` locator, version 0.10.0), the
regenerated schemas (`Process.states`, `Domain.relations`, dropped
`Domain.members`, `Domain.ubiquitous_language`, `NestedEntity.owner`), the
TypeSpec source, the four changed skeletons and the changed tests, against
quoin `origin/main` FR-121 and FR-123 and quire-rs `origin/main` FR-081 and
its reader `src/semantic/record.rs`.

Clean parts: `node scripts/generate-schemas.mjs --check` reports all 24
schemas match `typespec/main.tsp`, so the schemas were regenerated from the
source. The manifest changes match the skeletons: `domain` has the
`relationships` locator and a `## Relationships` table of `contains` rows
that its `allowed_links` admit; `event` has the `source` locator and a
`## Source` section; the `aggregate_root` skeleton keeps `## Members` and
drops the `aggregates`/`contains` rows, which quire-rs FR-081 would refuse as
`declared-in-members`. Removing `RELATIONSHIP_ORDER_UNIQUE` from
`tests/test_relationships.py` deletes a pin whose rows no longer exist.
`Domain.members`, `Domain.ubiquitous_language` and `NestedEntity.owner` are
referenced nowhere in schemas, TypeSpec or tests except as refusals; the
remaining `members`/`owner` mentions are the FR-008 construct declarations
(out of scope for this PR), the display-only `ubiquitous_language`
`section_body` locator, plan files and earlier review files.

## Verdict

**NOT MERGEABLE** — FND-001: the event skeleton authors `## Source` as a
bare id, but the reader the PR targets (quoin FR-121, quire-rs FR-081,
merged on quire-rs main) reads a scalar key only from one inline-code value.
Once that reader ships, the module's own event skeleton fails validation
with `semantic.feature-not-extractable` `source`, and TC-113 asserts the
wrong form. The fix is two backticks in the skeleton and the test's parse.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | high | The `event` skeleton's `## Source` body is the bare text `aggregate_root_001`. quoin FR-121 and quire-rs FR-081 read a scalar key "from a body of exactly one inline-code value", and quire-rs `src/semantic/record.rs` `read_key` (Node::Scalar) strips one surrounding backtick pair and otherwise emits `semantic.feature-not-extractable` with reason `source`. The quire-rs golden case authors `` `agg-001` ``. With `record-sections` now in `semantic.mappings` and `Event.json` declaring `source` as a `SemanticId`, the skeleton fails `validate_document` on the first engine that ships FR-081. TC-113 parses `body.split()` and looks the token up as an id, so it locks in the bare form and would fail on the correct `` `aggregate_root_001` ``. | spec_objects_business/skeletons/event.md:54-56, tests/test_record_key_owners.py:96-102 | implementation-bug-despite-evidence |

## Gates Run

Not an aggregate gate. `node scripts/generate-schemas.mjs --check` (24
schemas match), `pytest` with the existing quire 0.54.0 venv (242 passed,
7 skipped, 2 xfailed), and `quoin validate --strict` (quoin 0.29.1: no
findings). FND-001 was traced in quire-rs `origin/main` source and its
golden case; no quire-rs build was run.

## Dispositions

Round 1, checked against fix commit e6834e9 (schemas-check 24/24, pytest 242 passed, quoin validate --strict clean).

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | `skeletons/event.md` `## Source` is now `` `aggregate_root_001` `` and its comment says one inline-code id; TC-113 parses it with `` re.fullmatch(r"\s*`([^`\s]+)`\s*", body) ``, so a bare id now fails the test. |
