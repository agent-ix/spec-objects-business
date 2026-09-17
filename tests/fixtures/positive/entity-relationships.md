---
id: positive-004
title: "CustomerAccount"
type: entity
object: entity
---
# [positive-004] CustomerAccount

A customer account with one relationship row per verb an entity admits.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| account_id | UUID | 1..1 | identity |
| balance | Money | 1..1 | |

## Relationships

| Name | Verb | Target | Multiplicity |
|---|---|---|---|
| balance | contains | value-object-001 | 1..1 |
| lifecycle | owns | state-machine-001 | 1..1 |
| last_order | references | aggregate-root-001 | 0..1 |
| referrer | references | positive-004 | 0..1 |
