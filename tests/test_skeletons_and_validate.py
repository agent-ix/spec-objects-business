"""Assert ↔ skeleton parity + quire roundtrip tests for the object types.

Mirrors the spec-artifacts-iso pattern, adapted to this module's locator
vocabulary (``frontmatter_field`` / ``section_body`` / ``code_block`` — no
tables or id_patterns here):

* every object type ships a worked example skeleton in
  ``spec_objects_business/skeletons/<name>.md``;
* every required locator is satisfied by the skeleton (heading at the
  conventional H2 level, code block with the asserted language, frontmatter
  fields present with ``artifact_type`` equal to the type name);
* reverse direction: the skeleton carries no H2 heading the manifest does not
  assert (the skeleton cannot drift ahead of the contract);
* asserted section bodies are substantive (non-empty, no placeholder tokens);
* roundtrip: each skeleton passes the quire wheel's ``validate_document`` and
  mutations fail — skipped cleanly when the installed wheel predates the
  markdown validator (quire is intentionally NOT a dependency).
"""

from __future__ import annotations

import pathlib
import re

import pytest
import yaml

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent / "spec_objects_business"
MANIFEST_PATH = PKG_ROOT / "manifest.yaml"
SKELETONS_DIR = PKG_ROOT / "skeletons"

# Conventional heading level for every asserted section/code-block locator
# (the manifest locators carry no level facet; the skeletons use H2).
SECTION_LEVEL = 2

_PLACEHOLDER_TOKENS = ("TODO", "TBD", "{{", "}}", "placeholder", "none specified")


def _object_types() -> list[dict]:
    return yaml.safe_load(MANIFEST_PATH.read_text()).get("object_types", [])


def _object_type(name: str) -> dict:
    return next(ot for ot in _object_types() if ot["name"] == name)


def _type_names() -> list[str]:
    return [ot["name"] for ot in _object_types()]


def _locators(ot: dict) -> dict[str, dict]:
    be = ot.get("body_extraction") or {}
    return ((be.get("yield_pattern") or {}).get("match")) or {}


def _skeleton_path(name: str) -> pathlib.Path:
    return SKELETONS_DIR / f"{name}.md"


def _skeleton_text(name: str) -> str:
    return _skeleton_path(name).read_text()


def _frontmatter(markdown: str) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert m, "skeleton missing frontmatter"
    return yaml.safe_load(m.group(1))


