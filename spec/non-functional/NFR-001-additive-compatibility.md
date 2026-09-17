---
id: NFR-001
title: "Compatibility of the semantic contract"
type: NFR
quality_attribute: compatibility
relationships:
  - target: "ix://agent-ix/spec-objects-business/FR-003"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-business/FR-005"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-business/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-007"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-009"
    type: "depends_on"
---
# NFR-001: Compatibility of the semantic contract

## Statement

The module SHALL be additive for the Properties forms and for every locator
outside the declared model-table sections: each 0.2.0 `body_extraction`
locator outside those sections is unchanged, each 0.2.0 skeleton that authors
no model-table section in an undeclared form validates with at most
warning-level semantic findings, and the untyped `properties` string is
byte-identical between 0.2.0 and the current manifest.

The declared model-table sections (FR-006) and the `## Relationships` section
(FR-007) SHALL refuse every form the manifest does not declare. The FR-007
`relationships` mapping token is module-wide, so the Relationships break
applies to all eleven object types: at 0.4.0 a `## Relationships` section was
unread prose in any form; from 0.5.0 a list, fence, or diagram there is
refused with `semantic.feature-not-extractable`, a prose-only section yields
the warning `semantic.relationships-no-block`, and a table, including a header-only
table, on an object type that declares no `relationships` locator is refused
with `semantic.record-invalid`. An object id (FR-009) SHALL match
`^[A-Za-z][A-Za-z0-9_]*$`: an artifact whose id carries a hyphen, as every
0.2.0 skeleton's does, is refused with its required `id` missing. These refusals are breaking for an artifact that
authors one of those sections in another form, so the manifest declares
`compatibility_posture: strict` (FR-003).

## Scope

- Applies to: `manifest.yaml`, the shipped schemas, and the skeletons.
- Additive: the Properties forms and every locator outside the declared
  model-table sections.
- Breaking: the declared model-table sections (`domain` `Ubiquitous Language`,
  `aggregate_root` `Members`, `state_machine` `States` and `Transitions`,
  `process` `Workflow` and `States`, `enumeration` `Values`, `population`
  `Members`), which hold only their declared table and prose; and the
  `## Relationships` section on all eleven object types, which holds only the
  FR-104 table (rows checked against `edge_types` and `allowed_links`) and is
  admitted only on `entity`, `aggregate_root`, `process`, and `repository`
  (the last two once `agent-ix/quire-rs#435` lowers their rows into `emits`
  and `persists`); and the object id, which admits no hyphen (FR-009), on
  all eleven object types.
- Operational context: existing corpus artifacts authored in legacy
  Properties forms (bullet lists, free-column tables) under `legacy_forms:
  warning`; no corpus repository is edited.

## Rationale

A module that turned legacy Properties forms into errors would force corpus
edits; a module that changed a locator would change every existing
extraction record. The domain model is declared in spec artifacts as tables
the engine extracts, so the sections that hold it admit only those tables.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| 0.2.0 locators changed outside the declared model-table sections, the FR-009 `id` regex aside | 0 | 0 | Test |
| 0.2.0 skeletons whose type's required model tables are all authored as those tables in 0.2.0, ids in FR-009 underscore form, under the current manifest: error findings, per skeleton | 0 | 0 | Test |
| Each legacy-form `## Properties` skeleton under the current manifest: `semantic.legacy-properties-form` warnings | 1 | 1 | Test |
| `properties` string for each legacy skeleton, 0.2.0 vs current | identical | identical | Test |

## Verification

No 0.2.0 skeleton carries a frontmatter `object:` key, so Quire runs
headings-only validation on it and never assembles or checks a typed record;
NFR-001-AC-2 asserts that rather than assuming it. The measured set excludes
each skeleton whose type requires a model table that the 0.2.0 skeleton does
not author as that table: `aggregate_root` (Members list), `state_machine`
(diagram), and `process` (Workflow diagram). The `domain` skeleton's bulleted
Ubiquitous Language stays in the set and passes only because the `vocabulary`
table is optional.

Once a legacy-form artifact declares `object:`, quire 0.46.0 assembles its
declaration record as `{}` and validates it against the type schema, so it
fails `semantic.record-invalid` at error severity even under `legacy_forms:
warning`. `agent-ix/quire-rs#391` owns that rule. The module carries that case
as an explicit expected failure beside NFR-001-AC-2 rather than relaxing a
schema.

A checked-in copy of the 0.2.0 `body_extraction` and of the 0.2.0 skeletons is
compared against the current manifest and validated under it: the locator
definitions outside the declared model-table sections are equal apart from the
FR-009 `regex` on `id`, each measured skeleton, its id written with
underscores, validates with no error, each legacy skeleton that carries a
legacy-form `## Properties` yields exactly one legacy-form warning, and its
extracted `properties` string is unchanged.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every 0.2.0 `body_extraction` locator outside the declared model-table sections is present with identical facets (0 changed), except that the `id` locator also carries the FR-009 `regex`. | Test |
| NFR-001-AC-2 | Each 0.2.0 skeleton, its id written with underscores (FR-009), validates under the current manifest with 0 error findings, excluding the skeletons whose type requires a model table that the 0.2.0 skeleton does not author as that table (`aggregate_root` Members list, `state_machine` diagram, `process` Workflow diagram). The `domain` skeleton's bulleted Ubiquitous Language passes only because the `vocabulary` table is optional. | Test |
| NFR-001-AC-3 | Each 0.2.0 skeleton carrying a legacy-form `## Properties` yields exactly 1 `semantic.legacy-properties-form` warning. | Test |
| NFR-001-AC-4 | Each such skeleton's extracted `properties` string, its id written with underscores, is byte-identical under 0.2.0 and the current manifest. | Test |

## Dependencies

- **Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md), [FR-005](../functional/FR-005-executable-skeletons.md), [FR-006](../functional/FR-006-model-table-locators.md), [FR-007](../functional/FR-007-relationships-table.md), [FR-009](../functional/FR-009-object-ids.md); quoin FR-074 (`ix://agent-ix/quoin/FR-074`)
- **Downstream**: corpus promotion (`agent-ix/quoin#291` sweep), outside this module
