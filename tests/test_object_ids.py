"""Object frontmatter admits artifact IDs without relaxing semantic names."""

from __future__ import annotations

import json
import shutil

import pytest
import yaml

from tests.conftest import (
    BUNDLE_PACKAGE,
    NEGATIVE_DIR,
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


@pytest.mark.trace("TC-103", "FR-009-AC-1")
def test_object_frontmatter_schema_and_locators_share_id_contract():
    base = json.loads((SCHEMAS_DIR / "ObjectFrontmatter.json").read_text())
    assert base["properties"]["id"]["type"] == "string"
    assert base["properties"]["id"]["pattern"] == OBJECT_ID_PATTERN
    assert {"id", "title", "type"} <= set(base["required"])
    for name in OBJECT_TYPES:
        ot = object_type(name)
        assert ot["frontmatter_schema_ref"] == "schemas/ObjectFrontmatter.json"
        loc = locators(ot)["id"]
        assert loc["from"] == "frontmatter_field", name
        assert loc["path"] == ["id"], name
        assert "regex" not in loc, name
        assert loc["required"] is True, name


@pytest.mark.trace("TC-104", "FR-009-AC-2")
def test_object_frontmatter_accepts_artifact_ids_and_refuses_malformed_names(
    schema_registry,
):
    validator = schema_registry("ObjectFrontmatter")
    base = {"title": "OrderLine", "type": "entity", "object": "entity"}
    for good in (
        "order_line_001",
        "nested_entity_001",
        "Order",
        "a1",
        "FR-271",
        "DOM-001",
        "SM-001",
        "PROC-001",
        "VO-001",
        "order-line-001",
    ):
        assert list(validator.iter_errors({**base, "id": good})) == [], good
    for bad in (
        "_order",
        "1order",
        "",
        "FR-",
        "FR--271",
        "-FR-271",
        "FR-271-",
        "FR 271",
        "FR/271",
    ):
        assert not validator.is_valid({**base, "id": bad}), bad


@pytest.mark.trace("TC-104", "FR-009-AC-2")
@pytest.mark.parametrize("path", AUTHORED, ids=lambda p: f"{p.parent.name}/{p.name}")
def test_every_skeleton_and_fixture_frontmatter_validates(schema_registry, path):
    validator = schema_registry("ObjectFrontmatter")
    front = frontmatter(path.read_text())
    assert list(validator.iter_errors(front)) == [], path.name


@pytest.mark.trace("TC-105", "FR-009-AC-3")
@pytest.mark.parametrize(
    "path", sorted(SKELETONS_DIR.glob("*.md")), ids=lambda p: p.name
)
def test_quire_accepts_hyphenated_object_ids_and_refuses_malformed_ids(
    quire_engine, path
):
    text = path.read_text()
    front = frontmatter(text)
    registry = quire_engine.Registry.load_from([str(PACKAGE_ROOT)])
    baseline = registry.validate("ObjectFrontmatter", front)
    assert baseline == [], baseline

    hyphenated = text.replace(
        f"id: {front['id']}\n", f"id: {front['id'].replace('_', '-') }\n", 1
    )
    hyphenated_front = frontmatter(hyphenated)
    result = registry.validate("ObjectFrontmatter", hyphenated_front)
    assert result == [], result

    malformed = hyphenated.replace(
        f"id: {front['id'].replace('_', '-')}\n",
        f"id: {front['id'].replace('_', '-')}--bad\n",
        1,
    )
    malformed_front = frontmatter(malformed)
    result = registry.validate("ObjectFrontmatter", malformed_front)
    assert result, malformed


@pytest.mark.trace("TC-104", "FR-009-AC-2")
def test_composed_artifact_keeps_its_typed_id(tmp_path, quire_engine):
    """The artifact schema owns frontmatter; object validation adds its body."""
    combined_module = tmp_path / "combined-module"
    shutil.copytree(PACKAGE_ROOT, combined_module)
    manifest_path = combined_module / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())
    manifest.setdefault("artifact_types", []).append(
        {"name": "FR", "frontmatter_schema_ref": "schemas/FR.json"}
    )
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
    schemas = combined_module / "schemas"
    (schemas / "FR.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "https://schemas.example.test/FR.json",
                "type": "object",
                "properties": {
                    "id": {"type": "string", "pattern": "^FR-[0-9]+$"},
                    "type": {"const": "FR"},
                    "object": {"const": "enumeration"},
                    "title": {"type": "string"},
                },
                "required": ["id", "type", "object", "title"],
            }
        )
    )
    artifact = """---
id: FR-271
type: FR
object: enumeration
title: Diagnostic codes
---
# FR-271: Diagnostic code vocabulary

## Values

| Value | Description |
|---|---|
| Draft | Draft state |
"""
    # Put both archetypes in one temporary module so the Python API validates
    # the artifact schema and composed enumeration body in one engine pass.
    result = quire_engine.validate_document(
        "FR", str(combined_module), artifact, BUNDLE_PACKAGE
    )
    assert result["is_valid"], result["errors"]
