---
id: SR-002
title: "Failure-domain review of the #4 semantic data schemas spec"
type: SpecReview
analysis: failure-domain
scope: "spec/spec.md, spec/stakeholder/StR-001-module-activation.md, spec/usecase/US-001-declare-business-objects-against-semantic-core.md, spec/functional/FR-001-module-manifest-activates.md, spec/functional/FR-002-emitted-json-schemas.md, spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-004-role-schemas.md, spec/functional/FR-005-executable-skeletons.md, spec/non-functional/NFR-001-additive-compatibility.md, spec/integration/IT-001-manifest-activation-roundtrip.md, spec/integration/IT-002-quoin-module-install.md, spec/tests.md"
review_set: all
---
# SR-002: Failure-domain review of the #4 semantic data schemas spec

## Summary

Failure-domain analysis (extension-point failure policy, entity identity,
evaluation purity, topological robustness) of the issue #4 spec set, grounded
against the upstream contract it consumes: `semantic-core/main.tsp`, quoin
FR-070..FR-075 and `src/semantic/data-schema.ts`, quire-rs FR-069..FR-072 and
`src/semantic/surface.rs` (`declaration_record`), `validate_document.rs`
(`semantic_findings`), `properties.rs`, `clauses.rs`, and the 0.2.0 skeletons
and `manifest.yaml` on this branch. Twelve findings: one high, five medium,
six low. The high finding is a contradiction between NFR-001 and FR-004 that
the engine as shipped makes unavoidable: every legacy 0.2.0 artifact of a type
whose schema has a required key yields an empty or under-filled declaration
record, and quire validates that record against the sealed schema
unconditionally, so "zero errors for legacy artifacts" cannot hold for eight
of the ten types.

## Verdict

