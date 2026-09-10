from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIRS = ("statutes", "regulations", "policies", "legislation")
IL_BUCKETS = (*CONTENT_DIRS, "programs")
IGNORED_ROOT_DIRS = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    # The shared validator checks immutable toolchain repositories out here
    # before running this repository's tests. Tracked paths are rejected by a
    # separate test, so ignoring this transient directory does not weaken the
    # committed layout contract.
    "_axiom",
    "__pycache__",
}
ALLOWED_ROOT_DIRS = {
    ".axiom",
    ".github",
    "data",
    "docs",
    "il",
    "src",
    "tests",
}
ALLOWED_ROOT_FILES = {
    ".gitignore",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "LICENSE",
    "LICENSE-CODE",
    "NOTICE",
    "README.md",
    "known-missing-money-atoms.yaml",
    "known-validation-gaps.yaml",
    "oracle-coverage-pending.yaml",
}
# Hebrew-letter section suffixes transliterate by ORDINAL, not by sound.
HEBREW_SUFFIX_ORDINALS = {
    "א": "a",
    "ב": "b",
    "ג": "c",
    "ד": "d",
    "ה": "e",
    "ו": "f",
    "ז": "g",
    "ח": "h",
    "ט": "i",
    "י": "j",
}


def rulespec_files() -> list[Path]:
    return sorted(
        path
        for bucket in CONTENT_DIRS
        for path in (ROOT / "il" / bucket).rglob("*.yaml")
        if not path.name.endswith(".test.yaml")
    )


def test_only_il_namespace_present() -> None:
    jurisdiction_names = {
        child.name
        for child in ROOT.iterdir()
        if child.is_dir()
        and re.fullmatch(r"[a-z]{2}(?:-[a-z0-9-]+)*", child.name)
        and any((child / marker).is_dir() for marker in CONTENT_DIRS)
    }
    assert jurisdiction_names <= {"il"}


def test_il_content_buckets_exist() -> None:
    for bucket in IL_BUCKETS:
        assert (ROOT / "il" / bucket).is_dir()


def test_root_inventory_is_allowed() -> None:
    directories = {
        child.name
        for child in ROOT.iterdir()
        if child.is_dir() and child.name not in IGNORED_ROOT_DIRS
    }
    files = {
        child.name for child in ROOT.iterdir() if child.is_file() and child.name != ".git"
    }
    assert not directories - ALLOWED_ROOT_DIRS
    assert not files - ALLOWED_ROOT_FILES


def test_transient_axiom_workspace_has_no_tracked_paths() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--", "_axiom"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    assert tracked == b""


def test_programs_remain_empty_until_program_guard_is_enabled() -> None:
    tracked_content = [
        path
        for path in (ROOT / "il" / "programs").rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]
    assert tracked_content == []


def test_structure_manifest_matches_repository_contract() -> None:
    manifest = yaml.safe_load((ROOT / ".axiom/repository-structure.yaml").read_text())
    assert manifest["version"] == 1
    assert set(manifest["allowed_root_directories"]) == ALLOWED_ROOT_DIRS
    assert set(manifest["allowed_root_files"]) == ALLOWED_ROOT_FILES


def test_every_rulespec_has_companion_test() -> None:
    for path in rulespec_files():
        assert path.with_name(path.stem + ".test.yaml").exists()


def test_empty_ratchets_have_current_shapes() -> None:
    validation_gaps = yaml.safe_load((ROOT / "known-validation-gaps.yaml").read_text())
    assert validation_gaps == {"validate_failures": {}}

    missing_money = yaml.safe_load((ROOT / "known-missing-money-atoms.yaml").read_text())
    assert missing_money == {"total_allowed": 0}

    # The oracle-coverage pending ratchet is no longer empty: with the pilot's
    # modules merged, every executable output is declared pending
    # classification (there is no PolicyEngine Israel model to map it to), so
    # the shape is pinned instead of the emptiness.
    pending = yaml.safe_load((ROOT / "oracle-coverage-pending.yaml").read_text())
    assert set(pending) == {"version", "issue", "ceiling", "entries"}
    assert pending["version"] == 1
    assert pending["issue"] == "https://github.com/TheAxiomFoundation/rulespec-il/issues/2"
    assert pending["ceiling"] == len(pending["entries"])


