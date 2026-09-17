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
ref item lines : OrderLine[0..*]
ref item subtotal : Money[1..1]
ref item shipping_fee : Money[1..1]
ref item grand_total : Money[1..1]
attribute placed_at : Timestamp[0..1]
```

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
