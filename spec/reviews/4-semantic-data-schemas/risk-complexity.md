---
id: SR-006
title: "Risk & complexity review of the issue #4 semantic data schemas"
type: SpecReview
analysis: risk-complexity
scope: "spec/spec.md, spec/usecase/US-001, spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/integration/IT-002, spec/tests.md"
review_set: all
---
# SR-006: Risk & complexity review of the issue #4 semantic data schemas

## Summary

Scored every requirement in the issue #4 set (US-001, FR-001..FR-005, NFR-001,
IT-002) on technical risk and volatility, verifying each engine-facing claim
against the current code: `declaration_record` in
`quire-rs/src/semantic/surface.rs` emits only `fields`, `clauses`, and
`operations`; `semantic_findings` in `quire-rs/src/validate_document.rs`
validates that record against the resolved `data_schema` unconditionally; a
legacy-form `## Properties` returns `unavailable("legacy-form")` in
`quire-rs/src/semantic/properties.rs`; `$ref` resolution in both
`quoin/src/semantic/data-schema.ts` and `quire-rs/src/semantic/resolver.rs`
accepts only module-bundle siblings and the vendored semantic-core bundle.
One requirement pair is unsatisfiable as written under the engine (NFR-001's
zero-error legacy metric against FR-004's `fields`-required entity schema),
the version-embedding `$id` couples every schema byte and digest to the
manifest version, and roughly half of FR-004's shape rules (ten declared-but-
unextracted keys plus `relations`) can be verified only against hand-built
JSON records, never through the extraction path the module exists to serve.

## Verdict

