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
attribute email_verified : Boolean[1..1]
attribute display_name : String[1..1] { minLength: 1 }
attribute registered_at : Timestamp[1..1]
attribute first_order_placed_at : Timestamp[0..1]
attribute suspended : Boolean[1..1]
attribute suspended_at : Timestamp[0..1]
```

## Invariants

The clauses the Customer declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### CustomerWithAPlacedOrderHasAVerifiedEmail

```quire
present(self.first_order_placed_at) implies self.email_verified
```

### SuspensionTimeIsRecordedExactlyWhenSuspended

```quire
self.suspended = present(self.suspended_at)
```
