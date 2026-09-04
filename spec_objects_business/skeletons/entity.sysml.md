---
id: entity-001
title: "Customer"
type: entity
object: entity
---
<!-- entity authoring skeleton, alternate Properties form. Declares exactly the
     same fields as entity.md, authored as one ```sysml``` fence instead of the
     typed table (FR-005-AC-2). One artifact carries one form; the alternate is
     a separate file, never a second block in the same artifact. -->
# [entity-001] Customer

## Properties

```sysml
attribute customer_id : UUID[1..1] { identity }
attribute email : String[1..1] { minLength: 3, maxLength: 254 }
attribute display_name : String[1..1] { minLength: 1 }
ref item default_shipping_address : Money[0..1]
ref item status : OrderStatus[1..1]
attribute registered_at : Timestamp[1..1]
```

## Invariants

The clauses the Customer declaration enforces. Each clause owns one
`ocl` fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### EmailIsVerifiedBeforeFirstOrder

```ocl
context Customer
inv EmailIsVerifiedBeforeFirstOrder:
  self.status <> OrderStatus::Placed or self.email->notEmpty()
```

### SuspendedCustomerPlacesNoOrder

```ocl
context Customer
inv SuspendedCustomerPlacesNoOrder:
  self.status = OrderStatus::Cancelled implies self.orders->forAll(o | o.placedAt < self.registeredAt)
```
