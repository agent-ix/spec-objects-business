"""Role-schema tests (FR-004): each object type's declaration schema accepts
the records its role
admits and refuses the records its role forbids.

Every record here is hand-built JSON validated against the shipped schema
files. The keys the installed engine does not populate yet (`relations`,
`members`, `states`, `transitions`, `steps`, `values`, `emits`, `persists`,
`source`, `vocabulary`) can be exercised no other way, so these are **schema
evidence, not extraction evidence** — the extraction path for them is quoin
FR-123 and its quire-rs successor. Tests that depend on it say so in their
docstring.
"""

from __future__ import annotations

import json

import pytest

from tests.conftest import (
    MODEL_OF,
    OBJECT_TYPES,
    SCHEMAS_DIR,
)


# Multiplicity.json requires `ordered`/`unique`; a
# producer clamps both `false` on a singular multiplicity (`upper` at most
# one — meaningless there, no functionality lost). Every field this helper
# builds is singular (1..1), so both are `false`.
def field(name: str, target: str = "String", *, identity: bool = False) -> dict:
    decl = {
        "name": name,
        "type": {
            "target": target,
            "multiplicity": {"lower": 1, "upper": 1, "ordered": False, "unique": False},
        },
    }
    if identity:
        decl["identity"] = True
    return decl


CLAUSE = {"language": "quire", "clauseId": "SomeInvariant"}
OPERATION = {"name": "get", "params": [field("order_id", "UUID")]}
SPAN = {
    "sourceIdentity": "ix://local/spec/spec",
    "path": "order.md",
    "startLine": 12,
    "startColumn": 1,
    "endLine": 12,
    "endColumn": 24,
}
EXPRESSION = {"kind": "expression", "text": "total > 0 and open()", "sourceSpan": SPAN}
RELATION = {
    "verb": "contains",
    "category": "structural",
    "target": "ix://agent-ix/spec-objects-business/type/OrderLine",
}


def ok(validator, record) -> bool:
    return not list(validator.iter_errors(record))


def why(validator, record) -> list[str]:
    return [error.message for error in validator.iter_errors(record)]


@pytest.mark.trace("TC-030", "FR-004-AC-1")
def test_every_object_type_schema_differs_from_every_other_and_none_is_bare(
    schema_registry,
):
    schemas = {
        name: json.loads((SCHEMAS_DIR / f"{MODEL_OF[name]}.json").read_text())
        for name in OBJECT_TYPES
    }
    fingerprints = {}
    for name, schema in schemas.items():
        assert set(schema) > {
            "$schema",
            "$id",
            "type",
        }, f"{name} is a bare `type: object`"
        assert schema["unevaluatedProperties"] == {"not": {}}, f"{name} is not sealed"
        fingerprints[name] = (
            tuple(sorted(schema.get("required", []))),
            tuple(sorted(schema.get("properties", {}))),
            json.dumps(
                {k: v for k, v in schema["properties"].items() if "contains" in v},
                sort_keys=True,
            ),
        )
    for left in OBJECT_TYPES:
        for right in OBJECT_TYPES:
            if left < right:
                assert (
                    fingerprints[left] != fingerprints[right]
                ), f"{left} and {right} are identical"


@pytest.mark.trace("TC-031", "FR-004-AC-2")
def test_entity_requires_fields_with_at_least_one_identity(schema_registry):
    entity = schema_registry("Entity")
    assert ok(entity, {"fields": [field("customer_id", "UUID", identity=True)]})
    assert not ok(entity, {"fields": [field("customer_id", "UUID")]})
    assert not ok(entity, {})
    assert not ok(entity, {"fields": []})


@pytest.mark.trace("TC-032", "FR-004-AC-3")
def test_value_object_refuses_identity_and_relations(schema_registry):
    """`relations` is exercised against a hand-built record: the extractor does
    not populate it (agent-ix/quoin#335)."""
    value_object = schema_registry("ValueObject")
    assert ok(value_object, {"fields": [field("amount", "Decimal")]})
    assert not ok(value_object, {"fields": [field("amount", "Decimal", identity=True)]})
    assert not ok(
        value_object, {"fields": [field("amount", "Decimal")], "relations": [RELATION]}
    )


@pytest.mark.trace("TC-033", "FR-004-AC-4")
def test_aggregate_root_requires_an_identity_field_and_at_least_one_clause(
    schema_registry,
):
    root = schema_registry("AggregateRoot")
    record = {"fields": [field("order_id", "UUID", identity=True)], "clauses": [CLAUSE]}
    assert ok(root, record)
    assert not ok(root, {"fields": record["fields"]})
    assert not ok(root, {"fields": record["fields"], "clauses": []})
    assert not ok(root, {"fields": [field("total", "Decimal")], "clauses": [CLAUSE]})


