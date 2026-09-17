---
id: FR-006
title: "Declare every object-type model table in the manifest"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-005"
    type: "refines"
  - target: "ix://agent-ix/quire-rs/FR-075"
    type: "depends_on"
---
# FR-006: Declare every object-type model table in the manifest

## Description

The manifest SHALL declare, as a `table_row` locator, every object-type model
table Quire extracts for this module's types (values, states, transitions,
steps, members, vocabulary), and the skeletons SHALL author those sections as
exactly those tables, so that the domain model is declared in spec artifacts
typed by this module's object types and Quire extracts it as the manifest
directs, refusing every form the manifest does not declare.

## Inputs

- The quire-rs FR-075 model-table column sets, each first column the entry
  key: `Value | Description`, `State | Description`,
  `From | To | Trigger | Guard | Emits`,
  `Step | Kind | Consumes | Emits | Description`, `Member | Multiplicity`,
  `Term | Description`.
- The manifest `semantic.mappings` tokens of FR-003.
- The Quire wheel FR-005 Inputs names, at quire-rs `6eec7e8` or later.

## Outputs

- One `table_row` locator per model table in `manifest.yaml`.
- A semantic record per skeleton whose `model` carries one entry per table row
  and whose `availability.model` is `available`.
- Positive and negative fixtures under `tests/fixtures/positive/` and
  `tests/fixtures/negative/`.

## Behavior

- The manifest SHALL declare these model-table locators, each `from: table_row` with `under_section` the heading below, `assert.columns` the full column set of its table, and `assert.min_rows: 1`:

  | Object type | Locator | Section | Columns | Required |
  |---|---|---|---|---|
  | `enumeration` | `values_table` | `Values` | `Value, Description` | true |
  | `domain` | `vocabulary` | `Ubiquitous Language` | `Term, Description` | false |
  | `aggregate_root` | `members` | `Members` | `Member, Multiplicity` | true |
  | `state_machine` | `states` | `States` | `State, Description` | true |
  | `state_machine` | `transitions` | `Transitions` | `From, To, Trigger, Guard, Emits` | true |
  | `process` | `steps` | `Workflow` | `Step, Kind, Consumes, Emits, Description` | true |
  | `process` | `states` | `States` | `State, Description` | false |

- Each model table SHALL own its own `##` section, because `validate_document` asserts the first table under a locator's section.
- Every declared column SHALL appear in the table header; an empty cell is how an author leaves an optional value (`Guard`, `Emits`, `Consumes`, `Description`) unset.
- A `state_machine` transition's `From` and `To` SHALL name rows of its `## States` table, its `Trigger` SHALL name an operation of the same artifact, and its `Guard`, when present, SHALL name an invariant clause of the same artifact.
- A `process` step's `Kind` SHALL be one of `command`, `event`, `decision`, `compensation`, `wait`.
- An `aggregate_root` member's `Member` SHALL name a declaration by its title, and its `Multiplicity` SHALL be a multiplicity (`1..*`, `3..3`).
- A section that owns a model table SHALL hold only that table and prose; a diagram, fence, or list there is refused with `semantic.feature-not-extractable`.
- If a table with a model-table header appears under a section this manifest does not declare for the artifact's type, then Quire SHALL refuse it with `semantic.feature-not-extractable`.
- The declared-model positive fixture SHALL exercise every FR-003 mapping token beyond the Properties forms: a `specializes` relationship, `abstract: true`, `Presence`, `Subsets`, and `Redefines` columns, and `Requires:`, `Ensures:`, `Modifies:`, `Creates:`, and `Deletes:` operation lines.
- Every object type that carries fields SHALL admit a `specializes` link to its own type in `allowed_links`, so a declared generalization is not a disallowed edge.
- Each negative fixture SHALL name its `expect:` code and fail for that reason: an enumeration `## Values` list, a state-machine `## States` diagram, a transition naming an unknown state, a transition naming an unknown trigger, a transition guard naming no clause, a step with an unknown kind, an aggregate `## Members` list, a duplicate vocabulary term, a model table under a section the type does not declare, and a `Presence` cell that is neither `required` nor `optional`.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-006-CON-1 | The manifest SHALL use only locator keys the pinned FR-035 module-manifest schema admits (`columns`, `min_rows`); column optionality and cell vocabularies are the engine's FR-075 checks, not manifest facets. | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | The `table_row` locators whose `assert.columns` equal a model-table column set are exactly the seven in Behavior, with the listed section, `required` flag, and `min_rows: 1`, and no other assert key. | Test |
| FR-006-AC-2 | The `enumeration`, `domain`, `aggregate_root`, `state_machine`, and `process` skeletons extract with `availability.model` `available`, no error, no `semantic.feature-not-extractable`, and one model entry per table row, in row order, keyed by the table's first column. | Test |
| FR-006-AC-3 | The declared-model positive fixture validates, and its record carries the `specializes` target, `abstract: true`, the `Presence`, `Subsets`, and `Redefines` cells, one operation frame with its `Requires:`, `Ensures:`, `Modifies:`, `Creates:`, and `Deletes:` lines, and the transition guard. | Test |
| FR-006-AC-4 | Each of the ten negative fixtures in Behavior fails `validate_document` with an error carrying its `expect:` code, and every model table has at least one. | Test |
| FR-006-AC-5 | No skeleton carries an `ocl` fence, a `Pre:` or `Post:` line, or a `mermaid` fence outside the domain ERD; every extracted skeleton clause has language `quire` and no `semantic.clause-language-unchecked` advisory. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md); quire-rs FR-071 (clauses and operation contracts) and FR-075 (model features); `@agent-ix/semantic-core` 0.2.0
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [NFR-001](../non-functional/NFR-001-additive-compatibility.md)
