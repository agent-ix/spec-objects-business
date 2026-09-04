---
id: Task-009
title: "IT-002 — Quoin install roundtrip with unconditional state restore"
type: Task
status: blocked
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-business/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-business/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-business/IT-002
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-027
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-070
    type: verifies
---
# Task-009: IT-002 — Quoin install roundtrip

## Scope

Demonstrate the boundary between the shipped module directory and the Quoin module
installer, and leave the operator's machine exactly as it was found.

## Subtasks

- [ ] **Record first.** Capture `quoin module` output, including any existing `spec-objects-business` entry (source, ref, sha).
- [ ] **Install.** `quoin module install path:<checkout>/spec_objects_business` — exit 0, no `semantic.*` diagnostic at error severity.
- [ ] **List.** `quoin module` contains `spec-objects-business` sourced from the path.
- [ ] **Inspect.** `semantic/package-manifest.json` exists with `package.identity` `agent-ix/spec-objects-business` and one export per `semantic.exports` entry. This is a contract check on quoin FR-075, not a claim this module owns.
- [ ] **Restore unconditionally.** Re-install the recorded source and ref, or remove the module if none was installed — whether or not the earlier steps passed. Assert that `quoin module` equals the step-1 recording (SC-05) and that the restore ran after a failure (SC-06).

## Deliverables

- The recorded demonstration transcript with the Quoin commit under test
- Tests/rows for TC-027 and TC-070

## Notes

- No released Quoin carries the semantic installer (`agent-ix/quoin` main `3e842ce`,
  no tag contains it), so the criterion stays `Demonstration` and the precondition
  names the build rather than a version. When a release carries FR-070/FR-073/FR-075,
  retype FR-003-AC-5 and script this against a temporary Quoin home.
- The install mutates global state. The restore step is the deliverable, not an
  afterthought.
