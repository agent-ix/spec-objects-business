---
id: negative-009
title: "OrderLifecycleWithStateDiagram"
type: state_machine
object: state_machine
expect: semantic.feature-not-extractable
because: "the States section holds only the declared State table; a mermaid diagram there is a form the manifest does not declare"
---
# [negative-009] OrderLifecycleWithStateDiagram

## Invariants

### CancelIsAllowedUntilCapture

```quire
self.current_state = "Draft" or self.current_state = "Placed"
```

## Operations

### place

Convert a draft order into a binding purchase request.

## States

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Placed: place
```

## Transitions

| From | To | Trigger | Guard | Emits |
|---|---|---|---|---|
| Draft | Placed | place | | OrderPlaced |
