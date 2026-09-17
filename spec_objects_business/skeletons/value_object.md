---
id: value-object-001
title: "Money"
type: value_object
object: value_object
---
<!-- value_object authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: value_object, object: value_object.
     - "## Properties" (H2, required): the immutable components of the value,
       header exactly `Field | Type | Multiplicity | Constraints`. A value
       object has no identity of its own, so NO row carries `identity`
       (ValueObject.json refuses one).
     - "## Invariants" (H2): one `### <clauseId>` per clause with one ```quire```
       fence holding a Quire expression. -->
# [value-object-001] Money

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| amount_minor | Integer | 1..1 | min: 0, max: 1000000000000 |
| currency | String | 1..1 | minLength: 3, maxLength: 3 |

## Invariants

The clauses the Money declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### AmountMinorIsNonNegative

```quire
self.amount_minor >= 0
```