def test_scoped_indexes() -> None:
    for relative in (
        "data/oracles/oracle-index.json",
        "data/coverage/tax-benefit-source-map.json",
    ):
        payload = json.loads((ROOT / relative).read_text())
        assert payload["jurisdiction"] == "il"


def test_no_reference_is_declared_executable() -> None:
    """Israel has no wired oracle. Nothing in the index may claim otherwise."""
    payload = json.loads((ROOT / "data/oracles/oracle-index.json").read_text())
    for oracle in payload["oracles"]:
        assert oracle["executable"] is False, oracle["id"]
        assert oracle["kind"] in {"reference", "candidate_oracle"}, oracle["id"]


def test_no_oracle_coverage_is_claimed_while_none_is_wired() -> None:
    """A pending declaration is visible debt, not a coverage claim.

    Israel has no wired oracle, so every executable output the classifier finds
    is declared pending classification: each entry names one `il:` output with
    its source and date and nothing else -- no PolicyEngine variable, parameter
    or mapping type, which would be a claim of coverage this pilot cannot make.
    The ceiling equals the declared count, so the ratchet can only drain.
    """
    pending = yaml.safe_load((ROOT / "oracle-coverage-pending.yaml").read_text())
    entries = pending["entries"]
    assert entries, "the pilot's executable outputs must be declared pending"
    assert pending["ceiling"] == len(entries)
    for entry in entries:
        assert set(entry) == {"legal_id", "source", "since"}, entry
        assert entry["legal_id"].startswith("il:statutes/"), entry["legal_id"]
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", entry["since"]), entry
    assert len({entry["legal_id"] for entry in entries}) == len(entries)


def test_pilot_is_bound_to_the_published_corpus_release() -> None:
    """toolchain.toml and the coverage map name the same signed il-rulespec release."""
    import tomllib

    toolchain = tomllib.loads((ROOT / ".axiom/toolchain.toml").read_text())["toolchain"]
    assert set(toolchain) == {
        "axiom_corpus_release",
        "axiom_corpus_release_content_sha256",
        "validation_waiver_set_sha256",
    }
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", toolchain["axiom_corpus_release"])
    assert toolchain["axiom_corpus_release"] != "current"
    for key in ("axiom_corpus_release_content_sha256", "validation_waiver_set_sha256"):
        assert re.fullmatch(r"[0-9a-f]{64}", toolchain[key]), key
    payload = json.loads((ROOT / "data/coverage/tax-benefit-source-map.json").read_text())
    candidate = payload["release_candidate"]
    assert candidate["status"] == "published"
    assert candidate["name"] == toolchain["axiom_corpus_release"]
    assert candidate["content_sha256"] == toolchain["axiom_corpus_release_content_sha256"]
    assert [scope["release"] for scope in payload["corpus_scopes"]] == [candidate["name"]]


def test_registry_visibility_is_public() -> None:
    # Flipped from "experimental" on 2026-09-07 together with the app's family
    # entry (the two-key promotion axiom.org's check-rulespec-drift.mjs enforces).
    text = (ROOT / ".axiom/registry.toml").read_text()
    assert 'app_visibility = "public"' in text


def test_statute_module_paths_use_ordinal_hebrew_suffix_transliteration() -> None:
    """section-121b, not section-121v; section-36a, not section-36alef.

    Statute modules are named for the section they encode. Composed pipelines and
    policy-publication modules under il/policies/ are named for what they are, so
    they are outside this contract.
    """
    allowed = set(HEBREW_SUFFIX_ORDINALS.values())
    for path in rulespec_files():
        if path.parent.name == "composed" or "policies" in path.parts:
            continue
        match = re.fullmatch(r"section-(\d+)([a-z]*)", path.stem)
        assert match is not None, path
        suffix = match.group(2)
        assert suffix == "" or suffix in allowed, path


