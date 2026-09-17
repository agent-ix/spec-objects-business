---
id: negative-012
title: "OrderLifecycleWithDanglingGuard"
type: state_machine
object: state_machine
expect: semantic.dangling-clause-ref
because: "a transition Guard names an invariant clause of the same artifact; NoSuchClause is not one"
---
# [negative-012] OrderLifecycleWithDanglingGuard

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
| Draft | Placed | place | NoSuchClause | |
