---
id: entity_001
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
# [entity_001] Customer

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| customer_id | UUID | 1..1 | identity |
| email | String | 1..1 | minLength: 3, maxLength: 254 |
| email_verified | Boolean | 1..1 | |
| display_name | String | 1..1 | minLength: 1 |
| registered_at | Timestamp | 1..1 | |
| first_order_placed_at | Timestamp | 0..1 | |
| suspended | Boolean | 1..1 | |
| suspended_at | Timestamp | 0..1 | |

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