def test_source_map_names_only_sections_that_are_encoded() -> None:
    """The coverage map must not list a section with no module on disk."""
    payload = json.loads((ROOT / "data/coverage/tax-benefit-source-map.json").read_text())
    instrument_dirs = {
        "income-tax-ordinance": ROOT / "il/statutes/income-tax-ordinance",
        "national-insurance-law-1995": ROOT / "il/statutes/national-insurance-law-1995",
    }
    for instrument in payload["instruments"]:
        directory = instrument_dirs[instrument["id"]]
        on_disk = {
            path.stem
            for path in directory.glob("*.yaml")
            if not path.name.endswith(".test.yaml")
        }
        for section in instrument["encoded_sections"]:
            number = section.split(" ")[0]
            slug = "section-" + "".join(
                HEBREW_SUFFIX_ORDINALS.get(character, character) for character in number
            )
            assert slug in on_disk, (instrument["id"], section, slug)


def test_policy_modules_carry_an_official_publisher_capture() -> None:
    """A current-year amount may only enter through il/policies/.

    The coverage map must record the publication behind every policy module, with
    a sha256 and a retrieval time, so a supplied number can always be traced.
    """
    policy_modules = sorted(
        path
        for path in (ROOT / "il" / "policies").rglob("*.yaml")
        if not path.name.endswith(".test.yaml")
    )
    payload = json.loads((ROOT / "data/coverage/tax-benefit-source-map.json").read_text())
    recorded = {item["module"] for item in payload.get("policy_publications", [])}
    for path in policy_modules:
        relative = str(path.relative_to(ROOT))
        assert relative in recorded, relative
    for item in payload.get("policy_publications", []):
        assert len(item["sha256"]) == 64, item["id"]
        assert item["url"].startswith("https://"), item["id"]
        assert item["retrieved_at"].endswith("Z"), item["id"]


def _cited_corpus_paths() -> set[str]:
    """Every corpus_citation_path reached from any proof atom in any module."""
    found: set[str] = set()

    def walk(node) -> None:
        if isinstance(node, dict):
            value = node.get("corpus_citation_path")
            if isinstance(value, str):
                found.add(value)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    for path in rulespec_files():
        walk(yaml.safe_load(path.read_text(encoding="utf-8")))
    return found


def test_source_map_accounts_for_every_provision_the_modules_cite() -> None:
    """The other direction: nothing may be cited without being declared.

    `test_source_map_names_only_sections_that_are_encoded` stops the map claiming a
    module that does not exist. This stops the reverse — a provision a shipped number
    actually depends on that the map never mentions, so anything built from the map
    under-reports the law behind the answer. NII §65 and ITO §2 are exactly that case:
    both are applied in the composition and neither is a module, so both are declared
    under `applied_without_a_module`.
    """
    payload = json.loads((ROOT / "data/coverage/tax-benefit-source-map.json").read_text())
    declared = set()
    for instrument in payload["instruments"]:
        prefix = f"il/statute/{instrument['id']}"
        declared.add(prefix)
        for section in instrument["encoded_sections"]:
            declared.add(f"{prefix}/section-{section.split(' ')[0]}")
        for entry in instrument.get("applied_without_a_module") or []:
            declared.add(entry["corpus_citation_path"])

    # encoded_sections prints Hebrew suffixes (33א); citation paths transliterate (33a).
    ordinals = {hebrew: latin for hebrew, latin in HEBREW_SUFFIX_ORDINALS.items()}
    expanded = set(declared)
    for value in declared:
        for hebrew, latin in ordinals.items():
            if value.endswith(hebrew):
                expanded.add(value[: -len(hebrew)] + latin)

    missing = sorted(_cited_corpus_paths() - expanded)
    assert not missing, (
        "these provisions are cited by a proof atom but appear nowhere in "
        "data/coverage/tax-benefit-source-map.json, so the map under-reports the law "
        "behind a computed number:\n  " + "\n  ".join(missing)
    )
