---
id: FR-010
title: "Give every record key one owner and one authored form"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-business/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-business/FR-004"
    type: "refines"
  - target: "ix://agent-ix/spec-objects-business/FR-006"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-business/FR-007"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-123"
    type: "depends_on"
---
# FR-010: Give every record key one owner and one authored form

## Description

The module SHALL declare in each record schema only keys that quoin FR-123 (and
FR-071, FR-072, FR-104, FR-121, quire-rs FR-075 and FR-076) give exactly one
authored source, and SHALL name in its manifest and skeletons the sections that
fill them, so that no key is authored twice. A key that has no source (the unmapped keys
below) is stated as such and never filled by a second form.

## Inputs

- quoin FR-123, its "Downstream, `agent-ix/spec-objects-business`" list, and
  FR-121 for the `record-sections` token and the `## Source` inline-code id.
- The enumeration `## Values` table `Value | Description` that FR-006 already
  declares as the `values` locator with `min_rows: 1`. quoin FR-071 now
  publishes the same form, so the list form `- value — doc` stays refused
  (FR-006-AC-4) and no module change is needed for it.

## Outputs

- `Process.json` declaring `states`, `Domain.json` declaring `relations`, and
  `Domain.json` and `NestedEntity.json` declaring neither `members`,
  `ubiquitous_language` nor `owner`.
- `record-sections` in the manifest `semantic.mappings`, an event `source`
  locator, and a `## Source` section in the `event` skeleton.
- A `relationships` locator and a `## Relationships` table on `domain`.
- An `aggregate_root` skeleton that authors membership once.

## Behavior

- Every top-level key of every record schema SHALL be, for its own object type, one of: `fields`, `clauses`, `operations`, `operationExpressions` (FR-071, FR-072), `relations` (FR-104), `emits`, `persists` (FR-076, from `## Relationships` rows), `source` (FR-121), `values`, `states`, `transitions`, `steps`, `vocabulary` (FR-123), `members` of `aggregate_root` (FR-123), or one of the unmapped keys `members` and `extent` of `population` (FR-123-AC-8 lists population `members` as unmapped; `extent` is in no owned list). A key outside that list for its object type fails FR-010-AC-1.
- `population` `members` and `extent` SHALL be unmapped: no extractor copies them into the record, so they are declared for hand-built records only. The `population` frontmatter `extent` is the only authored form of `extent`, and no skeleton SHALL author an `## Extent` section, which the module-wide `record-sections` token would otherwise read as a second authored form. Its `## Members` table stays a model table (FR-006).
- No record schema SHALL declare `owner` or `ubiquitous_language`. The owner of a nested entity is the single inbound `aggregates` or `contains` edge the bundle declares for it, a bundle rule (`single_owner` in its construct, FR-008) that no per-artifact extraction carries; its `## Parent` section stays human-facing prose. The `ubiquitous_language` section prose stays a body-extraction string, not a record key; the structured key is `vocabulary`.
- `Domain.json` SHALL declare `relations` and no `members`, and the `domain` object type SHALL declare the FR-007 `relationships` locator, because a domain has no member table and its `contains` edges are domain relationships.
- `Process.json` SHALL declare `states` as `EnumValue[]`, matching the `process` `States` locator FR-006 declares, so a process with a `## States` table yields a record its schema accepts.
- The manifest `semantic.mappings` SHALL name `record-sections`, and the `event` object type SHALL declare an optional `source` locator (`section_body` after `Source`), whose section holds exactly one inline-code artifact id (`` `aggregate_root_001` ``, backticks and nothing else, the form FR-121 reads a scalar key from), the aggregate root that publishes the event.
- No skeleton SHALL author an `## Owner`, `## Extent`, `## Emits` or `## Persists` section; `emits` and `persists` are `## Relationships` rows.
- The `aggregate_root` skeleton SHALL author membership once, in `## Members`, and its `## Relationships` table SHALL carry no `aggregates` or `contains` row, because Quire derives that edge from the member table (quoin FR-123).

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-010-CON-1 | The module SHALL NOT copy a quire-rs or quoin fixture; the extraction of `values`, `states`, `transitions`, `steps`, `members`, `vocabulary` and `source` into the record is those repositories' to prove. | Boundary | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-010-AC-1 | Every top-level key of every shipped record schema is in the owner list above, none declares `owner` or `ubiquitous_language`, `Domain.json` declares `relations` and no `members`, and `Process.json` declares `states`. | Test |
| FR-010-AC-2 | A `Process` record with `states` entries validates and one whose entry lacks `value` fails; a `Domain` record with `relations` validates while one with `members` or `ubiquitous_language` fails. | Test |
| FR-010-AC-3 | The manifest `semantic.mappings` names `record-sections`; `event` declares the optional `source` locator; the `event` skeleton's `## Source` holds exactly one inline-code id, in backticks, naming an `aggregate_root` skeleton. | Test |
| FR-010-AC-4 | `nested_entity` keeps `## Parent` as a required prose locator, and no skeleton authors an `## Owner`, `## Extent`, `## Emits` or `## Persists` section. | Test |
| FR-010-AC-5 | The `aggregate_root` skeleton authors a non-empty `## Members` table and no `aggregates` or `contains` row in its `## Relationships` table. | Test |
| FR-010-AC-6 | The `domain` skeleton validates under the module's bundle package with a `## Relationships` table of `contains` rows. | Test |

## Dependencies

- **Upstream**: [FR-004](./FR-004-role-schemas.md), [FR-006](./FR-006-model-table-locators.md), [FR-007](./FR-007-relationships-table.md); quoin FR-123 and FR-121; quire-rs FR-075 and FR-076
- **Downstream**: quire-rs FR-081 (record-sections extraction, PLAT-1370, merged on quire-rs main) copies model entries to record keys and reads `## Source`, but the installed 0.54.0 wheel predates it; until a release carries it, `values`, `states`, `transitions`, `steps`, `members`, `vocabulary` and `source` are verified here as schema evidence and as `model` entries (FR-006-AC-2), not as extracted record keys.
