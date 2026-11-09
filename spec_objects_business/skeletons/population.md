---
id: population_001
title: "OrderPopulation"
type: population
object: population
extent: closed
---
<!-- population authoring skeleton (spec-objects-business). Contract:
     - Frontmatter MUST carry id, title, type: population, object: population,
       and `extent: closed` or `extent: open` (the one extent of the whole
       population: closed fixes its membership, open lets it grow).
     - "## Members" (H2, required): a `| Type |` table with at least one row.
       Type names a declared type; members carry no multiplicity. Each Type
       appears once; a list there is refused, and so is the retired
       `| Type | Extent |` table.
     - "## Invariants" (H2, optional): one `### <clauseId>` per clause, each
       owning one `quire` fence holding a Quire expression.
     A population declares which instances exist together, not data:
     Population.json forbids `fields` and `operations`, so there is no
     "## Properties" and no "## Operations" section. -->
# [population_001] OrderPopulation

OrderPopulation is the set of instances the OrderManagement context holds at
one time: orders, the customers who place them, and their fulfilments.

## Members

| Type |
|---|
| Order |
| Customer |
| OrderFulfilment |
