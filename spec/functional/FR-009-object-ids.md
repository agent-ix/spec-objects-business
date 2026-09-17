---
id: FR-009
title: "Write object ids with underscores"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-002"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-005"
    type: "refines"
  - target: "ix://agent-ix/quire-specification/FR-154"
    type: "depends_on"
---
# FR-009: Write object ids with underscores

## Description

The id of an artifact whose type is one of this module's object types SHALL be
a letter followed by letters, digits and underscores, so that an object id is
one identifier token wherever it is named. A hyphen is refused. Artifact-type
ids such as `FR-100` are not object ids and this requirement does not govern
them. The rule is the object id rule of QSpec FR-154 (merged at
`ac06d5a`): QSL model intake refuses a model node whose artifact id is not an
object id, and refuses a reference to an id no admitted node carries, so both
the ids and the references to them are enforced at intake as well as here.

## Inputs

- `typespec/main.tsp`, emitted per [FR-002](./FR-002-emitted-json-schemas.md).
- The shared `id` locator of `manifest.yaml`.

## Outputs

- The TypeSpec scalar `ObjectId` (`@pattern("^[A-Za-z][A-Za-z0-9_]*$")`) and
  the model `ObjectFrontmatter` (`id: ObjectId`, `title`, `type`, optional
  `object`, other keys admitted), emitted as `ObjectId.json` and
  `ObjectFrontmatter.json`.
- The `id` locator every object type shares, carrying
  `regex: ^([A-Za-z][A-Za-z0-9_]*)$`.
- Skeleton and fixture ids in underscore form (`entity_001`,
  `aggregate_root_001`, `nested_entity_001`, ...), and every reference to them. The rule is the object id rule of QSpec FR-154 (merged at
`ac06d5a`): QSL model intake refuses a model node whose artifact id is not an
object id, and refuses a reference to an id no admitted node carries, so both
the ids and the references to them are enforced at intake as well as here.

## Behavior

- The object id pattern SHALL be carried by `ObjectId` in `typespec/main.tsp`, and `ObjectFrontmatter.id` SHALL reference it.
- Every object type's `id` locator SHALL be the one shared locator: `from: frontmatter_field`, `path: [id]`, `required: true`, and a `regex` that anchors and captures exactly the `ObjectId` pattern.
- When an object artifact's id matches the pattern, Quire SHALL extract it unchanged.
- If an object artifact's id is present and does not match the pattern, then Quire SHALL refuse the artifact with one pattern-mismatch diagnostic that names the id value and the pattern. Known gap: today the locator yields no value and Quire reports `[<type>] required 'id' (frontmatter_field(id)) is missing`; `agent-ix/quire-rs#451` adds the pattern-mismatch diagnostic, and until it lands that criterion is an expected failure.
- Every skeleton and every positive and negative fixture SHALL carry an underscore id, and every row, prose line or test that names one SHALL name it in that form.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | `ObjectId.json` is a string schema with the pattern `^[A-Za-z][A-Za-z0-9_]*$`, `ObjectFrontmatter.json` requires `id`, `title` and `type` with `id` referencing `ObjectId.json`, and every object type's `id` locator is a required `frontmatter_field` whose `regex` is `^([A-Za-z][A-Za-z0-9_]*)$`. | Test |
| FR-009-AC-2 | `ObjectFrontmatter.json` accepts `order_line_001`, `nested_entity_001`, `Order` and `a1` and refuses `order-line-001`, `nested-entity_001`, `_order`, `1order` and the empty string; every skeleton and fixture frontmatter validates and carries no hyphen in its id. | Test |
| FR-009-AC-3 | Every skeleton reports no missing-id error through `validate_document`; the same skeleton with its id hyphenated is refused, today with only the missing-id error; the 0.2.0 `entity` skeleton (`entity-001`) is refused with exactly that one error. | Test |
| FR-009-AC-4 | A skeleton with its id hyphenated fails with exactly one error, which names the hyphenated id and the pattern and is not the missing-id error (expected failure while `agent-ix/quire-rs#451` is open). | Test |

## Dependencies

- **Upstream**: [FR-002](./FR-002-emitted-json-schemas.md); quire-rs locator `regex` on `frontmatter_field`; QSpec FR-154 object id rule (`ix://agent-ix/quire-specification/FR-154`, `ac06d5a`); `agent-ix/quire-rs#451` (pattern-mismatch diagnostic)
- **Constrains**: [NFR-001](../non-functional/NFR-001-additive-compatibility.md) (a hyphenated object id is a breaking refusal)
- **Downstream**: filament-core-data's extraction-frontend fixtures name object artifacts `DM-001`, `AR-001`, `EN-001`, `EV-001`, `NE-001`, `PR-001`, `RP-001`, `SM-001`, `VO-001`; pinning this version refuses each of them, so those ids and every reference to them become underscore ids and the fixture goldens are regenerated (`agent-ix/filament-core-data#175`)
