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
    period = case.get("period", "2026-01")
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
    """Including rules the case asserts on OTHER modules it imports.

    The composed capstone is the case that matters: it imports ITO §121, so it cannot
    answer a period earlier than §121's own commencement however its own versions are
    dated.
    """
    commencements = _commencements_by_module()
    cases = _load(test_path) or []

    failures = []
    for case in cases:
        start = _case_start(case)
        for output in (case.get("output") or {}):
            resolved = _resolve(str(output))
            if resolved is None:
                continue
            module_id, rule_name = resolved
            commences = (commencements.get(module_id) or {}).get(rule_name)
            if commences is not None and start < commences:
                failures.append(
                    f"{case.get('name')}: asks for {start}, but "
                    f"{module_id}#{rule_name} commences {commences}"
                )
    assert not failures, (
        f"{module_path.relative_to(ROOT)} has companion cases dated before the rules "
        "they assert are in force:\n  " + "\n  ".join(failures)
    )


def test_section_121_schedule_is_restricted_to_its_commencement() -> None:
    """The §121 bands must not claim to have been in force before 2026-01-01."""
    module = _load(IL / "statutes/income-tax-ordinance/section-121.yaml")
    offenders = []
    for rule in module["rules"]:
        for version in rule.get("versions") or []:
            start = _as_date(version["effective_from"])
            if start != SECTION_121_COMMENCEMENT:
                offenders.append(f"{rule['name']}: {start}")
    assert not offenders, (
        "ITO §121 carries the post-amendment-288 schedule, which commenced "
        f"{SECTION_121_COMMENCEMENT} (ס״ח 3511, פרק ג׳ §6). Every version must say so; "
        "these do not:\n  " + "\n  ".join(offenders)
    )


def test_section_121_has_no_version_covering_an_earlier_year() -> None:
    """An earlier period must fail to resolve, not receive the 2026 schedule.

    The pre-288 amounts are not in this repository's corpus, so the honest behaviour is
    for a 2025 request to find no version in force rather than to be answered with the
    2026 bands.
    """
    module = _load(IL / "statutes/income-tax-ordinance/section-121.yaml")
    earlier = dt.date(2025, 12, 31)
    covering = [
        rule["name"]
        for rule in module["rules"]
        for version in rule.get("versions") or []
        if _as_date(version["effective_from"]) <= earlier
    ]
    assert not covering, (
        "these ITO §121 rules would answer a 2025 request with the 2026 schedule: "
        + ", ".join(sorted(set(covering)))
    )
