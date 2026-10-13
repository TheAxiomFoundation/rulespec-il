# rulespec-il Agent Notes

> ⚠️ **Single source of truth for agent instructions.**
> `CLAUDE.md` and `GEMINI.md` both reference this file. Edit here, not in copies.

This repository holds Israel RuleSpec encodings, source-registry material, and
oracle references.

## Status: bounded pilot, encoder-generated

Two instruments — פקודת מס הכנסה (Income Tax Ordinance) and חוק הביטוח הלאומי
[נוסח משולב], התשנ״ה–1995 — at section granularity, plus one composed monthly
capstone. This is a proof of concept for a specific conversation, not coverage,
and the repository says so throughout: the app lists it as a bounded, uncertified
pilot (`app_visibility = "public"` since 2026-09-07), and no oracle coverage is
declared. Validation is bound to the signed corpus release named in
`.axiom/toolchain.toml`.

**Every atomic module here is produced by the supervised encoder** and carries an
apply manifest under `.axiom/encoding-manifests/`. With the guard on, a new or
changed module needs a manifest signed with the production apply key, which
axiom-encode's "Targeted signed RuleSpec re-encode" workflow produces after a
`production-signing` approval; a local `encode --apply` manifest is refused. Hand-written YAML is never a
module. The only hand work is a findings file handed back to the encoder for a
repair round, and the composed pipeline under `il/statutes/composed/`, which is
assembled rather than encoded.

The shared generated-content guard is on (#12). The modules on main came from a
local bootstrap build of axiom-encode, and their manifests are signed with a
throwaway local key, not the production apply key the guard verifies. The guard
checks only the modules a pull request changes, so those stay as they are until
they are re-encoded. `docs/ENCODING-GAPS.md` records the whole of it.

## Do

- Treat this as a pilot. Never write completeness, certification, or
  fitness-for-use language into this repository.
- Encode from the **Hebrew** text. English rule names and summaries are working
  aids and never the authority.
- Follow the source priority in `docs/sources-and-provenance.md`: Knesset
  national legislation database → Reshumot / ספר החוקים gazette PDFs → ספר החוקים
  הפתוח (he.wikisource, the consolidation the Knesset database itself links to)
  → Nevo as cross-check only. Record the tier on every provenance record.
- Produce every module through the encoder, never by hand. A defect in a
  generated module is fixed by writing a findings file and running another
  encoder round, not by editing the YAML.
- Put current-year regulated amounts — the credit-point value, the indexed
  §121ב threshold, the child-allowance basic amounts — only under `il/policies/`,
  encoded by the encoder from an ingested `il/policy` corpus citation of an
  official רשות המסים or ביטוח לאומי publication. No such scope exists yet, so
  today every current-year amount is a module `#input` whose provenance the
  fixtures state, recorded in `docs/ENCODING-GAPS.md`. Never take a current
  amount from OECD, Nevo, Wikisource annotations, or kol-zchut.
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

- Do not change `.axiom/toolchain.toml`, `.axiom/workflow-toolchain.toml` or
  workflow pins in a content PR. They move only in a dedicated, independently
  reviewed toolchain PR, as in #14.
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
