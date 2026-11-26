"""Model-table tests (FR-006): the manifest declares every object-type model
table quire-rs extracts, the skeletons author those tables, and every form the
manifest does not declare is refused.
"""

from __future__ import annotations

import json
import re
from importlib.metadata import version as package_version

import pytest

from tests.conftest import (
    MODEL_TABLES,
    NEGATIVE_DIR,
    PACKAGE_ROOT,
    POSITIVE_DIR,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    TABLE_SPECS,
    frontmatter,
    load_manifest,
    locators,
    object_type,
    object_types,
    semantic_target_value,
)

REQUIRED = {
    ("domain", "vocabulary"): False,
    ("aggregate_root", "members"): True,
    ("state_machine", "states"): True,
    ("state_machine", "transitions"): True,
    ("process", "steps"): True,
    ("process", "states"): False,
    ("enumeration", "values"): True,
    ("population", "population"): True,
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

QUIRE_ENGINE_VERSION = tuple(
    int(part) for part in package_version("quire").split(".")[:3]
)

# The key column of each model table, as the Markdown names it.
KEY_COLUMN = {
    "values": "Value",
    "states": "State",
    "transitions": "Trigger",
    "steps": "Step",
    "members": "Member",
    "vocabulary": "Term",
    "population": "Type",
}

# The model-table locator each model-table negative fixture refuses, keyed by
# fixture; its object type is the fixture's frontmatter `type`.
MODEL_NEGATIVE_LOCATOR = {
    "enumeration-values-as-list.md": "values",
    "state_machine-states-as-diagram.md": "states",
    "state_machine-transition-unknown-state.md": "transitions",
    "state_machine-transition-unknown-trigger.md": "transitions",
    "state_machine-transition-dangling-guard.md": "transitions",
    "process-step-unknown-kind.md": "steps",
    "process-states-as-list.md": "states",
    "aggregate_root-members-as-list.md": "members",
    "domain-vocabulary-duplicate-term.md": "vocabulary",
    "population-members-duplicate-type.md": "population",
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
    "process-states-as-list.md": "semantic.feature-not-extractable",
    "population-members-duplicate-type.md": "semantic.duplicate-model-entry",
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


@pytest.mark.trace("TC-080", "FR-006-AC-1", "FR-013-AC-1", "FR-013-CON-2")
def test_every_model_table_locator_declares_the_engine_column_set():
    declared = {}
    for ot in object_types():
        for key, loc in locators(ot).items():
            if loc.get("from") != "table_row":
                continue
            columns = (loc.get("assert") or {}).get("columns") or []
            # quire-rs recognizes a model table by its first column being a
            # table key, then requires every column to belong to that table.
            matches = [f for f, cols in TABLE_SPECS.items() if columns[:1] == cols[:1]]
            if matches:
                (feature,) = matches
                assert set(columns) <= set(TABLE_SPECS[feature]), (ot["name"], key)
                declared[(ot["name"], key)] = (feature, loc["under_section"])
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
        expected_assert = {"columns", "min_rows"}
        if (name, key) == ("process", "steps"):
            expected_assert.add("optional_columns")
            assert loc["assert"]["optional_columns"] == [
                "Consumes",
                "Emits",
                "Description",
            ]
            receiver_locator = object_type(name)["body_extraction"]["yield_pattern"][
                "match"
            ][key][1]
            assert receiver_locator["under_section"] == "Steps"
            assert receiver_locator["assert"]["columns"] == [
                "Step",
                "Kind",
                "Consumes",
                "Emits",
                "Receiver",
                "Description",
            ]
            assert receiver_locator["assert"]["optional_columns"] == [
                "Consumes",
                "Emits",
                "Receiver",
                "Description",
            ]
            assert object_type(name)["allowed_links"]["receiver"] == ["RoleSpec"]
            step_schema = json.loads((SCHEMAS_DIR / "ProcessStep.json").read_text())
            assert step_schema["properties"]["receiver"]["$ref"].endswith(
                "/SemanticId.json"
            )
            assert "receiver" not in step_schema["required"]
        assert set(loc["assert"]) == expected_assert, (name, key)


@pytest.mark.trace(
    "TC-124",
    "FR-013-AC-2",
    "FR-013-AC-3",
    "FR-013-AC-4",
    "FR-013-AC-5",
    "FR-013-CON-3",
)
@pytest.mark.xfail(
    strict=True,
    condition=QUIRE_ENGINE_VERSION < (0, 63, 2),
    reason="typed model-table references require the unreleased Quire 0.63.2 engine",
)
def test_process_step_receiver_is_optional_typed_and_resolves_in_the_bundle(
    quire_engine, semantic_module, bundle_index
):
    manifest = load_manifest()
    process_schema = json.loads((SCHEMAS_DIR / "Process.json").read_text())
    step_schema = json.loads((SCHEMAS_DIR / "ProcessStep.json").read_text())
    step_kind_schema = json.loads((SCHEMAS_DIR / "StepKind.json").read_text())
    edge_types = {}
    for verb, entry in manifest["edge_types"].items():
        edge_types[verb] = {"category": entry["category"]}
        if "inverse" in entry:
            edge_types[verb]["inverse"] = entry["inverse"]
        if entry.get("composite"):
            edge_types[verb]["composite"] = True
    relation_vocabulary = {
        "objectType": "process",
        "edgeTypes": edge_types,
        "roles": {ot["name"]: ot.get("roles", []) for ot in object_types()},
        "allowedLinks": {ot["name"]: ot["allowed_links"] for ot in object_types()},
    }
    receiver_bundle = {
        **bundle_index,
        "imports": {"agent-ix/spec-artifacts-process": ["RoleSpec"]},
        "importedArtifacts": [
            {
                "package": "agent-ix/spec-artifacts-process",
                "id": "ROLE",
                "object": "RoleSpec",
            }
        ],
    }
    path = POSITIVE_DIR / "process-step-receiver.md"

    def extract(text):
        return quire_engine.extract_semantic(
            {
                "markdown": text,
                "module": semantic_module,
                "path": str(path),
                "sourceIdentity": "ix://agent-ix/spec-objects-business/PROCESS-RECEIVER-SYN-001",
                "bodyExtraction": object_type("process")["body_extraction"],
                "dataSchema": process_schema,
                "schemaDocuments": {
                    step_schema["$id"]: step_schema,
                    step_kind_schema["$id"]: step_kind_schema,
                },
                "objectType": "process",
                "bundle": receiver_bundle,
                "relationVocabulary": relation_vocabulary,
            }
        )

    text = path.read_text()
    valid = extract(text)
    assert not any(
        diagnostic.get("severity") == "error"
        for diagnostic in valid.get("diagnostics", [])
    ), valid
    assert valid.get("record", {}).get("steps", [{}])[0].get("receiver") == (
        "ix://agent-ix/spec-artifacts-process/ROLE"
    ), valid
    assert any(
        relation["validationPath"] == "/record/steps/0/receiver"
        for relation in valid["recordRelations"]
    ), valid

    no_receiver = extract((SKELETONS_DIR / "process.md").read_text())
    assert not any(
        diagnostic.get("severity") == "error"
        for diagnostic in no_receiver.get("diagnostics", [])
    ), no_receiver
    assert [step["name"] for step in no_receiver["model"]["steps"]] == [
        "receive_order",
        "reserve_stock",
        "stock_reserved",
        "capture_payment",
        "payment_captured",
        "release_reservation",
        "release_to_warehouse",
        "await_shipment",
    ]
    empty_receiver = extract(
        text.replace(
            "ix://agent-ix/spec-artifacts-process/ROLE |",
            "|",
        )
    )
    assert not any(
        diagnostic.get("severity") == "error"
        for diagnostic in empty_receiver.get("diagnostics", [])
    ), empty_receiver
    assert "receiver" not in empty_receiver["record"]["steps"][0]

    absent_receiver_column = extract(
        text.replace(" | Receiver", "")
        .replace("|---|---|---|---|---|---|", "|---|---|---|---|---|")
        .replace(" | ix://agent-ix/spec-artifacts-process/ROLE", "")
    )
    assert not any(
        diagnostic.get("severity") == "error"
        for diagnostic in absent_receiver_column.get("diagnostics", [])
    ), absent_receiver_column
    assert (
        absent_receiver_column["record"]["steps"] == empty_receiver["record"]["steps"]
    ), "omitting the Receiver column preserves the receiverless step"

    wrong_kind = extract(
        text.replace(
            "ix://agent-ix/spec-artifacts-process/ROLE",
            "ix://agent-ix/spec-objects-business/entity_001",
        )
    )
    assert any(
        diagnostic.get("code") == "semantic.reference-kind-mismatch"
        for diagnostic in wrong_kind.get("diagnostics", [])
    ), wrong_kind

    missing = extract(
        text.replace(
            "ix://agent-ix/spec-artifacts-process/ROLE",
            "ix://agent-ix/spec-artifacts-process/MISSING",
        )
    )
    assert any(
        diagnostic.get("code") == "semantic.invalid-model-cell"
        and diagnostic.get("reason") == "target-not-id"
        for diagnostic in missing.get("diagnostics", [])
    ), missing


@pytest.mark.trace("TC-088", "FR-006-CON-1")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-006-CON-1 requires each model-table locator to declare its optional "
        "columns as `assert.optional_columns`. "
        "agent-ix/filament-core-service#31 owns the "
        "schema change. The row is an expected failure, never a skip."
    ),
)
def test_every_model_table_locator_declares_its_optional_columns():
    for name, tables in MODEL_TABLES.items():
        for key in tables:
            loc = locators(object_type(name))[key]
            assert "optional_columns" in loc["assert"], (name, key)


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
            expected = [row[spec.index(KEY_COLUMN[feature])] for row in rows]
            if feature == "population":
                entries = record["model"]["population"]["members"]
                actual = [
                    semantic_target_value(e["type"]["target"]).rsplit("/", 1)[-1]
                    for e in entries
                ]
            else:
                entries = record["model"][feature]
                actual = [e[ENTRY_KEY[feature]] for e in entries]
            assert actual == expected, (name, feature)


