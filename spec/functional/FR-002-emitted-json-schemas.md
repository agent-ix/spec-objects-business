---
id: FR-002
title: "Emit the module's JSON Schemas from a TypeSpec package importing semantic-core"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-033"
    type: "depends_on"
---
# FR-002: Emit the module's JSON Schemas from a TypeSpec package importing semantic-core

## Description

The module build SHALL emit one JSON Schema 2020-12 document per business
object type from a TypeSpec source that imports `@agent-ix/semantic-core`
0.1.0, using the official `@typespec/json-schema` emitter at a pinned
toolchain, into `spec_objects_business/schemas/`, so that the shipped schema
is the compiled one and any drift between source and shipped bytes fails the
build.

## Inputs

- `typespec/main.tsp`: namespace `AgentIx.SpecObjects.Business`, decorated
  `@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-business/<version>/")`
  where `<version>` is the manifest `version`.
- `@agent-ix/semantic-core` 0.1.0 from npm.ix (`FieldDecl`, `TypeRef`,
  `Multiplicity`, `ConstraintDecl`, `RelationDecl`, `OperationDecl`,
  `ClauseRef`, `EnumValue`, `KernelScalar`, `Identifier`, `SemanticId`).
- `@typespec/compiler` 1.15.0 and `@typespec/json-schema` 1.15.0 as exact
  `devDependencies` in `package.json`, resolved through `package-lock.json`.

## Outputs

- `spec_objects_business/schemas/<Model>.json`, one per model of the module
  namespace, rendered as two-space JSON with a trailing newline.
- `spec_objects_business/schemas/toolchain.json`: compiler and emitter names and
  versions, the `$id` base, the emitted file list, the normalization record
  (name, version, applied, rewritten files), and `sha256:<hex>` over the
  emitted files.
- The `data_schema.digest` of every exported object type in `manifest.yaml`,
  rewritten to the SHA-256 of the shipped file bytes.

## Behavior

- `make schemas` SHALL run `node scripts/generate-schemas.mjs`.
- The generator SHALL compile `typespec/` with `tsp compile`, keep only the emitted files whose `$id` starts with the module base, and discard the re-emitted semantic-core files.
- If the emitter leaves any `$id` relative, then the generator SHALL rewrite it to `<base><file>` and record the rewrite in `toolchain.json`.
- When no `$id` is relative, the generator SHALL record the normalization as `applied: false`.
- Every emitted schema SHALL declare `$schema: https://json-schema.org/draft/2020-12/schema` and `$id: https://schemas.agent-ix.org/agent-ix/spec-objects-business/<manifest version>/<Model>.json`.
- Every `$ref` in an emitted schema SHALL name either a sibling `https://schemas.agent-ix.org/agent-ix/spec-objects-business/<manifest version>/<File>.json` that ships in `schemas/`, or `https://schemas.agent-ix.org/semantic-core/0.1.0/<Model>.json`.
- If the `@jsonSchema` base version in `typespec/main.tsp` differs from the manifest `version`, then the generator SHALL fail naming both values.
- `make schemas-check` SHALL run the generator with `--check`.
- When any emitted file differs from the committed output, a committed file is stale, `toolchain.json` differs, or a manifest digest differs from the shipped bytes, the check SHALL exit non-zero naming each such file.
- When nothing differs, the check SHALL exit zero.
- The generator SHALL write files under `spec_objects_business/schemas/` only.
- The generator SHALL edit `manifest.yaml` only at `data_schema.digest` values.
- The Python package SHALL include `spec_objects_business/schemas/*.json` in the wheel and sdist.
- The npm staging script SHALL copy `schemas/` beside `manifest.yaml`, so the npm tarball ships the schemas the manifest references.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-002-CON-1 | The build SHALL use the official `@typespec/json-schema` emitter only; no custom emitter and no hand-edited emitted file. | Architecture | Inspection |
| FR-002-CON-2 | The repository SHALL carry no `.npmrc`, no `file:` or `link:` dependency, and no upper version bound on the TypeSpec toolchain beyond the exact pin. | Packaging | Inspection |
| FR-002-CON-3 | Emission SHALL be deterministic: two runs over one source produce byte-identical files. | Integrity | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-002-AC-1 | After `make schemas`, `spec_objects_business/schemas/` holds exactly the ten object-type models plus the support models the source declares, and `toolchain.json` lists them with compiler 1.15.0 and emitter 1.15.0. | Test |
| FR-002-AC-2 | Every shipped schema declares the 2020-12 `$schema` and the `$id` `https://schemas.agent-ix.org/agent-ix/spec-objects-business/0.3.0/<Model>.json` matching its file name. | Test |
| FR-002-AC-3 | Every `$ref` across the shipped schemas resolves to a shipped sibling or to semantic-core `0.1.0`; a `$ref` to any other host or version is absent. | Test |
| FR-002-AC-4 | `make schemas-check` on the committed tree exits zero; after one byte of any shipped schema or one manifest digest is changed, it exits non-zero naming that file. | Test |
| FR-002-AC-5 | A `@jsonSchema` base whose version segment differs from the manifest `version` makes the generator fail naming both versions. | Test |
| FR-002-AC-6 | The wheel built by `make build` contains `spec_objects_business/schemas/<Model>.json` for every exported model. | Test |

## Dependencies

- **Upstream**: [US-001](../usecase/US-001-declare-business-objects-against-semantic-core.md); semantic-core FR-033 (`ix://agent-ix/filament-core-data/FR-033`); the generation pattern of `packages/semantic-core/scripts/generate.mjs` in filament-core-data
- **Downstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md)
