---
title: Add a receiving role to a process step
type: how-to
description: Describe the role that accepts a handoff from a business process step.
engine_version: 0.63.2
---

# Add a receiving role to a process step

Add a `Receiver` cell to describe the role that accepts a process handoff.

## Before you start

Use Quire engine 0.63.2 or later and a module version containing typed process receivers. Run the commands from this repository's root.

Declare the receiving role as a `RoleSpec` artifact in the composed bundle. The example uses the role ID `ROLE` from the process module. Load that module when validating the composed bundle.

## Steps

1. Use a `Steps` table for the process. Place `Receiver` after `Emits` and before `Description`.
2. Enter one role reference in each step that hands off work. Use the role's exact ID in `ix://agent-ix/spec-artifacts-process/ROLE`.
3. Save this example as `process.md`, replacing the role reference with your receiving role:

   ```markdown
   ---
   id: PROCESS-HANDOFF
   title: Receive a request
   type: process
   object: process
   ---

   # Receive a request

   ## Properties

   | Field | Type | Multiplicity | Constraints |
   |---|---|---|---|
   | correlation_id | UUID | 1..1 | identity |

   ## Steps

   | Step | Kind | Consumes | Emits | Receiver | Description |
   |---|---|---|---|---|---|
   | accept_request | command | | | ix://agent-ix/spec-artifacts-process/ROLE | Receive the handoff |
   ```

   A step without a handoff can leave `Receiver` empty. You can also omit the entire column. Existing five-column `Workflow` tables remain valid.

4. Extract the process fields:

   ```sh
   quire extract process.md --module spec_objects_business
   ```

## Expected output

The extraction's `steps` field contains the step name, kind, receiving-role reference, and description. Its `edges` list includes the role ID as a reference target:

```json
{
  "target": "ROLE",
  "type": "references"
}
```

The receiver describes a role. Staff assignments and authorization remain decisions recorded by their owners.

## Verify the result

Check that the extracted reference names the intended role. When validating the composed bundle, resolve it to the declared `RoleSpec`; a different artifact type or an absent target is invalid.

From the repository root, run the compatibility and typed-reference checks:

```sh
poetry run pytest tests/test_model_tables.py -k process_step_receiver --no-cov
```

The check covers a populated receiver, an empty cell, the earlier receiverless `Workflow` shape, and invalid targets.
