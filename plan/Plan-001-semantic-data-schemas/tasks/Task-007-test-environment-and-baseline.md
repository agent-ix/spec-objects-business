---
id: Task-007
title: "Test environment — Quire provisioning, the no-vacuous-skip gate and the 0.2.0 baseline"
type: Task
status: not_started
track: B
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-business/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-business/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-business/TC-018
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-019
    type: verifies
  - target: ix://agent-ix/spec-objects-business/TC-058
    type: verifies
---
# Task-007: Test environment, provisioning and the 0.2.0 baseline

## Scope

Make the semantic test dependency explicit and provisioned, make its absence a
failure rather than a skip, and freeze the 0.2.0 artifacts every compatibility check
compares against. This task runs first and independently of the generator.

## Subtasks

- [ ] **`make dev-quire`.** A documented target that installs the Quire wheel FR-005 Inputs names into the module's Python environment. It is the provisioning path, not a side install someone remembers to do.
- [ ] **Hard fail, never skip.** A shared test helper resolves Quire once; when the wheel is absent or lacks `extract_semantic`, every semantic test fails with a message naming the missing function, `make dev-quire`, and `agent-ix/quire-rs#392`. No semantic matrix row may pass or be reported green without the engine under test.
- [ ] **One named exception.** NFR-001-AC-2 / TC-061 is an explicit expected failure naming `agent-ix/quire-rs#391`. Nothing else is exempt.
- [ ] **Do not declare `quire` in `pyproject.toml`.** `internal-pypi` serves 0.33.0 at most and no `quire-rs` tag carries the semantic layer, so the only index with 0.46.0 is the dev-only `pypi.ix` and a committed source ref there would break CI. `agent-ix/quire-rs#392` is the blocking issue; when it publishes, this target is replaced by a committed dev dependency.
- [ ] **Freeze the 0.2.0 baseline.** Check in a copy of the 0.2.0 `body_extraction` block and of the ten 0.2.0 skeletons as read-only fixtures, captured before Task-004 or Task-005 changes anything.
- [ ] **Packaging and boundary inspections.** TC-018 (no `.npmrc`, no `file:`/`link:`, exact toolchain pins), TC-019 (`package-lock.json` resolves from npmjs except `@agent-ix/semantic-core`), TC-058 (the branch diff touches no corpus repository and no vendored fixture).

## Deliverables

- `Makefile` / poe target `dev-quire`
- `tests/conftest.py` engine-resolution helper and the hard-fail rule
- `tests/fixtures/baseline-0.2.0/` (locators + ten skeletons)
- Tests for TC-018, TC-019, TC-058

## Notes

- The whole point of this task is that a missing engine is visible. Do not add a
  skip marker, an `importorskip`, or a try/except that lets a semantic row report
  green on a machine with no Quire.
- Unblocks: Task-004 (needs the baseline), Task-008 (needs both).
