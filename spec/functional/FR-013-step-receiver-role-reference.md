---
id: FR-013
title: "Declare typed receiving roles on process steps"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-020"
    type: "depends_on"
---
# FR-013: Declare typed receiving roles on process steps

## Description

When a business process step hands off work, the `Workflow` table SHALL accept
one typed receiver reference to a `RoleSpec` artifact. The validator SHALL
reject an unresolved receiver or a receiver that targets another artifact
type. Processes without a receiving role SHALL remain valid when the `Receiver`
column is absent or empty.

## Behavior

- The `Workflow` table SHALL admit an optional `Receiver` column after `Emits`
  and before `Description`. An empty cell or an absent column SHALL mean that
  the step does not declare a receiving role.
- A non-empty `Receiver` cell SHALL contain one `SemanticId` that identifies a
  `RoleSpec` artifact declared by `spec-artifacts-process`.
- Extraction SHALL preserve the receiver on the corresponding structured
  `ProcessStep` record. Each step SHALL have at most one receiver.
- Validation SHALL resolve each non-empty receiver against the composed bundle
  and SHALL reject a missing target or a target whose artifact type is not
  `RoleSpec`.
- A receiver SHALL describe the role responsible for accepting a handoff.
- The module SHALL NOT use a receiver reference to assign a person, authorize
  an action, select a runtime recipient, or execute a step.
- A process step without a handoff SHALL omit the `Receiver` value.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-013-CON-1 | The module's qualification suite SHALL mark receiver extraction and target-kind validation as unavailable until the engine emits structured `ProcessStep` records and resolves receiver `SemanticId` values against the composed bundle. | Compatibility | Inspection |
| FR-013-CON-2 | The Business manifest SHALL mark `Receiver` as an optional column once the module-manifest schema admits the optional-column facet. | Compatibility | Test |
| FR-013-CON-3 | Existing process documents without a `Receiver` column SHALL remain valid when checked by an engine that supports the optional-column facet. | Compatibility | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-013-AC-1 | The process `Workflow` locator declares `Receiver` after `Emits` and before `Description`, and marks it optional. | Inspection |
| FR-013-AC-2 | A process with no `Receiver` column and a process with an empty `Receiver` cell both remain valid and preserve their existing step data. | Test |
| FR-013-AC-3 | A populated `Receiver` cell containing a `RoleSpec` SemanticId is extracted on its corresponding `ProcessStep` and resolves to the declared role artifact in a composed bundle. | Integration |
| FR-013-AC-4 | A receiver that resolves to a non-`RoleSpec` artifact is rejected with `disallowed-edge-target`. | Integration |
| FR-013-AC-5 | A receiver that names no artifact is rejected as an unresolved target. | Integration |
| FR-013-AC-6 | A receiving-role reference is descriptive metadata only; it does not trigger a step, grant authority, or assign a person. | Inspection |

## Dependencies

- **Process role definition**: [FR-020](ix://agent-ix/spec-artifacts-process/FR-020) declares the `RoleSpec` artifact type.
- **Table shape**: [FR-006](./FR-006-model-table-locators.md) declares the `Workflow` table locator.
- **Engine capability**: the engine must preserve model-table rows as structured `ProcessStep` records, admit an optional `Receiver` table column, and resolve the receiver's target kind in the composed bundle before the behavior in this requirement can be qualified.
