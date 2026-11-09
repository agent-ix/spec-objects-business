"""Closed-union and graph object types (FR-010, PLAT-160).

`variant_set` declares a closed discriminated union (a variant set with a
payload per variant); `graph` declares an acyclic partial order. Neither is a
lifecycle, so neither reuses `enumeration` or `state_machine`.
"""

from __future__ import annotations

import pytest

from tests.conftest import (
    PACKAGE_ROOT,
    POSITIVE_DIR,
    REPO_ROOT,
    SKELETONS_DIR,
    frontmatter,
    load_manifest,
    locators,
    object_type,
)
from tests.test_role_schemas import CLAUSE, OPERATION, field, ok

REFUSED_DIR = REPO_ROOT / "tests" / "fixtures" / "refused"


def validate(quire_engine, path):
    text = path.read_text()
    return quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )


@pytest.mark.trace("TC-111", "FR-010-AC-1")
def test_the_manifest_declares_variant_set_and_graph_with_their_links():
    manifest = load_manifest()
    assert {"variant_set", "graph"} <= set(manifest["semantic"]["exports"])
    assert object_type("variant_set")["allowed_links"] == {
        "references": ["enumeration", "value_object", "variant_set"]
    }
    graph_links = object_type("graph")["allowed_links"]
    assert set(graph_links) == {"references"}
    assert {"event", "process", "entity", "graph"} <= set(graph_links["references"])
    for name, schema in (("variant_set", "VariantSet"), ("graph", "Graph")):
        assert object_type(name)["data_schema"] == {"schema": f"schemas/{schema}.json"}


@pytest.mark.trace("TC-112", "FR-010-AC-2")
def test_a_variant_set_authors_a_variants_table_and_refuses_a_list(quire_engine):
    variants = locators(object_type("variant_set"))["variants"]
    assert variants["required"] is True
    assert variants["assert"] == {
        "columns": ["Variant", "Payload", "Description"],
        "min_rows": 1,
    }
    result = validate(quire_engine, POSITIVE_DIR / "variant_set-diagnostic-cause.md")
    assert result["is_valid"], result["errors"]
    skeleton = validate(quire_engine, SKELETONS_DIR / "variant_set.md")
    assert skeleton["is_valid"], skeleton["errors"]
    refused = validate(quire_engine, REFUSED_DIR / "variant_set-variants-as-list.md")
    assert not refused["is_valid"]
    assert "'variants'" in refused["errors"][0]["message"]


@pytest.mark.trace("TC-113", "FR-010-AC-3")
def test_a_graph_authors_a_mermaid_block_and_refuses_prose_alone(quire_engine):
    graph = locators(object_type("graph"))["graph"]
    assert graph["required"] is True
    assert (graph["from"], graph["language"]) == ("code_block", "mermaid")
    assert "states" not in locators(object_type("graph"))
    for path in (POSITIVE_DIR / "graph-causal-control.md", SKELETONS_DIR / "graph.md"):
        result = validate(quire_engine, path)
        assert result["is_valid"], result["errors"]
    refused = validate(quire_engine, REFUSED_DIR / "graph-without-diagram.md")
    assert not refused["is_valid"]
    assert "'graph'" in refused["errors"][0]["message"]


@pytest.mark.trace("TC-114", "FR-010-AC-4")
def test_variant_set_and_graph_schemas_are_sealed_against_lifecycle_and_data(
    schema_registry,
):
    variant_set = schema_registry("VariantSet")
    graph = schema_registry("Graph")
    assert ok(variant_set, {}) and ok(graph, {})
    assert ok(variant_set, {"clauses": [CLAUSE]}) and ok(graph, {"clauses": [CLAUSE]})
    payload = {"target": "ix://agent-ix/spec-objects-business/type/DigestPair"}
    variants = [{"name": "digest_mismatch", "payload": {"target": payload["target"]}}]
    assert ok(variant_set, {"variants": variants})
    assert ok(variant_set, {"variants": [{"name": "unavailable"}]})
    assert not ok(variant_set, {"variants": [{"payload": payload}]})
    assert not ok(graph, {"variants": variants})
    forbidden = (
        {"fields": [field("anything")]},
        {"operations": [OPERATION]},
        {"states": [{"value": "Draft"}]},
        {"transitions": []},
    )
    for record in forbidden:
        assert not ok(variant_set, record), record
        assert not ok(graph, record), record
