"""Construct declaration tests (FR-008).

Each of the ten construct kinds declares its semantic IR `construct:` once, as
filament-core-data#172 reads it (FR-142, its `business` module table), in the
shape the FR-035 module-manifest schema at filament-core-service `5b2af8b`
admits. `population` declares none.
"""

from __future__ import annotations

import copy

import pytest

from tests.conftest import OBJECT_TYPES, load_manifest, object_type
from tests.test_activation_and_stakeholder import VENDORED_SCHEMA

CONSTRUCT_KINDS = tuple(name for name in OBJECT_TYPES if name != "population")

# The declarations filament-core-data#172 carries for this module (FR-142),
# hand-copied from its branch `fcd-172-modular-constructs` at `7b69d99`
# (`crates/extraction-frontend/fixtures/modules/spec-objects-business/manifest.yaml`),
# with each `meaning` replaced by its QSpec FR-208 id at `c8e3ca0`.
DECLARATIONS = {
    "domain": {
        "identity": "none",
        "shape": "namespace",
        "members": {
            "members": "required",
            "vocabulary": "required",
            "fields": "forbidden",
            "operations": "forbidden",
        },
        "rules": [
            "no_fields",
            "no_operations",
            "exclusive_membership",
            "members_not_namespace",
        ],
        "meaning": "quire.meaning.model.namespace/v1",
    },
    "entity": {
        "identity": "identified",
        "shape": "record",
        "members": {"fields": "required", "identityFields": "required"},
        "rules": ["identity_field_required"],
        "meaning": "quire.meaning.model.object-type/v1",
    },
    "value_object": {
        "identity": "value",
        "shape": "record",
        "members": {"fields": "required"},
        "rules": ["identity_field_forbidden"],
        "meaning": "quire.meaning.model.record-value-type/v1",
    },
    "aggregate_root": {
        "identity": "identified",
        "shape": "record",
        "members": {
            "fields": "required",
            "identityFields": "required",
            "clauses": "required",
            "members": "required",
        },
        "references": {"members": ["aggregate-member"]},
        "rules": ["identity_field_required", "min_clauses"],
        "meaning": "quire.meaning.model.object-type/v1",
    },
    "nested_entity": {
        "identity": "identified",
        "shape": "record",
        "members": {
            "fields": "required",
            "identityFields": "required",
            "owner": "required",
        },
        "references": {"owner": ["composite-owner"]},
        "rules": ["identity_field_required", "single_owner"],
        "meaning": "quire.meaning.model.object-type/v1",
    },
    "repository": {
        "identity": "none",
        "shape": "interface",
        "members": {
            "operations": "required",
            "persists": "required",
            "fields": "forbidden",
        },
        "references": {"persists": ["persistable"]},
        "rules": ["no_fields", "min_operations"],
        "meaning": "quire.meaning.model.persistence-interface/v1",
    },
    "event": {
        "identity": "none",
        "shape": "record",
        "members": {"fields": "required", "occurrenceField": "required"},
        "rules": ["identity_field_forbidden", "occurrence_field_required"],
        "meaning": "quire.meaning.model.event-type/v1",
        "immutable": True,
    },
    "state_machine": {
        "identity": "none",
        "shape": "state_machine",
        "members": {
            "operations": "required",
            "states": "required",
            "transitions": "required",
        },
        "references": {"transitions": ["event-like"]},
        "rules": ["min_operations"],
        "meaning": "quire.meaning.model.state-machine/v1",
    },
    "process": {
        "identity": "identified",
        "shape": "sequence",
        "members": {
            "fields": "required",
            "identityFields": "required",
            "steps": "required",
        },
        "references": {"steps": ["event-like"]},
        "rules": ["identity_field_required"],
        "meaning": "quire.meaning.model.process/v1",
    },
    "enumeration": {
        "identity": "none",
        "shape": "enumeration",
        "members": {
            "variants": "required",
            "fields": "forbidden",
            "relationships": "forbidden",
            "operations": "forbidden",
        },
        "rules": [],
        "meaning": "quire.meaning.model.variant-type/v1",
    },
}

# The roles each construct's references admit, carried by the named types.
ADDED_ROLES = {
    "entity": {"aggregate-member", "composite-owner"},
    "value_object": {"aggregate-member"},
    "aggregate_root": {"composite-owner"},
    "nested_entity": {"aggregate-member", "composite-owner"},
    "enumeration": {"aggregate-member"},
}

