---
id: event_001
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
# [event_001] OrderPlaced

OrderPlaced is published by the Order aggregate when a draft order is placed.
It is the integration contract consumed by Inventory (stock reservation),
Payments (capture), and Notifications (order confirmation).

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| occurred_at | Timestamp | 1..1 | |
| order_id | UUID | 1..1 | |
| customer_id | UUID | 1..1 | |
| line_count | Integer | 1..1 | min: 1, max: 1000 |
| subtotal | Money | 1..1 | |
| shipping_fee | Money | 1..1 | |
| grand_total | Money | 1..1 | |

## Invariants

The clauses the OrderPlaced declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### GrandTotalIsSubtotalPlusShippingFee

```quire
self.grand_total.amount_minor = self.subtotal.amount_minor + self.shipping_fee.amount_minor
```

### TotalsShareOneCurrency

```quire
self.subtotal.currency = self.grand_total.currency and self.shipping_fee.currency = self.grand_total.currency
```

## Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://specs.agent-ix.dev/events/order-placed.schema.json",
  "title": "OrderPlaced",
  "type": "object",
  "required": ["occurred_at", "order_id", "customer_id", "line_count", "subtotal", "shipping_fee", "grand_total"],
  "properties": {
    "occurred_at": { "type": "string", "format": "date-time" },
    "order_id": { "type": "string", "format": "uuid" },
    "customer_id": { "type": "string", "format": "uuid" },
    "line_count": { "type": "integer", "minimum": 1, "maximum": 1000 },
    "subtotal": {
      "type": "object",
      "required": ["amount_minor", "currency"],
      "properties": {
        "amount_minor": { "type": "integer", "minimum": 0, "maximum": 1000000000000 },
        "currency": { "type": "string", "minLength": 3, "maxLength": 3 }
      }
    },
    "shipping_fee": {
      "type": "object",
      "required": ["amount_minor", "currency"],
      "properties": {
        "amount_minor": { "type": "integer", "minimum": 0, "maximum": 1000000000000 },
        "currency": { "type": "string", "minLength": 3, "maxLength": 3 }
      }
    },
    "grand_total": {
      "type": "object",
      "required": ["amount_minor", "currency"],
      "properties": {
        "amount_minor": { "type": "integer", "minimum": 0, "maximum": 1000000000000 },
        "currency": { "type": "string", "minLength": 3, "maxLength": 3 }
      }
    }
  }
}
```
