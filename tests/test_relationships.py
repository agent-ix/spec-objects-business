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

# The object types that declare the Relationships table (FR-007): the
# relation-bearing types, and the types whose rows lower into typed keys.
TABLE_BEARING = (*RELATION_BEARING, "process", "repository")

RELATIONSHIPS_LOCATOR = {
    "from": "table_row",
    "under_section": "Relationships",
    "required": False,
    "assert": {"columns": ["Name", "Verb", "Target", "Multiplicity"]},
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
        if ot["name"] in TABLE_BEARING:
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


# The line of the one row every relationships negative refuses.
REFUSED_ROW_LINE = 21


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
        assert [
            (e["line"], e["message"].split(":", 1)[0]) for e in result["errors"]
        ] == [(REFUSED_ROW_LINE, front["expect"])], (name, result["errors"])
        record = extract_relations(quire_engine, semantic_module, path, bundle)
        (diagnostic,) = record["diagnostics"]
        assert diagnostic["code"] == front["expect"], name
        assert diagnostic["reason"] == reason, name
        assert diagnostic["line"] == REFUSED_ROW_LINE, name
        assert record["availability"]["relations"] == {
            "state": "unavailable",
            "reason": f"entry-errors: lines {REFUSED_ROW_LINE}",
            "lossy": False,
        }, name
        assert not record.get("relations"), name
        if reason == "inverse-verb":
            assert "aggregates" in diagnostic["message"], diagnostic
            assert "aggregate_root_001" in diagnostic["message"], diagnostic


@pytest.mark.trace("TC-093", "FR-007-AC-5")
def test_a_header_only_relationships_table_is_available_with_no_relations(
    quire_engine, semantic_module
):
    path = POSITIVE_DIR / "entity-relationships-header-only.md"
    text = path.read_text()
    result = quire_engine.validate_document(
        "entity", str(PACKAGE_ROOT), text, bundle_package=BUNDLE_PACKAGE
    )
    assert result["is_valid"], result["errors"]
    assert "min_rows" not in locators(object_type("entity"))["relationships"]["assert"]
    record = extract_relations(
        quire_engine, semantic_module, path, relationship_bundle(semantic_module)
    )
    assert record["availability"]["relations"]["state"] == "available"
    assert record.get("relations", []) == []
    assert not [
        d for d in record.get("diagnostics", []) if d.get("section") == "Relationships"
    ]


@pytest.mark.trace("TC-094", "FR-007-AC-6")
def test_a_relationships_table_on_a_type_without_relations_fails_its_record_schema(
    quire_engine,
):
    for ot in object_types():
        if ot["name"] in RELATION_BEARING:
            continue
        schema = (PACKAGE_ROOT / ot["data_schema"]["schema"]).read_text()
        assert '"relations"' not in schema, ot["name"]
    path = NEGATIVE_DIR / "value_object-relationships.md"
    text = path.read_text()
    front = frontmatter(text)
    assert front["expect"] == "semantic.record-invalid"
    header_only = text.split("| currency_code |")[0]
    for document in (text, header_only):
        result = quire_engine.validate_document(
            "value_object", str(PACKAGE_ROOT), document, bundle_package=BUNDLE_PACKAGE
        )
        assert not result["is_valid"]
        (error,) = result["errors"]
        assert error["message"].startswith("semantic.record-invalid:"), error
        assert "at relations:" in error["message"], error
        # agent-ix/quire-rs#440: the finding names no line today.
        assert error["line"] is None, error


@pytest.mark.trace("TC-095", "FR-007-AC-7")
def test_a_relationships_section_in_another_form_is_refused_or_warned(quire_engine):
    listed = NEGATIVE_DIR / "entity-relationships-as-list.md"
    text = listed.read_text()
    assert frontmatter(text)["expect"] == "semantic.feature-not-extractable"
    result = quire_engine.validate_document(
        "entity", str(PACKAGE_ROOT), text, bundle_package=BUNDLE_PACKAGE
    )
    heading = text.splitlines().index("## Relationships") + 1
    assert [(e["line"], e["message"].split(":", 1)[0]) for e in result["errors"]] == [
        (heading + 2, "semantic.feature-not-extractable")
    ], result["errors"]
    prose = (POSITIVE_DIR / "entity-relationships-prose.md").read_text()
    result = quire_engine.validate_document(
        "entity", str(PACKAGE_ROOT), prose, bundle_package=BUNDLE_PACKAGE
    )
    assert result["is_valid"], result["errors"]
    heading = prose.splitlines().index("## Relationships") + 1
    assert [
        (w["line"], w["message"].split(":", 1)[0])
        for w in result["warnings"]
        if "relationships" in w["message"].split(":", 1)[0]
    ] == [(heading, "semantic.relationships-no-block")], result["warnings"]


@pytest.mark.trace("TC-096", "FR-007-AC-8")
def test_validate_document_lowers_a_target_in_another_artifact_with_an_advisory(
    quire_engine,
):
    text = (POSITIVE_DIR / "entity-relationships-cross-artifact.md").read_text()
    result = quire_engine.validate_document(
        "entity", str(PACKAGE_ROOT), text, bundle_package=BUNDLE_PACKAGE
    )
    assert result["is_valid"], result["errors"]
    row = (
        text.splitlines().index(
            "| last_order | references | aggregate_root_999 | 0..1 |"
        )
        + 1
    )
    advisories = [
        w
        for w in result["warnings"]
        if w["message"].startswith("semantic.unresolved-target:")
    ]
    assert [w["line"] for w in advisories] == [row], result["warnings"]
    assert "aggregate_root_999" in advisories[0]["message"]
    assert "no bundle index" in advisories[0]["message"]


# The typed-key rows FR-007-AC-9 lowers: object type, row, record key, target.
TYPED_KEY_ROWS = (
    ("process", "| done | emits | event_001 | 0..1 |", "emits", "event_001"),
    (
        "repository",
        "| orders | persists | aggregate_root_001 | 0..* |",
        "persists",
        "aggregate_root_001",
    ),
)


RELATIONSHIPS_HEADER = (
    "\n## Relationships\n\n| Name | Verb | Target | Multiplicity |\n|---|---|---|---|\n"
)


def typed_key_document(name: str, row: str) -> str:
    return (SKELETONS_DIR / f"{name}.md").read_text() + RELATIONSHIPS_HEADER + row


def extract_document(quire_engine, semantic_module, name: str, text: str) -> dict:
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": semantic_module,
            "path": f"{name}.md",
            "sourceIdentity": f"ix://{BUNDLE_PACKAGE}/{frontmatter(text)['id']}",
            "bodyExtraction": object_type(name)["body_extraction"],
            "bundle": relationship_bundle(semantic_module),
            "relationVocabulary": relation_vocabulary(name),
        }
    )


