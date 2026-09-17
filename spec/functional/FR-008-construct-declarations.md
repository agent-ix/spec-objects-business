---
id: FR-008
title: "Declare the semantic IR construct of each object type"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/filament-core-service/FR-035"
    type: "depends_on"
  - target: "ix://agent-ix/filament-core-data/FR-142"
    type: "depends_on"
  - target: "ix://agent-ix/quire-specification/FR-208"
    type: "depends_on"
---
# FR-008: Declare the semantic IR construct of each object type

## Description

The manifest SHALL declare, once per object type, the semantic IR
`construct:` (filament-core-service FR-035 CR-004) of each of the ten
construct kinds — `domain`, `entity`, `value_object`, `aggregate_root`,
`nested_entity`, `repository`, `event`, `state_machine`, `process` and
`enumeration` — as filament-core-data FR-142 reads them, so that FCD and Quire
read each kind's identity, shape, members, references, rules and meaning from
module data rather than a hard-coded kind list.

## Inputs

- The FR-035 module-manifest schema at filament-core-service `e33070e`
  (`$defs/ConstructDeclaration`).
- The FR-142 core vocabulary and the `business` module declarations of
  `agent-ix/filament-core-data#172`
  (`schema/semantic/v1/construct-vocabulary.json`,
  `docs/semantic-data-system/contracts-v1.md`).
- The QSpec FR-208 meaning id vocabulary (`agent-ix/quire-specification`
  main).

## Outputs

- A `construct:` on each of the ten object types in `manifest.yaml`, and on
  `population` once filament-core-data declares a population shape.
- The roles `aggregate-member` and `composite-owner` on the object types the
  references admit, declared in the manifest's top-level `roles:` registry.

## Behavior

- Each construct SHALL be the declaration in this table:

| Object type | Identity | Shape | Members | References | Rules | Meaning |
|---|---|---|---|---|---|---|
| `domain` | `none` | `namespace` | `members`, `vocabulary` required; `fields`, `operations` forbidden | — | `no_fields`, `no_operations`, `exclusive_membership`, `members_not_namespace` | `quire.meaning.namespace` |
| `entity` | `identified` | `record` | `fields`, `identityFields` required | — | `identity_field_required` | `quire.meaning.model.object-type/v1` |
| `value_object` | `value` | `record` | `fields` required | — | `identity_field_forbidden` | `quire.meaning.model.value-type/v1` |
| `aggregate_root` | `identified` | `record` | `fields`, `identityFields`, `clauses`, `members` required | `members`: `aggregate-member` | `identity_field_required`, `min_clauses` | `quire.meaning.model.object-type/v1` |
| `nested_entity` | `identified` | `record` | `fields`, `identityFields`, `owner` required | `owner`: `composite-owner` | `identity_field_required`, `single_owner` | `quire.meaning.model.object-type/v1` |
| `repository` | `none` | `interface` | `operations`, `persists` required; `fields` forbidden | `persists`: `persistable` | `no_fields`, `min_operations` | `quire.meaning.persistence-interface` |
| `event` | `none` | `record` | `fields`, `occurrenceField` required | — | `identity_field_forbidden`, `occurrence_field_required` | `quire.meaning.model.value-type/v1` |
| `state_machine` | `none` | `state_machine` | `operations`, `states`, `transitions` required | `transitions`: `event-like` | `min_operations` | `quire.meaning.state-machine` |
| `process` | `identified` | `sequence` | `fields`, `identityFields`, `steps` required | `steps`: `event-like` | `identity_field_required` | `quire.meaning.process` |
| `enumeration` | `none` | `enumeration` | `variants` required; `fields`, `relationships`, `operations` forbidden | — | none | `quire.meaning.model.variant-type/v1` |

- `population` SHALL declare a construct whose meaning is `quire.meaning.model.population/v1` (QSpec FR-208). Known gap: the FR-142 core vocabulary has no population shape, so the manifest carries no `population` construct until `agent-ix/filament-core-data#174` adds one.
- `entity`, `value_object`, `nested_entity` and `enumeration` SHALL carry the role `aggregate-member`; `entity`, `aggregate_root` and `nested_entity` SHALL carry the role `composite-owner`.
- The manifest SHALL declare `aggregate-member` and `composite-owner` in its top-level `roles:` registry (FR-040 form: `<role>: { description: "..." }`), so that a registry loading this module beside spec-artifacts-iso reports no `UnknownRole` for either.
- Every declaration SHALL use only FR-142 core vocabulary terms, and each rule's member presence SHALL be the presence the declaration states, or the member's default where it states none.
- Every `references` entry SHALL name an FR-142 reference member the declaration does not forbid, and only roles an object type of this manifest carries, never `*` and never an object type name.
- The six meanings of `entity`, `value_object`, `aggregate_root`, `nested_entity`, `event` and `enumeration` are FR-208 values. The meanings of `domain`, `repository`, `state_machine` and `process` are not FR-208 values, so under FR-208-AC-3 model intake refuses those four kinds.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | Exactly the ten construct kinds declare a `construct:`, `population` declares none while `agent-ix/filament-core-data#174` is open, and the manifest has zero violations against the FR-035 schema at `e33070e`. | Test |
| FR-008-AC-2 | Each declaration equals its row of the Behavior table, each type carries the roles the table's references admit, and exactly `entity`, `value_object`, `aggregate_root`, `nested_entity`, `event` and `enumeration` bind an FR-208 meaning. | Test |
| FR-008-AC-3 | Each declaration's identity, shape, member names and rules are FR-142 core vocabulary, no rule repeats, each rule's member presence holds, and each `references` entry names a non-forbidden reference member and only roles an object type of the manifest carries, never `*` or a type name. | Test |
| FR-008-AC-4 | A wildcard reference role, an identity outside the enum, a member presence outside the enum, and a missing `meaning` are each refused by the FR-035 schema at the construct path. | Test |
| FR-008-AC-5 | The manifest `roles:` registry declares exactly `aggregate-member` and `composite-owner`, each with a description; applying the quire-rs FR-040 load check to this manifest beside the spec-artifacts-iso roles and archetypes reports no unknown role other than the pre-existing `process` → `action` and `repository` → `data_schema` link targets, and removing the registry reports both roles unknown on every type that carries them. | Test |

## Dependencies

- **Upstream**: filament-core-service FR-035 CR-004 at `e33070e`; filament-core-data FR-142 (`agent-ix/filament-core-data#172`); QSpec FR-208; quire-rs FR-040 roles registry (`src/loader/mod.rs` load check); the spec-artifacts-iso `roles:` registry; [FR-003](./FR-003-semantic-manifest-contract.md)
- **Downstream**: `agent-ix/quire-rs#445` carries each declaration on `CompiledArchetype::construct()`; filament-core-data pins this manifest version. Its extraction-frontend fixtures name object artifacts with hyphenated ids (`EN-001`, `VO-001`, `AR-001`, …), which this version refuses (FR-009), so pinning it renames those ids to underscore form and regenerates the goldens (`agent-ix/filament-core-data#175`); `agent-ix/filament-core-data#174` adds the population shape the `population` construct needs
