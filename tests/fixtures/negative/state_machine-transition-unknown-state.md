---
id: negative-010
title: "OrderLifecycleWithUnknownState"
type: state_machine
object: state_machine
expect: semantic.unknown-state
because: "a transition From and To name rows of the States table; Archived is not one"
---
# [negative-010] OrderLifecycleWithUnknownState

## Invariants

### CancelIsAllowedUntilCapture

```quire
self.current_state = "Draft" or self.current_state = "Placed"
```

## Operations

### place

Convert a draft order into a binding purchase request.

## States

| State | Description |
|---|---|
| Draft | The order is being assembled |
| Placed | The customer committed to the order |

## Transitions

| From | To | Trigger | Guard | Emits |
|---|---|---|---|---|
| Placed | Archived | place | | |