@pytest.mark.trace("TC-097", "FR-007-AC-9")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-007-AC-9: process `emits` and repository `persists` rows lower into "
        "the typed record keys, never `relations`. agent-ix/quire-rs#435 builds "
        "that lowering; today the rows lower into `relations` and the record "
        "fails `semantic.record-invalid` (TC-098 pins that). An expected "
        "failure, never a skip."
    ),
)
@pytest.mark.parametrize(
    ("name", "row", "key", "target"), TYPED_KEY_ROWS, ids=[r[0] for r in TYPED_KEY_ROWS]
)
def test_process_emits_and_repository_persists_rows_lower_into_typed_keys(
    quire_engine, semantic_module, name, row, key, target
):
    assert locators(object_type(name))["relationships"] == RELATIONSHIPS_LOCATOR
    text = typed_key_document(name, row + "\n")
    result = quire_engine.validate_document(
        name, str(PACKAGE_ROOT), text, bundle_package=BUNDLE_PACKAGE
    )
    assert result["is_valid"], result["errors"]
    record = extract_document(quire_engine, semantic_module, name, text)
    assert record[key] == [f"ix://{BUNDLE_PACKAGE}/{target}"], record
    assert not record.get("relations"), record
    row_name, verb, cell_target, multiplicity = table_rows(text, "Relationships")[0]
    (source,) = record["relationSources"]
    assert {k: source[k] for k in ("name", "verb", "target", "multiplicity")} == {
        "name": row_name,
        "verb": verb,
        "target": cell_target,
        "multiplicity": multiplicity,
    }, source
    assert source["sourceSpan"]["startLine"] == text.splitlines().index(row) + 1
    availability = record["availability"]["relations"]
    assert availability["state"] == "available", availability
    assert not availability.get("lossy"), availability

    header_only = typed_key_document(name, "")
    result = quire_engine.validate_document(
        name, str(PACKAGE_ROOT), header_only, bundle_package=BUNDLE_PACKAGE
    )
    assert result["is_valid"], result["errors"]
    record = extract_document(quire_engine, semantic_module, name, header_only)
    assert record["availability"]["relations"]["state"] == "available"
    assert record[key] == [], record
    assert record.get("relationSources", []) == []
    assert not record.get("relations"), record


@pytest.mark.trace("TC-098", "FR-007-AC-10")
@pytest.mark.parametrize(
    ("name", "row", "key", "target"), TYPED_KEY_ROWS, ids=[r[0] for r in TYPED_KEY_ROWS]
)
def test_process_and_repository_rows_are_refused_until_typed_key_lowering_lands(
    quire_engine, name, row, key, target
):
    # agent-ix/quire-rs#435: this pins today's blocker and flips when it lands,
    # at which point TC-097 passes and this test is removed.
    text = typed_key_document(name, row + "\n")
    result = quire_engine.validate_document(
        name, str(PACKAGE_ROOT), text, bundle_package=BUNDLE_PACKAGE
    )
    assert not result["is_valid"]
    (error,) = result["errors"]
    assert error["message"].startswith("semantic.record-invalid:"), error
    assert "at relations:" in error["message"], error
