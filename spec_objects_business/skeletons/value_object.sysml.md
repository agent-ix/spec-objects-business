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
attribute amount_minor : Integer[1..1] { min: 0, max: 1000000000000 }
attribute currency : String[1..1] { minLength: 3, maxLength: 3 }
```

## Invariants

The clauses the Money declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### AmountMinorIsNonNegative

```quire
self.amount_minor >= 0
```
