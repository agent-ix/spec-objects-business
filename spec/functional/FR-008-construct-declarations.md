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

- The FR-035 module-manifest schema's `$defs/ConstructDeclaration`, whose
  optional `immutable` boolean (`agent-ix/filament-core-service#37`)
  filament-core-data reads to render a construct's instances read-only, frozen,
  with no setters. Absent means `false`.
- The FR-142 core vocabulary and the `business` module declarations of
  `agent-ix/filament-core-data#172`
  (`schema/semantic/v1/construct-vocabulary.json`,
  `docs/semantic-data-system/contracts-v1.md`).
- The QSpec FR-208 meaning id vocabulary (`agent-ix/quire-specification`
  `c8e3ca0`).

## Outputs

- A `construct:` on each of the ten object types in `manifest.yaml`, and on
  `population` once filament-core-data declares a population shape.
- The roles `aggregate-member` and `composite-owner` on the object types the
  references admit, declared in the manifest's top-level `roles:` registry.

## Behavior

- Each construct SHALL be the declaration in this table:

| Object type | Identity | Shape | Members | References | Rules | Meaning | Immutable |
|---|---|---|---|---|---|---|---|
| `domain` | `none` | `namespace` | `members`, `vocabulary` required; `fields`, `operations` forbidden | — | `no_fields`, `no_operations`, `exclusive_membership`, `members_not_namespace` | `quire.meaning.model.namespace/v1` | — |
| `entity` | `identified` | `record` | `fields`, `identityFields` required | — | `identity_field_required` | `quire.meaning.model.object-type/v1` | — |
| `value_object` | `value` | `record` | `fields` required | — | `identity_field_forbidden` | `quire.meaning.model.record-value-type/v1` | — |
| `aggregate_root` | `identified` | `record` | `fields`, `identityFields`, `clauses`, `members` required | `members`: `aggregate-member` | `identity_field_required`, `min_clauses` | `quire.meaning.model.object-type/v1` | — |
| `nested_entity` | `identified` | `record` | `fields`, `identityFields`, `owner` required | `owner`: `composite-owner` | `identity_field_required`, `single_owner` | `quire.meaning.model.object-type/v1` | — |
| `repository` | `none` | `interface` | `operations`, `persists` required; `fields` forbidden | `persists`: `persistable` | `no_fields`, `min_operations` | `quire.meaning.model.persistence-interface/v1` | — |
| `event` | `none` | `record` | `fields`, `occurrenceField` required | — | `identity_field_forbidden`, `occurrence_field_required` | `quire.meaning.model.event-type/v1` | `true` |
| `state_machine` | `none` | `state_machine` | `operations`, `states`, `transitions` required | `transitions`: `event-like` | `min_operations` | `quire.meaning.model.state-machine/v1` | — |
| `process` | `identified` | `sequence` | `fields`, `identityFields`, `steps` required | `steps`: `event-like` | `identity_field_required` | `quire.meaning.model.process/v1` | — |
| `enumeration` | `none` | `enumeration` | `variants` required; `fields`, `relationships`, `operations` forbidden | — | none | `quire.meaning.model.variant-type/v1` | — |

- `population` SHALL declare a construct whose meaning is `quire.meaning.model.population/v1` (QSpec FR-208). Known gap: the FR-142 core vocabulary has no population shape, so the manifest carries no `population` construct until `agent-ix/filament-core-data#174` adds one.
- `event`'s `construct:` SHALL declare `immutable: true`; no other of the ten kinds' `construct:` SHALL declare `immutable`, because absence already means `false` and `event` is the only kind whose instances filament-core-data renders read-only, frozen, with no setters.
- `entity`, `value_object`, `nested_entity` and `enumeration` SHALL carry the role `aggregate-member`; `entity`, `aggregate_root` and `nested_entity` SHALL carry the role `composite-owner`.
- The manifest SHALL declare `aggregate-member` and `composite-owner` in its top-level `roles:` registry (FR-040 form: `<role>: { description: "..." }`), so that a registry loading this module beside spec-artifacts-iso reports no `UnknownRole` for either.
- Every declaration SHALL use only FR-142 core vocabulary terms, and each rule's member presence SHALL be the presence the declaration states, or the member's default where it states none.
- Every `references` entry SHALL name an FR-142 reference member the declaration does not forbid, and only roles an object type of this manifest carries, never `*` and never an object type name.
- Every construct `meaning` SHALL be a QSpec FR-208 meaning id, spelled exactly as FR-208 lists it at `c8e3ca0`. FR-208 gives invariants (`## Invariants` clauses) and `specializes` generalization their meaning on `value_object`, `event`, `state_machine` and `process`, and gives `Pre:`/`Post:` operation contracts their meaning on `state_machine` and `process` only.
- The module SHALL refuse every form FR-208 (`c8e3ca0`) states as an intake refusal for the meaning a kind binds, wherever this module's own record schema (FR-004) governs the refused member. SOB refuses at the record-schema layer with `semantic.record-invalid`, not with FR-208's own diagnostic codes; each bullet below names the FR-208 refusal SOB's schema reaches for that form.
  - `ValueObject.json` (`record-value-type/v1`) carries no `operations` key: an operation on a `value_object` refuses the form FR-208 refuses as `unsupported_construct`/`declaration-form`.
  - `Event.json` (`event-type/v1`) carries no `operations` key: an operation on an `event` refuses the form FR-208 refuses as `invalid_model_binding`/`malformed-declaration`.
  - `Repository.json` (`persistence-interface/v1`) carries no `clauses` key, and each `operations[]` entry's `pre` and `post` must be empty or absent: a `quire` clause, and a `Pre:`/`Post:` contract, on a `repository` operation each refuse the form FR-208 refuses as `unsupported_construct`/`declaration-form`. FR-208 also refuses a non-empty operation frame (`Modifies:`/`Creates:`/`Deletes:`) on a persistence interface; that data reaches no member this module's record schema declares (FR-006, blocked on `agent-ix/quire-rs#431`), so this module cannot refuse it at the record-schema layer. FR-208 also refuses an empty `persists` on a persistence interface; `Repository.json` admits both `persists: []` and an absent `persists` and refuses neither — FR-004's optional-key rule admits an absent array, FR-007-AC-9 admits a header-only empty typed key, and extracting `persists` from an artifact's body is blocked on `agent-ix/quire-rs#435` — so this module does not implement that refusal.
  - `Domain.json` (`namespace/v1`) carries no `fields`, `operations`, or `clauses` key: a field or an operation on a `domain` refuses the form FR-208 refuses as `invalid_model_binding`/`malformed-declaration`; a `quire` clause on a `domain` refuses the form FR-208 refuses as `unsupported_construct`/`declaration-form`.
  - Neither `repository` nor `domain` carries `specializes` in its `allowed_links` (FR-006-AC-7 names only field-bearing types), so a `specializes` relationship naming either is already refused as an unadmitted edge (quire-rs FR-076): FR-208's `supertypes` refusal on a persistence interface or a namespace.
  - FR-208's Generalization rule (a `supertypes[]` entry naming a node of another meaning is refused) is already satisfied for `entity`, `aggregate_root`, `nested_entity` (`object-type/v1`) and `enumeration` (`variant-type/v1`): each type's `allowed_links.specializes`, where declared, names only its own kind. FR-208 states no further per-meaning intake refusal for `object-type` beyond this generalization rule and the meanings' member lists above. For `variant-type`, FR-208 additionally refuses a clause that *names* a variant type; that refusal reads a clause's target, and a clause's body is opaque `quire` grammar this module's record schema never parses, so it is outside this layer's reach.
