---
id: NFR-001
title: "Additive compatibility of the semantic contract"
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
---
# NFR-001: Additive compatibility of the semantic contract

## Statement

The module SHALL keep every artifact of the checked-in 0.2.0 skeleton set
whose type declares no required FR-006 model table — the seven skeletons other
than `aggregate_root`, `state_machine`, and `process`, which is the population
this NFR measures — validating against the current manifest with at most
warning-level semantic findings.

The module SHALL keep every 0.2.0 `body_extraction` locator definition
unchanged except the five whose sections FR-006 declares as model tables
(`domain.ubiquitous_language`, `aggregate_root.members`,
`state_machine.diagram`, `process.diagram`, `process.states`), and SHALL keep
the untyped `properties` string those locators yield byte-identical between
0.2.0 and the current manifest. Yields of the other 0.2.0 locators are
unmeasured and are not claimed.

## Scope

- Applies to: `manifest.yaml`, the shipped schemas, and the skeletons, outside
  the FR-006 model-table sections. An artifact of `aggregate_root`,
  `state_machine`, or `process` authors its model tables to validate.
- Operational context: existing corpus artifacts authored in legacy
  Properties forms (bullet lists, free-column tables) under `legacy_forms:
  warning`; no corpus repository is edited.

## Rationale

The ticket's merge gate is advisory-only until corpus promotion. A module that
turned legacy artifacts into errors would force corpus edits this campaign
forbids; a module that changed a locator would change every existing
extraction record. The FR-006 model tables are the declared exception: the
domain model is declared in spec artifacts as tables the engine extracts, and
the sections that hold it carry no other form.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| 0.2.0 locators changed outside the FR-006 model tables | 0 | 0 | Test |
| Measured 0.2.0 skeleton set under the current manifest: error findings, per skeleton | 0 | 0 | Test |
| Each legacy-form `## Properties` skeleton under the current manifest: `semantic.legacy-properties-form` warnings | 1 | 1 | Test |
| `properties` string for each legacy skeleton, 0.2.0 vs current | identical | identical | Test |

## Verification

NFR-001-AC-2 holds on the population this NFR measures, and the measurement
says why: no 0.2.0 skeleton carries a frontmatter `object:` key, so Quire
runs headings-only validation on it and never assembles or checks a typed
record. That is what makes the manifest additive for the artifacts that exist today,
and it is asserted rather than assumed.

The engine defect behind it is real but differently scoped: once a
legacy-form artifact *does* declare `object:`, quire 0.46.0 assembles its
declaration record as `{}` and validates it against the type schema
unconditionally, so it fails `semantic.record-invalid` at error severity even
under `legacy_forms: warning`. `agent-ix/quire-rs#391` owns that rule. The
module carries that case as an explicit expected failure beside NFR-001-AC-2
rather than relaxing a schema, so the day the engine changes, the row turns
red and is noticed.

A checked-in copy of the 0.2.0 `body_extraction` and of all ten 0.2.0
skeletons is compared against the current manifest and validated under it:
the locator definitions outside the FR-006 model tables are equal, each
measured skeleton validates, with no error, and each legacy skeleton —
where it carries a legacy-form `## Properties` — exactly one
legacy-form warning, and its extracted `properties` string is unchanged.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every 0.2.0 `body_extraction` locator outside the five FR-006 model-table locators is present with identical facets (0 changed). | Test |
| NFR-001-AC-2 | Each of the seven measured skeletons of the checked-in 0.2.0 set validates under the current manifest with 0 error findings. | Test |
| NFR-001-AC-3 | Each 0.2.0 skeleton carrying a legacy-form `## Properties` yields exactly 1 `semantic.legacy-properties-form` warning. | Test |
| NFR-001-AC-4 | Each such skeleton's extracted `properties` string is byte-identical under 0.2.0 and the current manifest. | Test |

## Dependencies

- **Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md), [FR-005](../functional/FR-005-executable-skeletons.md), [FR-006](../functional/FR-006-model-table-locators.md); quoin FR-074 (`ix://agent-ix/quoin/FR-074`)
- **Downstream**: corpus promotion (`agent-ix/quoin#291` sweep), outside this module
