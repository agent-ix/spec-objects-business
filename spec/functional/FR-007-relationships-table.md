---
id: FR-007
title: "Declare domain relationships as a Relationships table"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-006"
    type: "refines"
  - target: "ix://agent-ix/quoin/FR-104"
    type: "depends_on"
  - target: "ix://agent-ix/quire-rs/FR-076"
    type: "depends_on"
---
# FR-007: Declare domain relationships as a Relationships table

## Description

The manifest SHALL declare the quoin FR-104 `## Relationships` table on every
object type whose declaration record admits `relations`, and SHALL declare in
its `edge_types` every verb its `allowed_links` name, so that an artifact
states its domain relationships as rows Quire lowers to `relations`, and
Quire refuses every row whose verb, target, or multiplicity the module does
not admit.

## Inputs

- quoin FR-104 (`agent-ix/quoin` `99bd4f0`): the `relationships` mapping token
  and the `Name | Verb | Target | Multiplicity` table.
- quire-rs FR-076 (`agent-ix/quire-rs` `44df254`): the row checks, their
  refusal reasons, and the Python `validate_document(..., bundle_package=...)`
  surface.
- The `edge_types` of `agent-ix/spec-artifacts-iso`
  (`spec_artifacts_iso/manifest.yaml`).
- The FR-004 record schemas: `Entity` and `AggregateRoot` admit `relations`; `Process` admits `emits` and `Repository` admits `persists`.

## Outputs

- `relationships` in the manifest `semantic.mappings`.
- A `relationships` `table_row` locator on `entity`, `aggregate_root`, `process`, and `repository`.
- One `edge_types` entry per verb any `allowed_links` names.
- A `## Relationships` table in the `aggregate_root` skeletons.
- Positive fixtures for a populated table, a header-only table, a prose-only
  section, and a target in another artifact; negative fixtures for the four
  row refusals, a list-form section, and a table on a type without `relations`.

## Behavior

