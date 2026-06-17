---
id: IT-001
title: "Manifest activation roundtrip against filament-core"
type: IT
relationships:
  - target: "ix://agent-ix/spec-objects-business/FR-001"
    type: "verifies"
---
# [IT-001] Manifest activation roundtrip

## Objective

Verify the integration boundary between this Module's published manifest and a
clean `filament-core-service` instance: activating `manifest.yaml` SHALL land all
declared contributions in the database, and re-activating the same manifest SHALL
be an idempotent no-op. Without this test, a manifest that fails to register its
contributions — or that duplicates rows on re-activation — would go undetected.

## Target Integration

The system under test is this Module's manifest as consumed by
`filament-core-service`. The external dependency is the running
`filament-core-service` reached over its HTTP API. The integration type exercised
is an HTTP activation call (`POST /api/v1/modules/activate`) followed by HTTP
reads of the registry endpoints (`/api/v1/archetypes`, `/api/v1/object-types`,
`/api/v1/grammars`, `/api/v1/artifact-types`).

## Preconditions

A `filament-core-service` instance is running and reachable on a clean cluster
(or the kind dev cluster) with an empty `modules` table, so that the absence of
duplicate rows after re-activation is meaningful. This repo's
`spec_objects_business/manifest.yaml` is available as the activation payload.

## Inputs

The activation payload is `spec_objects_business/manifest.yaml` from this repo's
package, posted to `POST /api/v1/modules/activate`. The same manifest bytes are
reused unchanged for the re-activation step so that the content hash is identical.

## Test Procedure

Each step performs one discrete action and has its own success criterion.

1. Deploy `filament-core-service` to a clean cluster (or use the kind dev cluster).
   - IT-001-SC-01: the service reports ready and the `modules` table is empty.
2. POST `spec_objects_business/manifest.yaml` to `/api/v1/modules/activate`.
   - IT-001-SC-02: the endpoint returns `200 OK` and a `modules` row is created.
3. GET `/api/v1/archetypes`, `/api/v1/object-types`, `/api/v1/grammars`, and
   `/api/v1/artifact-types`.
   - IT-001-SC-03: every item declared by the manifest is present with the
     declared attributes.
4. Re-POST the same manifest unchanged.
   - IT-001-SC-04: the activation is an idempotent no-op (same `modules.id`, same
     SHA-256 content hash, no row duplication).

## Expected Results

Activation succeeds with `200 OK`, a single `modules` row is created, and each
declared archetype, object type, grammar, and artifact type appears in the
corresponding registry endpoint with the correct attributes. Re-activating the
identical manifest produces the same `modules.id` and the same SHA-256 content
hash with no duplicated rows. The test passes only when every per-step success
criterion holds.

## Dependencies

**Upstream**: FR-001 (Module manifest activates against filament-core), which this
test verifies. **Downstream**: none — no other test depends on this one.
