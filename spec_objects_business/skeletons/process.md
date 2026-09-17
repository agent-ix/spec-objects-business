---
id: process-001
title: "OrderFulfilment"
type: process
object: process
---
<!-- process authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: process, object: process.
     - "## Properties" (H2): the process's typed fields; at least one carries
       `identity` — the correlation key that ties every step to one run.
     - "## Invariants" (H2): one `### <clauseId>` per clause, each owning one
       `quire` fence holding a Quire expression.
     - "## Workflow" (H2, required): a
       `| Step | Kind | Consumes | Emits | Description |` table. Kind is one
       of command, event, decision, compensation, wait.
     - "## States" (H2, optional): a `| State | Description |` table.
     - Only the declared tables belong under Workflow and States; a diagram
       or list there is refused.
     - "## Specification" and "## Algorithm" (H2) are optional prose. -->
# [process-001] OrderFulfilment

OrderFulfilment is the long-running process that turns a placed order into a
shipped one. It reacts to OrderPlaced and coordinates Inventory, Payments,
and the warehouse.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| correlation_id | UUID | 1..1 | identity |
| order_id | UUID | 1..1 | |
| started_at | Timestamp | 1..1 | |
| reservation_deadline | Duration | 1..1 | |
| stock_refused | Boolean | 1..1 | |
| capture_failed | Boolean | 1..1 | |
| compensated | Boolean | 1..1 | |

## Invariants

The clauses the OrderFulfilment declaration enforces. Each clause owns one
`quire` fence under its own `### <clauseId>` heading.

### CompensationFollowsARefusedReservationOrAFailedCapture

```quire
self.compensated implies (self.stock_refused or self.capture_failed)
```

### CaptureIsNotAttemptedAfterAStockRefusal

```quire
self.stock_refused implies not self.capture_failed
```

## Workflow

| Step | Kind | Consumes | Emits | Description |
|---|---|---|---|---|
| receive_order | event | OrderPlaced | | Start a run keyed by a fresh correlation id |
| reserve_stock | command | | | Ask Inventory to reserve stock for every line |
| stock_reserved | decision | | | Continue to payment, or record the refusal and compensate |
| capture_payment | command | | | Ask Payments to capture the grand total |
| payment_captured | decision | | | Continue to the warehouse, or record the failure and compensate |
| release_reservation | compensation | | | Release the stock reservation and cancel the order |
| release_to_warehouse | command | | | Hand the order to the warehouse to pick and pack |
| await_shipment | wait | | | Wait for the carrier to confirm the hand-over |

## States

| State | Description |
|---|---|
| Reserving | Stock is being reserved for every line |
| Capturing | Payment is being captured |
| Fulfilling | The warehouse holds the order |
| Compensating | A failed step is being undone |

## Specification

The process is correlated by `correlation_id` and is idempotent per
`order_id`: a duplicate OrderPlaced for an order already in flight is
discarded. `reservation_deadline` bounds how long stock may be held before
the run compensates.

## Algorithm

1. On OrderPlaced, start a run keyed by a fresh `correlation_id`.
2. Reserve stock for every line; on refusal, set `stock_refused`, compensate
   and cancel the order.
3. Capture payment for `grand_total`; on decline, set `capture_failed` and
   release the reservation.
4. Release the order to the warehouse and wait for the shipment confirmation.
5. Close the run once the carrier confirms the hand-over.
