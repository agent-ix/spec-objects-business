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
| amount | Decimal(19,2) | 1..1 | |
| currency | String | 1..1 | minLength: 3, maxLength: 3 |

## Invariants

The clauses the Money declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### CurrencyIsIso4217Alpha3

```quire
size(self.currency) = 3
```

### ArithmeticIsSingleCurrency

```quire
present(self.amount) implies present(self.currency)
```
