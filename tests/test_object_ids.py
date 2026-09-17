"""Object id tests (FR-009).

An object id — the id of an artifact whose type is one of this module's object
types — uses underscores; a hyphen is refused. `ObjectId` in
`typespec/main.tsp` states the pattern once; the manifest's shared `id` locator
carries it so Quire refuses a hyphenated id at validation.
"""

from __future__ import annotations

import json

import pytest

from tests.conftest import (
    BASELINE_DIR,
    NEGATIVE_DIR,
    OBJECT_ID_LOCATOR_REGEX,
    OBJECT_ID_PATTERN,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    POSITIVE_DIR,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    frontmatter,
    locators,
    object_type,
)

AUTHORED = sorted(
    list(SKELETONS_DIR.glob("*.md"))
    + list(POSITIVE_DIR.glob("*.md"))
    + list(NEGATIVE_DIR.glob("*.md"))
)


def _missing_id(kind: str) -> str:
    return f"[{kind}] required 'id' (frontmatter_field(id)) is missing"


@pytest.mark.trace("TC-103", "FR-009-AC-1")
def test_the_pattern_is_stated_once_and_carried_by_every_id_locator():
    object_id = json.loads((SCHEMAS_DIR / "ObjectId.json").read_text())
    assert object_id["type"] == "string"
    assert object_id["pattern"] == OBJECT_ID_PATTERN
    base = json.loads((SCHEMAS_DIR / "ObjectFrontmatter.json").read_text())
    assert base["properties"]["id"]["$ref"].endswith("/ObjectId.json")
    assert {"id", "title", "type"} <= set(base["required"])
    assert OBJECT_ID_LOCATOR_REGEX == f"^({OBJECT_ID_PATTERN[1:-1]})$"
    for name in OBJECT_TYPES:
        loc = locators(object_type(name))["id"]
        assert loc["from"] == "frontmatter_field", name
        assert loc["regex"] == OBJECT_ID_LOCATOR_REGEX, name
        assert loc["required"] is True, name


@pytest.mark.trace("TC-104", "FR-009-AC-2")
def test_underscore_ids_validate_and_hyphenated_ids_are_refused_by_the_schema(
    schema_registry,
):
    validator = schema_registry("ObjectFrontmatter")
    base = {"title": "OrderLine", "type": "nested_entity", "object": "nested_entity"}
    for good in ("order_line_001", "nested_entity_001", "Order", "a1"):
        assert list(validator.iter_errors({**base, "id": good})) == [], good
    for bad in ("order-line-001", "nested-entity_001", "_order", "1order", ""):
        assert not validator.is_valid({**base, "id": bad}), bad


@pytest.mark.trace("TC-104", "FR-009-AC-2")
@pytest.mark.parametrize("path", AUTHORED, ids=lambda p: f"{p.parent.name}/{p.name}")
def test_every_skeleton_and_fixture_frontmatter_validates(schema_registry, path):
    validator = schema_registry("ObjectFrontmatter")
    front = frontmatter(path.read_text())
    assert list(validator.iter_errors(front)) == [], path.name
    assert "-" not in front["id"], path.name


@pytest.mark.trace("TC-105", "FR-009-AC-3")
@pytest.mark.parametrize(
    "path", sorted(SKELETONS_DIR.glob("*.md")), ids=lambda p: p.name
)
def test_quire_refuses_the_hyphenated_form_of_each_skeleton_id(quire_engine, path):
    text = path.read_text()
    front = frontmatter(text)
    kind = front["type"]
    underscore = quire_engine.validate_document(kind, str(PACKAGE_ROOT), text)
    assert _missing_id(kind) not in [e["message"] for e in underscore["errors"]]
    hyphenated = text.replace(
        f"id: {front['id']}\n", f"id: {front['id'].replace('_', '-')}\n", 1
    )
    assert hyphenated != text
    result = quire_engine.validate_document(kind, str(PACKAGE_ROOT), hyphenated)
    assert not result["is_valid"]
    messages = [e["message"] for e in result["errors"]]
    assert messages and set(messages) == {_missing_id(kind)}, messages


@pytest.mark.trace("TC-105", "FR-009-AC-3")
def test_a_hyphenated_020_artifact_is_refused_only_for_its_id(quire_engine):
    path = BASELINE_DIR / "skeletons" / "entity.md"
    text = path.read_text()
    assert "-" in frontmatter(text)["id"]
    result = quire_engine.validate_document("entity", str(PACKAGE_ROOT), text)
    assert [e["message"] for e in result["errors"]] == [_missing_id("entity")]


@pytest.mark.trace("TC-107", "FR-009-AC-4")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-009-AC-4: a present id that does not match the pattern is reported "
        "as a pattern mismatch naming the value and the pattern. "
        "agent-ix/quire-rs#451 builds that diagnostic; today the locator yields "
        "no value and Quire reports `required 'id' (frontmatter_field(id)) is "
        "missing` (TC-105 pins it). An expected failure, not a skip."
    ),
)
def test_a_hyphenated_id_is_reported_as_a_pattern_mismatch(quire_engine):
    path = SKELETONS_DIR / "entity.md"
    text = path.read_text()
    front = frontmatter(text)
    value = front["id"].replace("_", "-")
    hyphenated = text.replace(f"id: {front['id']}\n", f"id: {value}\n", 1)
    result = quire_engine.validate_document("entity", str(PACKAGE_ROOT), hyphenated)
    messages = [e["message"] for e in result["errors"]]
    assert _missing_id("entity") not in messages, messages
    assert len(messages) == 1, messages
    assert value in messages[0] and OBJECT_ID_LOCATOR_REGEX in messages[0], messages
