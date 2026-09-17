---
id: nested_entity_001
title: "OrderLine"
type: nested_entity
object: nested_entity
---
<!-- nested_entity authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: nested_entity, object: nested_entity.
     - "## Properties" (H2): typed fields; at least one carries `identity`,
       and that identity is local to the owner — a rule the schema cannot
       express and the reader does not check.
     - "## Invariants" (H2): one `### <clauseId>` per clause.
     - "## Parent" (H2, required): the owning aggregate root and how it
       mediates every mutation. Derived view; `owner` is the typed key. -->
# [nested_entity_001] OrderLine

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| line_number | Integer | 1..1 | identity, min: 1, max: 1000 |
| product_id | UUID | 1..1 | |
| quantity | Integer | 1..1 | min: 1, max: 10000 |
| unit_price | Money | 1..1 | |
| line_total | Money | 1..1 | |

## Invariants

The clauses the OrderLine declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### LineTotalIsQuantityTimesUnitPrice

```quire
self.line_total.amount_minor = self.quantity * self.unit_price.amount_minor
```

### LineTotalIsInTheUnitPriceCurrency

```quire
self.line_total.currency = self.unit_price.currency
```

## Parent

OrderLine belongs to the **Order** aggregate root (`aggregate_root_001`). An
order line is identified by `line_number`, which is unique only within its
parent order — there is no global OrderLine identity and no repository for
order lines. External callers reference a line as the pair
(`order_id`, `line_number`). All lifecycle operations go through the parent:
`Order.add_line(product_id, quantity, unit_price)`,
`Order.change_quantity(line_number, quantity)`, and
`Order.remove_line(line_number)`. The parent recomputes its totals and
re-checks its invariants on every line mutation, and deleting the Order
deletes its lines with it.
