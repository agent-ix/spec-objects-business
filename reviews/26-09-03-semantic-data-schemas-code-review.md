---
id: SR-009
title: "Code review — spec-objects-business semantic data schemas (#4)"
type: SpecReview
analysis: code-review
scope: "typespec/, scripts/generate-schemas.mjs, spec_objects_business/, tests/, plan/Plan-001-semantic-data-schemas/"
review_set: subset
---
# SR-009: Code review — semantic data schemas (#4)

## Summary

Reviewed the whole `spec/4-semantic-data-schemas` branch diff against `main`:
the TypeSpec source and generator, the 0.3.0 manifest, the seventeen emitted
schemas, the rewritten skeletons and negative fixtures, and the 141-case test
suite, together with an implementation-gap pass over the spec set. Every gate
was run rather than assumed. Six findings — one high, three medium, two low —
all fixed in this branch except the two that are engine defects filed
upstream and carried as strict expected failures.

## Verdict

**CONDITIONAL** — the one high finding (a silently unbacked matrix row) is
fixed and re-measured at 101/101; the remaining findings are fixed or are
upstream defects with tickets and expected-failure tests. No finding is
outstanding in this repository.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | A `black`-wrapped multi-line `@pytest.mark.trace(...)` is not matched by the declared `pytest-trace-marker` form, so TC-070 and its six IT-002 success criteria reported **unbacked** with no diagnostic — indistinguishable from a test nobody wrote. Two stacked `@pytest.mark.trace` decorators lose one of the two the same way. Fixed by keeping every marker on one line and splitting the IT-002 assertions across two tests; filed upstream as `agent-ix/quire-rs#395`. Coverage went 100/101 → 101/101. | tests/test_quoin_install_roundtrip.py:44 |
| FND-002 | medium | `npm pack` left the staged npm payload (`manifest.yaml`, `schemas/`, `skeletons/`) at the repository root. A `manifest.yaml` there makes every Filament tool discover the repo root as a second module; `quire validate` in this repo then failed with "no archetype registered" for every document, and the cause is invisible. Fixed by a `postpack` hook (`scripts/stage-npm.mjs --clean`), and TC-071 asserts both that the tree was clean before and that the hook ran. | scripts/stage-npm.mjs:34, package.json:20, tests/test_schema_emission.py:243 |
| FND-003 | medium | TC-012 checked only that a non-sibling `$ref` carried the semantic-core prefix. The generator's normalization falls back to that base for any relative `$ref` it does not recognise as a sibling, so a dangling `https://schemas.agent-ix.org/semantic-core/0.1.0/Nonexistent.json` would have passed. Fixed: the assertion now resolves each such `$ref` against the installed semantic-core package. | tests/test_schema_emission.py:118 |
| FND-004 | medium | FR-003 Behavior claimed "one refused schema fails every object type of the module (quire-rs FR-069)", carried over from the failure-domain review. Measured against quire 0.46.0 the granularity is different: a wrong `data_schema` digest drops that object type alone, while an unknown `semantic` key drops the whole module. Spec corrected, the disposition on FND-111 updated, and TC-026 asserts the measured behaviour. | spec/functional/FR-003-semantic-manifest-contract.md:47, tests/test_manifest_semantic.py:130 |
| FND-005 | medium | Both module-load refusals are silent: no `ArchetypeLoadFailure`, no `semantic.*` code, nothing naming the offending key, path, or digest through any surface this module can read. FR-003-AC-6's "naming the key or the path" half is therefore not dischargeable. Filed as `agent-ix/quire-rs#394` (sibling of the open `#221`); the criterion stands and is carried as a strict `xfail` naming both, not relaxed and not skipped. | tests/test_manifest_semantic.py:151 |
| FND-006 | low | `# pragma: no cover` comments sat on five environment guards in the test tree. Coverage is measured over `spec_objects_business/` only, so they suppressed nothing — but a pragma that reads as "this is allowed to be uncovered" is exactly the habit the integrity rule forbids. Removed. | tests/conftest.py:131, tests/test_schema_emission.py:170 |

## Gates Run

| Gate | Result |
|---|---|
| `make lint` (ruff + black + `schemas-check`) | pass — all checks passed, 17 schemas match the committed output |
| `make test` | pass — 134 passed, 7 skipped, 2 xfailed, coverage 100% (`--cov-fail-under=100`) |
| `quire validate --scope . "spec/**/*.md"` | pass — zero errors, zero grammar warnings |
| `quire validate --scope . "plan/**/*.md"` | pass |
| `quire coverage --scope .` | 101/101 rows backed (100%); `spec/tests.md` 56/56 |
| `node scripts/generate-schemas.mjs --check` | pass on the committed tree |
| `poetry build` / `npm pack` | both exercised by TC-015 and TC-071 |

## Language Dispatch

Python (`pyproject.toml`, `tests/*.py`) plus two Node build scripts and one
TypeSpec source. No Rust and no React in the change, so those lanes do not
apply. The repo's own idiom — module-level `test_*` functions with
`@pytest.mark.trace(...)`, not `TestFeature` classes — was followed; the
generic "leverage test classes" rule is outranked by the existing convention
in `tests/test_manifest.py` and `tests/test_skeletons_and_validate.py`.

## Test Standards

- **Tracking tags.** Every test carries `@pytest.mark.trace(...)` with its TC
  id and the acceptance criterion or constraint it discharges; the marker is
  registered in `pyproject.toml`, so `filterwarnings = ["error"]` does not
  turn an unknown mark into a failure.
- **No mocks anywhere.** Every test drives the real generator, the real
  emitter, the real Quire engine, or the real shipped bytes. There is no
  `unittest.mock`, no `@patch`, and no `mocker` usage in the change, so the
  mock-boundary rules are vacuously satisfied — and no test can pass against
  a hollow stub.
