---
id: NFR-001
title: "Additive compatibility of the semantic contract"
type: NFR
quality_attribute: compatibility
relationships:
  - target: "ix://agent-ix/spec-objects-business/FR-003"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-business/FR-005"
    type: "constrains"
---
# NFR-001: Additive compatibility of the semantic contract

## Statement

The module SHALL keep every artifact that validated against version 0.2.0
validating against version 0.3.0 with at most warning-level semantic
findings, while the untyped `properties` string and every 0.2.0 locator yield
stay byte-identical.

## Scope

- Applies to: `manifest.yaml`, the shipped schemas, and the skeletons.
- Operational context: existing corpus artifacts authored in legacy
  Properties forms (bullet lists, free-column tables) under `legacy_forms:
  warning`; no corpus repository is edited.

## Rationale

The ticket's merge gate is advisory-only until corpus promotion. A module that
turned legacy artifacts into errors would force corpus edits this campaign
forbids; a module that changed a locator would change every existing
extraction record.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| 0.2.0 locators changed | 0 | 0 | Test |
| Legacy-form 0.2.0 entity skeleton under 0.3.0: error findings | 0 | 0 | Test |
| Legacy-form 0.2.0 entity skeleton under 0.3.0: `semantic.legacy-properties-form` warnings | 1 | 1 | Test |
| `properties` string for the legacy skeleton, 0.2.0 vs 0.3.0 | identical | identical | Test |

## Verification

A checked-in copy of the 0.2.0 `body_extraction` and of the 0.2.0 entity
skeleton is compared against the 0.3.0 manifest and validated under it: the
locators are equal, the legacy skeleton validates with exactly one
legacy-form warning and no error, and its extracted `properties` string is
unchanged.

## Dependencies

- **Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md), [FR-005](../functional/FR-005-executable-skeletons.md); quoin FR-074 (`ix://agent-ix/quoin/FR-074`)
- **Downstream**: corpus promotion (`agent-ix/quoin#291` sweep), outside this module
