"""Quoin install roundtrip (IT-002, FR-003-AC-5): the module installs into
Quoin with the semantic
contract, and the operator's prior module state is restored unconditionally.

This row is a **Demonstration**: no released Quoin carries the semantic
installer (`agent-ix/quoin` main `3e842ce`, no tag contains it), and the
install mutates the operator's global `quoin module` store. It therefore runs
only when both are true:

* a Quoin whose `module install` understands `path:` is on `PATH`, and
* `QUOIN_INSTALL_ROUNDTRIP=1` is set, which is the operator saying "you may
  touch my global module store".

The restore step runs whether or not the install succeeded (IT-002-SC-06).
"""

from __future__ import annotations

import os
import shutil
import subprocess

import pytest

from tests.conftest import OBJECT_TYPES, PACKAGE_ROOT

OPT_IN = os.environ.get("QUOIN_INSTALL_ROUNDTRIP") == "1"
QUOIN = shutil.which("quoin")

needs_quoin = pytest.mark.skipif(
    not (OPT_IN and QUOIN),
    reason=(
        "IT-002 is a Demonstration against a Quoin built from agent-ix/quoin "
        "main at or after 3e842ce (no release carries the semantic installer), "
        "and it mutates the operator's global module store. Set "
        "QUOIN_INSTALL_ROUNDTRIP=1 with such a Quoin on PATH to run it; the "
        "matrix row stays 🚧 until then."
    ),
)


def quoin(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([QUOIN, *args], capture_output=True, text=True, check=False)


@pytest.mark.trace("TC-027", "FR-003-AC-5")
@pytest.mark.trace(
    "TC-070",
    "IT-002-SC-01",
    "IT-002-SC-02",
    "IT-002-SC-03",
    "IT-002-SC-04",
    "IT-002-SC-05",
    "IT-002-SC-06",
)
@pytest.mark.integration
@needs_quoin
def test_the_module_installs_into_quoin_and_the_prior_state_is_restored():
    import json

    # IT-002-SC-01: record the listing before touching anything.
    before = quoin("module")
    assert before.returncode == 0, before.stderr
    recorded = before.stdout

    try:
        # IT-002-SC-02: install with no `semantic.*` error diagnostic.
        install = quoin("module", "install", f"path:{PACKAGE_ROOT}")
        assert install.returncode == 0, install.stderr
        combined = install.stdout + install.stderr
        assert "semantic." not in combined or "error" not in combined.lower(), combined

        # IT-002-SC-03: the module is listed, sourced from the path.
        listing = quoin("module")
        assert listing.returncode == 0
        assert "spec-objects-business" in listing.stdout

        # IT-002-SC-04: the derived package manifest names every export.
        # A contract check on quoin FR-075, not a claim this module owns.
        installed_root = os.path.expanduser(
            "~/.ix/filament/modules/spec-objects-business"
        )
        package_manifest = os.path.join(
            installed_root, "semantic", "package-manifest.json"
        )
        assert os.path.isfile(package_manifest), package_manifest
        derived = json.loads(open(package_manifest).read())
        assert derived["package"]["identity"] == "agent-ix/spec-objects-business"
        assert len(derived["exports"]) == len(OBJECT_TYPES)
    finally:
        # IT-002-SC-05/SC-06: the restore runs even when a step above failed.
        quoin("module", "install", "spec-objects-business")
        after = quoin("module")
        assert after.stdout == recorded, (
            "the prior quoin module state was not restored:\n"
            f"before:\n{recorded}\nafter:\n{after.stdout}"
        )