Not ready for `spec-to-plan` until FND-100 is dispositioned: the spec must
either change the FR-004 required-key rules, or record an upstream quire-rs
requirement (skip record validation when a declaration kind is
`unavailable`/`not_applicable`) as a blocking dependency, or narrow NFR-001 to
what the engine can deliver. FND-101..FND-105 are medium and each has a
one-paragraph fix; the low findings are proposed additions, not blockers.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-100 | high | NFR-001 (legacy 0.2.0 artifact: 0 errors) contradicts FR-004 required keys: quire validates `declaration_record()` (only `fields`/`clauses`/`operations`, each absent when `unavailable` or `not_applicable`) against the sealed schema unconditionally, so a legacy entity yields `{}` and `semantic.record-invalid` (error); the same holds for nested_entity, value_object, aggregate_root, event, process (no `fields`), repository (`operations: []` fails `minItems 1`), and state_machine. The NFR is unmeetable for 8/10 types as written. | NFR-001, FR-004 Behavior table, FR-004-AC-9, FR-003 Description, FR-005-AC-1, TC-061 | wrong-requirement |
| FND-101 | medium | Dual authority for the same declarations with no agreement rule: `event` keeps the `## Schema` JSON fence (required) beside the new typed `## Properties`; `state_machine` keeps the mermaid `## States & Transitions` (required) beside required `## Operations` and optional `transitions`; `aggregate_root` keeps `## Members` prose beside `members: RelationDecl[]`; `nested_entity` keeps `## Parent` beside `owner`; `process` keeps `## Workflow` beside `steps`. Nothing says which is authoritative or that they must agree, so a fixture can drift silently. | FR-005 Behavior (kernel sections bullet), FR-004 Outputs, FR-003 Behavior (locators unchanged) | missing-requirement |
| FND-102 | medium | Cross-reference identity key is unstated: FR-005 resolves `Type` cells by skeleton frontmatter `title` "(an `Identifier`)", but the 0.2.0 titles are `Order Management`, `Order state vocabulary`, `Order Lifecycle`, `Order Fulfilment` (not Identifiers), ids are `entity-001` (not Identifiers, yet quire step 2 matches by id first), no uniqueness rule exists across the ten titles (quire: `semantic.ambiguous-type`), and a title equal to a kernel scalar name (`String`, `Timestamp`, `Duration`) is silently shadowed by precedence step 1. | FR-005 Behavior (Type cell bullet), FR-005-AC-3, quire-rs FR-070 precedence | missing-requirement |
| FND-103 | medium | FR-004 claims roles are "told apart by the shape of their records rather than by name alone", but the minimal record `{ fields: [one identity field] }` validates against `Entity`, `NestedEntity`, and `Process` alike; `{ fields: [non-identity] }` validates against `ValueObject` only by the absence of a flag. FR-004-AC-1 tests pairwise rule difference, not record disjointness, so the description overstates what the schemas do and the issue AC "roles are semantically distinct" is met by name after all. | FR-004 Description, FR-004-AC-1, FR-004-CON-2 | wrong-requirement |
| FND-104 | medium | FR-004 says every cross-reference (`type.target`, `RelationDecl.target`, `emits`, `persists`, `source`) is "reported by the extractor rather than silently accepted", but the extractor resolves `Type` cells only; `emits`, `persists`, `source`, `ProcessStep.consumes/emits`, `Transition.emits` are pattern-checked `SemanticId`s with no resolution, and `Transition.from`/`to` are bare `Identifier`s with no rule that they name a member of `states`. A dangling event or state reference is accepted with no finding. | FR-004 Behavior (cross-reference bullet, `Transition`, `ProcessStep`), FR-004-AC-7 | wrong-requirement |
| FND-105 | medium | IT-002 / FR-003-AC-5 mutate the operator's global quoin module store and restore it in step 5, but no step defines what happens when step 2 or 3 fails (the prior entry is lost and every other repo's `quoin` on the machine sees a half-installed module); the precondition hard-codes `/home/peter/dev/quoin` and `make build && npm i -g .`, so the test cannot run anywhere else. | IT-002 Preconditions, IT-002 Test Procedure step 2 and 5, FR-003-AC-5, TC-027, TC-070 | missing-requirement |
| FND-106 | low | Identity cardinality is unstated: `Entity`/`AggregateRoot`/`Process` require "≥ 1 identity field" so a composite key of two or more identity rows is admitted without saying so; `NestedEntity` identity "local to the owner" is prose the schema cannot express and no reader rule enforces. | FR-004 Behavior table rows entity, nested_entity, aggregate_root, process | missing-requirement |
| FND-107 | low | Negative fixtures assert only that the error message "contains its `expect:` code"; five of the eight named cases all surface as `semantic.record-invalid`, so a fixture that fails for the wrong schema rule still passes. | FR-005 Behavior (negative fixture bullet), FR-005-AC-5, TC-054 | correct-requirement-no-evidence |
| FND-108 | low | Generator failure policy is incomplete: nothing says `--check` writes nothing (it otherwise edits `manifest.yaml` digests), nothing says a `tsp compile` failure or an emission of zero module-base files fails the build rather than emptying `schemas/`, and nothing says whether `npm ci` (lockfile-exact) is the install path that makes the 1.15.0 pin hold. | FR-002 Behavior, FR-002-CON-3, FR-002-AC-4 | missing-requirement |
| FND-109 | low | Digests are over raw bytes with "no line-ending normalization" (quoin FR-073), but the spec sets no `.gitattributes` `eol=lf` rule for `schemas/*.json` and `manifest.yaml`; a checkout under `core.autocrlf=true` installs with `semantic.data-schema-digest-mismatch`. | FR-002 Outputs, FR-003-AC-2 | missing-requirement |
| FND-110 | low | "If the installed Quire wheel lacks `extract_semantic`, the semantic tests SHALL skip" makes the gate green on an old wheel; FR-003-AC-4, FR-004-AC-2..10, FR-005-AC-1..5 and NFR-001 all pass vacuously in that environment. | FR-005 Behavior (last bullet), tests.md rows TC-024..TC-063 | wrong-requirement |
| FND-111 | low | Refusal granularity is unstated: under quire-rs FR-069 one bad digest, `$id`, or `$ref` fails every object type of the module (`ArchetypeLoadFailure` x10), and quoin refuses the whole install; FR-003-AC-6 says "refused naming the path" without saying that all ten archetypes disappear, which is what a consumer of this fixture module will observe. | FR-003 Behavior (loader bullet), FR-003-AC-6, IT-002-SC-02 | missing-requirement |

## Finding Detail

### FND-100 (high): NFR-001 cannot hold under the FR-004 required keys

Grounding, all in the engine the spec names as its validator (quire 0.46.0):

- `surface.rs` `declaration_record()` emits only `fields`, `clauses`,
  `operations`, each omitted when its `Option` is `None`.
- `properties.rs`: a bullet-list or free-column `## Properties` sets `fields`
  `unavailable` (`legacy-form`), `fields: None`. `clauses.rs`: an
  `## Operations` section with no `### <name>` heading yields
  `operations: Some([])`, `available`; an absent section yields `None`.
- `validate_document.rs` `semantic_findings()`: after collecting diagnostics it
  calls `arch.data_validator().validate(&record.declaration_record())`
  unconditionally and pushes `semantic.record-invalid` as an **error**.

