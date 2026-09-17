"""Relationships tests (FR-007): the manifest declares the `## Relationships`
table on the object types whose record admits `relations`, the skeletons
author their domain relationships in it, and Quire refuses every row the edge
registry or `allowed_links` does not admit.
"""

from __future__ import annotations

import re

import pytest

from tests.conftest import (
    BUNDLE_PACKAGE,
    NEGATIVE_DIR,
    PACKAGE_ROOT,
    POSITIVE_DIR,
    SKELETONS_DIR,
    frontmatter,
    load_manifest,
    locators,
    object_type,
    object_types,
)
from tests.test_model_tables import table_rows

# The object types whose record schema admits `relations` (FR-004).
RELATION_BEARING = ("entity", "aggregate_root")

RELATIONSHIPS_LOCATOR = {
    "from": "table_row",
    "under_section": "Relationships",
    "required": False,
    "assert": {"columns": ["Name", "Verb", "Target", "Multiplicity"], "min_rows": 1},
}

# The domain verbs of the manifest `edge_types`, as agent-ix/spec-artifacts-iso
# declares them (category, inverse).
DOMAIN_VERBS = {
    "contains": ("structural", "part_of"),
    "aggregates": ("structural", "part_of"),
    "composes": ("structural", "composed_by"),
    "triggers": ("behavioral", "triggered_by"),
    "transitions_to": ("behavioral", None),
    "raises": ("behavioral", None),
    "reads": ("dataflow", None),
    "writes": ("dataflow", None),
    "consumes": ("dataflow", None),
    "emits": ("dataflow", "emitted_by"),
    "carries": ("dataflow", None),
    "persists": ("dependency", None),
    "owns": ("dependency", None),
    "operates_on": ("realization", None),
    "references": ("traceability", None),
}

# Each relationships negative fixture and the FR-076 refusal reason it carries.
RELATIONSHIP_NEGATIVES = {
    "entity-relationships-unknown-verb.md": "unknown-verb",
    "entity-relationships-inverse-verb.md": "inverse-verb",
    "entity-relationships-target-not-allowed.md": "target-not-allowed",
    "entity-relationships-bad-multiplicity.md": "multiplicity",
}


def relation_vocabulary(name: str) -> dict:
    manifest = load_manifest()
    edge_types = {}
    for verb, entry in manifest["edge_types"].items():
        edge_types[verb] = {"category": entry["category"]}
        if entry.get("inverse"):
            edge_types[verb]["inverse"] = entry["inverse"]
    return {
        "objectType": name,
        "edgeTypes": edge_types,
        "roles": {ot["name"]: ot.get("roles", []) for ot in object_types()},
        "allowedLinks": {ot["name"]: ot["allowed_links"] for ot in object_types()},
    }


def relationship_bundle(semantic_module) -> dict:
    """The bundle index: every skeleton and positive fixture artifact with its
    object type."""
    artifacts = {}
    for path in sorted(SKELETONS_DIR.glob("*.md")) + sorted(POSITIVE_DIR.glob("*.md")):
        front = frontmatter(path.read_text())
        artifacts[front["id"]] = front["object"]
    return {
        "package": BUNDLE_PACKAGE,
        "objects": [],
        "enumerations": [],
        "imports": {},
        "artifacts": [{"id": i, "object": o} for i, o in artifacts.items()],
    }


def extract_relations(quire_engine, semantic_module, path, bundle):
    text = path.read_text()
    front = frontmatter(text)
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": semantic_module,
            "path": str(path),
            "sourceIdentity": f"ix://{BUNDLE_PACKAGE}/{front['id']}",
            "bodyExtraction": object_type(front["object"])["body_extraction"],
            "bundle": bundle,
            "relationVocabulary": relation_vocabulary(front["object"]),
        }
    )


def expected_relations(text: str) -> list[dict]:
    manifest = load_manifest()
    relations = []
    for name, verb, target, multiplicity in table_rows(text, "Relationships"):
        entry = manifest["edge_types"][verb]
        lower, _, upper = multiplicity.partition("..")
        bound = {"lower": int(lower)}
        if upper != "*":
            bound["upper"] = int(upper)
        relations.append(
            {
                "name": name,
                "verb": verb,
                "category": entry["category"],
                "composite": entry.get("inverse") == "part_of",
                "target": f"ix://{BUNDLE_PACKAGE}/{target}",
                "multiplicity": bound,
            }
        )
    return relations


