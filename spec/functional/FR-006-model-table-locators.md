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
table Quire extracts for this module's types (population, values, states,
transitions, steps, members, vocabulary), and the skeletons SHALL author those
sections as exactly those tables, with every clause a valid Quire expression,
so that the domain model is declared in spec artifacts typed by this module's
object types and Quire extracts it as the manifest directs, refusing every
form the manifest does not declare.

## Inputs

- The quire-rs FR-075 model-table column sets, each first column the entry
  key: `Type | Extent`, `Value | Description`, `State | Description`,
  `From | To | Trigger | Guard | Emits`,
  `Step | Kind | Consumes | Emits | Description`, `Member | Multiplicity`,
  `Term | Description`.
- The manifest `semantic.mappings` tokens of FR-003.
- The Quire expression grammar: QSpec `proposals/quire-v1/shared-grammar.md`
  and `proposals/state-core/profile.md`.
- The Quire wheel FR-005 Inputs names, at quire-rs `6eec7e8` or later.

## Outputs

- One `table_row` locator per model table in `manifest.yaml`.
- A `specializes` entry in the manifest `edge_types`.
- A semantic record per skeleton whose `model` carries one entry per table row
  and whose `availability.model` is `available`.
- Positive and negative fixtures under `tests/fixtures/positive/` and
  `tests/fixtures/negative/`.

## Behavior

- The manifest SHALL declare these model-table locators, each `from: table_row` with `under_section` the heading below, `assert.min_rows: 1`, `assert.columns` the column set of its table, and `assert.optional_columns` the optional columns below:

  | Object type | Locator | Section | Columns | Optional columns | Required |
  |---|---|---|---|---|---|
  | `population` | `population` | `Members` | `Type, Extent` | none | true |
  | `enumeration` | `values` | `Values` | `Value, Description` | `Description` | true |
  | `domain` | `vocabulary` | `Ubiquitous Language` | `Term, Description` | `Description` | false |
  | `aggregate_root` | `members` | `Members` | `Member, Multiplicity` | none | true |
  | `state_machine` | `states` | `States` | `State, Description` | `Description` | true |
  | `state_machine` | `transitions` | `Transitions` | `From, To, Trigger, Guard, Emits` | `Guard, Emits` | true |
  | `process` | `steps` | `Workflow` | `Step, Kind, Consumes, Emits, Description` | `Consumes, Emits, Description` | true |
  | `process` | `states` | `States` | `State, Description` | `Description` | false |

