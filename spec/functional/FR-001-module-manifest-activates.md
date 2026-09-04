---
id: FR-001
title: "Module manifest activates against filament-core"
type: FR
relationships:
  - target: "ix://agent-ix/filament-core-service/FR-035"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/StR-001"
    type: "traces_to"
---
# FR-001: Module manifest activates against filament-core

## Description

The module **SHALL** publish a Filament Module manifest (`spec_objects_business/manifest.yaml`) that filament-core-service accepts at `POST /api/v1/modules/activate`. Conformance to [FR-035](ix://agent-ix/filament-core-service/FR-035) and idempotent re-activation are stated as separate obligations in Behavior.


## Inputs

- `manifest.yaml` (this repo's package)
- Activation endpoint: `POST /api/v1/modules/activate`

## Outputs

Stated at the HTTP boundary, which is the only surface this module observes;
the service's storage layout is filament-core-service's own concern.

- `200 OK` from `POST /api/v1/modules/activate` carrying the module's content hash.
- Every contributed archetype, object type, grammar, and artifact type readable
  from `/api/v1/archetypes`, `/api/v1/object-types`, `/api/v1/grammars`, and
  `/api/v1/artifact-types`.

## Behavior

- The manifest **SHALL** validate against `module-manifest.schema.json` v1.0.0 at filament-core-service revision `a77f31e` or later (CR-003, the revision that admits the `semantic` block and the reference-form `data_schema`); the same revision is the one Quoin and Quire vendor, so all three consumers judge the manifest against one schema (FR-003 Inputs pins the same value).
- The manifest **SHALL** activate such that re-posting identical bytes yields the same content hash and no duplicated contribution, which filament-core-service delivers per FR-026-AC-1.
- While `agent-ix/filament-core-service#23` is open, the service stores a reference-form `data_schema` verbatim rather than resolving it into a snapshot, so the registered `data_schema` of every exported object type **SHALL** be the reference object as posted (`{schema, digest}`), and FR-001-AC-4 is read against that value.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | Manifest validates against FR-035 JSON Schema | Test |
| FR-001-AC-2 | Activation against clean filament-core succeeds with 200 | Test |
| FR-001-AC-3 | Re-activation returns no-op (same content hash) | Test |
| FR-001-AC-4 | Each declared archetype/object_type/artifact_type appears at the corresponding registry endpoint after activation, and each exported object type's registered `data_schema` equals the reference object as posted | Test |

## Dependencies

- **Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035), FR-026, FR-034
- **Downstream**: consumer agents/editors discovering this module's contributions
