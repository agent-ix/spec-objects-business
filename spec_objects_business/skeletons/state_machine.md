---
id: state_machine_001
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
       per transition command, with `Pre:`/`Post:` lines naming
       clause ids declared in this artifact.
     - "## States" (H2, required): a `| State | Description |` table.
     - "## Transitions" (H2, required): a
       `| From | To | Trigger | Guard | Emits |` table. From/To name states,
       Trigger names an operation, Guard names an invariant clause.
     - Only the declared tables belong under States and Transitions; a
       diagram or list there is refused. -->
# [state_machine_001] OrderLifecycle

The Order aggregate moves through these states. Transitions are commands on
the aggregate root. Placing an order publishes OrderPlaced. Cancellation is
allowed only from Draft and Placed: the Transitions table declares no
`cancel` or `discard` row from any later state.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| order_id | UUID | 1..1 | |
| current_state | OrderStatus | 1..1 | |
| entered_state_at | Timestamp | 1..1 | |
| placed_at | Timestamp | 0..1 | |

## Invariants

The clauses the OrderLifecycle declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### DraftOrderHasNoPlacementTime

```quire
self.current_state = OrderManagement::OrderStatus::Draft implies not present(self.placed_at)
```

### OrderPastPlacementRecordsItsPlacementTime

```quire
(self.current_state = OrderManagement::OrderStatus::Placed or self.current_state = OrderManagement::OrderStatus::Paid or self.current_state = OrderManagement::OrderStatus::Shipped or self.current_state = OrderManagement::OrderStatus::Delivered) implies present(self.placed_at)
```

## Operations

The operations the OrderLifecycle declaration exposes. Each operation owns one
`### <name>` heading with an optional parameter table, a `Returns:` line
where it returns a value, and `Pre:`/`Post:` lines where it names
clauses declared in this artifact.

### place

Convert a draft order into a binding purchase request.

Post: OrderPastPlacementRecordsItsPlacementTime

### discard

Abandon a draft order before it is placed.

### capture_payment

Confirm payment for a placed order at the authorised amount.

### cancel

Cancel a placed order before payment capture succeeds.

### ship

Hand the paid order to the carrier.

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
| Draft | Placed | place | | OrderPlaced |
| Draft | Cancelled | discard | | |
| Placed | Paid | capture_payment | | |
| Placed | Cancelled | cancel | | |
| Paid | Shipped | ship | | |
| Shipped | Delivered | confirm_delivery | | |