- Until the FR-035 module-manifest schema admits `assert.optional_columns` (`agent-ix/filament-core-service#31`), the manifest SHALL list every column in `assert.columns` and declare no `optional_columns`; an author leaves an optional value unset with an empty cell.
- Each model table SHALL own its own `##` section.
- A `population` member's `Type` SHALL name a declaration, its `Extent` SHALL be a multiplicity (`0..*`, `1..1`), and each `Type` SHALL appear once; a repeated `Type` is refused with `semantic.duplicate-model-entry`.
- A `state_machine` transition's `From` and `To` SHALL name rows of its `## States` table, its `Trigger` SHALL name an operation of the same artifact, and its `Guard`, when present, SHALL name an invariant clause of the same artifact.
- A `process` step's `Kind` SHALL be one of `command`, `event`, `decision`, `compensation`, `wait`.
- An `aggregate_root` member's `Member` SHALL name a declaration by its title, and its `Multiplicity` SHALL be a multiplicity (`1..*`, `3..3`).
- Every name in an `Emits` or `Consumes` cell and on a `Creates:` line SHALL name a declaration of the skeleton bundle, and a `Deletes:` line SHALL name the declaration whose instance is deleted, never a field.
- A section that owns a model table SHALL hold only that table and prose; a diagram, fence, or list there is refused with `semantic.feature-not-extractable`.
- If a table with a model-table header appears under a section this manifest does not declare for the artifact's type, then Quire SHALL refuse it with `semantic.feature-not-extractable`.
- Every skeleton and fixture clause SHALL be a valid Quire expression: an enumeration value is written in its qualified form `Model::Enum::Variant` (the model alias is `OrderManagement`, pending `agent-ix/quire-specification#84`), `present()` applies only to a `0..1` field, every field a clause reads is declared in the same artifact, and each clause name states exactly what its expression checks.
- An invariant SHALL hold in every state the model allows. A condition that holds only on some transitions belongs to that transition's `Guard` or its operation's `Pre:`; stating it there as an inline Quire expression is `agent-ix/quire-rs#433`. Until then, a `Guard` or `Pre:` line that names an invariant is always true, and the declared-model positive fixture uses one only to exercise extraction.
- The declared-model positive fixture SHALL exercise every FR-003 mapping token beyond the Properties forms: a `specializes` relationship, `abstract: true`, `Presence`, `Subsets`, and `Redefines` columns, and `Pre:`, `Post:`, `Modifies:`, `Creates:`, and `Deletes:` operation lines.
- The manifest SHALL declare `specializes` in its `edge_types` with category `structural` and inverse `generalizes`, and every object type that carries fields SHALL admit a `specializes` link to its own type in `allowed_links`, so a declared generalization is a known, allowed edge.
- Each negative fixture SHALL name its `expect:` code and fail for that reason: an enumeration `## Values` list, a state-machine `## States` diagram, a process `## States` list, a transition naming an unknown state, a transition naming an unknown trigger, a transition guard naming no clause, a step with an unknown kind, an aggregate `## Members` list, a duplicate vocabulary term, a duplicate population member type, a model table under a section the type does not declare, and a `Presence` cell that is neither `required` nor `optional`.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-006-CON-1 | Each model-table locator SHALL declare its optional columns as the manifest facet `assert.optional_columns`. Blocked on `agent-ix/filament-core-service#31`: the pinned FR-035 schema admits `columns` and `min_rows` only, so the manifest carries the full column list and no other assert key until it admits the facet. | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | The `table_row` locators whose first `assert.columns` entry is a model-table key are exactly the eight in Behavior, with the listed section, `required` flag, `min_rows: 1`, and every column belonging to that table. | Test |
| FR-006-AC-2 | The `population`, `enumeration`, `domain`, `aggregate_root`, `state_machine`, and `process` skeletons extract with `availability.model` `available`, no error, no `semantic.feature-not-extractable`, and one model entry per table row, in row order, keyed by the table's first column. | Test |
| FR-006-AC-3 | The declared-model positive fixture validates, and its record carries the `specializes` target, `abstract: true`, the `Presence`, `Subsets`, and `Redefines` cells, one operation frame with its `Pre:`, `Post:`, `Modifies:`, `Creates:`, and `Deletes:` lines, and the transition guard and emitted event; its `current_state` is typed by the `ReturnStatus` enumeration fixture whose values equal its `## States` rows. | Test |
| FR-006-AC-4 | Each of the twelve negative fixtures in Behavior fails `validate_document` with an error carrying its `expect:` code, and every model table has at least one. | Test |
| FR-006-AC-5 | No skeleton carries an `ocl` fence or a `mermaid` fence outside the domain ERD, and every operation contract line is a `Pre:` or `Post:` line; every extracted skeleton clause has language `quire` and no `semantic.clause-language-unchecked` advisory. | Test |
| FR-006-AC-6 | The population positive fixture validates and extracts one population member per `## Members` row, in row order, with its type and extent. | Test |
| FR-006-AC-7 | The manifest `edge_types` declares `specializes` with category `structural` and inverse `generalizes`, and every field-bearing object type admits `specializes` in `allowed_links`. | Test |
| FR-006-AC-8 | Every skeleton and fixture `quire` fence is a valid Quire expression by the rules in Behavior, and every `Emits`, `Consumes`, `Creates:`, and `Deletes:` name resolves. | Inspection |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md); quire-rs FR-071 (clauses and operation contracts) and FR-075 (model features); `@agent-ix/semantic-core` 0.3.0; `agent-ix/filament-core-service#31` (optional columns), `agent-ix/quire-rs#433` (inline guard expressions), `agent-ix/quire-specification#84` (fence model alias)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [NFR-001](../non-functional/NFR-001-additive-compatibility.md)
