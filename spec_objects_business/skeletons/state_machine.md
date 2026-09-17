---
id: state-machine-001
title: "OrderLifecycle"
type: state_machine
object: state_machine
---
<!-- state_machine authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: state_machine, object: state_machine.
     - "## Properties" (H2): the machine's context fields, in the same typed
       table form every other type uses.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning one
       `quire` fence that holds a Quire expression.
     - "## Operations" (H2, required by StateMachine.json): one `### <name>`
       per transition command, with `Requires:`/`Ensures:` lines naming
       clause ids declared in this artifact.
     - "## States" (H2, required): a `| State | Description |` table.
     - "## Transitions" (H2, required): a
       `| From | To | Trigger | Guard | Emits |` table. From/To name states,
       Trigger names an operation, Guard names an invariant clause.
     - Only the declared tables belong under States and Transitions; a
       diagram or list there is refused. -->
# [state-machine-001] OrderLifecycle

The Order aggregate moves through these states. Transitions are commands on
the aggregate root; every transition emits a corresponding domain event.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| order_id | UUID | 1..1 | |
| current_state | OrderStatus | 1..1 | |
| entered_state_at | Timestamp | 1..1 | |

## Invariants

The clauses the OrderLifecycle declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### CancelIsAllowedUntilCapture

```quire
self.current_state = "Draft" or self.current_state = "Placed"
```

### ShippedIsImmutable

```quire
self.current_state = "Shipped" implies present(self.entered_state_at)
```

## Operations

The operations the OrderLifecycle declaration exposes. Each operation owns one
`### <name>` heading with an optional parameter table, a `Returns:` line
where it returns a value, and `Requires:`/`Ensures:` lines where it names
clauses declared in this artifact.

### place

Convert a draft order into a binding purchase request.

Requires: CancelIsAllowedUntilCapture

### discard

Abandon a draft order before it is placed.

### capture_payment

Confirm payment for a placed order at the authorised amount.

### cancel

Cancel a placed order before payment capture succeeds.

Requires: CancelIsAllowedUntilCapture

### ship

Hand the paid order to the carrier.

Ensures: ShippedIsImmutable

### confirm_delivery

Record the carrier's delivery confirmation.

## States

| State | Description |
|---|---|
| Draft | The order is being assembled and binds nobody |
| Placed | The customer committed to the order |
| Paid | Payment was captured at the authorised amount |
| Shipped | The carrier holds the order |
| Delivered | The carrier confirmed delivery |
| Cancelled | The order ended before payment capture |

## Transitions

| From | To | Trigger | Guard | Emits |
|---|---|---|---|---|
| Draft | Placed | place | CancelIsAllowedUntilCapture | OrderPlaced |
| Draft | Cancelled | discard | | OrderDiscarded |
| Placed | Paid | capture_payment | | PaymentCaptured |
| Placed | Cancelled | cancel | CancelIsAllowedUntilCapture | OrderCancelled |
| Paid | Shipped | ship | | OrderShipped |
| Shipped | Delivered | confirm_delivery | | OrderDelivered |
