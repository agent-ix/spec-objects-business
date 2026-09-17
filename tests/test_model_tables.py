"""Model-table tests (FR-006): the manifest declares every object-type model
table quire-rs extracts, the skeletons author those tables, and every form the
manifest does not declare is refused.
"""

from __future__ import annotations

import re

import pytest

from tests.conftest import (
    MODEL_TABLES,
    NEGATIVE_DIR,
    PACKAGE_ROOT,
    POSITIVE_DIR,
    SKELETONS_DIR,
    TABLE_SPECS,
    frontmatter,
    locators,
    object_type,
    object_types,
)

REQUIRED = {
    ("domain", "vocabulary"): False,
    ("aggregate_root", "members"): True,
    ("state_machine", "states"): True,
    ("state_machine", "transitions"): True,
    ("process", "steps"): True,
    ("process", "states"): False,
    ("enumeration", "values_table"): True,
}

# The key column of each model entry, as the engine names it.
ENTRY_KEY = {
    "values": "value",
    "states": "value",
    "transitions": "trigger",
    "steps": "name",
    "members": "target",
    "vocabulary": "term",
}

# The fixture-name fragment that names each model table.
STEM_OF = {
    "values": "values",
    "states": "states",
    "transitions": "transition",
    "steps": "step",
    "members": "members",
    "vocabulary": "vocabulary",
}

# One negative fixture per model table, plus the refusal of a model table
# under a section the manifest does not declare.
MODEL_NEGATIVES = {
    "enumeration-values-as-list.md": "semantic.feature-not-extractable",
    "state_machine-states-as-diagram.md": "semantic.feature-not-extractable",
    "state_machine-transition-unknown-state.md": "semantic.unknown-state",
    "state_machine-transition-unknown-trigger.md": "semantic.unknown-trigger",
    "state_machine-transition-dangling-guard.md": "semantic.dangling-clause-ref",
    "process-step-unknown-kind.md": "semantic.invalid-model-cell",
    "aggregate_root-members-as-list.md": "semantic.feature-not-extractable",
    "domain-vocabulary-duplicate-term.md": "semantic.duplicate-model-entry",
    "entity-table-under-undeclared-section.md": "semantic.feature-not-extractable",
    "entity-presence-not-a-presence.md": "semantic.invalid-model-cell",
}


def extract(quire_engine, module, path, bundle=None):
    text = path.read_text()
    request = {
        "markdown": text,
        "module": module,
        "path": str(path),
        "sourceIdentity": f"ix://agent-ix/spec-objects-business/{frontmatter(text)['id']}",
        "bodyExtraction": object_type(frontmatter(text)["object"])["body_extraction"],
    }
    if bundle is not None:
        request["bundle"] = bundle
    return quire_engine.extract_semantic(request)


def table_rows(text: str, heading: str) -> list[list[str]]:
    """The data rows of the first table under `## <heading>`, read straight
    from the Markdown — an oracle independent of the engine."""
    match = re.search(
        rf"^## {re.escape(heading)}[ \t]*$(.*?)(?=^## |\Z)", text, re.S | re.M
    )
    assert match, heading
    lines = [ln for ln in match.group(1).splitlines() if ln.startswith("|")]
    return [[c.strip() for c in ln.strip("|").split("|")] for ln in lines[2:]]


@pytest.mark.trace("TC-080", "FR-006-AC-1", "FR-006-CON-1")
def test_every_model_table_locator_declares_the_engine_column_set():
    declared = {}
    for ot in object_types():
        for key, loc in locators(ot).items():
            if loc.get("from") != "table_row":
                continue
            columns = (loc.get("assert") or {}).get("columns")
            matches = [f for f, cols in TABLE_SPECS.items() if cols == columns]
            if matches:
                declared[(ot["name"], key)] = (matches[0], loc["under_section"])
    expected = {
        (name, key): spec
        for name, tables in MODEL_TABLES.items()
        for key, spec in tables.items()
    }
    assert declared == expected
    for (name, key), required in REQUIRED.items():
        loc = locators(object_type(name))[key]
        assert loc["required"] is required, (name, key)
        assert loc["assert"]["min_rows"] == 1, (name, key)
        assert set(loc["assert"]) == {"columns", "min_rows"}, (name, key)


