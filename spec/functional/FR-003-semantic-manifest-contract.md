---
id: FR-003
title: "Declare the semantic-module contract in the manifest"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-001"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-073"
    type: "depends_on"
---
# FR-003: Declare the semantic-module contract in the manifest

## Description

`spec_objects_business/manifest.yaml` SHALL carry the quoin FR-070 `semantic`
block and reference every exported object type's emitted schema by path and
digest (quoin FR-073), at manifest `version` 0.6.0, so that Quoin verifies
the shipped schemas at install and Quire validates every declaration record
against them, while every extraction locator outside the FR-006 model tables
keeps its meaning.

## Inputs

- The emitted schemas and digests of [FR-002](./FR-002-emitted-json-schemas.md).
- The module-manifest schema with the `semantic` block, at
  `agent-ix/filament-core-service` revision `e33070e` (CR-004) — the same
  revision FR-001 names. Quire vendors it byte-identically
  (`sha256:6782f74f…`); Quoin still vendors an older copy
  (`sha256:69cf9738…` at quoin `99bd4f0`) and re-vendors it under
  `agent-ix/quoin#559`. That skew is a defect on Quoin, not a change here.

## Outputs

- `manifest.yaml` with `version: 0.6.0`, a `semantic` block, and reference-form
  `data_schema` on every exported object type.

## Behavior

- The manifest `semantic` block SHALL carry exactly these keys and values: `contract_version: 1.0.0`, `semantic_core: 0.2.0`, `package: agent-ix/spec-objects-business`, `exports` listing every object type that ships a schema, `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, generalization, abstract-types, presence, subsetting, redefinition, effect-frames, relationships]`, `compatibility_posture: strict`, `legacy_forms: warning`.
- `semantic.exports` SHALL name all eleven object types: `domain`, `entity`, `value_object`, `aggregate_root`, `nested_entity`, `repository`, `event`, `state_machine`, `process`, `enumeration`, `population`.
- `compatibility_posture` SHALL be `strict`, because the declared model-table sections refuse every form the manifest does not declare (NFR-001), which is a breaking change for an artifact authoring one of those sections in another form; `additive` would misstate that, and `declared-lossy` names lossy mappings, which this module declares none of.
- Every exported object type's `data_schema` SHALL be `{ schema: schemas/<Model>.json, digest: sha256:<hex> }` where `<hex>` is the SHA-256 of the shipped file bytes.
- No exported object type SHALL carry an inline `data_schema`.
- The manifest `version` SHALL be `0.6.0`, because the emitted `$id` embeds it and the FR-006 model-table locators, the FR-007 `## Relationships` table, the FR-008 construct declarations and the FR-009 object id pattern change what an object type declares and admits.
- The six quire-rs FR-075 tokens `generalization`, `abstract-types`, `presence`, `subsetting`, `redefinition`, and `effect-frames` SHALL gate extraction of their forms; `typed-table` and `sysml-fence` SHALL name the two Properties forms as quoin mapping ids. The FR-075 tokens name: `generalization` the frontmatter `specializes` relationship, `abstract-types` the frontmatter `abstract` flag, `presence`, `subsetting`, and `redefinition` the Properties `Presence`, `Subsets`, and `Redefines` columns, and `effect-frames` the operation `Modifies:`, `Creates:`, and `Deletes:` lines. Quire refuses a `specializes`, `abstract`, `Presence`, `Subsets`, `Redefines`, `Modifies:`, `Creates:`, or `Deletes:` form whose token the block does not name with `semantic.feature-not-extractable`. The quoin FR-104 token `relationships` gates the FR-007 `## Relationships` table.
- Every `body_extraction` locator present at version 0.2.0 SHALL remain present with the same `from`, heading, `language`, `required`, `multiple`, and `assert` facets, except the locators whose sections FR-006 declares as model tables (`domain.ubiquitous_language`, `aggregate_root.members`, `state_machine.diagram`, `process.diagram`, `process.states`).
- The `properties` string locator (`section_body` after `Properties`) on `entity` and `value_object` SHALL stay in place, so the untyped `properties` string continues to be yielded beside the semantic record.
- Where an object type gains a locator after 0.2.0 that is not an FR-006 model table, that locator SHALL be `required: false`, so existing artifacts stay valid (the additions themselves are specified by FR-005).
- The manifest SHALL load through Quire's registry loader with no `ArchetypeLoadFailure` for any object type and with the recorded schema digest equal to the manifest digest.
- Measured against quire 0.46.0: a refused schema drops that object type alone, while a manifest key the loader cannot parse (an unknown `semantic` key) drops every object type of the module, so a consumer sees the module as absent. Both refusals are silent — no diagnostic names the offending key, path, or digest — which `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394` record as engine defects; the naming half of FR-003-AC-6 is blocked on them and is verified as an explicit expected failure rather than dropped.
- The manifest SHALL install through `quoin module install path:<module dir>` with no `semantic.*` error diagnostic.
- When the install has completed, `quoin module` SHALL list `spec-objects-business`.
- If Quoin or Quire rejects the manifest, then this module SHALL correct its own manifest or schemas rather than relax the contract keys, the digests, or the `$id` rules to make a consumer accept them.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-003-CON-1 | The `semantic` block SHALL contain no key outside the admitted list. Quire's loader refusal of an unknown key is verified here (FR-003-AC-6); Quoin's refusal is the neighbour's own obligation (quoin FR-070) and is assumed, evidenced only by the clean install of IT-002. | Compatibility | Test |
| FR-003-CON-2 | The manifest SHALL mark every locator added after 0.2.0 outside the FR-006 model tables `required: false`. | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | The loaded `semantic` block equals the nine admitted keys with the values above, and `exports` equals the eleven object-type names. | Test |
| FR-003-AC-2 | For every exported type, `data_schema` is the reference form, the referenced file exists, and its SHA-256 equals the recorded digest. | Test |
| FR-003-AC-3 | Every 0.2.0 locator outside the FR-006 model tables, compared against the checked-in 0.2.0 baseline, is present unchanged; every added locator outside them is `required: false`. | Test |
| FR-003-AC-4 | `quire.Registry.load_from([module dir])` lists all eleven archetypes and `validate_document` on each skeleton reports no `semantic.*` load failure. | Test |
| FR-003-AC-5 | `quoin module install path:<module dir>` exits zero and `quoin module` lists `spec-objects-business`; the previously installed entry is restored afterwards. | Demonstration |
| FR-003-AC-6 | A manifest copy whose `semantic` block gains a key `foo` is refused by Quire's loader naming `foo`; a copy whose digest is altered is refused naming the path. | Test |

## Dependencies

- **Upstream**: [FR-001](./FR-001-module-manifest-activates.md), [FR-002](./FR-002-emitted-json-schemas.md); quoin FR-070/FR-073 (`ix://agent-ix/quoin/FR-070`, `ix://agent-ix/quoin/FR-073`); quire-rs FR-069 (`ix://agent-ix/quire-rs/FR-069`)
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md), [FR-006](./FR-006-model-table-locators.md), [FR-007](./FR-007-relationships-table.md), [IT-002](../integration/IT-002-quoin-module-install.md)
