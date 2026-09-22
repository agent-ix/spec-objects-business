"""Additive-compatibility tests (NFR-001): the module stays additive over the
checked-in 0.2.0 set outside the sections FR-006 declares as model tables.

The population is the frozen baseline under `tests/fixtures/baseline-0.2.0/`:
the 0.2.0 `body_extraction` locators and all ten 0.2.0 skeletons, captured
before this change touched anything.
"""

from __future__ import annotations

import json

import pytest

from tests.conftest import (
    BASELINE_DIR,
    OBJECT_ID_LOCATOR_REGEX,
    PACKAGE_ROOT,
    REQUIRED_MODEL_TABLE_TYPES,
    SUPERSEDED_020_LOCATORS,
    frontmatter,
    locator_facets_since_020,
    locators,
    object_type,
    semantic_core_engine_xfail,
    with_object_id,
)

LEGACY_PROPERTIES_SKELETONS = ("entity", "value_object")


def baseline_locators() -> dict:
    return json.loads((BASELINE_DIR / "body_extraction.json").read_text())


def baseline_skeletons() -> list:
    return sorted((BASELINE_DIR / "skeletons").glob("*.md"))


def extract(quire_engine, module, path):
    return quire_engine.extract_semantic(
        {
            "markdown": path.read_text(),
            "module": module,
            "path": str(path),
            "bundle": {
                "package": module["package"],
                "objects": [],
                "enumerations": [],
                "imports": {},
            },
        }
    )


@pytest.mark.trace("TC-060", "NFR-001-AC-1")
def test_no_baseline_locator_definition_changed():
    baseline = baseline_locators()
    assert baseline["version"] == "0.2.0"
    changed = []
    for name, extraction in baseline["object_types"].items():
        old = (extraction or {})["yield_pattern"]["match"]
        new = locators(object_type(name))
        for key, facets in old.items():
            if key in SUPERSEDED_020_LOCATORS.get(name, set()):
                continue
            if key not in new or locator_facets_since_020(key, new[key]) != facets:
                changed.append(f"{name}.{key}")
        assert new["id"]["regex"] == OBJECT_ID_LOCATOR_REGEX, name
    assert changed == []


@pytest.mark.trace("TC-061", "NFR-001-AC-2")
@semantic_core_engine_xfail()
def test_every_baseline_skeleton_validates_under_the_new_manifest(quire_engine):
    """Measured, not assumed: the 0.2.0 skeletons carry no frontmatter
    `object:` key, so Quire runs headings-only validation on them and the
    typed record is never assembled or checked. The skeletons of the types
    whose FR-006 model tables are required are outside the population. Each
    is measured with its id in the FR-009 underscore form; the hyphenated
    form is refused (TC-104)."""
    baseline = baseline_skeletons()
    assert len(baseline) == 10
    failures = {}
    measured = 0
    for path in baseline:
        text = with_object_id(path.read_text())
        if frontmatter(text)["type"] in REQUIRED_MODEL_TABLE_TYPES:
            continue
        measured += 1
        assert "object:" not in frontmatter(text), path.name
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        if result["errors"]:
            failures[path.name] = [e["message"] for e in result["errors"]]
    assert measured == 7
    assert failures == {}


@pytest.mark.trace("TC-061", "NFR-001-AC-2")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "The engine defect NFR-001's Verification names: once a legacy-form "
        "artifact carries `object:`, quire 0.46.0 assembles its declaration "
        "record as `{}` and checks it against the type schema "
        "unconditionally, so it fails `semantic.record-invalid` at error "
        "severity even under `legacy_forms: warning`. "
        "agent-ix/quire-rs#391 owns the rule. The schema is not relaxed and "
        "the row is an expected failure, never a skip."
    ),
)
def test_a_legacy_form_artifact_that_declares_its_object_is_not_an_error(quire_engine):
    text = (BASELINE_DIR / "skeletons" / "entity.md").read_text()
    text = text.replace("type: entity\n", "type: entity\nobject: entity\n", 1)
    result = quire_engine.validate_document("entity", str(PACKAGE_ROOT), text)
    assert [e["message"] for e in result["errors"]] == []


@pytest.mark.trace("TC-062", "NFR-001-AC-3")
@semantic_core_engine_xfail()
def test_each_legacy_form_skeleton_yields_exactly_one_legacy_warning(
    quire_engine, semantic_module
):
    for name in LEGACY_PROPERTIES_SKELETONS:
        path = BASELINE_DIR / "skeletons" / f"{name}.md"
        record = extract(quire_engine, semantic_module, path)
        warnings = [
            d
            for d in record.get("diagnostics", [])
            if d.get("code") == "semantic.legacy-properties-form"
        ]
        assert len(warnings) == 1, (name, record.get("diagnostics"))
        assert warnings[0]["severity"] == "warning", name
        assert record["availability"]["fields"]["state"] == "unavailable", name


@pytest.mark.trace("TC-063", "NFR-001-AC-4")
@semantic_core_engine_xfail()
def test_the_properties_string_is_byte_identical_across_versions(quire_engine):
    """The untyped `properties` yield is what every existing consumer reads;
    the current locators must leave it untouched."""
    for name in LEGACY_PROPERTIES_SKELETONS:
        path = BASELINE_DIR / "skeletons" / f"{name}.md"
        text = with_object_id(path.read_text())
        extracted = quire_engine.extract(name, str(PACKAGE_ROOT), text)
        records = extracted["extraction"]
        assert len(records) == 1, (name, records)
        assert records[0]["properties"] == expected_properties_string(path), name


def expected_properties_string(path) -> str:
    """The `## Properties` body as it stood at 0.2.0, read straight from the
    frozen fixture — an independent oracle, not another engine run."""
    import re

    text = path.read_text()
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    match = re.search(
        r"^## Properties[ \t]*$(.*?)(?=^## |\Z)", text, re.DOTALL | re.MULTILINE
    )
    assert match, f"{path.name} has no `## Properties` section"
    return match.group(1).strip()
