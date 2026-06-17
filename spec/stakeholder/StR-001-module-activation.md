---
id: StR-001
title: "Tier-2 business objects"
type: StR
---
# [StR-001] Tier-2 business objects

## Stakeholder Need

The Filament platform, spec authors, and agent CLI generators require that
DDD-driven specifications **SHALL** yield extractable graph entities for domains,
entities, value objects, aggregates, repositories, events, processes, and state
machines. The need is stated from the perspective of those consumers and avoids
prescribing a specific encoding.

## Rationale

DDD modelling has no first-class representation in the spec graph today, so
domain concepts cannot be discovered, traced, or generated against. Shipping a
tier-2 business object module gives authors and agent generators a shared,
extractable vocabulary for the principal DDD building blocks, which is why the
need exists.

## Validation Criteria

This need is considered satisfied when:

- A Module activation against `filament-core` registers the contents this module
  declares (StR-001-AC-1).
- Agent CLI generators (`minijinja-cli`) can produce valid artifacts using the
  templates and schemas this module ships (StR-001-AC-2).

Satisfaction is judged by demonstrating both outcomes against a running
`filament-core` instance with this module's manifest.

## Dependencies

**Upstream**: filament-core-service FR-035 (Module Manifest Schema).
**Downstream**: agent CLI generators and editors that consume this module's
declared ObjectTypes, templates, and schemas.
