---
id: negative-021
title: "CustomerWithUnknownVerb"
type: entity
object: entity
expect: semantic.invalid-model-cell
because: "a Verb is an edge_types verb; places is not declared"
---
# [negative-021] CustomerWithUnknownVerb

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| customer_id | UUID | 1..1 | identity |

## Relationships

| Name | Verb | Target | Multiplicity |
|---|---|---|---|
| orders | places | aggregate-root-001 | 0..* |
