# rulespec-il Agent Notes

> ⚠️ **Single source of truth for agent instructions.**
> `CLAUDE.md` and `GEMINI.md` both reference this file. Edit here, not in copies.

This repository holds Israel RuleSpec encodings, source-registry material, and
oracle references.

## Status: bounded, hand-authored pilot

Two instruments — פקודת מס הכנסה (Income Tax Ordinance) and חוק הביטוח הלאומי
[נוסח משולב], התשנ״ה–1995 — at section granularity, plus one composed monthly
capstone. This is a proof of concept for a specific conversation, not coverage,
and every surface in the repository says so: `app_visibility = "experimental"`,
no `.axiom/toolchain.toml`, no oracle coverage declared.

Unlike rulespec-am and rulespec-dk, the pilot modules here were **hand-authored
against captured snapshots**, not produced by the supervised encoder. The
shared generated-content guard is therefore pinned off in
`.github/workflows/repository-checks.yml`. Any campaign that supersedes the
pilot turns that guard on and re-encodes through the encoder.

## Do

- Treat this as a pilot. Never write completeness, certification, or
  fitness-for-use language into this repository.
- Encode from the **Hebrew** text. English rule names and summaries are working
  aids and never the authority.
- Follow the source priority in `docs/sources-and-provenance.md`: Knesset
  national legislation database → Reshumot / ספר החוקים gazette PDFs → ספר החוקים
  הפתוח (he.wikisource, the consolidation the Knesset database itself links to)
  → Nevo as cross-check only. Record the tier on every provenance record.
- Put current-year regulated amounts — the credit-point value, the indexed
  §121ב threshold, the child-allowance basic amounts — only under `il/policies/`
  from a captured official רשות המסים or ביטוח לאומי publication. If no such
  capture exists, make the amount a module `#input` and say so in
  `docs/ENCODING-GAPS.md`. Never take a current amount from OECD, Nevo,
  Wikisource annotations, or kol-zchut.
- Keep proof excerpts verbatim NFC substrings of the captured provision, with
  gershayim (״), geresh (׳) and maqaf (־) exactly as captured. YAML-quote any
  excerpt containing `: `.
- Transliterate Hebrew section suffixes by **ordinal**: א→a, ב→b, ג→c …
  §121ב → `section-121b`, §36א → `section-36a`, §120ב → `section-120b`.
- Give every module a companion `.test.yaml` assigning **every** local `#input`
  fact, including the FALSE ones, and give every derived rule an assertion.
- Use `period_kind` values `month`, `benefit_week`, `tax_year`, or `custom` —
  never `year`.
- Record divergence from a reference (OECD TaxBEN and similar) in
  `docs/ENCODING-GAPS.md` as `unexplained`, with both numbers.
- Read TheAxiomFoundation/.github#39 before opening any PR here.

## Do Not

- Do not add `.axiom/toolchain.toml` or change workflow pins in a content PR.
  Toolchain binding is a dedicated gated PR after the Israel corpus release is
  cut, signed and registered.
- Do not file issues against OECD or any other external oracle. Divergences are
  recorded here as `unexplained`.
- Do not assert an indexed current-year amount that the statute does not state.
  §33א states 504 ILS and §121ב states 640,000 ILS as **nominal** amounts under
  the §120א/§120ב indexation mechanism; the current values are not in the text.
- Do not treat the OECD TaxBEN description, press reporting, or a Wikisource
  editorial annotation as law.
- Do not migrate OpenFisca or PolicyEngine code mechanically as RuleSpec.
- Do not add repository-root content trees, `.yml` aliases, symlinks, or Python
  under `il/`.
