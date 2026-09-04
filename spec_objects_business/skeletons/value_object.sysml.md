---
id: value-object-001
title: "Money"
type: value_object
object: value_object
---
<!-- value_object authoring skeleton, alternate Properties form: exactly the
     fields of value_object.md as one ```sysml``` fence (FR-005-AC-2). -->
# [value-object-001] Money

## Properties

```sysml
attribute amount : Decimal(19,2)[1..1]
attribute currency : String[1..1] { minLength: 3, maxLength: 3 }
```

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
