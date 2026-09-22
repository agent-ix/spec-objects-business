"""Shared fixtures for the module's test suite.

Two policies are enforced here and nowhere else:

* **The engine is a hard dependency of the semantic rows.** ``quire`` is not
  declared in ``pyproject.toml`` — no index a repository may commit against
  carries 0.46.0 (``internal-pypi`` serves 0.33.0 at most and no ``quire-rs``
  tag carries the semantic layer), so the wheel is provisioned by
  ``make dev-quire`` and ``agent-ix/quire-rs#392`` is the blocking issue. When
  it is absent the semantic tests **fail**; they never skip, because a skipped
  row is not coverage (FR-005).
* **The emitted schemas are read from the committed tree**, and every
  ``$ref`` to semantic-core resolves against the package the toolchain
  installs, so a record test validates against the real bytes.
"""

from __future__ import annotations

import functools
import hashlib
import json
import pathlib
import re
from typing import Any

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_objects_business"
# The bundle every skeleton and fixture belongs to: relationship targets
# qualify under it (FR-007).
BUNDLE_PACKAGE = "agent-ix/spec-objects-business"
MANIFEST_PATH = PACKAGE_ROOT / "manifest.yaml"
SCHEMAS_DIR = PACKAGE_ROOT / "schemas"
SKELETONS_DIR = PACKAGE_ROOT / "skeletons"
NEGATIVE_DIR = REPO_ROOT / "tests" / "fixtures" / "negative"
POSITIVE_DIR = REPO_ROOT / "tests" / "fixtures" / "positive"
BASELINE_DIR = REPO_ROOT / "tests" / "fixtures" / "baseline-0.2.0"
SEMANTIC_CORE_DIR = (
    REPO_ROOT
    / "node_modules"
    / "@agent-ix"
    / "semantic-core"
    / "generated"
    / "json-schema"
)

SEMANTIC_CORE_BASE = "https://schemas.agent-ix.org/semantic-core/0.3.0/"

QUIRE_MISSING = (
    "the Quire wheel exposing `extract_semantic` is not installed in this "
    "environment. Run `make dev-quire` (agent-ix/quire-rs#392 tracks publishing "
    "0.46.0 to an index this repository may depend on). The semantic tests fail "
    "rather than skip, because a skipped row is not coverage."
)

#: The manifest declares `semantic_core: 0.3.0` (the only real, published
#: version — 0.1.0/0.2.0 never left a private dev-only mirror). quire-rs
#: vendors semantic-core bundles by exact version string
#: (`src/semantic/vendored.rs` `SEMANTIC_CORE_VERSIONS`) and the installed
#: wheel (pypi.ix's quire 0.46.0, the latest published anywhere) only vendors
#: 0.1.0/0.2.0, so every call through the engine for THIS module now fails: a
#: direct `extract_semantic` call raises `semantic.unsupported-semantic-core`,
#: and `validate_document`/`Registry.load_from` (which read the manifest from
#: disk themselves) silently load zero archetypes, so they report
#: `quire.QuireSchemaError`/a failed `is_valid` instead. Confirmed empirically
#: (verified against 0.3.0 directly, not assumed from the error string).
#: agent-ix/quire-rs#487 already tracks vendoring 0.3.0 (filed against
#: spec-objects-architecture hitting the identical gap first); this module is
#: a second, independent instance of the same root cause, not a new issue.
SEMANTIC_CORE_ENGINE_ISSUE = "agent-ix/quire-rs#487"
SEMANTIC_CORE_ENGINE_REASON = (
    "the installed quire wheel (0.46.0, the latest published anywhere) only "
    "vendors semantic-core 0.1.0/0.2.0 and this module's real semantic_core is "
    "0.3.0, so extract_semantic/validate_document/Registry.load_from all "
    f"fail against it; {SEMANTIC_CORE_ENGINE_ISSUE}"
)

OBJECT_TYPES = (
    "domain",
    "entity",
    "value_object",
    "aggregate_root",
    "nested_entity",
    "repository",
    "event",
    "state_machine",
    "process",
    "enumeration",
    "population",
)

MODEL_OF = {
    "domain": "Domain",
    "entity": "Entity",
    "value_object": "ValueObject",
    "aggregate_root": "AggregateRoot",
    "nested_entity": "NestedEntity",
    "repository": "Repository",
    "event": "Event",
    "state_machine": "StateMachine",
    "process": "Process",
    "enumeration": "Enumeration",
    "population": "Population",
}

