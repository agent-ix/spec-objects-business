"""Activation and stakeholder tests, covering FR-001, IT-001 and the
StR-001 validation criteria.

FR-001-AC-1 and StR-001-VC-3 are discharged here against the committed tree.
FR-001-AC-2..AC-4, StR-001-VC-1 and StR-001-VC-2 need a running
`filament-core-service` at revision `a77f31e` or later; they are environment-
gated and their matrix rows stay `🚧` with that note. That is pre-existing
debt from issue #1, not this issue's, and it is not the semantic suite: the
Quire rows fail rather than skip (see `conftest.py`).
"""

from __future__ import annotations

import hashlib
import json
import os

import pytest

from tests.conftest import (
    MANIFEST_PATH,
    MODEL_OF,
    OBJECT_TYPES,
    REPO_ROOT,
    load_manifest,
)

# The filament-core-service module-manifest schema at revision `a77f31e`
# (CR-003, the revision that admits the `semantic` block and the reference-form
# `data_schema`), vendored byte-identically by Quoin and Quire. FR-001, FR-003
# and IT-001 all judge this manifest against this one revision.
VENDORED_SCHEMA = REPO_ROOT / "tests" / "fixtures" / "module-manifest.schema.json"
VENDORED_SCHEMA_DIGEST = (
    "69cf9738600e7d8daa45ed5cd7231b17ca8dc58d068bd36af9b0d2c9b69dcbbc"
)

FILAMENT_CORE_URL = os.environ.get("FILAMENT_CORE_URL")
needs_filament_core = pytest.mark.skipif(
    not FILAMENT_CORE_URL,
    reason=(
        "FR-001-AC-2..AC-4 / IT-001 need a running filament-core-service at "
        "revision a77f31e or later (no release tag contains it). Set "
        "FILAMENT_CORE_URL to run them; the matrix row stays 🚧 until then."
    ),
)


@pytest.mark.trace("TC-001", "FR-001-AC-1")
def test_the_manifest_validates_against_the_pinned_fr035_schema(quire_engine):
    digest = hashlib.sha256(VENDORED_SCHEMA.read_bytes()).hexdigest()
    assert digest == VENDORED_SCHEMA_DIGEST, (
        "the vendored module-manifest schema is not the a77f31e revision the "
        "spec pins; FR-001 and FR-003 would judge the manifest against "
        "different schemas"
    )
    violations = quire_engine.validate_manifest(load_manifest(), str(VENDORED_SCHEMA))
    assert violations == [], violations


@pytest.mark.trace("TC-002", "FR-001-AC-2")
@pytest.mark.integration
@needs_filament_core
def test_activation_against_a_clean_filament_core_returns_200():
    import urllib.request

    request = urllib.request.Request(
        f"{FILAMENT_CORE_URL.rstrip('/')}/api/v1/modules/activate",
        data=MANIFEST_PATH.read_bytes(),
        headers={"Content-Type": "application/yaml"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        assert response.status == 200


@pytest.mark.trace("TC-003", "FR-001-AC-3")
@pytest.mark.integration
@needs_filament_core
def test_reactivation_is_a_content_hash_no_op():
    import urllib.request

    hashes = []
    for _ in range(2):
        request = urllib.request.Request(
            f"{FILAMENT_CORE_URL.rstrip('/')}/api/v1/modules/activate",
            data=MANIFEST_PATH.read_bytes(),
            headers={"Content-Type": "application/yaml"},
            method="POST",
        )
        with urllib.request.urlopen(request) as response:
            hashes.append(json.loads(response.read())["content_hash"])
    assert hashes[0] == hashes[1]


@pytest.mark.trace("TC-004", "FR-001-AC-4")
@pytest.mark.trace("TC-005", "StR-001-VC-1")
@pytest.mark.integration
@needs_filament_core
def test_every_declared_contribution_is_readable_from_the_registry_endpoints():
    """FR-001-AC-4 and StR-001-VC-1 observe the same run: activation registers
    the contents this module declares, and each exported object type's
    registered `data_schema` is the reference object as posted while
    agent-ix/filament-core-service#23 is open."""
    import urllib.request

    with urllib.request.urlopen(
        f"{FILAMENT_CORE_URL.rstrip('/')}/api/v1/object-types"
    ) as response:
        registered = {row["name"]: row for row in json.loads(response.read())}
    manifest = load_manifest()
    for declared in manifest["object_types"]:
        row = registered[declared["name"]]
        assert row["data_schema"] == declared["data_schema"]


@pytest.mark.trace("TC-006", "StR-001-VC-2")
@pytest.mark.integration
@needs_filament_core
def test_a_generator_produces_an_artifact_that_validates_against_the_shipped_module(
    quire_engine,
):
    """StR-001-VC-2, demonstration: an artifact authored from a shipped
    skeleton validates against the module the service serves."""
    from tests.conftest import PACKAGE_ROOT, SKELETONS_DIR, frontmatter

    text = (SKELETONS_DIR / "entity.md").read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )
    assert result["is_valid"]


@pytest.mark.trace("TC-075", "StR-001-VC-3")
def test_every_object_type_ships_a_typed_contract_a_fixture_reader_can_consume(
    schema_registry,
):
    """StR-001-VC-3: an entity and an enumeration are distinguishable to a
    consumer by schema alone, without reading the prose."""
    for name in OBJECT_TYPES:
        model = MODEL_OF[name]
        schema = json.loads(
            (
                REPO_ROOT / "spec_objects_business" / "schemas" / f"{model}.json"
            ).read_text()
        )
        assert schema.get("properties"), f"{name} carries no declared shape"
        assert set(schema) > {"$schema", "$id", "type"}, name

    entity_record = {
        "fields": [
            {
                "name": "customer_id",
                "type": {"target": "UUID", "multiplicity": {"lower": 1, "upper": 1}},
                "identity": True,
            }
        ]
    }
    enumeration_record = {"values": [{"value": "Draft"}, {"value": "Placed"}]}
    entity = schema_registry("Entity")
    enumeration = schema_registry("Enumeration")
    assert not list(entity.iter_errors(entity_record))
    assert list(entity.iter_errors(enumeration_record))
    assert not list(enumeration.iter_errors(enumeration_record))
    assert list(enumeration.iter_errors(entity_record))
