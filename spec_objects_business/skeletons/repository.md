---
id: repository_001
title: "OrderRepository"
type: repository
object: repository
---
<!-- repository authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: repository, object: repository.
     - "## Operations" (H2, required): one `### <name>` per operation, an
       optional `| Param | Type | Multiplicity | Constraints |` table, a
       `Returns:` line where the operation returns a value, and optional
       `Pre:`/`Post:` lines naming clause ids declared in the same
       artifact. This skeleton declares no clauses, so it writes no
       Pre:/Post: lines.
     A repository declares no data of its own: Repository.json forbids
     `fields`, so there is no "## Properties" section. -->
# [repository_001] OrderRepository

## Operations

The operations the OrderRepository declaration exposes. Each operation owns one
`### <name>` heading with an optional parameter table, a `Returns:` line
where it returns a value, and `Pre:`/`Post:` lines where it names clauses
declared in this artifact.

### get

Load the full Order aggregate (root plus all order lines) in one consistent
read; raises `OrderNotFound` when no order carries that id.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| order_id | UUID | 1..1 | |

Returns: Order[1..1]

### save

Persist the whole aggregate atomically using optimistic concurrency on the
order's version; raises `ConcurrentModification` when the stored version has
advanced.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| order | Order | 1..1 | |

### next_identity

Allocate a new unique order id without touching any aggregate state.

Returns: UUID[1..1]

### find_by_customer

Return read-only summaries for the customer's orders, newest first; never
returns partially hydrated aggregates.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| customer_id | UUID | 1..1 | |
| page | Integer | 1..1 | min: 1 |

Returns: Order[0..* ordered]
