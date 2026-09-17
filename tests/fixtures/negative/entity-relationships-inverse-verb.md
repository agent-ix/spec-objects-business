---
id: negative-022
title: "CustomerWithInverseVerb"
type: entity
object: entity
expect: semantic.invalid-model-cell
because: "part_of is the inverse label of contains and aggregates; the owning artifact declares the forward verb"
---
# [negative-022] CustomerWithInverseVerb

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| customer_id | UUID | 1..1 | identity |

## Relationships

| Name | Verb | Target | Multiplicity |
|---|---|---|---|
| order | part_of | aggregate-root-001 | 1..1 |
