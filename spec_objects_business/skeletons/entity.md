---
id: entity-001
title: "Customer"
type: entity
object: entity
---
<!-- entity authoring skeleton (spec-objects-business). Fill every section with
     substantive content. Contract (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: entity, object: entity.
     - "## Properties" (H2, required): one typed row per attribute, header
       exactly `Field | Type | Multiplicity | Constraints`. At least one row
       carries the `identity` constraint.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning
       exactly one ```quire``` fence holding a Quire expression. -->
# [entity-001] Customer

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| customer_id | UUID | 1..1 | identity |
| email | String | 1..1 | minLength: 3, maxLength: 254 |
| display_name | String | 1..1 | minLength: 1 |
| default_shipping_address | Money | 0..1 | |
| status | OrderStatus | 1..1 | |
| registered_at | Timestamp | 1..1 | |

## Invariants

The clauses the Customer declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### EmailIsVerifiedBeforeFirstOrder

```quire
self.status = "Draft" or size(self.email) >= 3
```

### SuspendedCustomerPlacesNoOrder

```quire
self.status = "Cancelled" implies present(self.registered_at)
```
