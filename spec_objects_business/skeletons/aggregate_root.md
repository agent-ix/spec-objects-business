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
     - Each invariant owns one `quire` fence holding a Quire expression.
     - "## Members" (H2, required): a `| Member | Multiplicity |` table naming
       every declaration inside the consistency boundary. Prose may follow
       the table; a list or diagram there is refused.
     - "## Relationships" (H2, optional): a `| Name | Verb | Target | Multiplicity |`
       table, one row per domain relationship. Verb is an `edge_types` verb
       this type's allowed_links admit, never an inverse label or
       `specializes`; Target is an artifact id; Multiplicity is required. -->
# [aggregate-root-001] Order

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| order_id | UUID | 1..1 | identity |
| customer_id | UUID | 1..1 | |
| status | OrderStatus | 1..1 | |
| lines | OrderLine | 0..* | |
| subtotal | Money | 1..1 | |
| shipping_fee | Money | 1..1 | |
| grand_total | Money | 1..1 | |
| placed_at | Timestamp | 0..1 | |

## Invariants

The clauses the Order declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### GrandTotalIsSubtotalPlusShippingFee

```quire
self.grand_total.amount_minor = self.subtotal.amount_minor + self.shipping_fee.amount_minor
```

### TotalsShareOneCurrency

```quire
self.subtotal.currency = self.grand_total.currency and self.shipping_fee.currency = self.grand_total.currency
```

### PlacedPaidShippedOrDeliveredOrderCarriesAtLeastOneLine

```quire
(self.status = OrderManagement::OrderStatus::Placed or self.status = OrderManagement::OrderStatus::Paid or self.status = OrderManagement::OrderStatus::Shipped or self.status = OrderManagement::OrderStatus::Delivered) implies size(self.lines) >= 1
```

### DraftOrderHasNoPlacementTime

```quire
self.status = OrderManagement::OrderStatus::Draft implies not present(self.placed_at)
```

## Members

| Member | Multiplicity |
|---|---|
| OrderLine | 0..* |
| Money | 3..3 |

All members share one transaction, so the aggregate is loaded and persisted
as a whole. Order is the only member addressable from outside the aggregate;
OrderLine instances are created, amended, and removed only through Order
operations, and the three Money values are recomputed whenever a line changes.

## Relationships

| Name | Verb | Target | Multiplicity |
|---|---|---|---|
| lines | aggregates | nested-entity-001 | 0..* |
| totals | contains | value-object-001 | 3..3 |
| status | references | enumeration-001 | 1..1 |
| placed | emits | event-001 | 0..1 |