Consequence per 0.2.0 skeleton under the FR-004 table:

| 0.2.0 skeleton | record produced | FR-004 rule violated | finding |
|---|---|---|---|
| entity (bullet list) | `{}` | `fields` required | error |
| value_object (bullet list) | `{}` | `fields` required | error |
| nested_entity (`## Parent` only) | `{}` | `fields` required | error |
| aggregate_root (`## Members` only) | `{}` | `fields`, `clauses` required | error |
| event (`## Schema` only) | `{}` | `fields` required | error |
| process (`## Workflow` only) | `{}` | `fields` required | error |
| state_machine (mermaid only) | `{}` | `operations` required | error |
| repository (bullet list under `## Operations`) | `{ operations: [] }` | `operations` minItems 1 | error |
| domain, enumeration | `{}` | none | passes |

NFR-001 targets "Legacy-form 0.2.0 entity skeleton under 0.3.0: error
findings 0" and its statement covers "every artifact that validated against
0.2.0". Both are false by construction; TC-061 will be red on the first run.
FR-004-AC-9 ("`{}` fails against every other type") is the same rule stated
from the schema side, so the two requirements assert opposite outcomes for the
same input.

A fix must say one of:

1. **Upstream gate (recommended, keeps the roles).** Add to FR-003 or FR-004:
   "Quire SHALL validate the declaration record against the data schema only
   when every kind the schema requires is `available`; a record with an
   `unavailable` or `not_applicable` required kind is reported by that kind's
   own diagnostic and not by `semantic.record-invalid`." File it against
   quire-rs FR-072 and list it in the spec Dependencies as blocking; NFR-001's
   Verification then names the quire version that carries it.
2. **Schema side.** Make every key optional and move the role rules under
   `if fields present then …` (`dependentSchemas`), and reword FR-004-AC-2/4/5/6
   and AC-9 so "a record with no `fields` fails" becomes "a record with an
   empty `fields` fails". This loses "entity without a Properties table is
   refused", which the negative fixture list in FR-005 currently relies on.
3. **Narrow NFR-001.** Restate the target as "at most one
   `semantic.legacy-properties-form` warning and one `semantic.record-invalid`
   error" and drop "with at most warning-level semantic findings". This
   contradicts the ticket merge gate ("advisory-only until corpus promotion")
   and should be refused unless Peter dispositions it.

Whichever is chosen, extend the NFR-001 measurement from one entity skeleton
to a checked-in 0.2.0 copy of all ten skeletons (the current
`spec_objects_business/skeletons/` on `main`), because the entity row is the
only one the metric table measures.

### FND-101 (medium): two authorities for one declaration

FR-005 keeps the 0.2.0 kernel sections "exactly as the manifest asserts them"
and adds the typed sections beside them. For four types the same fact is now
authored twice with no rule tying the copies together:

- `event`: `## Schema` JSON fence (`schema_json`, required) declares the
  payload; `## Properties` declares `fields` with the required `Timestamp`
  row. Nothing says the fence's `properties` must equal the table's rows, so
  `occurred_at` can be renamed in one and not the other and every AC passes.
- `state_machine`: the mermaid `stateDiagram-v2` (required) carries the
  states and trigger labels (`place`, `capture_payment`); FR-004 requires
  `operations` "(each transition command)" and admits `transitions[]`, with
  no rule that the `### <name>` operations equal the diagram's trigger set.
- `aggregate_root`: `## Members` prose (required) beside optional
  `members: RelationDecl[]`; `nested_entity`: `## Parent` beside `owner`;
  `process`: `## Workflow` mermaid beside `steps[]`.

quoin FR-072's rationale ("one clause has one language and one editable
authority") is the principle this spec should carry over. Fix: add to FR-005
Behavior "Where a type carries both a kernel section and a typed section that
declare the same facts (`event` `## Schema`/`## Properties`; `state_machine`
`## States & Transitions`/`## Operations`), the typed section SHALL be the
authority and the kernel section a derived view; the negative fixture set
SHALL include one case per pair where the two disagree, failing with a named
reason" — and, since quire has no such check today, either add a module test
that diffs them (TC) or state that disagreement is unverified until the
extractor reads the kernel section (owner: quire-rs).

### FND-102 (medium): the resolution key for cross-references is undefined

FR-005 says "Every `Type` cell that names another skeleton SHALL use that
skeleton's frontmatter `title` (an `Identifier`)". Three failure modes:

1. Four current titles are not Identifiers (`Order Management`, `Order state
   vocabulary`, `Order Lifecycle`, `Order Fulfilment`); nothing requires the
   0.3.0 skeletons to retitle, and a `Type` cell with a space is
   `semantic.invalid-type-token` (error), not `unresolved`.
