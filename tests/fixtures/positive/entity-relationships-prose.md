---
id: positive-006
title: "ArchivedCustomer"
type: entity
object: entity
---
# [positive-006] ArchivedCustomer

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| customer_id | UUID | 1..1 | identity |

## Relationships

An archived customer keeps no live relationships; its orders are reached
through the order archive.
