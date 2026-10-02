"""Construct declaration tests (FR-008).

Each of the ten construct kinds declares its semantic IR `construct:` once, as
filament-core-data#172 reads it (FR-142, its `business` module table), in the
shape filament-core-service's module-manifest schema admits under
`ObjectTypeEntry.construct`. `population` declares none.

Refusal of a malformed declaration is filament-core-service's obligation,
verified where that schema is applied: at activation, or in a consumer that
applies it. FR-008 Behavior records when it becomes observable here (PLAT-902).
"""

from __future__ import annotations

import pytest

from tests.conftest import OBJECT_TYPES, load_manifest, object_type

CONSTRUCT_KINDS = tuple(name for name in OBJECT_TYPES if name != "population")

# The roles each construct's references admit, carried by the named types.
ADDED_ROLES = {
    "entity": {"aggregate-member", "composite-owner"},
    "value_object": {"aggregate-member"},
    "aggregate_root": {"composite-owner"},
    "nested_entity": {"aggregate-member", "composite-owner"},
    "enumeration": {"aggregate-member"},
}


@pytest.mark.trace("TC-099", "FR-008-AC-1")
def test_exactly_the_ten_construct_kinds_declare_a_construct():
    declared = {
        ot["name"] for ot in load_manifest()["object_types"] if "construct" in ot
    }
    assert declared == set(CONSTRUCT_KINDS)
    assert len(CONSTRUCT_KINDS) == 10
    assert "construct" not in object_type("population")


@pytest.mark.trace("TC-108", "FR-008-AC-6")
def test_only_event_declares_immutable():
    for kind in CONSTRUCT_KINDS:
        construct = object_type(kind)["construct"]
        if kind == "event":
            assert construct["immutable"] is True
        else:
            assert "immutable" not in construct, kind


@pytest.mark.trace("TC-101", "FR-008-AC-3")
@pytest.mark.parametrize("kind", CONSTRUCT_KINDS)
def test_references_name_only_carried_roles(kind):
    manifest = load_manifest()
    carried = {role for ot in manifest["object_types"] for role in ot.get("roles", [])}
    type_names = {ot["name"] for ot in manifest["object_types"]}
    construct = object_type(kind)["construct"]
    for member, roles in construct.get("references", {}).items():
        assert roles and "*" not in roles, (kind, member)
        assert set(roles) <= carried, (kind, member, roles)
        assert not set(roles) & type_names, (kind, member, roles)


@pytest.mark.trace("TC-106", "FR-008-AC-5")
def test_construct_roles_are_declared_in_the_manifest_roles_registry():
    manifest = load_manifest()
    assert set(manifest["roles"]) == {"aggregate-member", "composite-owner"}
    for role in manifest["roles"].values():
        assert set(role) == {"description"} and role["description"]
    for kind, added in ADDED_ROLES.items():
        assert added <= set(object_type(kind).get("roles", [])), kind
