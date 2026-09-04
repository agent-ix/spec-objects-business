---
id: aggregate-root-001
title: "Order"
type: aggregate_root
object: aggregate_root
---
<!-- aggregate_root authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: aggregate_root, object: aggregate_root.
     - "## Properties" (H2): the root's own typed fields, at least one
       carrying `identity`.
     - "## Invariants" (H2, required by AggregateRoot.json's `clauses`): the
       root exists to enforce invariants, so it declares at least one.
     - "## Members" (H2, required): everything inside the consistency
       boundary. It is a derived, human-facing view of the same facts the
       typed sections declare; the typed sections are the authority. -->
# [aggregate-root-001] Order

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| order_id | UUID | 1..1 | identity |
| customer_id | UUID | 1..1 | |
| status | OrderStatus | 1..1 | |
| subtotal | Money | 1..1 | |
| shipping_fee | Money | 1..1 | |
| grand_total | Money | 1..1 | |
| placed_at | Timestamp | 0..1 | |

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
  from outside the aggregate and the single entry point for all mutations.
- **OrderLine** (nested entity, 1..n) — one per purchased product, identified
  by `line_number` local to the order; created, amended, and removed only
  through Order methods.
- **Money: subtotal, shipping_fee, grand_total** (owned value objects) —
  recomputed by the root whenever a line changes.
- **ShippingAddress** (owned value object) — frozen at the moment the order
  is placed.

All members share one transaction, so the aggregate is loaded and persisted
as a whole. The invariants this boundary enforces are declared above under
`## Invariants`, which is their authority; this section is the human-facing
view of the boundary.
