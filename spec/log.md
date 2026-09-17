---
type: log
title: "Update Log"
description: "Chronological log of structural changes to this bundle."
---
# Update Log

## History

* **2026-06-15** — Adopted OKF-compatible bundle structure with directory indexes.
* **2026-09-03** — Issue #4 (semantic data schemas): added US-001, FR-002..FR-005, NFR-001, IT-002; converted `tests.md` to a `TestMatrix`; spec scope extended to the TypeSpec-emitted schemas and the semantic-module contract.
* **2026-09-03** — Issue #4 review round: eight SpecReviews under `spec/reviews/4-semantic-data-schemas/` (base, dependency, EARS, evidence, failure-domain, integrity, risk-complexity, scope-boundary); every high and every real medium applied, each with a recorded disposition. Filed `agent-ix/quire-rs#392` (publish the 0.46.0 wheel to a committable index) and pinned filament-core-service `a77f31e` across FR-001, FR-003 and IT-001.
* **2026-09-16** — Issue #4 model features: added FR-006 (object-type model tables as manifest `table_row` locators); FR-003 pins semantic-core 0.2.0, manifest 0.4.0 and the FR-075 mapping tokens; FR-005 skeletons author `quire` clauses, `Requires:`/`Ensures:` lines and the model tables; NFR-001 measures additivity outside the model tables.
* **2026-09-16** — Issue #4 review of PR #8: added the `population` object type (FR-004, FR-006); every skeleton and fixture clause is valid Quire (FR-006 clause rules, TC-084 Inspection); `specializes` declared in `edge_types`; FR-003 posture `strict` and the FR-075 tokens separated from the quoin mapping ids; FR-006 states the target optional columns (`agent-ix/filament-core-service#31`); NFR-001 states where the contract is additive and where it is strict.
* **2026-09-17** — Issue #9 relations: added FR-007 (the quoin FR-104 `## Relationships` table on `entity` and `aggregate_root`, every `allowed_links` verb declared in `edge_types`); FR-003 adds the `relationships` mapping token and manifest 0.5.0; NFR-001 names the table as strict; `persists`, `source`, `owner` and `emits` stay on `agent-ix/quire-rs#435`.
* **2026-09-17** — PR #10 review: FR-007 pins quoin FR-104 at `99bd4f0`, drops `min_rows`, states the module-wide Relationships break (NFR-001), the sealed-type `semantic.record-invalid` refusal (`agent-ix/quire-rs#440`), the no-bundle-index target limit (`agent-ix/quoin#557`), and `emits` as a table verb that `agent-ix/quire-rs#435` derives from the rows.
* **2026-09-17** — PR #10 re-check: FR-007 adds the Relationships table on `process` and `repository`, whose rows lower into `emits` and `persists` (AC-9, expected failure on `agent-ix/quire-rs#435`); FR-004 `Process` gains optional `emits`; a header-only table on a type without the locator is refused too (FR-007, NFR-001).