2. quire FR-070 resolves `id` before `names`, and the bundle index carries
   `id`, `title`, and `name`; the spec does not require the ten titles (and
   ids) to be pairwise distinct across all three name slots, so a shared name
   is `semantic.ambiguous-type` and FR-005-AC-3 fails.
3. Kernel scalar names win at precedence step 1: a value object titled
   `Duration` or `String` is silently typed as the scalar with no finding.

Fix: add to FR-005 Behavior "Every skeleton's frontmatter `title` SHALL be a
semantic-core `Identifier`, distinct from every other skeleton's `id`,
`title`, and `name`, and outside the `KernelScalar` set; a violation is a
module test failure" and a TC row for it.

### FND-103 (medium): roles are distinct by rule, not by record

Pairwise rule difference (FR-004-AC-1) is weaker than the description's
claim. A record `{ fields: [{ name: id, type: { target: UUID }, identity: true }] }`
validates against `Entity.json`, `NestedEntity.json`, and `Process.json`;
the three differ only in which *optional* keys they admit and which they
forbid. If the intent is classification by shape, the fix is a discriminating
required key (e.g. `NestedEntity` requires `owner`, `Process` requires
`steps` with `minItems 1`), which FR-004's own "optional because today's
extractor does not populate it" rule forbids. If the intent is
schema-per-type with the archetype name as the discriminator, reword the
Description to say so and delete "rather than by name alone"; and add to
FR-004-CON-2 the statement that record disjointness across types is not a
goal.

### FND-104 (medium): only `Type` cells are resolved

FR-004 Behavior: "Every cross-reference a declaration makes (`type.target`,
`RelationDecl.target`, `emits`, `persists`, `source`) SHALL be a `SemanticId`
or `KernelScalar` … reported by the extractor rather than silently accepted
as a string." The extractor (`properties.rs` `map_type`) reports
`semantic.unresolved-type` for `Type` cells only. `emits`, `persists`,
`source`, `ProcessStep.consumes/emits`, and `Transition.emits` are
pattern-validated strings the schema accepts whatever they name; the spec
itself says the extractor does not populate them. `Transition.from`/`to`
and `trigger` are `Identifier`s with no rule that `from`/`to` name a value
in `states` or that `trigger` names an `operations[].name`. Fix: split the
bullet into (a) `type.target`: resolved and reported now, and (b) the
remaining keys: schema-shape only, resolution deferred to the extractor
ticket that populates them (name it), and add to `Transition` "reader rule:
`from` and `to` SHALL name a `states[].value`; `trigger` SHALL name an
`operations[].name`" so the rule exists when the key is filled.

### FND-105 (medium): IT-002 leaves the operator's machine in an unstated state on failure

Step 5 restores only when steps 1..4 ran; a failure at step 2 (install
rejected part-way) or step 3 has no defined recovery, and the prior module
entry recorded in step 1 is the only copy. Fix: make step 5 unconditional
("SHALL run whether or not steps 2..4 passed"), and add SC-06 "on any failure
the listing equals the step-1 recording". Replace the absolute path with
"the Quoin build under test" and record its commit in the result, so the test
is runnable outside this workstation.

## Checklist Coverage

### Extension points (trust boundaries)

- `make schemas` / `scripts/generate-schemas.mjs` calling `tsp compile`:
  failure policy partly stated (version mismatch fails naming both); compile
  failure, zero emitted files, and `--check` purity are not (FND-108).
- Negative fixtures' `expect:` frontmatter: strict (test fails), but the
  match is code-only (FND-107).
- Quire wheel absent/old: resilient by skip (FND-110).
- Quoin/Quire refusing the manifest: strict, module-wide (FND-111).

### Entity identity

- Object types: keyed by manifest `name`, unique by schema (fine).
- Fields: unique by `name` (semantic-core reader), stated by reference.
- Skeleton cross-references: key undefined (FND-102).
- Identity fields: cardinality and locality unstated (FND-106).
- Clauses and operations: unique by `clauseId`/`name` per artifact via quoin
  FR-072 (fine).

### Evaluation purity

- Generator edits `manifest.yaml` digests during a build; `--check` mode not
  declared read-only (FND-108).
- IT-002 mutates global state (FND-105).
- Kernel-section vs typed-section dual authority (FND-101).
- Clause fences are carried verbatim, never evaluated (quire FR-071-CON-1):
  fine.

### Topological robustness

