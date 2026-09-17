---
id: enumeration_001
title: "OrderStatus"
type: enumeration
object: enumeration
---
<!-- enumeration authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: enumeration, object: enumeration.
     - "## Values" (H2, required) is a `Value | Description` table with at
       least one row. The `values` locator declares it, and the engine
       reads each row as one enumeration value; a list there is refused.
     An enumeration declares labels, not data: Enumeration.json forbids
     `fields` and `operations`, so there is no "## Properties" section and no
     "## Invariants". -->
# [enumeration_001] OrderStatus

## Values

| Value | Description |
|---|---|
| Draft | The order is being assembled and its lines may still be amended. |
| Placed | The order is a binding purchase request awaiting payment capture. |
| Paid | Payment has been captured at the authorised amount. |
| Shipped | The order has been handed to the carrier and is immutable. |
| Delivered | The carrier has confirmed delivery to the customer. |
| Cancelled | The order was abandoned or cancelled before capture succeeded. |