Not ready for `spec-to-plan` until FND-180 is dispositioned (either NFR-001's
legacy metric is restated, or FR-004/quire-rs gain a rule that skips record
validation when `fields` availability is `legacy-form`). The remaining
findings are plannable as spikes, slices, and added evidence; none blocks
tasking on its own. Counts: 2 high, 8 medium, 4 low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|----|----------|---------|------|--------------|
| FND-180 | high | NFR-001 requires the legacy-form 0.2.0 entity skeleton to validate under 0.3.0 with zero errors, but FR-004 makes `fields` required on `Entity`, the legacy form yields no `fields` (`FieldsOutcome::unavailable("legacy-form")`), and `semantic_findings` validates the resulting `{}` record against `Entity.json` unconditionally, producing `semantic.record-invalid` at error severity. The two requirements cannot both hold under the current engine. | NFR-001, FR-004, FR-003-AC-4, TC-061 | wrong-requirement |
| FND-181 | high | The `$id` base embeds the manifest version (`.../spec-objects-business/0.3.0/`), so every version bump rewrites every `$id`, every sibling `$ref`, every shipped byte, every manifest digest, and `toolchain.json`; FR-002-AC-2 and FR-003-AC-2 hard-code `0.3.0`, so the acceptance criteria themselves churn per release, and downstream fixture readers (quire-contract-ir#52, filament-core-data#36) that key on `$id` break on each bump. | FR-002, FR-002-AC-2, FR-002-AC-5, FR-003-AC-2, FR-003 Behavior | wrong-requirement |
| FND-182 | medium | Ten keys FR-004 declares (`members`, `vocabulary`, `owner`, `emits`, `persists`, `source`, `states`, `transitions`, `steps`, `values`) plus `relations` are never emitted by `declaration_record`, so FR-004-AC-3 (`relations` refused), AC-7 (`transitions` trigger), AC-8 (`StepKind`), and TC-041 (`owner`) are provable only with synthetic JSON; the key names and shapes are a guess at a future extractor that may name or nest them differently, and nothing in this module detects that drift. | FR-004, FR-004-AC-3, FR-004-AC-7, FR-004-AC-8, TC-041 | correct-requirement-no-evidence |
| FND-183 | medium | Every schema edit flips its SHA-256 digest in `manifest.yaml` and `toolchain.json`; `make schemas-check` then fails any PR whose author edited `typespec/` without re-running `make schemas`, and a Quoin-installed copy (IT-002) goes stale on every edit. No requirement names the regeneration step as a pre-commit or CI obligation, so the digest gate will be the most frequent red build in the repo. | FR-002-AC-4, FR-003-AC-2, IT-002-SC-02 | missing-requirement |
| FND-184 | medium | The identity and occurrence item rules (≥1 / exactly 0 identity fields; ≥1 `Timestamp` field) depend on emitter support for `contains`/`minContains`/`maxContains` over a sibling marker schema and on the validator honouring them together with `unevaluatedProperties: {not: {}}`; the TypeSpec emitter side is known to support `@contains`/`@minContains`/`@maxContains`, but the "exactly zero" encoding (`minContains: 0` + `maxContains: 0`) and jsonschema 0.18's 2020-12 handling of `unevaluatedProperties` interacting with `$ref` siblings are unprototyped in this repo. | FR-004 Behavior, FR-004-AC-2, FR-004-AC-3, FR-004-AC-5 | correct-requirement-no-evidence |
| FND-185 | medium | The identity flag is set only when a Constraints cell carries the bare `identity` keyword (`properties.rs` reader) and is absent, not `false`, otherwise; the occurrence rule matches `type.target` equal to the bare kernel token `Timestamp`. Both are semantic-core 0.1.0 reader conventions, not schema-level guarantees; a 0.2.0 that renders `identity: false` or namespaces kernel scalars silently changes which records the module's schemas accept. | FR-004 Behavior, FR-004-AC-2, FR-004-AC-5, FR-002 Inputs | correct-requirement-no-evidence |
| FND-186 | medium | FR-002 specifies normalization of relative `$id` only; the emitter also produces relative `$ref`s (to re-emitted semantic-core models and to siblings), and FR-002-AC-3 requires absolute `$ref`s under two distinct bases. The `$ref` rewrite (and its record in `toolchain.json`) is an unstated generator step on which AC-3 and both consumers' resolvers depend. | FR-002 Behavior, FR-002-AC-3, FR-002 Outputs | missing-requirement |
| FND-187 | medium | `@agent-ix/semantic-core` 0.1.0 is served from npm.ix only, FR-002-CON-2 forbids a repo `.npmrc`, and FR-002 requires a committed `package-lock.json`; the lock will therefore record npm.ix resolved URLs, which the ecosystem rule reserves for stable builds. Toolchain reproducibility (FR-002-CON-3, TC-016) rests on a registry we control but the requirement does not name. | FR-002 Inputs, FR-002-CON-2, FR-002-CON-3 | missing-requirement |
| FND-188 | medium | FR-003's `semantic` block must be accepted byte-for-byte by two independently vendored copies of the module-manifest schema (Quoin, Quire) and FR-003-CON-1 requires both to reject an unknown key; version skew between the vendored copies makes one consumer accept what the other refuses, and the spec offers no pin for either copy. | FR-003 Behavior, FR-003-CON-1, FR-003-AC-6, IT-002 | correct-requirement-no-evidence |
| FND-189 | medium | FR-003-AC-5 and IT-002 mutate the operator's global `quoin module` state, pin an absolute developer path (`/home/peter/dev/quoin`), and rely on a manual restore; the only evidence for the Quoin boundary is a Demonstration that cannot run in CI. | FR-003-AC-5, IT-002 Preconditions, IT-002-SC-05, TC-027, TC-070 | correct-requirement-no-evidence |
| FND-190 | low | `validate_document` builds its `BundleIndex` from registry imports only (no objects), so cross-skeleton `Type` tokens resolve nowhere under it and surface as `semantic.unresolved-type` (advisory). FR-005-AC-1 still passes, but FR-005-AC-3's zero-unresolved claim holds only under `extract_semantic` with a hand-built bundle; the two criteria exercise different resolution paths and the spec does not say so. | FR-005-AC-1, FR-005-AC-3, TC-050, TC-052 | correct-requirement-no-evidence |
| FND-191 | low | FR-005-AC-4 expects `clauses` `available` for `aggregate_root` and `not_applicable` where absent, but FR-005 Behavior tells seven types to author `## Invariants`; the `not_applicable`/`missing` split depends on FR-003's new `required: false` locators and on `RequiredSections::from_dsl`, so the expected availability matrix is under-specified for the six non-root clause-bearing types. | FR-005-AC-4, FR-005 Behavior, FR-003 Behavior, TC-053 | wrong-requirement |
| FND-192 | low | FR-001 (unchanged since issue #1) needs a running `filament-core-service` for three of four criteria; it is low volatility but its evidence is environment-gated and stays `🚧` regardless of this change. | FR-001-AC-2, FR-001-AC-3, FR-001-AC-4, TC-002, TC-003, TC-004 | correct-requirement-no-evidence |
| FND-193 | low | The eight named negative fixtures (FR-005-AC-5) mix schema refusals (`semantic.record-invalid`) with extractor refusals (`semantic.invalid-type-token`, both-forms, dangling `Post:`); the `expect:` code for each is not listed, so the fixture set can drift from the diagnostic codes the engine actually emits without any row in the matrix noticing. | FR-005-AC-5, TC-054, TC-057 | missing-requirement |

## Risk Register

| Req | Tech Risk | Volatility | Drivers | Mitigation |
|-----|-----------|------------|---------|------------|
| US-001 | Low | Medium | Maintainer story; downstream frontends (#52, #36) may reshape what a "declaration record" must carry | Keep the story free of layout; let FR-004 absorb change |
| FR-001 | Medium | Low | Live filament-core, content-hash idempotency | Leave as-is; TC-002..004 stay environment-gated (FND-192) |
| FR-002 | High | High | Pinned external toolchain, npm.ix-only dependency, version-embedded `$id`, unstated `$ref` rewrite, byte-determinism gate | Spike the generator first against emitter 1.15.0; write the `$ref` normalization into Behavior; decide the `$id` versioning policy (FND-181, FND-186, FND-187) |
| FR-003 | Medium | High | Exact-key `semantic` block across two vendored schema copies, digests churning per edit, global Quoin install | Pin the vendored manifest-schema commit in both consumers; make `make schemas` a pre-commit target; scriptable install roundtrip (FND-183, FND-188, FND-189) |
| FR-004 | High | High | `contains`/`unevaluatedProperties` item rules, identity/`Timestamp` reader conventions, eleven keys the extractor never fills | Prototype `Entity`/`ValueObject`/`Event` end-to-end (TypeSpec → emitted → Quire record) before the other seven; mark unextracted keys as reserved and test them with synthetic records only, labelled as such (FND-182, FND-184, FND-185) |
| FR-005 | Medium | Medium | Two extraction paths (`validate_document` vs bundle-indexed `extract_semantic`), availability matrix, diagnostic codes for negatives | List the `expect:` code per negative; state which path each AC runs under (FND-190, FND-191, FND-193) |
| NFR-001 | High | Low | Zero-error legacy metric contradicts `fields`-required schemas under unconditional record validation | Resolve FND-180 before planning: restate the metric, or add a quire-rs rule that skips record validation on `legacy-form` availability |
| IT-002 | Medium | Medium | Manual, global-state, developer-path-bound | Parameterise the Quoin binary and run in a temp `QUOIN_HOME`; keep as Demonstration until then (FND-189) |

## Top hazards

1. NFR-001 versus FR-004 (FND-180): the legacy entity skeleton produces an empty declaration record, `Entity.json` requires `fields`, and the engine validates every record; either the metric or the engine rule must change before tasks are cut.
2. Version-embedded `$id` (FND-181): every release rewrites every schema, digest, and two acceptance criteria; downstream fixture readers key on the URL.
3. FR-004 shape rules without an extraction path (FND-182, FND-184, FND-185): the item rules that make the ten roles distinct are the least-evidenced part of the set; prototype three types end-to-end first.
4. Generator toolchain (FND-186, FND-187): the `$ref` rewrite and the npm.ix-only dependency are unstated but load-bearing for FR-002-AC-3 and FR-002-CON-3.
5. Consumer skew (FND-188, FND-189): two vendored manifest-schema copies and a manual global install are the only evidence that Quoin and Quire agree.

## Mitigation order

1. Disposition FND-180 (spec change or quire-rs ticket) and FND-181 (`$id` policy) with the architect; both are wrong-requirement and block plan generation.
2. Spike FR-002 + FR-004 for `Entity`, `ValueObject`, `Event` only: TypeSpec source, emitted schema, Quire record round trip, the three identity/occurrence rules, `unevaluatedProperties` behaviour in jsonschema 0.18.
3. Add Behavior lines for the `$ref` normalization, the regeneration obligation, and the `expect:` code per negative fixture.
4. Slice FR-004's remaining seven types and the eleven reserved keys into a follow-on task with synthetic-record tests explicitly labelled as not extraction-backed.
5. Script IT-002 against a temp Quoin home so TC-027/TC-070 can leave Manual.

## Failure-domain gaps

No `spec-failure-domain-analysis` deliverable exists for this review set yet
(`spec/reviews/4-semantic-data-schemas/` holds only this document). The
identity-confusion gap in FND-180 (legacy record versus typed record under one
schema) and the topology gap in FND-190 (two bundle-index paths) should be
carried into that analysis when it is written. Open gaps: NFR-001, FR-004,
FR-005.

## Dispositions

| Finding | Disposition |
|---|---|
| FND-180 | Applied: see failure-domain.md FND-100 / integrity.md FND-120. The metric is not restated to accommodate the defect and no schema is relaxed; `agent-ix/quire-rs#391` owns the engine rule and TC-061 is a named expected failure until it lands. |
| FND-181 | Applied as option (a), *and* the acceptance criteria are de-hardcoded, because the two are not in tension: the decision is recorded, and once the version is read from the manifest the criteria stop churning per release. FR-002 Behavior now states the decision explicitly — the `$id` base embeds the manifest `version` by intent, matching the semantic-core bundle convention (`https://schemas.agent-ix.org/semantic-core/0.1.0/`), so that one schema URL names exactly one immutable byte sequence and a downstream fixture reader that pinned a version can never silently read later bytes under the same URL. The cost the finding names (every bump rewrites every `$id`, `$ref`, digest and `toolchain.json`) is accepted and discharged by a stated bump procedure: the `@jsonSchema` base and the manifest `version` are edited in one commit, `make schemas` is re-run, and the re-emitted schemas, digests and `toolchain.json` are committed together; a commit carrying one half of the pair is refused by `make schemas-check` (FR-002-AC-5, FR-002-AC-8). FR-002-AC-2 now reads `<manifest version>` rather than `0.3.0`, FR-003-AC-2 was already version-free, and a new Behavior bullet forbids any criterion, test or fixture from hard-coding the version segment (FR-002-CON-5, TC-072, TC-074). The alternative — a version-less base — was rejected: it would make the same URL serve different bytes over time, which is exactly the failure mode the downstream fixture readers (`agent-ix/quire-contract-ir#52`, `agent-ix/filament-core-data#36`) cannot detect. |
| FND-182 | Applied: FR-004 Behavior requires every criterion over an unpopulated key to be verified against a hand-built record with that limitation named in the test, and `tests.md` gains a Test Environment note listing those rows, so no row claims extraction evidence it does not have. |
| FND-183 | Applied: `make lint` runs `make schemas-check`, so a `typespec/` edit that was never regenerated fails before push rather than at review. |
| FND-184 | Recorded and discharged by the implementation: the decorator recipe is now stated (integrity.md FND-121) and TC-030..TC-038 exercise `contains`/`minContains`/`maxContains` and `unevaluatedProperties` against the real emitted schemas and the real validator, which is the prototype the finding asks for. |
| FND-185 | Applied: FR-004 Behavior pins both readings as semantic-core 0.1.0 reader conventions and states that a semantic-core release that renders `identity: false` or namespaces kernel scalars is a breaking change handled by a version bump, not by widening a rule. |
| FND-186 | Applied: FR-002 Behavior covers the relative `$ref` rewrite under both bases and its record in `toolchain.json`. |
| FND-187 | Applied: FR-002-CON-4. |
| FND-188 | Applied: FR-003 Inputs pin revision `a77f31e` and state that a consumer vendoring an older copy is that consumer's skew defect. |
| FND-189 | Applied: IT-002 drops the developer path and makes the restore unconditional; the Demonstration classification is kept for the reason given under evidence.md FND-162. |
| FND-190 | Applied: FR-005-AC-1 and FR-005-AC-3 name their resolution paths (`validate_document` against the module; `extract_semantic` under a bundle index built from the skeleton frontmatter), so the two criteria no longer read as one claim. |
| FND-191 | Applied: FR-005-AC-4 enumerates the availability matrix per kind and per type. |
| FND-192 | Recorded, no change: TC-002..TC-004 stay environment-gated and their status column says so. |
| FND-193 | Applied: FR-005 Behavior names the `expect:` code for each of the eight negative fixtures. |