# FR-006: the model tables quire-rs extracts (its TABLE_SPECS column sets),
# and the locator of each object type that declares one.
TABLE_SPECS = {
    "values": ["Value", "Description"],
    "states": ["State", "Description"],
    "transitions": ["From", "To", "Trigger", "Guard", "Emits"],
    "steps": ["Step", "Kind", "Consumes", "Emits", "Description"],
    "members": ["Member", "Multiplicity"],
    "vocabulary": ["Term", "Description"],
    "population": ["Type", "Extent"],
}

MODEL_TABLES = {
    "domain": {"vocabulary": ("vocabulary", "Ubiquitous Language")},
    "aggregate_root": {"members": ("members", "Members")},
    "state_machine": {
        "states": ("states", "States"),
        "transitions": ("transitions", "Transitions"),
    },
    "process": {"steps": ("steps", "Workflow"), "states": ("states", "States")},
    "enumeration": {"values": ("values", "Values")},
    "population": {"members": ("population", "Members")},
}

# The 0.2.0 locators whose sections FR-006 declares as model tables.
SUPERSEDED_020_LOCATORS = {
    "domain": {"ubiquitous_language"},
    "aggregate_root": {"members"},
    "state_machine": {"diagram"},
    "process": {"diagram", "states"},
    "enumeration": {"values_table"},
}

# The object types whose FR-006 model tables are required.
REQUIRED_MODEL_TABLE_TYPES = (
    "aggregate_root",
    "state_machine",
    "process",
    "population",
)

SUPPORT_MODELS = (
    "IdentityField",
    "OccurrenceField",
    "OccurrenceTypeRef",
    "Term",
    "Transition",
    "ProcessStep",
    "StepKind",
    "PopulationMember",
    "ObjectId",
    "ObjectFrontmatter",
)


#: FR-009: an object id is a letter, then letters, digits and underscores.
#: `typespec/main.tsp` states it once as `ObjectId`; the manifest's shared `id`
#: locator carries it as a capturing `regex`.
OBJECT_ID_PATTERN = "^[A-Za-z][A-Za-z0-9_]*$"
OBJECT_ID_LOCATOR_REGEX = "^([A-Za-z][A-Za-z0-9_]*)$"


def locator_facets_since_020(key: str, locator: dict[str, Any]) -> dict[str, Any]:
    """A locator's facets as 0.2.0 recorded them: the FR-009 `regex` on the
    `id` locator is the one facet added since, so it is compared on its own."""
    if key != "id":
        return locator
    return {k: v for k, v in locator.items() if k != "regex"}


def with_object_id(markdown: str) -> str:
    """The artifact with its frontmatter `id` hyphens written as underscores
    (FR-009), every other byte unchanged."""
    return re.sub(
        r"^id: (\S+)$",
        lambda m: f"id: {m.group(1).replace('-', '_')}",
        markdown,
        count=1,
        flags=re.MULTILINE,
    )


def load_manifest() -> dict[str, Any]:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def manifest_version() -> str:
    return load_manifest()["version"]


def module_base() -> str:
    """The `$id` base, read from the manifest version — never hard-coded
    (FR-002-CON-5)."""
    return (
        "https://schemas.agent-ix.org/agent-ix/spec-objects-business/"
        f"{manifest_version()}/"
    )


def object_types() -> list[dict[str, Any]]:
    return load_manifest()["object_types"]


def object_type(name: str) -> dict[str, Any]:
    return next(ot for ot in object_types() if ot["name"] == name)