def actual_relations(record: dict) -> list[dict]:
    return [
        {"name": source["name"], **relation}
        for relation, source in zip(record["relations"], record["relationSources"])
    ]


@pytest.mark.trace("TC-089", "FR-007-AC-1")
def test_every_object_type_declares_the_relationships_table_and_every_verb_it_admits():
    manifest = load_manifest()
    assert "relationships" in manifest["semantic"]["mappings"]
    for ot in object_types():
        if ot["name"] in RELATION_BEARING:
            assert locators(ot)["relationships"] == RELATIONSHIPS_LOCATOR, ot["name"]
        else:
            assert "relationships" not in locators(ot), ot["name"]
    edge_types = manifest["edge_types"]
    assert set(edge_types) == {"specializes", *DOMAIN_VERBS}
    for verb, (category, inverse) in DOMAIN_VERBS.items():
        assert edge_types[verb]["category"] == category, verb
        assert edge_types[verb].get("inverse") == inverse, verb
        assert edge_types[verb]["description"], verb
    for ot in object_types():
        for verb in ot["allowed_links"]:
            assert verb in edge_types, (ot["name"], verb)


@pytest.mark.trace("TC-090", "FR-007-AC-2")
def test_every_skeleton_relationships_table_extracts_row_for_row(
    quire_engine, semantic_module
):
    bundle = relationship_bundle(semantic_module)
    authored = set()
    for path in sorted(SKELETONS_DIR.glob("*.md")):
        text = path.read_text()
        front = frontmatter(text)
        assert "relationships" not in front, path.name
        if not re.search(r"^## Relationships\s*$", text, re.M):
            continue
        authored.add(front["object"])
        result = quire_engine.validate_document(
            front["object"], str(PACKAGE_ROOT), text, bundle_package=BUNDLE_PACKAGE
        )
        assert result["is_valid"], (path.name, result["errors"])
        record = extract_relations(quire_engine, semantic_module, path, bundle)
        assert record["availability"]["relations"]["state"] == "available", (
            path.name,
            record["availability"]["relations"],
            record.get("diagnostics"),
        )
        assert not [
            d
            for d in record.get("diagnostics", [])
            if d.get("code") in ("semantic.unresolved-target",)
            or d.get("severity") == "error"
        ], (path.name, record.get("diagnostics"))
        assert actual_relations(record) == expected_relations(text), path.name
        verbs = [row[1] for row in table_rows(text, "Relationships")]
        assert "specializes" not in verbs, path.name
    assert authored == {"aggregate_root"}


@pytest.mark.trace("TC-091", "FR-007-AC-3")
def test_the_relationships_fixture_lowers_every_entity_verb(
    quire_engine, semantic_module
):
    path = POSITIVE_DIR / "entity-relationships.md"
    text = path.read_text()
    result = quire_engine.validate_document(
        "entity", str(PACKAGE_ROOT), text, bundle_package=BUNDLE_PACKAGE
    )
    assert result["is_valid"], result["errors"]
    record = extract_relations(
        quire_engine, semantic_module, path, relationship_bundle(semantic_module)
    )
    assert record["availability"]["relations"]["state"] == "available"
    relations = actual_relations(record)
    assert relations == expected_relations(text)
    assert {r["verb"] for r in relations} == set(
        object_type("entity")["allowed_links"]
    ) - {"specializes"}
    assert [r["composite"] for r in relations] == [True, False, False, False]


@pytest.mark.trace("TC-092", "FR-007-AC-4")
def test_every_relationships_negative_fails_for_its_own_reason(
    quire_engine, semantic_module
):
    bundle = relationship_bundle(semantic_module)
    for name, reason in RELATIONSHIP_NEGATIVES.items():
        path = NEGATIVE_DIR / name
        text = path.read_text()
        front = frontmatter(text)
        assert front["expect"] == "semantic.invalid-model-cell", name
        result = quire_engine.validate_document(
            front["type"], str(PACKAGE_ROOT), text, bundle_package=BUNDLE_PACKAGE
        )
        assert not result["is_valid"], name
        assert any(front["expect"] in e["message"] for e in result["errors"]), (
            name,
            result["errors"],
        )
        record = extract_relations(quire_engine, semantic_module, path, bundle)
        reasons = [
            d.get("reason")
            for d in record.get("diagnostics", [])
            if d.get("code") == front["expect"]
        ]
        assert reasons == [reason], (name, record.get("diagnostics"))
        assert not record.get("relations"), name
