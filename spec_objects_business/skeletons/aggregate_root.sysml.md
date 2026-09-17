---
id: aggregate-root-001
title: "Order"
type: aggregate_root
object: aggregate_root
---
<!-- aggregate_root authoring skeleton, alternate Properties form: exactly the
     fields of aggregate_root.md as one ```sysml``` fence (FR-005-AC-2). -->
# [aggregate-root-001] Order

## Properties

```sysml
attribute order_id : UUID[1..1] { identity }
attribute customer_id : UUID[1..1]
ref item status : OrderStatus[1..1]
ref item subtotal : Money[1..1]
ref item shipping_fee : Money[1..1]
ref item grand_total : Money[1..1]
attribute placed_at : Timestamp[0..1]
```

## Invariants

The clauses the Order declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### GrandTotalIsSubtotalPlusShipping

```quire
self.grand_total.amount = self.subtotal.amount + self.shipping_fee.amount
```

### PlacedOrderCarriesAtLeastOneLine

```quire
self.status != "Draft" implies size(self.lines) >= 1
```

### LinesAreAmendedOnlyWhileDraft

```quire
exists(l in self.lines: l.amended) implies self.status = "Draft"
```

## Members

| Member | Multiplicity |
|---|---|
| OrderLine | 1..* |
| Money | 3..3 |
