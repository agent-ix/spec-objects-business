"""QSpec FR-208 meaning-vocabulary refusal tests (agent-ix/spec-objects-business#15).

FR-008 binds each object type to a QSpec FR-208
(`agent-ix/quire-specification` `c8e3ca0`,
`spec/objects/foundation/FR-208-quire-meaning-vocabulary.md`) meaning id.
FR-208 states intake refusals for that meaning; this module's own record
schema (FR-004) must refuse the forms it governs. Several of the exercised
keys are not populated by the extractor yet, so — like
``tests/test_role_schemas.py`` — these are schema evidence, not extraction
evidence (`agent-ix/quoin#335`).

Not exercised here: FR-208 also refuses a non-empty operation frame
(`Modifies:`/`Creates:`/`Deletes:`) on a persistence interface. That data
reaches no member of `Repository.json`'s record (FR-006, blocked on
`agent-ix/quire-rs#431`), so this module cannot refuse it at the
record-schema layer.
"""

from __future__ import annotations

import pytest

from tests.conftest import object_type
from tests.test_role_schemas import CLAUSE, OPERATION, RELATION, field, ok


@pytest.mark.trace("TC-109", "FR-008-AC-7")
def test_value_object_refuses_an_operation(schema_registry):
    """FR-208 `record-value-type/v1`: an operation is `unsupported_construct`."""
    value_object = schema_registry("ValueObject")
    record = {"fields": [field("amount", "Decimal")]}
    assert ok(value_object, record)
    assert not ok(value_object, {**record, "operations": [OPERATION]})


@pytest.mark.trace("TC-109", "FR-008-AC-7")
def test_event_refuses_an_operation(schema_registry):
    """FR-208 `event-type/v1`: an operation is `invalid_model_binding`."""
    event = schema_registry("Event")
    record = {"fields": [field("occurred_at", "Timestamp")]}
    assert ok(event, record)
    assert not ok(event, {**record, "operations": [OPERATION]})


@pytest.mark.trace("TC-109", "FR-008-AC-7")
def test_repository_refuses_a_clause(schema_registry):
    """FR-208 `persistence-interface/v1`: a `quire` clause is
    `unsupported_construct`."""
    repository = schema_registry("Repository")
    record = {"operations": [OPERATION]}
    assert ok(repository, record)
    assert not ok(repository, {**record, "clauses": [CLAUSE]})


@pytest.mark.trace("TC-109", "FR-008-AC-7")
def test_repository_refuses_an_operation_contract(schema_registry):
    """FR-208 `persistence-interface/v1`: a `Pre:`/`Post:` contract is
    `unsupported_construct`; an operation with no contract still passes."""
    repository = schema_registry("Repository")
    assert ok(repository, {"operations": [{**OPERATION, "pre": [], "post": []}]})
    assert not ok(repository, {"operations": [{**OPERATION, "pre": [CLAUSE]}]})
    assert not ok(repository, {"operations": [{**OPERATION, "post": [CLAUSE]}]})


@pytest.mark.trace("TC-109", "FR-008-AC-7")
def test_domain_refuses_a_field_an_operation_and_a_clause(schema_registry):
    """FR-208 `namespace/v1`: a field or an operation is `invalid_model_binding`;
    a `quire` clause is `unsupported_construct`."""
    domain = schema_registry("Domain")
    record = {"members": [RELATION], "vocabulary": [{"term": "Order", "doc": "…"}]}
    assert ok(domain, record)
    assert not ok(domain, {**record, "fields": [field("anything")]})
    assert not ok(domain, {**record, "operations": [OPERATION]})
    assert not ok(domain, {**record, "clauses": [CLAUSE]})


@pytest.mark.trace("TC-109", "FR-008-AC-7")
def test_repository_and_domain_admit_no_specializes_link():
    """FR-208: `supertypes` on a persistence interface or a namespace is
    `unsupported_construct`. Neither is field-bearing (FR-006-AC-7), so
    neither declares `specializes` in `allowed_links`; a `specializes`
    relationship naming either is already refused as an unadmitted edge
    (quire-rs FR-076)."""
    for name in ("repository", "domain"):
        assert "specializes" not in object_type(name)["allowed_links"], name
