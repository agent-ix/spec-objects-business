---
id: negative-011
title: "OrderLifecycleWithUnknownTrigger"
type: state_machine
object: state_machine
expect: semantic.unknown-trigger
because: "a transition Trigger names an operation of the same artifact; archive is not one"
---
# [negative-011] OrderLifecycleWithUnknownTrigger

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
| Draft | Placed | archive | | |