@pytest.mark.trace("TC-081", "FR-006-AC-2")
def test_domain_ubiquitous_language_section_body_is_declared(
    quire_engine, semantic_module, bundle_index
):
    path = POSITIVE_DIR / "domain-ubiquitous-language-prose.md"
    record = extract(quire_engine, semantic_module, path, bundle_index)
    assert locators(object_type("domain"))["ubiquitous_language"] == {
        "from": "section_body",
        "after_heading": "Ubiquitous Language",
        "required": False,
    }
    assert not [
        diagnostic
        for diagnostic in record.get("diagnostics", [])
        if diagnostic.get("code") == "semantic.feature-not-extractable"
    ]


DECLARED_MODEL_FIXTURE = POSITIVE_DIR / "state_machine-declared-model.md"


@pytest.mark.trace("TC-082", "FR-006-AC-3")
def test_the_declared_model_fixture_extracts_every_mapping_feature(
    quire_engine, semantic_module, bundle_index
):
    path = DECLARED_MODEL_FIXTURE
    text = path.read_text()
    result = quire_engine.validate_document("state_machine", str(PACKAGE_ROOT), text)
    assert result["is_valid"], result["errors"]
    record = extract(quire_engine, semantic_module, path, bundle_index)
    model = record["model"]
    assert [semantic_target_value(s["target"]) for s in model["supertypes"]] == [
        "OrderLifecycle"
    ]
    assert model["abstract"]["value"] is True
    features = {f["field"]: f for f in model["fieldFeatures"]}
    assert features["order_id"]["presence"] == "required"
    assert features["reason"]["presence"] == "optional"
    assert features["returned_items"]["subsets"] == ["items"]
    assert features["current_state"]["redefines"] == "current_state"
    types = {
        f["name"]: semantic_target_value(f["type"]["target"]) for f in record["fields"]
    }
    assert types["current_state"].rsplit("/", 1)[-1] == "ReturnStatus"
    status = (POSITIVE_DIR / "enumeration-return-status.md").read_text()
    status_result = quire_engine.validate_document(
        "enumeration", str(PACKAGE_ROOT), status
    )
    assert status_result["is_valid"], status_result["errors"]
    assert [row[0] for row in table_rows(status, "Values")] == [
        row[0] for row in table_rows(text, "States")
    ]
    (frame,) = model["operationFrames"]
    assert frame["operation"] == "exchange"
    assert frame["modifies"] == [
        "self.current_state",
        "self.returned_items",
        "self.exchanged",
    ]
    assert frame["creates"] == ["Order"]
    assert frame["deletes"] == ["OrderLine"]
    assert [t["guard"] for t in model["transitions"]] == [
        "ReturnedItemsAreAtMostTheItems"
    ]
    assert [t["emits"] for t in model["transitions"]] == [
        "ix://agent-ix/spec-objects-business/event_001"
    ]
    assert not [
        d
        for d in record.get("diagnostics", [])
        if d.get("code") == "semantic.feature-not-extractable"
    ]