@pytest.mark.trace("TC-034", "FR-004-AC-5")
def test_event_requires_an_occurrence_field_and_refuses_identity_and_operations(
    schema_registry,
):
    event = schema_registry("Event")
    occurrence = field("occurred_at", "Timestamp")
    assert ok(event, {"fields": [occurrence, field("order_id", "UUID")]})
    assert not ok(event, {"fields": [field("order_id", "UUID")]})
    assert not ok(
        event, {"fields": [occurrence, field("order_id", "UUID", identity=True)]}
    )
    assert not ok(event, {"fields": [occurrence], "operations": [OPERATION]})


@pytest.mark.trace("TC-035", "FR-004-AC-6")
def test_repository_requires_operations_and_refuses_fields(schema_registry):
    repository = schema_registry("Repository")
    assert ok(repository, {"operations": [OPERATION]})
    assert not ok(repository, {"operations": []})
    assert not ok(
        repository, {"operations": [OPERATION], "fields": [field("cache", "String")]}
    )
    assert not ok(repository, {})


@pytest.mark.trace("TC-036", "FR-004-AC-7")
def test_state_machine_admits_states_and_transitions_and_refuses_a_triggerless_one(
    schema_registry,
):
    """`states` and `transitions` are hand-built: the extractor does not
    populate them (agent-ix/quoin#335)."""
    machine = schema_registry("StateMachine")
    transition = {"from": "Draft", "to": "Placed", "trigger": "place"}
    assert ok(machine, {"operations": [OPERATION]})
    assert ok(
        machine,
        {
            "operations": [OPERATION],
            "states": [{"value": "Draft"}, {"value": "Placed"}],
            "transitions": [transition],
        },
    )
    assert not ok(
        machine,
        {"operations": [OPERATION], "transitions": [{"from": "Draft", "to": "Placed"}]},
    )
    assert not ok(machine, {"operations": []})

    both = {**transition, "guard": CLAUSE, "guardExpression": EXPRESSION}
    assert not ok(machine, {"operations": [OPERATION], "transitions": [both]})
    guarded = {**transition, "guardExpression": EXPRESSION}
    assert ok(machine, {"operations": [OPERATION], "transitions": [guarded]})
    for bad in (
        {key: value for key, value in EXPRESSION.items() if key != "text"},
        {**EXPRESSION, "kind": "clause"},
        {**EXPRESSION, "text": ""},
    ):
        broken = {**transition, "guardExpression": bad}
        assert not ok(machine, {"operations": [OPERATION], "transitions": [broken]})


@pytest.mark.trace("TC-037", "FR-004-AC-8")
def test_process_requires_a_correlation_identity_and_admits_typed_steps(
    schema_registry,
):
    """`steps` is hand-built: the extractor does not populate it
    (agent-ix/quoin#335)."""
    process = schema_registry("Process")
    record = {"fields": [field("correlation_id", "UUID", identity=True)]}
    assert ok(process, record)
    assert ok(process, {**record, "steps": [{"name": "reserve", "kind": "command"}]})
    assert ok(
        process, {**record, "emits": ["ix://agent-ix/spec-objects-business/event_001"]}
    )
    assert not ok(
        process, {**record, "steps": [{"name": "reserve", "kind": "teleport"}]}
    )
    assert not ok(process, {"fields": [field("order_id", "UUID")]})


@pytest.mark.trace("TC-038", "FR-004-AC-9", "FR-004-CON-2")
def test_the_empty_record_passes_only_domain_enumeration_and_population(
    schema_registry,
):
    open_required = {"domain", "enumeration", "population", "variant_set", "graph"}
    for name in OBJECT_TYPES:
        validator = schema_registry(MODEL_OF[name])
        assert ok(validator, {}) is (name in open_required), name
    for name in open_required:
        validator = schema_registry(MODEL_OF[name])
        assert not ok(validator, {"fields": [field("anything")]}), name
        assert not ok(validator, {"operations": [OPERATION]}), name
    # The open-required types are told apart by their optional keys alone.
    assert ok(
        schema_registry("Domain"), {"vocabulary": [{"term": "Place", "doc": "…"}]}
    )
    assert not ok(
        schema_registry("Enumeration"), {"vocabulary": [{"term": "Place", "doc": "…"}]}
    )
    assert ok(schema_registry("Enumeration"), {"values": [{"value": "Draft"}]})
    assert not ok(schema_registry("Domain"), {"values": [{"value": "Draft"}]})
    member = {"type": {"target": "ix://agent-ix/spec-objects-business/type/Order"}}
    population = schema_registry("Population")
    assert ok(population, {"extent": "closed", "members": [member]})
    assert ok(population, {"extent": "open"})
    assert ok(population, {"members": [member]})
    assert not ok(population, {"extent": "sometimes", "members": [member]})
    assert not ok(
        population,
        {"extent": "open", "members": [{**member, "extent": {"lower": 0}}]},
    )
    assert not ok(schema_registry("Domain"), {"members": [member]})
    assert not ok(schema_registry("Enumeration"), {"members": [member]})


