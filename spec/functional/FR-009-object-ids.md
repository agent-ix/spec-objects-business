---
id: FR-009
title: "Admit segmented document ids in object frontmatter"
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
# FR-009: Admit segmented document ids in object frontmatter

## Description

The object frontmatter `id` SHALL accept a document id beginning with a letter
and optionally containing hyphen-separated segments of letters, digits and
underscores. This admits QSpec artifact ids such as `DOM-001`, `SM-001`,
`PROC-001` and `VO-001` in standalone object documents as well as composed
artifact documents. A composed document's artifact archetype still owns its
frontmatter validation; this module contributes the object body contract.

The frontmatter id is a document key, not a semantic identifier. This module
does not change `semantic-core`'s `Identifier` or `TypeRef` constraints. A
frontmatter id that contains a hyphen therefore does not by itself establish
that the same string is admissible as a QSL IR `<Name>` or a TypeRef target.

## Inputs

- `typespec/main.tsp`, emitted per [FR-002](./FR-002-emitted-json-schemas.md).
- The shared `id` locator of `manifest.yaml`.

## Outputs

- The TypeSpec model `ObjectFrontmatter` with a patterned string `id`,
  `title`, `type`, optional `object`, and other keys admitted, emitted as
  `ObjectFrontmatter.json`. Every object type references this schema.
- The shared `id` locator (`from: frontmatter_field`, `path: [id]`,
  `required: true`) preserves the id selected by the archetype-owned schema.
- Existing skeleton and fixture ids in underscore form (`entity_001`,
  `aggregate_root_001`, `nested_entity_001`, ...), which remain valid.

## Behavior

- `ObjectFrontmatter.id` SHALL carry the pattern
  `^[A-Za-z][A-Za-z0-9_]*(?:-[A-Za-z0-9_]+)*$`; each object type SHALL reference
  `ObjectFrontmatter.json` for standalone type-definition documents.
- Each object type's shared `id` locator SHALL be required and read the
  frontmatter `id` without imposing a second pattern.
- A standalone object type document SHALL admit `FR-271`, `DOM-001`,
  `SM-001`, `PROC-001` and `VO-001`; it SHALL refuse a leading, repeated or
  trailing hyphen and an id beginning with a digit or underscore.
- A typed artifact document with `object: enumeration` SHALL continue to
  accept `FR-271` under its artifact archetype schema while applying the
  enumeration body contract.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | `ObjectFrontmatter.json` requires `id`, `title` and `type` with `id` carrying `^[A-Za-z][A-Za-z0-9_]*(?:-[A-Za-z0-9_]+)*$`; every object type references that frontmatter schema and has a required `frontmatter_field` id locator with no locator regex. | Test |
| FR-009-AC-2 | `ObjectFrontmatter.json` accepts underscore ids and `FR-271`, `DOM-001`, `SM-001`, `PROC-001`, `VO-001`; it refuses malformed ids with leading, repeated or trailing hyphens, whitespace, slash, or a non-letter first character; every skeleton and fixture frontmatter validates, and a composed `FR` artifact with `object: enumeration` accepts `FR-271` for Quire validation. | Test |
| FR-009-AC-3 | Every skeleton validates through `validate_document`; changing its `id` to a well-formed hyphenated value still validates, while a repeated hyphen is refused by its frontmatter schema. | Test |

## Dependencies

- **Upstream**: [FR-002](./FR-002-emitted-json-schemas.md); quire-rs object-archetype frontmatter-schema validation; QSpec FR-154 object id rule (`ix://agent-ix/quire-specification/FR-154`)
- **Downstream**: QSpec artifact documents with `object:` may retain their hyphenated document ids. Semantic IR names and TypeRef targets remain governed by their own identifier constraints.