@pytest.mark.trace("TC-082", "FR-006-AC-3")
def test_the_declared_model_frame_carries_its_pre_and_post_lines(
    quire_engine, semantic_module, bundle_index
):
    record = extract(
        quire_engine, semantic_module, DECLARED_MODEL_FIXTURE, bundle_index
    )
    (frame,) = record["model"]["operationFrames"]
    assert frame["pre"] == ["ReturnedItemsAreAtMostTheItems"]
    assert frame["post"] == ["ExchangedReturnHasReturnedItems"]


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
    covered = set()
    for name, locator in MODEL_NEGATIVE_LOCATOR.items():
        assert name in MODEL_NEGATIVES, name
        front = frontmatter((NEGATIVE_DIR / name).read_text())
        assert locator in MODEL_TABLES[front["type"]], (name, locator)
        covered.add((front["type"], locator))
    declared = {
        (object_name, locator)
        for object_name, tables in MODEL_TABLES.items()
        for locator in tables
    }
    assert covered == declared


@pytest.mark.trace("TC-087", "FR-006-AC-5")
def test_skeleton_clauses_are_quire_and_contract_lines_are_pre_post(
    quire_engine, semantic_module, bundle_index
):
    contract_lines = []
    for path in sorted(SKELETONS_DIR.glob("*.md")):
        text = path.read_text()
        assert not re.search(r"^```ocl", text, re.M), path.name
        assert not re.search(r"^(Requires|Ensures):", text, re.M), path.name
        contract_lines += [
            (path.name, m.group(1)) for m in re.finditer(r"^(Pre|Post):", text, re.M)
        ]
        assert not re.search(r"^```mermaid", text, re.M) or path.name in {
            "domain.md",
            "graph.md",
        }, path.name
        record = extract(quire_engine, semantic_module, path, bundle_index)
        for clause in record.get("clauses") or []:
            assert clause["language"] == "quire", (path.name, clause)
        assert not [
            d
            for d in record.get("diagnostics", [])
            if d.get("code") == "semantic.clause-language-unchecked"
        ], path.name
    # The state_machine skeleton writes the `Post:` line of its operation.
    assert ("state_machine.md", "Post") in contract_lines, contract_lines


