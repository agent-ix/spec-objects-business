---
id: SR-020
title: "Spec review — PR #54 FR-011 and the FR-003/004/005/007/008 edits"
type: SpecReview
analysis: base
scope: "agent-ix/spec-objects-business; spec/functional/FR-011-variant-set-and-graph.md, FR-003, FR-004, FR-005, FR-007, FR-008 edits, spec/spec.md, spec/tests.md TC-118..TC-121, spec/integration/IT-002 (PR #54)"
review_set: subset
---
# SR-020: Spec review — PR #54

## Summary

Ticket: PLAT-160. Reviewed the new FR-011 (statement, Behavior, AC-1..4,
Dependencies), the count-free edits to FR-003, FR-004, FR-005, FR-007, FR-008,
IT-002 and spec.md, and the tests.md rows TC-118..TC-121, against FR-010 and
quire-rs `origin/main` FR-081. `quire validate` on the changed files reports
FR-011 clean. The failures it reports in `spec/tests.md` are on the existing
TC-085 row, which this PR does not touch.

Clean parts: the type split is argued well. An `enumeration` is payload-free,
and its construct meaning is a closed set of named cases with no payload, so a
payload union is new. A `graph` has no current state, so it is not a
`state_machine`. FR-008-AC-1 states why neither type declares a construct.
FR-004's table rows and AC-9 match the schemas. No leftover "eleven" or "ten
object types" count remains in `spec/`. The ten-construct-kinds count in
FR-008 is a real fact, not a type count.

## Verdict

**NOT MERGEABLE as written.** FR-011 says the `## Variants` table is read only
by this manifest's body extraction, while FR-010 makes `record-sections`
module-wide and quire-rs FR-081 reads `## Variants` into the `variants` record
key. FR-011 also declares a record key that FR-010's owner list forbids
(FND-001). FR-011-AC-1 is ambiguous (FND-002). The rest are low.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
|---|---|---|---|---|
| FND-001 | high | FR-011 says "The Quire engine reads no model table for either type, so the `## Variants` table and the `## Graph` fence are read by this manifest's body extraction only". With `record-sections` named module-wide (FR-010), quire-rs FR-081 matches `## Variants` to the `VariantSet` property `variants` and reads the table into the record. FR-011 also declares `variants` in `VariantSet`, which FR-010 Behavior's exhaustive owner list does not admit. That violates FR-010-AC-1 as written. FR-011 must state which mapping owns `variants`, with columns that FR-081 can read into `VariantDecl`, and FR-010's owner list must name it. Otherwise drop `variants` from the record. | spec/functional/FR-011-variant-set-and-graph.md:45, spec/functional/FR-011-variant-set-and-graph.md:41, spec/functional/FR-010-record-key-owners.md:48 | wrong-requirement |
| FND-002 | medium | FR-011-AC-1 says "`graph` admits `references` and no other verb, including `event`, `process`, `entity` and `graph`". It can be read as excluding those four types. It also does not fix the seven targets the Behavior states, so a test of it cannot fail on a dropped target (SR-019 FND-001). | spec/functional/FR-011-variant-set-and-graph.md:51 | wrong-requirement |
| FND-003 | low | FR-007 still lists the types with no `relationships` locator as `value_object`, `nested_entity`, `event`, `state_machine`, `enumeration`, `population`. `variant_set` and `graph` declare none either, and their sealed schemas refuse `relations` the same way. | spec/functional/FR-007-relationships-table.md:60 | wrong-requirement |
| FND-004 | low | Clause authoring differs between the two new types and FR-011 does not say so. `variant_set` declares an optional `invariants` locator, and its skeleton calls `## Invariants` "prose rules over the whole set", although FR-005 makes an Invariants section `### <clauseId>` plus one `quire` fence. `Graph.json` declares `clauses`, but `graph` has no `invariants` locator. | spec_objects_business/skeletons/variant_set.md:14, spec/functional/FR-011-variant-set-and-graph.md:42 | wrong-requirement |
| FND-005 | low | FR-011 says a graph holds "one `mermaid` fence" of nodes and edges. The `code_block` locator accepts the first fence of any mermaid diagram kind, and a second fence is not refused. FR-011's limits statement names only payload resolution and acyclicity as author rules. Add one fence and the `flowchart`/`graph` kind to it. | spec/functional/FR-011-variant-set-and-graph.md:39, spec/functional/FR-011-variant-set-and-graph.md:45 | wrong-requirement |

## Gates Run

`quire validate --scope .` on the changed spec files (quire 0.36.2, engine
0.50.2): FR-011 clean. `quoin validate --strict` (quoin 0.29.1): no findings.