@pytest.mark.trace("TC-081", "FR-006-AC-2")
def test_every_skeleton_extracts_its_model_tables_row_for_row(
    quire_engine, semantic_module, bundle_index
):
    for name, tables in MODEL_TABLES.items():
        path = SKELETONS_DIR / f"{name}.md"
        text = path.read_text()
        record = extract(quire_engine, semantic_module, path, bundle_index)
        assert record["availability"]["model"]["state"] == "available", name
        assert not [
            d
            for d in record.get("diagnostics", [])
            if d.get("severity") == "error"
            or d.get("code") == "semantic.feature-not-extractable"
        ], (name, record.get("diagnostics"))
        for feature, heading in tables.values():
            rows = table_rows(text, heading)
            assert rows, (name, heading)
            spec = TABLE_SPECS[feature]
            key_column = {
                "values": "Value",
                "states": "State",
                "transitions": "Trigger",
                "steps": "Step",
                "members": "Member",
                "vocabulary": "Term",
            }[feature]
            expected = [row[spec.index(key_column)] for row in rows]
            entries = record["model"][feature]
            assert [e[ENTRY_KEY[feature]] for e in entries] == expected, (
                name,
                feature,
            )


@pytest.mark.trace("TC-082", "FR-006-AC-3")
def test_the_declared_model_fixture_extracts_every_mapping_feature(
    quire_engine, semantic_module
):
    path = POSITIVE_DIR / "state_machine-declared-model.md"
    text = path.read_text()
    result = quire_engine.validate_document("state_machine", str(PACKAGE_ROOT), text)
    assert result["is_valid"], result["errors"]
    record = extract(quire_engine, semantic_module, path)
    model = record["model"]
    assert [s["target"] for s in model["supertypes"]] == ["OrderLifecycle"]
    assert model["abstract"]["value"] is True
    features = {f["field"]: f for f in model["fieldFeatures"]}
    assert features["order_id"]["presence"] == "required"
    assert features["reason"]["presence"] == "optional"
    assert features["returned_items"]["subsets"] == ["items"]
    assert features["current_state"]["redefines"] == "current_state"
    (frame,) = model["operationFrames"]
    assert frame["operation"] == "refund"
    assert frame["requires"] == ["ReturnIsOpen"]
    assert frame["ensures"] == ["ReturnIsSettled"]
    assert frame["modifies"] == ["self.current_state", "self.returned_items"]
    assert frame["creates"] == ["Refund"]
    assert frame["deletes"] == ["self.items"]
    assert [t["guard"] for t in model["transitions"]] == ["ReturnIsOpen"]
    assert not [
        d
        for d in record.get("diagnostics", [])
        if d.get("code") == "semantic.feature-not-extractable"
    ]


@pytest.mark.trace("TC-083", "FR-006-AC-4")
def test_every_model_table_and_undeclared_form_has_a_refusing_fixture(quire_engine):
    for name, code in MODEL_NEGATIVES.items():
        path = NEGATIVE_DIR / name
        text = path.read_text()
        front = frontmatter(text)
        assert front["expect"] == code, name
        result = quire_engine.validate_document(front["type"], str(PACKAGE_ROOT), text)
        assert not result["is_valid"], name
        assert any(code in e["message"] for e in result["errors"]), (
            name,
            [e["message"] for e in result["errors"]],
        )
    covered = {
        feature for tables in MODEL_TABLES.values() for feature, _ in tables.values()
    }
    stems = " ".join(MODEL_NEGATIVES)
    for feature in covered:
        assert STEM_OF[feature] in stems, feature


@pytest.mark.trace("TC-084", "FR-006-AC-5")
def test_skeleton_clauses_are_quire_and_contract_lines_are_requires_ensures(
    quire_engine, semantic_module, bundle_index
):
    for path in sorted(SKELETONS_DIR.glob("*.md")):
        text = path.read_text()
        assert not re.search(r"^```ocl", text, re.M), path.name
        assert not re.search(r"^(Pre|Post):", text, re.M), path.name
        assert (
            not re.search(r"^```mermaid", text, re.M) or path.name == "domain.md"
        ), path.name
        record = extract(quire_engine, semantic_module, path, bundle_index)
        for clause in record.get("clauses") or []:
            assert clause["language"] == "quire", (path.name, clause)
        assert not [
            d
            for d in record.get("diagnostics", [])
            if d.get("code") == "semantic.clause-language-unchecked"
        ], path.name