@pytest.mark.trace("TC-085", "FR-006-AC-6")
def test_the_population_fixture_extracts_one_member_per_row(
    quire_engine, semantic_module, bundle_index
):
    path = POSITIVE_DIR / "population-members.md"
    text = path.read_text()
    result = quire_engine.validate_document("population", str(PACKAGE_ROOT), text)
    assert result["is_valid"], result["errors"]
    record = extract(quire_engine, semantic_module, path, bundle_index)
    assert record["availability"]["model"]["state"] == "available"
    members = record["model"]["population"]["members"]
    rows = table_rows(text, "Members")
    assert [
        semantic_target_value(m["type"]["target"]).rsplit("/", 1)[-1] for m in members
    ] == [row[0] for row in rows]
    assert record["model"]["population"]["extent"] == "open"
    assert all("extent" not in m for m in members)

    duplicate = (NEGATIVE_DIR / "population-members-duplicate-type.md").read_text()
    refused = quire_engine.validate_document("population", str(PACKAGE_ROOT), duplicate)
    assert any(
        "semantic.duplicate-model-entry" in e["message"] for e in refused["errors"]
    ), refused["errors"]

    retired = text.replace("| Type |\n|---|", "| Type | Extent |\n|---|---|")
    retired = "\n".join(
        f"{line} 0..* |" if line.startswith("| ") and "Type" not in line else line
        for line in retired.splitlines()
    )
    refused = quire_engine.validate_document("population", str(PACKAGE_ROOT), retired)
    assert any(
        "semantic.feature-not-extractable" in e["message"] for e in refused["errors"]
    ), refused["errors"]


FIELD_BEARING = (
    "entity",
    "value_object",
    "aggregate_root",
    "nested_entity",
    "event",
    "state_machine",
    "process",
)


@pytest.mark.trace("TC-086", "FR-006-AC-7")
def test_specializes_is_a_declared_structural_edge_every_field_bearing_type_admits():
    edge = load_manifest()["edge_types"]["specializes"]
    assert edge["category"] == "structural"
    assert edge["inverse"] == "generalizes"
    assert edge["description"]
    for name in FIELD_BEARING:
        links = object_type(name)["allowed_links"]
        assert name in links["specializes"], name