- **No database interaction**, no network read: the only subprocesses are
  `node`, `poetry build`, `npm pack`, `git diff`, and (opt-in) `quoin`.
- **Skips.** Seven, and every one names the environment it needs and the
  matrix row that stays `🚧` because of it: a running
  `filament-core-service` at `a77f31e` or later (five) and an opt-in Quoin
  install roundtrip (two). No semantic test skips: `tests/conftest.py`
  `require_quire` **fails** when the engine is absent, naming
  `make dev-quire` and `agent-ix/quire-rs#392`.
- **Expected failures.** Two, both `strict=True` so they turn red the day the
  engine is fixed, and both naming the upstream issue in the reason.

## Completeness

No `TODO`, `FIXME`, or `XXX` in any authored file (the two matches are the
placeholder-token lists the skeleton tests search *for*). No `pass`
placeholder, no stub module, no empty class, no placeholder return. Every
test asserts behaviour: an AST pass over `tests/` found no test function
without an `assert` or a `pytest.raises`, and no test asserting only
`is not None` or `isinstance`.

## Spec-Code Faithfulness

Each requirement was checked against what the branch actually does, not
against what it claims:

- **FR-002** — `make schemas` runs the official `@typespec/json-schema`
  emitter through `tsp compile`; the only relative reference the emitter
  leaves is the `Event` `allOf` `$ref`, and `toolchain.json` records that one
  rewrite rather than a blanket `applied: true`. `--check` writes nothing
  (asserted by TC-073 comparing bytes before and after), fails on a mutated
  schema, a mutated digest, a stale file, and a half-bumped version pair.
- **FR-003** — the `semantic` block carries exactly the nine admitted keys;
  every exported type's digest equals the SHA-256 of the shipped bytes; every
  0.2.0 locator is byte-equal to the frozen baseline and every added locator
  is `required: false`.
- **FR-004** — no model is a placeholder: each of the ten is sealed
  (`unevaluatedProperties: {not: {}}`) and differs from every other in a
  required, forbidden, or item rule. The identity and occurrence rules were
  proved end-to-end through the real 2020-12 validator before the remaining
  seven types were authored (the Task-011 gate).
- **FR-005** — all thirteen skeletons validate clean, the three `sysml`
  alternates extract to `FieldDecl[]` identical to their tables, and all
  eight negative fixtures fail for their own reason (the assertion checks the
  message carries detail beyond the bare code, because five of the eight
  surface as `semantic.record-invalid`).
- **NFR-001** — the zero-error claim is *measured*, and the measurement
  explains itself: no 0.2.0 skeleton carries `object:`, so Quire never
  assembles a typed record for one. The engine defect that would otherwise
  bite is asserted separately as the expected failure under FND-005's
  sibling, `agent-ix/quire-rs#391`.

## Code-Test Alignment

Every criterion over a record key the extractor does not populate
(`relations`, `owner`, `members`, `states`, `transitions`, `steps`, `values`,
`emits`, `persists`, `source`, `vocabulary`) is verified against a hand-built
JSON record, and the test's docstring says so. That is FR-004's own rule, and
it keeps the suite from claiming extraction evidence it does not have. The
matrix carries the same statement in its Test Environment section, so a
reader of `spec/tests.md` sees the limitation without opening a test file.

## Gap Analysis

Discovery over the change surfaced four unstated requirements, all now
written down rather than left in code:

1. **Packaging side effect as a robustness gap.** Nothing said a pack must
   leave the tree as it found it. FND-002 is the failure that gap produced;
   the `postpack` hook and TC-071's before/after assertion close it.
2. **`$ref` fallback as an integrity gap.** The generator's normalization has
   a total function where the spec has a partial one — an unrecognised
   relative reference becomes a semantic-core URL rather than an error.
   FND-003 closes the observable half; the generator's own behaviour is left
   as-is because the emitter produces exactly one relative reference and the
   test now proves it resolves.
3. **Refusal granularity as a traceability gap.** FR-003 asserted a
   blast radius nobody had measured (FND-004). The lesson generalises: a
   neighbour's failure mode belongs in the spec only once it has been run.
4. **Tag binding as an evidence gap.** A marker that binds nothing is worse
   than a missing marker, because the row reads as "nobody wrote this test"
   (FND-001). `quire coverage` is now part of the gate list for this repo,
   not a thing checked once.

No further unstated requirement was found: `quire coverage` reports zero
unbacked rows, zero status lies, and zero untracked symbols.

## Edge Case & Logic Review

- **Input validation.** The generator reads the manifest version and the
  `@jsonSchema` base with anchored regexes rather than a YAML round trip, so
  anchors, aliases, and comments survive the digest rewrite; a manifest with
  no top-level `version` fails naming the file.
- **Failure policy.** A `tsp compile` failure, an emission with zero module
  models, a Node older than 20, a missing `tsp`, and a version mismatch each
  exit non-zero *without touching committed output*; `--check` is read-only
  by construction and TC-073 proves it byte-for-byte.
- **Determinism.** Two runs over one source are byte-identical (TC-016), and
  `.gitattributes` pins `eol=lf` on `*.json` and `*.tsp` so a checkout under
  `core.autocrlf` cannot change a digested byte.
- **Global state.** The only test that mutates the operator's machine is the
  Quoin roundtrip, and it is doubly gated (an opt-in env var and a Quoin on
  `PATH`) with an unconditional restore in a `finally` block.
- **Isolation.** Every destructive generator test runs in a throwaway copy of
  the tree with `node_modules` symlinked, so no test can corrupt the
  committed schemas or the manifest.
