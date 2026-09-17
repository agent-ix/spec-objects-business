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

- quoin FR-104 (`agent-ix/quoin` `2dad869`): the `relationships` mapping token
  and the `Name | Verb | Target | Multiplicity` table.
- quire-rs FR-076 (`agent-ix/quire-rs` `44df254`): the row checks, their
  refusal reasons, and the Python `validate_document(..., bundle_package=...)`
  surface.
- The `edge_types` of `agent-ix/spec-artifacts-iso`
  (`spec_artifacts_iso/manifest.yaml`).
- The FR-004 record schemas: `Entity` and `AggregateRoot` admit `relations`.

## Outputs

- `relationships` in the manifest `semantic.mappings`.
- A `relationships` `table_row` locator on `entity` and `aggregate_root`.
- One `edge_types` entry per verb any `allowed_links` names.
- A `## Relationships` table in the `aggregate_root` skeletons.
- A positive fixture and four negative fixtures.

## Behavior

- The manifest `semantic.mappings` SHALL include `relationships`.
- The `entity` and `aggregate_root` object types SHALL each declare the locator `relationships: { from: table_row, under_section: Relationships, required: false, assert: { columns: [Name, Verb, Target, Multiplicity], min_rows: 1 } }`.
- No other object type SHALL declare a `relationships` locator, because its record schema forbids `relations` (FR-004). Repository `persists`, event `source`, nested-entity `owner`, and aggregate/process `emits` are extracted by `agent-ix/quire-rs#435`, not by this table.
- The manifest `edge_types` SHALL declare every verb an `allowed_links` entry names, each with the description, category, and inverse `agent-ix/spec-artifacts-iso` declares, so a registry that loads both modules merges identical entries.
- Each row's `Verb` SHALL be an `edge_types` verb the artifact's object type admits in `allowed_links`; its `Target` SHALL be an artifact id whose object type satisfies that verb's `allowed_links` targets; its `Multiplicity` SHALL be a multiplicity (`1..1`, `0..*`).
- `specializes` SHALL stay a frontmatter relationship only; a `specializes` row is refused (quire-rs FR-076 `generalization`).
- The `## Relationships` table SHALL be the one authority for an artifact's domain relationships; frontmatter `relationships` is the artifact-graph surface, and no skeleton declares a domain relationship there.
- The `aggregate_root` skeletons SHALL author a `## Relationships` table whose targets are skeleton artifact ids.
- If a row names a verb outside `edge_types`, an inverse label, a target whose object type the verb does not admit, or a malformed multiplicity, then Quire SHALL refuse it with `semantic.invalid-model-cell` and the reason `unknown-verb`, `inverse-verb`, `target-not-allowed`, or `multiplicity`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | `semantic.mappings` includes `relationships`; `entity` and `aggregate_root` declare the `relationships` locator above and no other object type declares one; `edge_types` is `specializes` plus the fifteen domain verbs with the spec-artifacts-iso category and inverse, and every `allowed_links` verb is declared. | Test |
| FR-007-AC-2 | Each skeleton with a `## Relationships` table validates under `bundle_package: agent-ix/spec-objects-business`, and extracts `availability.relations` `available` with one `relations` entry per row, in row order, carrying its verb, category, `composite`, `ix://` target, and multiplicity; no skeleton carries frontmatter `relationships` or a `specializes` row. | Test |
| FR-007-AC-3 | The entity positive fixture validates and lowers one relation per row covering every non-`specializes` verb `entity` admits, with `composite` true exactly for `contains`. | Test |
| FR-007-AC-4 | The unknown-verb, inverse-verb, target-not-allowed, and bad-multiplicity negative fixtures each fail `validate_document` with `semantic.invalid-model-cell`, extract exactly one diagnostic with their reason, and lower no relation. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md); quoin FR-104; quire-rs FR-076 (`agent-ix/quire-rs#418`)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [NFR-001](../non-functional/NFR-001-additive-compatibility.md)
