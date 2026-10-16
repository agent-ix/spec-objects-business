"""Object definition IDs remain strict while composed artifact IDs are typed."""

from __future__ import annotations

import json
import subprocess

import pytest

from tests.conftest import (
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
def test_object_definition_schema_and_locators_preserve_strictness():
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
def test_object_frontmatter_refuses_typed_ids_and_malformed_names(schema_registry):
    validator = schema_registry("ObjectFrontmatter")
    base = {"title": "OrderLine", "type": "entity", "object": "entity"}
    for good in ("order_line_001", "nested_entity_001", "Order", "a1"):
        assert list(validator.iter_errors({**base, "id": good})) == [], good
    for bad in (
        "order-line-001", "nested-entity_001", "_order", "1order", "",
        "FR-271", "fr-271", "FR-", "FRXYZ-1", "ENT-001",
    ):
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
def test_quire_refuses_hyphenated_object_ids(tmp_path, path):
    text = path.read_text()
    front = frontmatter(text)
    document = tmp_path / path.name
    document.write_text(text)
    arguments = [
        "quire", "validate", str(document), "--scope", str(tmp_path),
        "--module", str(PACKAGE_ROOT), "--pretty",
    ]
    baseline = subprocess.run(
        arguments, check=False, capture_output=True, text=True
    )
    assert baseline.returncode == 0, baseline.stdout + baseline.stderr

    malformed = text.replace(
        f"id: {front['id']}\n", f"id: {front['id'].replace('_', '-') }\n", 1
    )
    document.write_text(malformed)
    result = subprocess.run(
        arguments,
        check=False, capture_output=True, text=True,
    )
    assert result.returncode != 0, result.stdout + result.stderr
    assert "ObjectId" not in result.stderr


@pytest.mark.trace("TC-104", "FR-009-AC-2")
def test_composed_artifact_keeps_its_typed_id(quire_engine, tmp_path):
    """The artifact schema owns frontmatter; object validation adds its body."""
    artifact_module = tmp_path / "artifact-module"
    artifact_module.mkdir()
    (artifact_module / "manifest.yaml").write_text(
        """module: test-artifacts
version: 0.1.0
artifact_types:
  - name: FR
    frontmatter_schema_ref: schemas/FR.json
object_types: []
"""
    )
    schemas = artifact_module / "schemas"
    schemas.mkdir()
    (schemas / "FR.json").write_text(json.dumps({
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
    }))
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
    # With explicit roots this validates the artifact schema and the composed
    # enumeration body extraction in one engine pass.
    path = tmp_path / "FR-271.md"
    path.write_text(artifact)
    result = subprocess.run(
        [
            "quire", "validate", str(path), "--scope", str(tmp_path),
            "--module", str(PACKAGE_ROOT), "--module", str(artifact_module),
            "--pretty",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