def _strip_frontmatter(markdown: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", markdown, count=1, flags=re.DOTALL)


def _strip_code_fences(body: str) -> str:
    """Drop fenced code blocks so fence content is never mistaken for headings."""
    return re.sub(r"^```.*?^```\s*$", "", body, flags=re.DOTALL | re.MULTILINE)


def _skeleton_headings(markdown: str) -> list[tuple[int, str]]:
    body = _strip_code_fences(_strip_frontmatter(markdown))
    out: list[tuple[int, str]] = []
    for line in body.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
    return out


def _skeleton_code_blocks(markdown: str) -> list[tuple[str | None, str, str]]:
    """Return ``[(language, content, preceding_h2)]`` for every fenced block."""
    body = _strip_frontmatter(markdown)
    out: list[tuple[str | None, str, str]] = []
    current_h2 = ""
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        heading = re.match(r"^##\s+(.*\S)\s*$", lines[i])
        if heading:
            current_h2 = heading.group(1).strip()
            i += 1
            continue
        fence = re.match(r"^```(\S*)\s*$", lines[i])
        if fence:
            lang = fence.group(1) or None
            content: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                content.append(lines[i])
                i += 1
            out.append((lang, "\n".join(content), current_h2))
        i += 1
    return out


def _split_sections(markdown: str, level: int = SECTION_LEVEL) -> dict[str, str]:
    body = _strip_frontmatter(markdown)
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    prefix = "#" * level + " "
    in_fence = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith(prefix):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[len(prefix) :].strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


# ─── Skeleton presence + frontmatter ─────────────────────────────────────


@pytest.mark.parametrize("name", _type_names(), ids=lambda n: n)
def test_skeleton_exists(name: str) -> None:
    assert _skeleton_path(name).exists(), f"missing skeleton {_skeleton_path(name)}"


def test_no_orphan_skeletons() -> None:
    """Every skeleton file corresponds to a declared object type."""
    names = set(_type_names())
    for path in SKELETONS_DIR.glob("*.md"):
        assert path.stem in names, f"skeleton {path.name} has no object type"


@pytest.mark.parametrize("name", _type_names(), ids=lambda n: n)
def test_skeleton_frontmatter_required_fields(name: str) -> None:
    """Frontmatter carries id/title/artifact_type; artifact_type == type name."""
    fm = _frontmatter(_skeleton_text(name))
    for field in ("id", "title", "artifact_type"):
        assert fm.get(field), f"{name}: frontmatter missing {field!r}"
    assert fm["artifact_type"] == name, (
        f"{name}: frontmatter artifact_type is {fm['artifact_type']!r}, "
        f"expected {name!r}"
    )


# ─── Forward parity: every asserted locator is satisfied ─────────────────


@pytest.mark.parametrize("name", _type_names(), ids=lambda n: n)
def test_required_locators_satisfied_by_skeleton(name: str) -> None:
    """Every ``required: true`` locator is satisfied: section_body headings
    exist at H2, code blocks exist with the asserted language under the
    asserted heading, frontmatter fields are present."""
    ot = _object_type(name)
    md = _skeleton_text(name)
    headings = set(_skeleton_headings(md))
    blocks = _skeleton_code_blocks(md)
    fm = _frontmatter(md)

    required = {key: loc for key, loc in _locators(ot).items() if loc.get("required")}
    assert required, f"{name}: manifest declares no required locators"

    for key, loc in required.items():
        kind = loc["from"]
        if kind == "frontmatter_field":
            path = loc["path"]
            assert fm.get(path[0]), f"{name}: frontmatter field {path} missing"
        elif kind == "section_body":
            heading = loc["after_heading"]
            assert (SECTION_LEVEL, heading) in headings, (
                f"{name}: required section_body heading {heading!r} (H2) "
                f"absent from skeleton"
            )
        elif kind == "code_block":
            heading = loc["after_heading"]
            lang = loc.get("language")
            assert (SECTION_LEVEL, heading) in headings, (
                f"{name}: required code_block heading {heading!r} (H2) "
                f"absent from skeleton"
            )
            matching = [
                b for b in blocks if b[2] == heading and (lang is None or b[0] == lang)
            ]
            assert (
                matching
            ), f"{name}: no ```{lang} code block under {heading!r} in skeleton"
            assert matching[0][
                1
            ].strip(), f"{name}: ```{lang} block under {heading!r} is empty"
        else:  # pragma: no cover - guards against new locator kinds
            pytest.fail(f"{name}: unhandled required locator kind {kind!r}")


# ─── Reverse parity: skeleton cannot drift ahead of the contract ─────────


@pytest.mark.parametrize("name", _type_names(), ids=lambda n: n)
def test_skeleton_headings_all_asserted(name: str) -> None:
    """Every H2 heading in the skeleton maps to an asserted locator (required
    or optional) — a heading with no manifest assert is drift."""
    ot = _object_type(name)
    asserted = {
        loc["after_heading"]
        for loc in _locators(ot).values()
        if loc["from"] in ("section_body", "code_block")
    }
    for level, text in _skeleton_headings(_skeleton_text(name)):
        if level != SECTION_LEVEL:
            continue
        assert text in asserted, (
            f"{name}: skeleton heading {text!r} (H2) is not asserted by the "
            f"manifest (skeleton drifted ahead of the contract)"
        )


@pytest.mark.parametrize("name", _type_names(), ids=lambda n: n)
def test_skeleton_code_block_languages_asserted(name: str) -> None:
    """Every fenced block under an asserted code_block heading carries the
    asserted language."""
    ot = _object_type(name)
    lang_by_heading = {
        loc["after_heading"]: loc.get("language")
        for loc in _locators(ot).values()
        if loc["from"] == "code_block"
    }
    for lang, _content, heading in _skeleton_code_blocks(_skeleton_text(name)):
        if heading in lang_by_heading and lang_by_heading[heading] is not None:
            assert lang == lang_by_heading[heading], (
                f"{name}: block under {heading!r} is ```{lang}, manifest "
                f"asserts ```{lang_by_heading[heading]}"
            )


# ─── Substantive bodies ──────────────────────────────────────────────────


@pytest.mark.parametrize("name", _type_names(), ids=lambda n: n)
def test_asserted_section_bodies_substantive(name: str) -> None:
    """Every asserted section present in the skeleton has a non-empty,
    non-placeholder body."""
    ot = _object_type(name)
    asserted = {
        loc["after_heading"]
        for loc in _locators(ot).values()
        if loc["from"] in ("section_body", "code_block")
    }
    sections = _split_sections(_skeleton_text(name))
    assert sections, f"{name}: skeleton has no H2 sections"
    for heading, body in sections.items():
        assert heading in asserted  # guaranteed by the reverse-parity test
        assert body, f"{name}: section {heading!r} is empty in skeleton"
        lowered = body.lower()
        for token in _PLACEHOLDER_TOKENS:
            assert (
                token.lower() not in lowered
            ), f"{name}: section {heading!r} carries placeholder token {token!r}"


# ─── Roundtrip via the quire wheel (guarded) ─────────────────────────────


def _quire_doc_validator():
    """Return the quire wheel iff it exposes the markdown validator."""
    try:
        import quire
    except ImportError:
        return None
    if not hasattr(quire, "validate_document"):
        return None
    return quire


@pytest.mark.parametrize("name", _type_names(), ids=lambda n: n)
def test_roundtrip_skeleton_validates(name: str) -> None:
    """Each skeleton passes ``validate_document`` against this module.

    Skips when the installed quire wheel predates the markdown-default
    validator; build/install a local quire-rs wheel to exercise it."""
    quire = _quire_doc_validator()
    if quire is None:
        pytest.skip("quire wheel lacks validate_document")
    res = quire.validate_document(name, str(PKG_ROOT), _skeleton_text(name))
    assert res["is_valid"], res["errors"]


def test_roundtrip_mutations_fail() -> None:
    """Deleting a required section / code block / frontmatter field each
    fail validation."""
    quire = _quire_doc_validator()
    if quire is None:
        pytest.skip("quire wheel lacks validate_document")
    root = str(PKG_ROOT)

    def reasons(name: str, doc: str) -> set[str]:
        res = quire.validate_document(name, root, doc)
        assert not res["is_valid"], doc
        return {e["reason"] for e in res["errors"]}

    # a. delete the required Properties section from entity
    base = _skeleton_text("entity")
    mutated = re.sub(
        r"## Properties.*", "## Notes\n\nNothing here.\n", base, flags=re.DOTALL
    )
    assert mutated != base, "entity mutation did not apply"
    assert "missing" in reasons("entity", mutated)

    # b. strip the json code block from event
    base = _skeleton_text("event")
    mutated = re.sub(r"```json.*?```", "Schema prose only.", base, flags=re.DOTALL)
    assert mutated != base, "event mutation did not apply"
    assert "missing" in reasons("event", mutated)

    # c. drop the frontmatter id
    base = _skeleton_text("state_machine")
    mutated = base.replace("id: state-machine-001\n", "", 1)
    assert mutated != base, "state_machine mutation did not apply"
    assert "missing" in reasons("state_machine", mutated)
