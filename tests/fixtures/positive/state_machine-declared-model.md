---
id: positive-001
title: "ReturnLifecycle"
type: state_machine
object: state_machine
relationships:
  - type: specializes
    target: OrderLifecycle
abstract: true
---
# [positive-001] ReturnLifecycle

A return reuses the order lifecycle's context and declares its own states,
transitions, and operation frames.

## Properties

| Field | Type | Multiplicity | Constraints | Presence | Subsets | Redefines |
|---|---|---|---|---|---|---|
| order_id | UUID | 1..1 | identity | required | | |
| items | String | 0..* | | | | |
| returned_items | String | 0..* | | | items | |
| current_state | OrderStatus | 1..1 | | required | | current_state |
| reason | String | 0..1 | | optional | | |

## Invariants

### ReturnIsOpen

```quire
self.current_state = "Requested"
```

### ReturnIsSettled

```quire
self.current_state = "Refunded" implies size(self.returned_items) >= 1
```

## Operations

### refund

Refund the returned items.

Requires: ReturnIsOpen
Ensures: ReturnIsSettled
Modifies: self.current_state, self.returned_items
Creates: Refund
Deletes: self.items

## States

| State | Description |
|---|---|
| Requested | The customer asked to return items |
| Refunded | The refund was issued |

## Transitions

| From | To | Trigger | Guard | Emits |
|---|---|---|---|---|
| Requested | Refunded | refund | ReturnIsOpen | ReturnRefunded |
