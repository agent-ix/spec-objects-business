---
id: IT-002
title: "Module installs into Quoin with the semantic contract"
type: IT
relationships:
  - target: "ix://agent-ix/spec-objects-business/FR-003"
    type: "verifies"
---
# IT-002: Module installs into Quoin with the semantic contract

## Objective

Verify the boundary between this module's shipped directory and the Quoin
module installer: `quoin module install path:<dir>` SHALL accept the
`semantic` block, resolve every reference-form `data_schema`, verify every
digest and `$ref`, derive the package manifest, and list the module. Without
this test, a module that Quire accepts but Quoin refuses would ship.

## Target Integration

The system under test is `spec_objects_business/` as consumed by a Quoin
built from `agent-ix/quoin` main at or after commit `3e842ce` (FR-070,
FR-073, FR-075). The integration type is a local CLI invocation over the
filesystem; no network read is involved.

## Preconditions

Quoin is built and installed globally from `/home/peter/dev/quoin` (`make
build && npm i -g .`). The current `quoin module` listing is recorded so the
prior `spec-objects-business` entry (source, ref, sha) can be restored.

## Inputs

The module directory `spec_objects_business/` from this branch, containing
`manifest.yaml`, `schemas/`, and `skeletons/`.

## Test Procedure

1. Record `quoin module` output before the install.
   - IT-002-SC-01: the listing is captured, including any existing
     `spec-objects-business` entry.
2. Run `quoin module install path:/home/peter/dev/spec-objects-business/spec_objects_business`.
   - IT-002-SC-02: exit code 0 and no `semantic.*` diagnostic at `error` severity.
3. Run `quoin module`.
   - IT-002-SC-03: the listing contains `spec-objects-business` sourced from
     the path.
4. Inspect the installed module root.
   - IT-002-SC-04: `semantic/package-manifest.json` exists with
     `package.identity` `agent-ix/spec-objects-business` and one export per
     `semantic.exports` entry.
5. Restore the prior state: re-install the recorded source and ref, or remove
   the module if none was installed.
   - IT-002-SC-05: `quoin module` equals the recording of step 1.

## Expected Results

The install succeeds with exit code 0, the module is listed, the derived
package manifest names the ten exports, and the prior module state is
restored. The test passes only when every per-step success criterion holds.

## Dependencies

**Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md).
**Downstream**: none.
