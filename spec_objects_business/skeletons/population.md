---
id: population-001
title: "OrderPopulation"
type: population
object: population
---
<!-- population authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: population, object: population.
     - "## Members" (H2, required): a `| Type | Extent |` table with at least
       one row. Type names a declared type; Extent is the multiplicity of its
       instances in the population. Each Type appears once; a list there is
       refused.
     - "## Invariants" (H2, optional): one `### <clauseId>` per clause, each
       owning one `quire` fence holding a Quire expression.
     A population declares which instances exist together, not data:
     Population.json forbids `fields` and `operations`, so there is no
     "## Properties" and no "## Operations" section. -->
# [population-001] OrderPopulation

OrderPopulation is the set of instances the OrderManagement context holds at
one time: any number of orders, each placed by one of at least one customer.

## Members

| Type | Extent |
|---|---|
| Order | 0..* |
| Customer | 1..* |
| OrderFulfilment | 0..* |