# The FR-142 core vocabulary, hand-copied from filament-core-data#172
# `schema/semantic/v1/construct-vocabulary.json` at `7b69d99` (branch
# `fcd-172-modular-constructs`, not yet on main).
IDENTITIES = {"identified", "value", "none"}
SHAPES = {
    "record",
    "enumeration",
    "interface",
    "state_machine",
    "sequence",
    "namespace",
}
OPTIONAL_BY_DEFAULT = {
    "fields",
    "variants",
    "relationships",
    "operations",
    "clauses",
    "supertypes",
    "abstract",
}
FORBIDDEN_BY_DEFAULT = {
    "identityFields",
    "owner",
    "members",
    "occurrenceField",
    "states",
    "transitions",
    "steps",
    "persists",
    "vocabulary",
    "direction",
    "interfaceType",
    "multiplicity",
    "declaredType",
    "flowDirection",
    "sourceEnd",
    "targetEnd",
    "sourceElement",
    "targetElement",
    "featureOrder",
}
REFERENCE_MEMBERS = {
    "owner",
    "members",
    "transitions",
    "steps",
    "persists",
    "interfaceType",
    "declaredType",
    "sourceEnd",
    "targetEnd",
    "sourceElement",
    "targetElement",
}
RULES = {
    "identity_field_required": ("identityFields", "required"),
    "identity_field_forbidden": ("identityFields", "forbidden"),
    "min_clauses": ("clauses", "required"),
    "occurrence_field_required": ("occurrenceField", "required"),
    "no_fields": ("fields", "forbidden"),
    "no_operations": ("operations", "forbidden"),
    "min_operations": ("operations", "required"),
    "single_owner": ("owner", "required"),
    "exclusive_membership": ("members", "required"),
    "members_not_namespace": ("members", "required"),
}

# QSpec FR-208 meaning ids, hand-copied from agent-ix/quire-specification
# `spec/objects/foundation/FR-208-quire-meaning-vocabulary.md` at `c8e3ca0`.
FR208_MEANINGS = {
    "quire.meaning.model.object-type/v1",
    "quire.meaning.model.value-type/v1",
    "quire.meaning.model.variant-type/v1",
    "quire.meaning.model.record-value-type/v1",
    "quire.meaning.model.event-type/v1",
    "quire.meaning.model.state-machine/v1",
    "quire.meaning.model.process/v1",
    "quire.meaning.model.persistence-interface/v1",
    "quire.meaning.model.namespace/v1",
    "quire.meaning.model.population/v1",
    "quire.meaning.systems.interface/v1",
    "quire.meaning.systems.part/v1",
    "quire.meaning.systems.port/v1",
    "quire.meaning.systems.connection/v1",
    "quire.meaning.systems.allocation/v1",
}


def _presence(construct: dict, member: str) -> str:
    if member in construct["members"]:
        return construct["members"][member]
    return "optional" if member in OPTIONAL_BY_DEFAULT else "forbidden"


def _object_type_in(manifest: dict, name: str) -> dict:
    return next(ot for ot in manifest["object_types"] if ot["name"] == name)


@pytest.mark.trace("TC-099", "FR-008-AC-1")
def test_ten_kinds_declare_a_construct_and_the_manifest_validates(quire_engine):
    declared = {
        ot["name"] for ot in load_manifest()["object_types"] if "construct" in ot
    }
    assert declared == set(CONSTRUCT_KINDS)
    assert len(CONSTRUCT_KINDS) == 10
    assert "construct" not in object_type("population")
    violations = quire_engine.validate_manifest(load_manifest(), str(VENDORED_SCHEMA))
    assert violations == [], violations


@pytest.mark.trace("TC-108", "FR-008-AC-6")
def test_only_event_declares_immutable(quire_engine):
    manifest = load_manifest()
    for kind in CONSTRUCT_KINDS:
        construct = object_type(kind)["construct"]
        if kind == "event":
            assert construct["immutable"] is True
        else:
            assert "immutable" not in construct, kind
    violations = quire_engine.validate_manifest(manifest, str(VENDORED_SCHEMA))
    assert violations == [], violations


@pytest.mark.trace("TC-100", "FR-008-AC-2")
@pytest.mark.parametrize("kind", CONSTRUCT_KINDS)
def test_each_declaration_is_the_fr142_declaration(kind):
    assert object_type(kind)["construct"] == DECLARATIONS[kind]
    roles = set(object_type(kind).get("roles", []))
    assert ADDED_ROLES.get(kind, set()) <= roles, (kind, roles)


@pytest.mark.trace("TC-100", "FR-008-AC-2")
@pytest.mark.parametrize("kind", CONSTRUCT_KINDS)
def test_each_kind_binds_an_fr208_meaning(kind):
    assert object_type(kind)["construct"]["meaning"] in FR208_MEANINGS, kind


@pytest.mark.trace("TC-101", "FR-008-AC-3")
@pytest.mark.parametrize("kind", CONSTRUCT_KINDS)
def test_each_declaration_speaks_only_the_core_vocabulary(kind):
    construct = object_type(kind)["construct"]
    assert construct["identity"] in IDENTITIES
    assert construct["shape"] in SHAPES
    assert set(construct["members"]) <= OPTIONAL_BY_DEFAULT | FORBIDDEN_BY_DEFAULT
    assert len(construct["rules"]) == len(set(construct["rules"]))
    for rule in construct["rules"]:
        member, presence = RULES[rule]
        assert _presence(construct, member) == presence, (kind, rule)


