---
id: StR-001
title: "Tier-2 business objects"
type: StR
---
# StR-001: Tier-2 business objects

## Stakeholder Need

The Filament platform, spec authors, and agent CLI generators require that the
module **SHALL** make DDD-driven specifications yield extractable graph entities
for domains, entities, value objects, aggregates, repositories, events,
processes, and state machines, each carrying a structural contract a consumer
can read without reading the prose. The need is stated from the perspective of
those consumers and avoids prescribing a specific encoding.

## Rationale

DDD modelling has no first-class representation in the spec graph today, so
domain concepts cannot be discovered, traced, or generated against. Shipping a
tier-2 business object module gives authors and agent generators a shared,
extractable vocabulary for the principal DDD building blocks, which is why the
need exists.

## Validation Criteria


| ID | Criteria | Validation |
|----|----------|------------|
| StR-001-VC-1 | A Module activation against `filament-core` registers the contents this module declares. | Demonstration |
| StR-001-VC-2 | Spec authors and agent generators can produce artifacts that validate against the skeletons and schemas this module ships. | Demonstration |
| StR-001-VC-3 | Every business object type carries one typed structural contract that the downstream frontends (`agent-ix/quire-contract-ir#52`, `agent-ix/filament-core-data#36`) can consume read-only, so an entity and an enumeration are distinguishable to a consumer without reading the prose. | Demonstration |

Satisfaction is judged by demonstrating the first two outcomes against a
running `filament-core` instance with this module's manifest, and the third
against the shipped schemas and skeletons read as fixtures.

## Dependencies

**Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) (Module Manifest Schema).
**Downstream**: agent CLI generators and editors that consume this module's
declared ObjectTypes, templates, and schemas.
