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
     - "## Invariants" (H2): one `### <clauseId>` per clause with one ```ocl```
       fence. -->
# [value-object-001] Money

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| amount | Decimal(19,2) | 1..1 | |
| currency | String | 1..1 | minLength: 3, maxLength: 3 |

## Invariants

The clauses the Money declaration enforces. Each clause owns one
`ocl` fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### CurrencyIsIso4217Alpha3

```ocl
context Money
inv CurrencyIsIso4217Alpha3:
  self.currency.size() = 3 and self.currency = self.currency.toUpperCase()
```

### ArithmeticIsSingleCurrency

```ocl
context Money
inv ArithmeticIsSingleCurrency:
  self.add(other) implies other.currency = self.currency
```