- `$ref` graph: cycles refused by both consumers (`semantic.schema-ref-cycle`);
  the ten models plus `IdentityField`, `OccurrenceField`, `Term`,
  `Transition`, `ProcessStep`, `StepKind` form a DAG onto semantic-core.
  No finding.
- Bundle index over skeletons: lookup, not traversal; no cycle risk. No
  finding.
- State graph (`states`/`transitions`): no reachability, terminal-state, or
  membership rule (FND-104); acceptable while the extractor does not populate
  it, provided the rule is written down for when it does.

## Proposed Additions

- **FR** (FR-003 or FR-004): declaration-record validation precondition, or
  the schema-side conditional rules — one of the three FND-100 options, with
  the upstream quire-rs ticket recorded as a blocking dependency.
- **NFR** (NFR-001): extend the measurement to all ten 0.2.0 skeletons.
- **FR** (FR-005): typed section is the authority where a kernel section
  overlaps it (FND-101); skeleton titles are distinct Identifiers outside the
  kernel scalar set (FND-102).
- **FR** (FR-004): reader rules for `Transition.from/to/trigger`; scope the
  "reported by the extractor" claim to `type.target` (FND-104); identity
  cardinality and nested-entity locality (FND-106).
- **IT** (IT-002): unconditional restore step and machine-independent
  preconditions (FND-105).
- **FR** (FR-002): `--check` writes nothing; compile failure and empty
  emission fail the build; `npm ci` is the install path (FND-108); add a
  `.gitattributes` `eol=lf` rule for `schemas/*.json` and `manifest.yaml`
  (FND-109).
- **FR** (FR-005): replace skip-on-old-wheel with a hard failure naming the
  minimum Quire version, or pin the wheel in the test dependency set
  (FND-110).

## Dispositions

| Finding | Disposition |
|---|---|
| FND-100 | Applied as option 1 (upstream gate), without relaxing a schema: `agent-ix/quire-rs#391` records the engine defect (an `unavailable` kind validated as `{}`), `spec.md` Out of Scope names it, NFR-001 Verification states that NFR-001-AC-2 is unsatisfiable by any module schema until it lands, and TC-061 is an explicit expected failure naming it. FR-004's required keys are unchanged. NFR-001's measurement is extended from the entity skeleton to the checked-in 0.2.0 skeleton set, as the finding's closing paragraph asks. |
| FND-101 | Applied: FR-005 Behavior states that where a typed section and a kernel section declare the same facts the typed section is the authority and the kernel section a derived view, and enumerates the pairs. |
| FND-102 | Applied: FR-005 Behavior requires every skeleton `title` to be an `Identifier`, distinct across the skeletons and outside the `KernelScalar` names; FR-005-AC-8 and TC-059 verify it. |
| FND-103 | Applied: FR-004's Description no longer claims record disjointness — it claims that each role refuses the records that violate its own rules, and says why full pairwise disjointness is not claimed. FR-004-CON-2 restated accordingly. |
| FND-104 | Applied: the cross-reference bullet now scopes resolution and the `semantic.unresolved-type` finding to `type.target` (quire-rs FR-070) and defers the other keys to `agent-ix/quoin#335`; the `Transition.from`/`to`/`trigger` membership rules are stated as reader rules and explicitly not claimed as schema refusals. |
| FND-105 | Applied: IT-002 step 5 is unconditional, IT-002-SC-06 asserts that it runs after a failure, and the developer path is replaced by `<checkout>`. |
| FND-106 | Applied: FR-004 Behavior states that a composite key (two or more identity rows) is admitted, and that nested-entity identity locality is prose the schema does not express. |
| FND-107 | Recorded, no change to the criterion; the implementation asserts the failing schema path or diagnostic detail per fixture, not the code alone, so a fixture that fails for the wrong rule does not pass. |
| FND-108 | Applied: FR-002 Behavior adds `--check` writes nothing, a `tsp compile` failure or zero module models exits non-zero without touching committed output, and the Node 20 / missing-`tsp` failure. |
| FND-109 | Applied: FR-002 Behavior requires the `.gitattributes` `eol=lf` rule for `*.json` and `*.tsp`. |
| FND-110 | Applied: the skip clause is gone. See dependency.md FND-141. |
| FND-111 | Applied, with the granularity corrected against the engine: FR-003 Behavior now states what quire 0.46.0 actually does — a refused schema drops that object type alone, while an unknown `semantic` key drops every object type of the module. The finding's "all ten archetypes disappear" reading holds for the unknown-key case only. Both refusals are silent; `agent-ix/quire-rs#221` and `agent-ix/quire-rs#394` record that, and FR-003-AC-6's naming half is an explicit expected failure citing them. |
