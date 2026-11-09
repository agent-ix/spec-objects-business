---
id: SR-018
title: "Code review — PR #54 variant_set and graph object types"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-business; spec_objects_business/manifest.yaml, spec_objects_business/schemas/{VariantSet,VariantDecl,Graph}.json, spec_objects_business/skeletons/{variant_set,graph}.md, typespec/main.tsp, tests/ (PR #54 diff vs origin/main 0aa44f8, head 5527158)"
review_set: subset
---
# SR-018: Code review — PR #54

## Summary

Ticket: PLAT-160 (gaps 4 and 5). Reviewed the PR #54 diff against
`origin/main` (0aa44f8): the `variant_set` and `graph` manifest entries, the
`VariantSet`, `VariantDecl` and `Graph` TypeSpec models and their emitted
schemas, the two skeletons, the positive and refused fixtures, and the test
changes. The quire-rs FR-081 record-sections reader was traced in quire-rs
`origin/main` `src/semantic/record.rs` (`owner()`, header matching, cell
kinds) and `src/validate_document.rs` (record schema wiring).

Gates run on head 5527158 with the `spec-objects-business-Dc60l5v7` venv
(quire 0.54.0, Python 3.13) after `npm ci`: full pytest 268 passed, 7
skipped, 2 xfailed, coverage 100%; `node scripts/generate-schemas.mjs
--check` reports 27 schemas matching. The installed 0.54.0 wheel does not
carry FR-081 (its `extract_semantic` returns no `record` key even for the
event `## Source` section), so the record-sections path was traced in
source, not executed.

## Verdict

**NOT MERGEABLE as written.** The schemas are sealed and match the TypeSpec
source, the manifest exports, `data_schema` references and skeletons agree,
no sibling module (architecture, safety, iso) declares a union or graph
type, and the `tests/fixtures/refused/` placement is justified: both refusals
are `required '<key>' ... is missing` errors, which the negative sweep's
`semantic.*` code list cannot hold. But the `variant_set` record key
`variants` and its `## Variants` table do not agree (FND-001): under the
module's own `record-sections` token, quire-rs FR-081 reads that table into
`variants` and refuses its `Variant` and `Description` columns and its TypeRef
`Payload` cells, so the skeleton and positive fixture fail as soon as a quire
release carries FR-081. FND-002 is medium; the rest are low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | high | `VariantSet.json` declares `variants: VariantDecl[]` with `VariantDecl = { name: Identifier, payload?: TypeRef }`, and the manifest names `record-sections`. quire-rs FR-081 (`record.rs` `owner()`) does not own `variants` (it is not an FR-075 model-table key), so `## Variants` normalizes to `variants` and is read as an array-of-objects table: header `Variant` and `Description` match no `VariantDecl` property (`semantic.invalid-model-cell` `column-unknown`), and every non-empty `Payload` cell is a TypeRef object (`nested-object-cell`). `validate_document` wires the record schema on quire-rs main, so the `variant_set` skeleton and positive fixture fail TC-119 once a quire release ships FR-081. Under 0.54.0 the key is never filled. Align the table and the record: columns that match `VariantDecl` (for example `Name \| Payload \| Description` with a `description` property and a cell-readable `payload` such as a `SemanticId`), or drop `variants` from the record. | spec_objects_business/schemas/VariantSet.json:5-11, spec_objects_business/schemas/VariantDecl.json:5-12, typespec/main.tsp:759-775, spec_objects_business/skeletons/variant_set.md:26-31, spec_objects_business/manifest.yaml:535-541 | wrong-requirement |
| FND-002 | medium | The skeleton and positive fixture name variants in kebab case (`revision-mismatch`, `byte-digest-mismatch`), but `VariantDecl.name` is semantic-core `Identifier`, `^[A-Za-z_][A-Za-z0-9_]*$`. Any record built from these rows fails `VariantDecl`; the schema test in TC-121 uses `digest_mismatch`, so it never meets this. | spec_objects_business/skeletons/variant_set.md:28-30, tests/fixtures/positive/variant_set-diagnostic-cause.md:16-17 | implementation-bug-despite-evidence |
| FND-003 | low | The `Payload` sentinel `none` is not a type. Read into `payload` it becomes a target named `none` (a `target-not-id` refusal for a `SemanticId` cell). FR-081 omits the field of an empty cell, which is the no-payload form the schema already models. | spec_objects_business/skeletons/variant_set.md:31, tests/fixtures/positive/variant_set-diagnostic-cause.md:18 | wrong-requirement |
| FND-004 | low | The refused fixtures carry `expect:` and `because:` frontmatter that no test reads, and the values are wrong: `variant_set-variants-as-list.md` says `semantic.feature-not-extractable` and "a form the manifest does not declare", and `graph-without-diagram.md` says `required-locator-missing`, but both refusals are `[<type>] required '<key>' (...) is missing`. Delete the keys or assert them. | tests/fixtures/refused/variant_set-variants-as-list.md:6-7, tests/fixtures/refused/graph-without-diagram.md:6-7 | implementation-bug-despite-evidence |
| FND-005 | low | The new positive fixtures reuse ids already on main: `variant_set-diagnostic-cause.md` is `positive_004` like `entity-relationships.md`, and `graph-causal-control.md` is `positive_005` like `entity-relationships-header-only.md`. | tests/fixtures/positive/variant_set-diagnostic-cause.md:2, tests/fixtures/positive/graph-causal-control.md:2 | implementation-bug-despite-evidence |
| FND-006 | low | `assert len(skeletons) == 16` bumps a hard-coded count (was 14). The PR description says counts were made count-free. The number guards nothing that `OBJECT_TYPES` plus the three alternates does not already give. | tests/test_skeletons_semantic.py:78 | implementation-bug-despite-evidence |
| FND-007 | low | The PR description still says FR-010 with AC-1..4 and TC-111..TC-114. Commit 4fd2f0a renumbered the work to FR-011 and TC-118..TC-121, and FR-010 / TC-111..TC-116 are PLAT-240's (PR #53). | PR #54 description | implementation-bug-despite-evidence |

## Gates Run

- `pytest` (venv `spec-objects-business-Dc60l5v7`, quire 0.54.0): 268 passed, 7 skipped, 2 xfailed, coverage 100%.
- `node scripts/generate-schemas.mjs --check`: 27 schemas match.

## Dispositions

Round 1, checked against fix commit c12d7d8 (head 715eb3e).

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | `VariantDecl` is now `{ name: Identifier, payload?: SemanticId, description?: string }` and the table is `Name \| Payload \| Description`. Traced in quire-rs main `record.rs`: the headers normalize to `name`, `payload` and `description` (no `column-unknown`). `Identifier.json` resolves through the embedded semantic-core bundle to a text scalar, `SemanticId.json` is special-cased to `Scalar::SemanticId` (no `nested-object-cell`), and `description` is a text scalar. An empty cell is skipped before typing (`row()` line 932). A payload id resolves through `resolve_id`; with no bundle package or no bundle index it gives an advisory only. |
| FND-002 | fixed | Skeleton and fixture names are now `revision_mismatch` and similar; TC-121 refuses `digest-mismatch`. |
| FND-003 | fixed | The `none` sentinel is gone; a variant with no payload now has an empty `Payload` cell. |
| FND-004 | fixed | `expect:` and `because:` are removed from both refused fixtures. |
| FND-005 | fixed | The fixture ids are now `positive_variant_set_001` and `positive_graph_001`; no fixture id is duplicated. |
| FND-006 | fixed | The `len(skeletons) == 16` assertion is removed. |
| FND-007 | fixed | The PR description now says FR-011 / TC-118..TC-121 and attributes FR-010 / TC-111..TC-117 to PLAT-240 (#53). |
