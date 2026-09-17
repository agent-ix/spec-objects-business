---
id: negative-026
title: "CustomerWithRelationshipList"
type: entity
object: entity
expect: semantic.feature-not-extractable
because: "relationships are declared only as the Name | Verb | Target | Multiplicity table; a bullet list is refused"
---
# [negative-026] CustomerWithRelationshipList

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| customer_id | UUID | 1..1 | identity |

## Relationships

- lifecycle: owns state-machine-001
