---
id: event-001
title: "OrderPlaced"
type: event
object: event
---
<!-- event authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: event, object: event.
     - "## Properties" (H2): the declared payload as typed rows. An event
       declaration carries NO identity field (occurrence identity belongs to
       the runtime record) and at least one `Timestamp` occurrence field —
       Event.json refuses a record that breaks either rule.
     - "## Invariants" (H2): one `### <clauseId>` per clause.
     - "## Schema" (H2, required) holds a fenced `json` block. It is a
       derived, human-facing view of the declared payload; the typed table
       above is the authority. -->
# [event-001] OrderPlaced

OrderPlaced is published by the Order aggregate when a draft order is placed.
It is the integration contract consumed by Inventory (stock reservation),
Payments (capture), and Notifications (order confirmation).

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| occurred_at | Timestamp | 1..1 | |
| order_id | UUID | 1..1 | |
| customer_id | UUID | 1..1 | |
| line_count | Integer | 1..1 | min: 1 |
| grand_total | Money | 1..1 | |

## Invariants

The clauses the OrderPlaced declaration enforces. Each clause owns one
`ocl` fence under its own `### <clauseId>` heading; the fence text is carried
verbatim and never evaluated here.

### LineCountMatchesTheOrder

```ocl
context OrderPlaced
inv LineCountMatchesTheOrder:
  self.line_count = Order.allInstances()->any(o | o.order_id = self.order_id).lines->size()
```

### OccurredAtIsNotInTheFuture

```ocl
context OrderPlaced
inv OccurredAtIsNotInTheFuture:
  self.occurred_at <= now()
```

## Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://specs.agent-ix.dev/events/order-placed.schema.json",
  "title": "OrderPlaced",
  "type": "object",
  "required": ["occurred_at", "order_id", "customer_id", "line_count", "grand_total"],
  "properties": {
    "occurred_at": { "type": "string", "format": "date-time" },
    "order_id": { "type": "string", "format": "uuid" },
    "customer_id": { "type": "string", "format": "uuid" },
    "line_count": { "type": "integer", "minimum": 1 },
    "grand_total": {
      "type": "object",
      "required": ["amount", "currency"],
      "properties": {
        "amount": { "type": "string", "pattern": "^-?\\d+\\.\\d{2}$" },
        "currency": { "type": "string", "minLength": 3, "maxLength": 3 }
      }
    }
  }
}
```
