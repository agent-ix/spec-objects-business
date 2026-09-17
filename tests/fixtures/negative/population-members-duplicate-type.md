---
id: negative-019
title: "OrderPopulationWithDuplicateType"
type: population
object: population
expect: semantic.duplicate-model-entry
because: "each member Type is declared once; Order is declared twice"
---
# [negative-019] OrderPopulationWithDuplicateType

## Members

| Type | Extent |
|---|---|
| Order | 0..* |
| Order | 1..* |
