---
id: positive-007
title: "LegacyCustomer"
type: entity
object: entity
---
# [positive-007] LegacyCustomer

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| customer_id | UUID | 1..1 | identity |

## Relationships

| Name | Verb | Target | Multiplicity |
|---|---|---|---|
| last_order | references | aggregate-root-999 | 0..1 |