- Refusal of a malformed declaration — a wildcard reference role, an identity or member presence outside the enum, a missing `meaning`, a non-boolean `immutable` — is filament-core-service's obligation under FR-035, verified where that schema is applied. It becomes observable here once a published quire applies a schema admitting `ObjectTypeEntry.construct` (`agent-ix/quire-rs#455`); quire 0.46.0, the newest wheel any index carries, does not.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | Exactly the ten construct kinds declare a `construct:`, and `population` declares none while `agent-ix/filament-core-data#174` is open. | Test |
| FR-008-AC-2 | Each declaration equals its row of the Behavior table, each type carries the roles the table's references admit, and every one of the ten declarations binds an FR-208 meaning id at `c8e3ca0`. | Test |
| FR-008-AC-3 | Each declaration's identity, shape, member names and rules are FR-142 core vocabulary, no rule repeats, each rule's member presence holds, and each `references` entry names a non-forbidden reference member and only roles an object type of the manifest carries, never `*` or a type name. | Test |
| FR-008-AC-5 | The manifest `roles:` registry declares exactly `aggregate-member` and `composite-owner`, each with a description; applying the quire-rs FR-040 load check to this manifest beside the spec-artifacts-iso roles and archetypes reports no unknown role other than the pre-existing `process` → `action` and `repository` → `data_schema` link targets, and removing the registry reports both roles unknown on every type that carries them. | Test |
| FR-008-AC-6 | `event`'s `construct:` declares `immutable: true`; none of the other nine declarations declares `immutable`. | Test |
| FR-008-AC-7 | `ValueObject.json` refuses a record with `operations`; `Repository.json` refuses a record with `clauses`, and refuses an `operations[]` entry whose `pre` or `post` is non-empty, while admitting one whose `pre` and `post` are absent or empty; `Domain.json` refuses a record with `fields`, `operations`, or `clauses`; `repository` and `domain` admit no `specializes` target in `allowed_links`. Each refusal also admits a positive record that omits the refused form. | Test |

## Dependencies

- **Upstream**: filament-core-service FR-035 CR-004 (`agent-ix/filament-core-service#37` adds `immutable`); filament-core-data FR-142 (`agent-ix/filament-core-data#172`); QSpec FR-208; quire-rs FR-040 roles registry (`src/loader/mod.rs` load check); the spec-artifacts-iso `roles:` registry; [FR-003](./FR-003-semantic-manifest-contract.md)
- **Downstream**: `agent-ix/quire-rs#445` carries each declaration on `CompiledArchetype::construct()`; filament-core-data pins this manifest version. Its extraction-frontend fixtures name object artifacts with hyphenated ids (`EN-001`, `VO-001`, `AR-001`, …), which this version refuses (FR-009), so pinning it renames those ids to underscore form and regenerates the goldens (`agent-ix/filament-core-data#175`); `agent-ix/filament-core-data#174` adds the population shape the `population` construct needs
- **Downstream**: filament-core-data reads the enumeration Values table under the old locator key `values_table` (`crates/extraction-frontend/src/enumeration.rs` `VALUES_TABLE`, plus its fixture manifests and goldens); this release keys it `values`, so pinning it moves filament-core-data to `values` (`agent-ix/filament-core-data#177`)
