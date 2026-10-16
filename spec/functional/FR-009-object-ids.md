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

An object id SHALL be a letter followed by letters, digits and underscores, so
that an object id is one identifier token wherever it is named. A hyphen is
refused in object ids. A type-definition document whose frontmatter is governed
by this module uses the strict object-id pattern. An artifact document may also
declare an object body (for example, `type: FR; object: enumeration`); its
artifact archetype owns and validates the typed document id such as `FR-271`,
while this module contributes the object body contract. This artifact-level
acceptance does not establish that QSL admits the document as a type declaration.
When lifted into the QSL domain model, the document id supplies the IR type
identity's `<Name>` segment: `FR-271` therefore yields the name `FR-271`, which
QSpec FR-154 refuses because it contains a hyphen. QSpec FR-154 requires that IR `<Name>` segment to satisfy the
same object-id pattern before QSL admits a reference to it.

## Inputs

- `typespec/main.tsp`, emitted per [FR-002](./FR-002-emitted-json-schemas.md).
- The shared `id` locator of `manifest.yaml`.

## Outputs

- The TypeSpec model `ObjectFrontmatter` with a patterned string `id`,
  `title`, `type`, optional `object`, and other keys admitted, emitted as
  `ObjectFrontmatter.json`. Every object type references this schema.
- The shared `id` locator (`from: frontmatter_field`, `path: [id]`,
  `required: true`) preserves the id selected by the archetype-owned schema.
- Skeleton and fixture ids in underscore form (`entity_001`,
  `aggregate_root_001`, `nested_entity_001`, ...), and every reference to them.

## Behavior

- `ObjectFrontmatter.id` SHALL carry the pattern
  `^[A-Za-z][A-Za-z0-9_]*$`; each object type SHALL reference
  `ObjectFrontmatter.json` for standalone type-definition documents.
- Each object type's shared `id` locator SHALL be required and read the
  frontmatter `id` without imposing a second pattern.
- A standalone object type document SHALL refuse typed ids including
  `FR-271`, `fr-271`, `FR-`, `FRXYZ-1` and `ENT-001`. A typed artifact
  document with `object: enumeration` SHALL accept an id such as `FR-271`
  under its artifact archetype schema while applying the enumeration body
  contract.
- Every skeleton and every positive and negative fixture SHALL carry an underscore id, and every row, prose line or test that names one SHALL name it in that form.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | `ObjectFrontmatter.json` requires `id`, `title` and `type` with `id` carrying `^[A-Za-z][A-Za-z0-9_]*$`; every object type references that frontmatter schema and has a required `frontmatter_field` id locator with no locator regex. | Test |
| FR-009-AC-2 | `ObjectFrontmatter.json` accepts `order_line_001`, `nested_entity_001`, `Order` and `a1`; it refuses `FR-271`, `fr-271`, `FR-`, `FRXYZ-1`, `ENT-001`, `order-line-001`, `nested-entity_001`, `_order`, `1order` and the empty string; every skeleton and fixture frontmatter validates, and a composed `FR` artifact with `object: enumeration` accepts `FR-271`. | Test |
| FR-009-AC-3 | Every skeleton validates through `validate_document`; changing its `id` to a hyphenated value is refused by its frontmatter schema. | Test |

## Dependencies

- **Upstream**: [FR-002](./FR-002-emitted-json-schemas.md); quire-rs object-archetype frontmatter-schema validation; QSpec FR-154 object id rule (`ix://agent-ix/quire-specification/FR-154`)
- **Downstream**: object type-definition documents and references use underscore ids. A typed artifact document may keep its artifact id when its artifact archetype validates the frontmatter and this module contributes only the declared object body.
