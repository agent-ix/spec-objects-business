---
id: negative-014
title: "OrderWithMemberList"
type: aggregate_root
object: aggregate_root
expect: semantic.feature-not-extractable
because: "the Members section holds only the declared Member table; a bullet list there is a form the manifest does not declare"
---
# [negative-014] OrderWithMemberList

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| order_id | UUID | 1..1 | identity |

## Invariants

### PlacedOrderCarriesAtLeastOneLine

```quire
self.status != "Draft" implies size(self.lines) >= 1
```

## Members

- OrderLine 1..*
- Money 3..3
