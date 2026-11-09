---
id: FR-011
title: "Declare closed unions and partial-order graphs as object types"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-006"
    type: "depends_on"
---
# FR-011: Declare closed unions and partial-order graphs as object types

## Description

The manifest SHALL declare a `variant_set` object type for a closed
discriminated union and a `graph` object type for an acyclic partial order,
because `enumeration` (a flat label set) and `state_machine` (one current
state, transitions between states) fit neither. This module owns both: it
already owns `enumeration`, `state_machine` and `process`, and no other module
declares a union or a graph type.

## Inputs

- The `enumeration` and `state_machine` declarations of `manifest.yaml`.
- `typespec/main.tsp`, emitted per [FR-002](./FR-002-emitted-json-schemas.md).

## Outputs

- Object types `variant_set` and `graph`, exported from `semantic.exports`.
- Schemas `VariantSet.json`, `VariantDecl.json` and `Graph.json`.
- Skeletons `variant_set.md` and `graph.md`.

## Behavior

- A `variant_set` SHALL author a required `## Variants` table with the columns `Name`, `Payload` and `Description` and at least one row. Each `Name` SHALL be an identifier (`^[A-Za-z_][A-Za-z0-9_]*$`). `Payload`, when present, SHALL be the artifact id of the type the variant carries; an empty `Payload` cell means the variant carries no payload. The set is closed: its rows are every variant. A list under `## Variants` is refused as a missing required `variants` locator.
- A `variant_set`'s `allowed_links` SHALL admit `references` to `enumeration`, `value_object` and `variant_set`, so a payload can be a label set, a record or a nested union.
- A `graph` SHALL author a required `## Graph` section holding exactly one `mermaid` fence of kind `flowchart` or `graph`. Nodes with no path between them are unordered. Prose alone under `## Graph` is refused as a missing required `graph` locator.
- A `graph`'s `allowed_links` SHALL admit `references` to `entity`, `aggregate_root`, `value_object`, `enumeration`, `event`, `process` and `graph`.
- `VariantSet` SHALL be the sealed record `{ variants?: VariantDecl[], clauses?: ClauseRef[] }`, which admits no `fields`, `operations`, `states` or `transitions`.
- `Graph` SHALL be the sealed record `{ clauses?: ClauseRef[] }`, which admits no `fields`, `operations`, `states` or `transitions`.
- `VariantDecl` SHALL be the sealed record `{ name: Identifier, payload?: SemanticId, description?: string }`; a table cell reads a `SemanticId`, not a `TypeRef` object.
- Neither skeleton SHALL author an `## Invariants` section, and neither type declares an `invariants` locator; `clauses` is a record key for hand-built records only, as for `enumeration`.
- The `variants` key SHALL be filled from the `## Variants` table by the module-wide `record-sections` mapping (FR-010, quoin FR-121); its `Name`, `Payload` and `Description` headers are the `VariantDecl` property names that mapping matches. `Graph` has no graph-valued record key: the `## Graph` fence is read by this manifest's `graph` locator only.
- Neither type declares a `construct:`: the FR-142 core vocabulary has no union or partial-order shape ([FR-008](./FR-008-construct-declarations.md)).
- The engine does not check that a `Payload` resolves beyond the bundle target rules, that the diagram is acyclic, or that the fence holds exactly one diagram of `flowchart` or `graph` kind; the skeletons state these as rules for the author.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-011-AC-1 | `semantic.exports` names `variant_set` and `graph`; `variant_set` admits `references` to exactly `enumeration`, `value_object` and `variant_set`; `graph` admits `references` to exactly `entity`, `aggregate_root`, `value_object`, `enumeration`, `event`, `process` and `graph`, and no other verb; each has a reference-form `data_schema`. | Test |
| FR-011-AC-2 | The `variants` locator is required with the columns `Name`, `Payload`, `Description` and `min_rows: 1`; the `variant_set` skeleton and positive fixture validate; the list-form fixture is refused as a missing `variants`. | Test |
| FR-011-AC-3 | The `graph` locator is a required `code_block` with language `mermaid` and the `graph` type declares no `states` locator; the `graph` skeleton and positive fixture validate; the prose-only fixture is refused as a missing `graph`. | Test |
| FR-011-AC-4 | `VariantSet.json` and `Graph.json` accept the empty record and a `clauses` list; `VariantSet.json` accepts `variants` with and without a `payload` and `description`, and refuses a variant without a `name`, a non-identifier `name` and a `TypeRef` object `payload`; both refuse `fields`, `operations`, `states` and `transitions`; `Graph.json` refuses `variants`. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md); [FR-006](./FR-006-model-table-locators.md); `@agent-ix/semantic-core`
- **Downstream**: `agent-ix/quire-specification` object FRs that need a closed union or a causal graph (`FR-272`, `FR-220` there) can use these types instead of `value_object` and `aggregate_root`.
