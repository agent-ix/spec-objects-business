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
`ocl` fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### GrandTotalIsSubtotalPlusShipping

```ocl
context Order
inv GrandTotalIsSubtotalPlusShipping:
  self.grand_total = self.subtotal.add(self.shipping_fee)
```

### PlacedOrderCarriesAtLeastOneLine

```ocl
context Order
inv PlacedOrderCarriesAtLeastOneLine:
  self.status <> OrderStatus::Draft implies self.lines->size() >= 1
```

### LinesAreAmendedOnlyWhileDraft

```ocl
context Order
inv LinesAreAmendedOnlyWhileDraft:
  self.lines->exists(l | l.isDirty()) implies self.status = OrderStatus::Draft
```

## Members

- **Order** (root) — identified by `order_id`; the only member addressable
  from outside the aggregate.
- **OrderLine** (nested entity, 1..n) — created, amended, and removed only
  through Order methods.
- **Money: subtotal, shipping_fee, grand_total** (owned value objects).
- **ShippingAddress** (owned value object) — frozen when the order is placed.