- The manifest `semantic.mappings` SHALL include `relationships`.
- The `entity`, `aggregate_root`, `process`, and `repository` object types SHALL each declare the locator `relationships: { from: table_row, under_section: Relationships, required: false, assert: { columns: [Name, Verb, Target, Multiplicity] } }`, with no `min_rows`, so a header-only table declares that the artifact has no domain relationships; on `entity` and `aggregate_root` it extracts `available` with empty `relations`.
- No other object type SHALL declare a `relationships` locator.
- On `entity` and `aggregate_root`, whose records admit `relations` (FR-004), every row SHALL lower into `relations`.
- On `process` and `repository`, whose records forbid `relations` (FR-004), the rows SHALL lower into typed record keys instead: a process `emits` row into `emits`, and a repository `persists` row into `persists`; they SHALL NOT populate `relations`. Following quoin FR-104, nothing is invented or dropped: the typed key SHALL hold each row's qualified `ix://` target, `relationSources` SHALL still carry every row (its `Name`, `Verb`, `Target`, and `Multiplicity` cells and its line), so `availability.relations` is `available` and not lossy; a header-only table SHALL extract `available` with the typed key present and empty. This lowering is the target design and is built by `agent-ix/quire-rs#435`; until it lands, Quire lowers those rows into `relations` and refuses the record with exactly one `semantic.record-invalid` error at `relations`, so the `process` and `repository` skeletons author no `## Relationships` table.
- The `relationships` mapping token is module-wide, so on every one of the eleven object types a `## Relationships` section is read as the FR-104 table: a list, fence, or diagram there is refused with `semantic.feature-not-extractable`, and a section holding only prose yields the warning `semantic.relationships-no-block` and extracts nothing.
- If an artifact whose object type declares no `relationships` locator (`domain`, `value_object`, `nested_entity`, `event`, `state_machine`, `enumeration`, `population`) authors a `## Relationships` table, including a header-only table, then Quire SHALL refuse the record with `semantic.record-invalid` naming `relations`. That finding carries no line today; `agent-ix/quire-rs#440` makes it name the table line.
- The `## Relationships` table SHALL be the one authority for domain edges (quoin FR-104). `emits` SHALL stay a table verb on `aggregate_root` and `process`, and `persists` a table verb on `repository`; the record `emits` and `persists` keys `agent-ix/quire-rs#435` extracts SHALL be derived from those rows, never from a second declaration site. Event `source` and nested-entity `owner` remain `agent-ix/quire-rs#435`.
- The manifest `edge_types` SHALL declare every verb an `allowed_links` entry names, each with the description, category, and inverse `agent-ix/spec-artifacts-iso` declares, so a registry that loads both modules merges identical entries.
- Each row's `Verb` SHALL be an `edge_types` verb the artifact's object type admits in `allowed_links`; its `Target` SHALL be an artifact id whose object type satisfies that verb's `allowed_links` targets; its `Multiplicity` SHALL be a multiplicity (`1..1`, `0..*`).
- `specializes` SHALL stay a frontmatter relationship only; a `specializes` row is refused (quire-rs FR-076 `generalization`).
- The `## Relationships` table SHALL be the one authority for an artifact's domain relationships; frontmatter `relationships` is the artifact-graph surface, and no skeleton declares a domain relationship there.
- The `aggregate_root` skeletons SHALL author a `## Relationships` table whose targets are skeleton artifact ids.
- `validate_document` passes a bundle package but no bundle index, so it checks a row's target against `allowed_links` only when the target is the artifact's own id; a target in another artifact lowers with the advisory `semantic.unresolved-target` (`no-bundle-index`) and is not checked. Checking such targets in `quoin validate` is `agent-ix/quoin#557`; `extract_semantic` with a bundle index checks them today.
- If a row names a verb outside `edge_types`, an inverse label, a target whose object type the verb does not admit, or a malformed multiplicity, then Quire SHALL refuse it with `semantic.invalid-model-cell` at the row's line and the reason `unknown-verb`, `inverse-verb`, `target-not-allowed`, or `multiplicity`, and `availability.relations` SHALL be `unavailable` with reason `entry-errors: lines <n>`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | `semantic.mappings` includes `relationships`; `entity`, `aggregate_root`, `process`, and `repository` declare the `relationships` locator above, with no `min_rows`, and no other object type declares one; `edge_types` is `specializes` plus the fifteen domain verbs with the spec-artifacts-iso category and inverse, and every `allowed_links` verb is declared. | Test |
| FR-007-AC-2 | Each skeleton with a `## Relationships` table validates under `bundle_package: agent-ix/spec-objects-business`, and extracts `availability.relations` `available` with one `relations` entry per row, in row order, carrying its verb, category, `composite`, `ix://` target, and multiplicity; no skeleton carries frontmatter `relationships` or a `specializes` row. | Test |
| FR-007-AC-3 | The entity positive fixture validates and lowers one relation per row covering every non-`specializes` verb `entity` admits, with `composite` true exactly for `contains`. | Test |
| FR-007-AC-4 | The unknown-verb, inverse-verb, target-not-allowed, and bad-multiplicity negative fixtures each fail `validate_document` with exactly one error, `semantic.invalid-model-cell` at the row line; extract exactly one diagnostic, at that line with their reason; carry `availability.relations` `unavailable` with `entry-errors: lines <n>`; and lower no relation. The inverse-verb message names the forward verb `aggregates` and the target `aggregate-root-001`. | Test |
| FR-007-AC-5 | The header-only entity fixture validates and extracts `availability.relations` `available` with empty `relations` and no Relationships diagnostic. | Test |
| FR-007-AC-6 | No record schema other than `Entity` and `AggregateRoot` declares `relations`, and the `value_object` Relationships-table fixture and the same artifact with a header-only table each fail `validate_document` with exactly one `semantic.record-invalid` error at `relations` (line null until `agent-ix/quire-rs#440`). | Test |
| FR-007-AC-7 | The list-form entity fixture fails with `semantic.feature-not-extractable` at the list line, and the prose-only entity fixture validates with one `semantic.relationships-no-block` warning at the heading line. | Test |
| FR-007-AC-8 | Through `validate_document`, the entity fixture whose row targets `aggregate-root-999` validates with one `semantic.unresolved-target` advisory at that row naming the missing bundle index. | Test |
| FR-007-AC-9 | A `process` artifact with the row `done emits event-001 0..1` and a `repository` artifact with the row `orders persists aggregate-root-001 0..*` each validate, and extract `emits` and `persists` respectively holding the qualified target, no `relations`, one `relationSources` entry carrying the row's `Name`, `Verb`, `Target`, and `Multiplicity` cells and its line, and `availability.relations` `available` and not lossy; the same artifacts with a header-only table validate and extract `available` with the typed key present and empty. Each type is an explicit expected failure until `agent-ix/quire-rs#435`. | Test |
| FR-007-AC-10 | Until `agent-ix/quire-rs#435` lands, each of those `process` and `repository` artifacts fails `validate_document` with exactly one `semantic.record-invalid` error at `relations`; this criterion is removed when AC-9 passes. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md); quoin FR-104; quire-rs FR-076 (`agent-ix/quire-rs#418`); `agent-ix/quire-rs#435` (derived `emits`), `agent-ix/quire-rs#440` (record-invalid line), `agent-ix/quire-rs#441` (column-assert error reported twice), `agent-ix/quoin#557` (bundle index in `quoin validate`)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [NFR-001](../non-functional/NFR-001-additive-compatibility.md)