@pytest.mark.trace("TC-039", "FR-004-AC-10")
def test_an_unresolved_placeholder_target_is_accepted_and_a_bare_token_is_refused(
    schema_registry, quire_engine, semantic_module
):
    entity = schema_registry("Entity")
    placeholder = {
        "name": "mystery",
        "type": {
            "target": "ix://agent-ix/spec-objects-business/unresolved/Mystery",
            "multiplicity": {"lower": 1, "upper": 1, "ordered": False, "unique": False},
        },
        "identity": True,
    }
    assert ok(entity, {"fields": [placeholder]})
    bare = json.loads(json.dumps(placeholder))
    bare["type"]["target"] = "Mystery"
    assert not ok(entity, {"fields": [bare]})

    markdown = (
        '---\nid: probe-001\ntitle: "Probe"\ntype: entity\nobject: entity\n---\n'
        "# [probe-001] Probe\n\n## Properties\n\n"
        "| Field | Type | Multiplicity | Constraints |\n|---|---|---|---|\n"
        "| probe_id | UUID | 1..1 | identity |\n| mystery | Mystery | 1..1 | |\n"
    )
    record = quire_engine.extract_semantic(
        {
            "markdown": markdown,
            "module": semantic_module,
            "bundle": {
                "package": semantic_module["package"],
                "objects": [],
                "enumerations": [],
                "imports": {},
            },
        }
    )
    codes = [d.get("code") for d in record.get("diagnostics", [])]
    assert "semantic.unresolved-type" in codes


@pytest.mark.trace("TC-040", "FR-004-CON-1")
def test_no_module_schema_redeclares_a_semantic_core_model(schema_registry):
    """FR-004-CON-1: the module namespace contributes archetype shapes only."""
    grammar = {
        "FieldDecl",
        "TypeRef",
        "Multiplicity",
        "ConstraintDecl",
        "RelationDecl",
        "OperationDecl",
        "ClauseRef",
        "EnumValue",
        "KernelScalar",
        "Identifier",
        "SemanticId",
    }
    shipped = {path.stem for path in SCHEMAS_DIR.glob("*.json")}
    assert shipped & grammar == set(), f"the module redeclares {shipped & grammar}"
    for name in OBJECT_TYPES:
        schema = json.loads((SCHEMAS_DIR / f"{MODEL_OF[name]}.json").read_text())
        for key, prop in schema["properties"].items():
            item = prop.get("items", prop)
            if key in {"emits", "persists", "source"}:
                continue
            assert "$ref" in item, f"{name}.{key} is not validated by $ref"


@pytest.mark.trace("TC-041", "FR-004-AC-11")
def test_nested_entity_admits_a_local_identity_and_refuses_an_owner_and_relations(
    schema_registry,
):
    """The owner is a bundle fact (quoin FR-123), so the record carries no
    `owner` key; `relations` is refused as well."""
    nested = schema_registry("NestedEntity")
    record = {"fields": [field("line_number", "Integer", identity=True)]}
    assert ok(nested, record)
    assert not ok(nested, {**record, "owner": RELATION})
    assert not ok(nested, {**record, "relations": [RELATION]})
    assert not ok(nested, {"fields": [field("quantity", "Integer")]})


@pytest.mark.trace("TC-042", "FR-004-AC-12")
def test_operation_expressions_validate_beside_operations_and_repository_refuses_them(
    schema_registry,
):
    """`operationExpressions` is hand-built: it is the record key quire-rs
    emits beside `operations` for an inline `Pre:`/`Post:` expression."""
    identity_fields = [field("order_id", "UUID", identity=True)]
    entry = {"operation": "get", "slot": "pre", "expression": EXPRESSION}
    bases = {
        "Entity": {"fields": identity_fields},
        "NestedEntity": {"fields": identity_fields},
        "AggregateRoot": {"fields": identity_fields, "clauses": [CLAUSE]},
        "StateMachine": {},
        "Process": {"fields": identity_fields},
    }
    for name, base in bases.items():
        validator = schema_registry(name)
        record = {
            **base,
            "operations": [OPERATION],
            "operationExpressions": [entry, {**entry, "slot": "post"}],
        }
        assert ok(validator, record), name
        for bad in (
            {**entry, "slot": "during"},
            {key: value for key, value in entry.items() if key != "expression"},
        ):
            assert not ok(validator, {**record, "operationExpressions": [bad]}), name
    assert not ok(
        schema_registry("Repository"),
        {"operations": [OPERATION], "operationExpressions": [entry]},
    )