@pytest.mark.trace("TC-101", "FR-008-AC-3")
@pytest.mark.parametrize("kind", CONSTRUCT_KINDS)
def test_references_name_carried_roles_on_admitted_reference_members(kind):
    manifest = load_manifest()
    carried = {role for ot in manifest["object_types"] for role in ot.get("roles", [])}
    construct = object_type(kind)["construct"]
    for member, roles in construct.get("references", {}).items():
        assert member in REFERENCE_MEMBERS, (kind, member)
        assert _presence(construct, member) != "forbidden", (kind, member)
        assert roles and "*" not in roles, (kind, member)
        assert set(roles) <= carried, (kind, member, roles)
        type_names = {ot["name"] for ot in manifest["object_types"]}
        assert not set(roles) & type_names, (kind, member, roles)


@pytest.mark.trace("TC-102", "FR-008-AC-4")
@pytest.mark.parametrize(
    ("kind", "mutate", "path"),
    [
        (
            "aggregate_root",
            lambda c: c["references"].__setitem__("members", ["*"]),
            "construct.references.members[0]",
        ),
        (
            "entity",
            lambda c: c.__setitem__("identity", "keyed"),
            "construct.identity",
        ),
        (
            "domain",
            lambda c: c["members"].__setitem__("members", "sometimes"),
            "construct.members.members",
        ),
        ("event", lambda c: c.pop("meaning"), "construct.meaning"),
    ],
    ids=["wildcard-role", "unknown-identity", "unknown-presence", "missing-meaning"],
)
def test_a_malformed_declaration_is_refused(quire_engine, kind, mutate, path):
    manifest = copy.deepcopy(load_manifest())
    mutate(_object_type_in(manifest, kind)["construct"])
    violations = quire_engine.validate_manifest(manifest, str(VENDORED_SCHEMA))
    assert violations, kind
    assert any(v["path"].endswith(path) for v in violations), violations


# The spec-artifacts-iso registry a consumer loads beside this module
# (agent-ix/spec-artifacts-iso main `8a7d9ef`, `spec_artifacts_iso/manifest.yaml`
# `roles:` and `artifact_types[].name`).
SPEC_ARTIFACTS_ISO_ROLES = {
    "domain-object",
    "persistable",
    "event-like",
    "externally-exposed",
    "deployable",
    "measurable",
    "configurable",
    "business-intent",
    "sensitive",
}
SPEC_ARTIFACTS_ISO_ARCHETYPES = {
    "FR",
    "NFR",
    "StR",
    "US",
    "IT",
    "TC",
    "master-requirements",
    "index",
    "log",
    "Glossary",
}

# `allowed_links` targets that name neither a role nor an archetype of either
# module. They predate FR-008 and are outside its scope; pinned here so a new
# unknown role cannot hide among them.
PREEXISTING_UNKNOWN_ROLES = {("process", "action"), ("repository", "data_schema")}


def _unknown_roles(manifest: dict) -> set[tuple[str, str]]:
    """The quire-rs FR-040 load check (`src/loader/mod.rs`, quire-rs `724ad29`):
    every role an object type carries, and every `allowed_links` target token
    that is not `*` or an archetype name, must be declared in the roles
    registry merged across the loaded modules. The Python binding exposes no
    registry load diagnostics, so the rule is applied here to the same data."""
    roles = SPEC_ARTIFACTS_ISO_ROLES | set(manifest.get("roles", {}))
    archetypes = SPEC_ARTIFACTS_ISO_ARCHETYPES | {
        ot["name"] for ot in manifest["object_types"]
    }
    unknown = set()
    for ot in manifest["object_types"]:
        for targets in ot.get("allowed_links", {}).values():
            for token in targets:
                if token != "*" and token not in archetypes | roles:
                    unknown.add((ot["name"], token))
        for role in ot.get("roles", []):
            if role not in roles:
                unknown.add((ot["name"], role))
    return unknown


@pytest.mark.trace("TC-106", "FR-008-AC-5")
def test_construct_roles_are_declared_so_no_role_is_unknown_beside_iso():
    manifest = load_manifest()
    assert set(manifest["roles"]) == {"aggregate-member", "composite-owner"}
    for role in manifest["roles"].values():
        assert set(role) == {"description"} and role["description"]
    assert _unknown_roles(manifest) == PREEXISTING_UNKNOWN_ROLES


@pytest.mark.trace("TC-106", "FR-008-AC-5")
def test_without_the_roles_block_the_construct_roles_are_unknown():
    manifest = copy.deepcopy(load_manifest())
    del manifest["roles"]
    added = {(kind, role) for kind, roles in ADDED_ROLES.items() for role in roles}
    assert _unknown_roles(manifest) == PREEXISTING_UNKNOWN_ROLES | added
