"""Every companion case must ask for a period the module can actually answer.

A RuleSpec version is selected by the latest `effective_from` on or before the period's
start; if no version qualifies, the engine raises rather than answering. So a fixture
dated earlier than every version of the rule it asserts is a fixture that cannot run —
and, worse, a rule dated `0001-01-01` will silently answer such a fixture with a schedule
that was not in force in the year the fixture names. Review round 1 found exactly that on
ITO §121, whose bands commence 1 January 2026 (ס״ח 3511, פרק ג׳ §6) but were dated from
year 1 and asserted for tax year 2024.

These tests are the standing guard against it coming back. They read the YAML only; they
do not need the engine.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
IL = ROOT / "il"

# ITO §121's bands are the post-amendment-288 text. ס״ח 3511 of י״ג בניסן התשפ״ו,
# פרק ג׳ "ריווח מדרגות מס הכנסה", §6: תחילתו של פרק זה ביום י״ב בטבת התשפ״ו (1 בינואר 2026).
SECTION_121_COMMENCEMENT = dt.date(2026, 1, 1)

# The figures ס״ח 3511 §5 actually writes into §121, read from the captured gazette
# (sha256 4196057aa7d796bf64935647f4f3e3d02511fa00eaa215dc5ad914601b4e6583):
# §121(א)(1) -> 301,200; §121(א)(2) -> 301,201 עד 560,280 @35%;
# §121(ב)(1)(ג) upper -> 228,000; §121(ב)(1)(ד) -> 228,001 עד 301,200 @31%.
# 84,120 and 120,720 are NOT in this set — that act does not touch them.
AMENDMENT_288_FIGURES = {301200, 301201, 560280, 228000, 228001}


def _module_files() -> list[Path]:
    return sorted(
        path
        for path in IL.rglob("*.yaml")
        if not path.name.endswith(".test.yaml")
    )


def _load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _as_date(value) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value))


def _earliest_effective_from(rule: dict) -> dt.date | None:
    dates = [
        _as_date(version["effective_from"])
        for version in rule.get("versions") or []
        if version.get("effective_from")
    ]
    return min(dates) if dates else None


def _case_start(case: dict) -> dt.date:
    """A case with no period is an error, not a 2026 case.

    Defaulting here would let an undated fixture pass every check below while the
    engine resolved it against whatever period it inferred.
    """
    if "period" not in case:
        raise AssertionError(f"companion case {case.get('name')!r} declares no period")
    period = case["period"]
    if isinstance(period, dict):
        return _as_date(period["start"])
    text = str(period)
    if len(text) == len("2026-01"):
        return _as_date(f"{text}-01")
    return _as_date(text)


def _pairs() -> list[tuple[Path, Path]]:
    pairs = []
    for module_path in _module_files():
        test_path = module_path.with_suffix(".test.yaml")
        if test_path.exists():
            pairs.append((module_path, test_path))
    return pairs


def _commencements_by_module() -> dict[str, dict[str, dt.date]]:
    """{"statutes/.../section-121": {rule_name: earliest effective_from}}."""
    table: dict[str, dict[str, dt.date]] = {}
    for module_path in _module_files():
        module = _load(module_path) or {}
        module_id = module_path.relative_to(IL).with_suffix("").as_posix()
        table[module_id] = {
            rule["name"]: _earliest_effective_from(rule)
            for rule in module.get("rules") or []
            if rule.get("name")
        }
    return table


def _resolve(output_key: str) -> tuple[str, str] | None:
    """`il:statutes/x/section-1#rule` -> ("statutes/x/section-1", "rule")."""
    if "#" not in output_key:
        return None
    target, rule_name = output_key.rsplit("#", 1)
    _, _, path = target.partition(":")
    return path or None, rule_name


@pytest.mark.parametrize(
    "module_path,test_path",
    _pairs(),
    ids=lambda path: str(path.relative_to(ROOT)) if isinstance(path, Path) else path,
)
def test_no_companion_case_predates_the_rules_it_asserts(
    module_path: Path, test_path: Path
) -> None:
    """Every rule the case reaches, whether it asserts it or merely imports it.

    Asserted outputs are not the whole exposure: the composed capstone imports ITO §121
    and consumes it whether or not a case names `#income_tax` in its `output` map, so a
    case dated before §121 commences cannot run however its own versions are dated.
    Checking only `output` would have missed exactly that, which is the defect review
    round 1 raised.
    """
    commencements = _commencements_by_module()
    module = _load(module_path) or {}
    cases = _load(test_path) or []

    # Rules this module imports, and therefore reaches in every one of its cases.
    imported = []
    for entry in module.get("imports") or []:
        resolved = _resolve(str(entry))
        if resolved is not None:
            imported.append(resolved)

    failures = []
    unresolved = set()
    for case in cases:
        start = _case_start(case)
        reached = list(imported)
        for output in (case.get("output") or {}):
            resolved = _resolve(str(output))
            if resolved is None:
                continue
            reached.append(resolved)
        for module_id, rule_name in reached:
            if module_id not in commencements:
                unresolved.add(module_id)
                continue
            commences = commencements[module_id].get(rule_name)
            if commences is not None and start < commences:
                failures.append(
                    f"{case.get('name')}: asks for {start}, but "
                    f"{module_id}#{rule_name} commences {commences}"
                )

    assert not unresolved, (
        f"{module_path.relative_to(ROOT)} references modules that do not exist on disk, "
        "so their commencements were never checked: " + ", ".join(sorted(unresolved))
    )
    assert not failures, (
        f"{module_path.relative_to(ROOT)} has companion cases dated before the rules "
        "they reach are in force:\n  " + "\n  ".join(sorted(set(failures)))
    )


def _section_121_versions():
    module = _load(IL / "statutes/income-tax-ordinance/section-121.yaml")
    for rule in module["rules"]:
        for version in rule.get("versions") or []:
            yield rule["name"], version, _as_date(version["effective_from"])


def _carries_amendment_288_figures(version: dict) -> bool:
    """Does this version state a figure ס״ח 3511 §5 actually wrote?

    §5 replaces four things and nothing else: §121(א)(1)'s amount -> 301,200;
    §121(א)(2) -> "מ־301,201 ... עד 560,280 ... 35%"; §121(ב)(1)(ג)'s upper edge ->
    228,000; §121(ב)(1)(ד) -> "מ־228,001 ... עד 301,200 ... 31%". The 84,120 and
    120,720 edges and the 10%/14%/20%/47% rates are older text this act left alone,
    so a version stating only those is NOT dated by amendment 288.
    """
    values = version.get("values")
    if not isinstance(values, dict):
        return False
    return bool(AMENDMENT_288_FIGURES & {v for v in values.values()})


def test_amendment_288_figures_are_dated_from_its_commencement() -> None:
    """The figures ס״ח 3511 §5 wrote must carry that act's own commencement.

    This is anchored on the FIGURES, not on the module: a later ingest of the pre-288
    expression may legitimately add versions dated earlier, carrying the old amounts.
    What must never happen again is an amendment-288 figure claiming to have been in
    force before the act that wrote it.
    """
    offenders = [
        f"{name}: {start} states {sorted(AMENDMENT_288_FIGURES & set(version['values'].values()))}"
        for name, version, start in _section_121_versions()
        if _carries_amendment_288_figures(version) and start != SECTION_121_COMMENCEMENT
    ]
    assert not offenders, (
        "ITO §121 versions stating post-amendment-288 figures must commence "
        f"{SECTION_121_COMMENCEMENT} (ס״ח 3511, פרק ג׳ §6). These do not:\n  "
        + "\n  ".join(offenders)
    )


def test_no_earlier_period_receives_the_amendment_288_schedule() -> None:
    """A pre-2026 request must find the old amounts or nothing — never the new ones.

    Today no pre-288 expression is in this repository's corpus, so a 2025 request finds
    no version in force at all. That is the honest behaviour, and it is what this test
    enforces; it does NOT forbid the recorded resolution in docs/ENCODING-GAPS.md
    (`ito-section-121-dated-from-amendment-288`), which is to ingest the earlier
    expression and encode it as its own, earlier-dated version.
    """
    earlier = dt.date(2025, 12, 31)
    covering = [
        f"{name}: {start}"
        for name, version, start in _section_121_versions()
        if start <= earlier and _carries_amendment_288_figures(version)
    ]
    assert not covering, (
        "these ITO §121 versions would answer a 2025 request with amendment 288's "
        "figures: " + ", ".join(sorted(set(covering)))
    )