def locators(ot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    body = ot.get("body_extraction") or {}
    return ((body.get("yield_pattern") or {}).get("match")) or {}


def frontmatter(markdown: str) -> dict[str, Any]:
    match = re.match(r"---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert match, "document has no frontmatter"
    return yaml.safe_load(match.group(1))


def sha256_of(path: pathlib.Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def require_quire():
    """Import quire, or fail the test naming the provisioning path."""
    try:
        import quire
    except ImportError as error:
        pytest.fail(f"{QUIRE_MISSING} (import error: {error})")
    if not hasattr(quire, "extract_semantic"):
        pytest.fail(
            f"`extract_semantic` is missing from the installed quire: {QUIRE_MISSING}"
        )
    return quire


@pytest.fixture(scope="session")
def quire_engine():
    return require_quire()


@functools.cache
def engine_accepts_module_semantic_core() -> bool:
    """Whether the installed quire engine vendors a bundle for this module's
    *real* declared `semantic_core` (read from the manifest). Probed
    empirically against the manifest value, never assumed from the version
    number alone."""
    try:
        import quire
    except ImportError:
        return True  # `require_quire` fails those tests by name.
    version = load_manifest()["semantic"]["semantic_core"]
    request = {
        "markdown": (
            "---\nid: probe\ntitle: Probe\ntype: value_object\n"
            "object: value_object\n---\n# [probe] Probe\n\n"
            "## Properties\n\n| Field | Type | Multiplicity | Constraints |\n"
            "|---|---|---|---|\n| a | UUID | 1..1 | |\n"
        ),
        "module": {
            "contractVersion": "1.0.0",
            "semanticCore": version,
            "package": BUNDLE_PACKAGE,
            "exports": ["value_object"],
        },
        "path": "spec/probe.md",
        "bundle": {"package": BUNDLE_PACKAGE},
    }
    try:
        quire.extract_semantic(request)
    except TypeError as error:
        if "semantic.unsupported-semantic-core" in str(error):
            return False
        raise
    return True


def semantic_core_engine_xfail():
    """A strict xfail on an installed engine that does not vendor this
    module's declared `semantic_core` yet; agent-ix/quire-rs#487. Covers both
    failure shapes: a direct `extract_semantic` `TypeError` and the silent
    zero-archetype load that `validate_document`/`Registry.load_from` turn
    into a failed `is_valid` or an `unknown archetype` error."""
    return pytest.mark.xfail(
        condition=not engine_accepts_module_semantic_core(),
        strict=True,
        reason=SEMANTIC_CORE_ENGINE_REASON,
    )


@pytest.fixture(scope="session")
def manifest() -> dict[str, Any]:
    return load_manifest()


@pytest.fixture(scope="session")
def semantic_block(manifest: dict[str, Any]) -> dict[str, Any]:
    return manifest["semantic"]


@pytest.fixture(scope="session")
def semantic_module(semantic_block: dict[str, Any]) -> dict[str, Any]:
    """The `module` block `extract_semantic` takes, derived from the manifest."""
    return {
        "contractVersion": semantic_block["contract_version"],
        "semanticCore": semantic_block["semantic_core"],
        "package": semantic_block["package"],
        "exports": semantic_block["exports"],
        "imports": semantic_block["imports"],
        "compatibilityPosture": semantic_block["compatibility_posture"],
        "legacyForms": semantic_block["legacy_forms"],
        "mappings": semantic_block["mappings"],
    }


@pytest.fixture(scope="session")
def skeletons() -> list[pathlib.Path]:
    return sorted(SKELETONS_DIR.glob("*.md"))


@pytest.fixture(scope="session")
def bundle_index(semantic_block: dict[str, Any]) -> dict[str, Any]:
    """A bundle index built from the skeleton frontmatter (FR-005-AC-3)."""
    objects: list[dict[str, Any]] = []
    enumerations: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(SKELETONS_DIR.glob("*.md")):
        front = frontmatter(path.read_text())
        if front["id"] in seen:
            continue
        seen.add(front["id"])
        entry = {"id": front["id"], "names": [front["id"], front["title"]]}
        objects.append(entry)
        if front["object"] == "enumeration":
            enumerations.append(entry)
    return {
        "package": semantic_block["package"],
        "objects": objects,
        "enumerations": enumerations,
        "imports": {},
    }


@pytest.fixture(scope="session")
def schema_registry():
    """A 2020-12 validator factory over the shipped schemas plus semantic-core.

    Every `$ref` resolves locally: module models from the committed
    `schemas/` directory, grammar models from the semantic-core package the
    pinned toolchain installs.
    """
    from referencing import Registry, Resource

    if not SEMANTIC_CORE_DIR.is_dir():
        pytest.fail(
            "@agent-ix/semantic-core is not installed, so `$ref`s to the grammar "
            "cannot resolve. Run `npm ci` (FR-002-CON-4: `@agent-ix` resolves "
            "from npm.ix through the user-level npm config)."
        )
    resources = []
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        if path.name == "toolchain.json":
            continue
        schema = json.loads(path.read_text())
        resources.append((schema["$id"], Resource.from_contents(schema)))
    for path in sorted(SEMANTIC_CORE_DIR.glob("*.json")):
        schema = json.loads(path.read_text())
        uri = schema.get("$id") or f"{SEMANTIC_CORE_BASE}{path.name}"
        resources.append((uri, Resource.from_contents(schema)))
    registry = Registry().with_resources(resources)

    def validator_for(model: str):
        from jsonschema import Draft202012Validator

        schema = json.loads((SCHEMAS_DIR / f"{model}.json").read_text())
        return Draft202012Validator(schema, registry=registry)

    return validator_for
