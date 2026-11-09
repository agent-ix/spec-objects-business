"""Record-key owners (FR-010): every key a record schema declares has one
authored source, the keys quoin FR-123 leaves unmapped are not declared, and
the module names the sections that fill the rest."""

from __future__ import annotations

import json
import re

import pytest

from tests.conftest import (
    MODEL_OF,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    frontmatter,
    load_manifest,
    locators,
    object_type,
)
from tests.test_model_tables import table_rows
from tests.test_role_schemas import RELATION, ok

# The owner of every top-level key a record schema of this module declares.
KEY_OWNERS = {
    "fields": "quoin FR-071",
    "clauses": "quoin FR-072",
    "operations": "quoin FR-072",
    "operationExpressions": "quoin FR-072",
    "relations": "quoin FR-104",
    "emits": "quire-rs FR-076, from `## Relationships` rows",
    "persists": "quire-rs FR-076, from `## Relationships` rows",
    "source": "quoin FR-121, from `## Source`",
    "extent": "quire-rs FR-075, from frontmatter",
    "values": "quoin FR-123",
    "states": "quoin FR-123",
    "transitions": "quoin FR-123",
    "steps": "quoin FR-123",
    "members": "quoin FR-123 (aggregate_root) and quire-rs FR-075 (population)",
    "vocabulary": "quoin FR-123",
}

# Keys quoin FR-123 leaves unmapped: no schema declares them.
UNMAPPED = ("owner", "ubiquitous_language")


def declared_keys(name: str) -> set[str]:
    schema = json.loads((SCHEMAS_DIR / f"{MODEL_OF[name]}.json").read_text())
    return set(schema["properties"])


@pytest.mark.trace("TC-111", "FR-010-AC-1")
def test_every_declared_record_key_has_one_owner_and_the_unmapped_keys_are_absent():
    for name in OBJECT_TYPES:
        keys = declared_keys(name)
        assert keys <= set(KEY_OWNERS), (name, keys - set(KEY_OWNERS))
        assert not keys & set(UNMAPPED), (name, keys & set(UNMAPPED))
    assert "members" not in declared_keys("domain")
    assert "relations" in declared_keys("domain")
    assert "states" in declared_keys("process")


@pytest.mark.trace("TC-112", "FR-010-AC-2")
def test_process_states_and_domain_relations_validate_and_domain_members_do_not(
    schema_registry,
):
    process = schema_registry("Process")
    domain = schema_registry("Domain")
    identity = {
        "name": "case_id",
        "identity": True,
        "type": {
            "target": "String",
            "multiplicity": {"lower": 1, "upper": 1, "ordered": False, "unique": False},
        },
    }
    base = {"fields": [identity]}
    assert ok(process, {**base, "states": [{"value": "open", "doc": "Being worked"}]})
    assert not ok(process, {**base, "states": [{"doc": "no value"}]})
    assert ok(domain, {"relations": [RELATION]})
    assert not ok(domain, {"members": [RELATION]})
    assert not ok(domain, {"ubiquitous_language": "prose"})


@pytest.mark.trace("TC-113", "FR-010-AC-3")
def test_record_sections_is_named_and_event_source_is_one_inline_id_section():
    manifest = load_manifest()
    assert "record-sections" in manifest["semantic"]["mappings"]
    assert locators(object_type("event"))["source"] == {
        "from": "section_body",
        "after_heading": "Source",
        "required": False,
    }
    text = (SKELETONS_DIR / "event.md").read_text()
    body = re.search(r"^## Source\s*$(.*?)(?=^## |\Z)", text, re.S | re.M).group(1)
    (inline_id,) = body.split()
    published_by = {
        frontmatter(p.read_text())["id"]: frontmatter(p.read_text())["object"]
        for p in SKELETONS_DIR.glob("*.md")
    }
    assert published_by[inline_id] == "aggregate_root"


@pytest.mark.trace("TC-114", "FR-010-AC-4")
def test_nested_entity_parent_is_prose_and_no_skeleton_authors_an_owner_section():
    parent = locators(object_type("nested_entity"))["parent"]
    assert parent == {
        "from": "section_body",
        "after_heading": "Parent",
        "required": True,
    }
    for path in SKELETONS_DIR.glob("*.md"):
        assert not re.search(r"^## (Owner|Emits|Persists)\s*$", path.read_text(), re.M)


@pytest.mark.trace("TC-115", "FR-010-AC-5")
def test_aggregate_membership_is_authored_once_in_the_members_table():
    text = (SKELETONS_DIR / "aggregate_root.md").read_text()
    assert len(table_rows(text, "Members")) >= 1
    verbs = {row[1] for row in table_rows(text, "Relationships")}
    assert not verbs & {"aggregates", "contains"}


@pytest.mark.trace("TC-116", "FR-010-AC-6")
def test_domain_relationships_skeleton_extracts_its_contains_rows(
    quire_engine,
):
    text = (SKELETONS_DIR / "domain.md").read_text()
    result = quire_engine.validate_document(
        "domain",
        str(PACKAGE_ROOT),
        text,
        bundle_package="agent-ix/spec-objects-business",
    )
    assert result["is_valid"], result["errors"]
    rows = table_rows(text, "Relationships")
    assert rows and {row[1] for row in rows} == {"contains"}
