---
id: Task-001
title: "FR-002 — TypeSpec toolchain, schema generator and drift gate"
type: Task
status: not_started
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-013
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-014
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-016
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-017
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-072
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-073
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-074
    type: verifies
---
# Task-001: FR-002 — TypeSpec toolchain, schema generator and drift gate

## Scope

The enablement half of FR-002: everything that turns a TypeSpec source into shipped
schema bytes, and everything that refuses a tree where the two disagree. The models
themselves are Task-002; this task must work against a source that compiles.

## Subtasks

- [ ] **Pin the toolchain.** `@typespec/compiler` 1.15.0, `@typespec/json-schema` 1.15.0 and `@agent-ix/semantic-core` 0.1.0 as exact `devDependencies` (semantic-core moves out of `dependencies`: it is a build input, and the published artifact is Markdown and JSON). No `.npmrc`, no `file:`/`link:`, no upper bound.
- [ ] **Author `typespec/main.tsp`'s shell.** Namespace `AgentIx.SpecObjects.Business`, `@jsonSchema` base `https://schemas.agent-ix.org/agent-ix/spec-objects-business/<manifest version>/`, importing `@agent-ix/semantic-core`.
- [ ] **Write `scripts/generate-schemas.mjs`.** Node built-ins only. Compile with `tsp compile`; keep the files whose `$id` starts with the module base and discard re-emitted semantic-core files; rewrite any relative `$id`/`$ref` to the module base or to `https://schemas.agent-ix.org/semantic-core/0.1.0/`; record every rewrite (and `applied: false` when none was needed) in `toolchain.json`; render two-space JSON with a trailing newline.
- [ ] **Fail loudly.** Exit non-zero without touching committed output when `tsp compile` fails, when no module model is emitted, when Node is older than 20 or `tsp` is unresolvable, and when the `@jsonSchema` base version differs from the manifest `version` — naming both values.
- [ ] **Digest rewrite.** Rewrite `manifest.yaml`'s `data_schema.digest` values textually, so the file's YAML anchors and comments survive; write nothing else in the manifest.
- [ ] **`--check` mode.** Writes no file at all. Exits non-zero naming each file that differs, is stale (committed under `schemas/` with no emitted counterpart), or whose manifest digest disagrees with the shipped bytes.
- [ ] **Wire the targets.** `make schemas` and `make schemas-check` as poe tasks; `make lint` runs `schemas-check`.
- [ ] **`.gitattributes`.** `*.json` and `*.tsp` marked `eol=lf` so a checkout under `autocrlf` cannot change the digested bytes.

## Deliverables

- `typespec/main.tsp` (shell), `scripts/generate-schemas.mjs`, `.gitattributes`
- `package.json` / `package-lock.json` with the three exact pins
- `Makefile` + `pyproject.toml` poe tasks `schemas`, `schemas-check`; `lint` chained
- Tests for TC-013, TC-014, TC-016, TC-017, TC-072, TC-073, TC-074

## Notes

- FR-002-CON-1: the official `@typespec/json-schema` emitter only. No custom emitter,
  no hand-edited emitted file — a wrong schema is a source fix and a regeneration.
- FR-002-CON-5 and the bump procedure are this task's: the `$id` base embeds the
  manifest `version` by intent, and a bump is one atomic regeneration. TC-074 asserts
  that no test hard-codes the version segment, so every assertion reads it from
  `manifest.yaml`.
- `@agent-ix/semantic-core` resolves from npm.ix through the user-level npm config
  (FR-002-CON-4); `make schemas` therefore runs locally, not in the GitHub workflow,
  until `agent-ix/filament-core-data#11` publishes the package.
- Unblocks: Task-002 (a compiling source), Task-003 (the emitted set).
