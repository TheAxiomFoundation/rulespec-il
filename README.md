# rulespec-il

Israel RuleSpec source registry — **bounded pilot**.

> **This is a pilot, not coverage.** Two instruments, a handful of sections, one
> composed capstone. Nothing here is certified, complete, or fit for
> administrative use. `app_visibility` is `experimental`.

## What is encoded

A deliberately small, end-to-end-testable slice chosen so a reader can check
every number against the Hebrew statute:

| Module | Provision | What it encodes |
|---|---|---|
| `il/statutes/income-tax-ordinance/section-121.yaml` | פקודת מס הכנסה §121 | individual rate schedule — the §121(א) general bands and the §121(ב)(1) reduced bands for earned income (הכנסה מיגיעה אישית), for tax years 2025 and 2026 |
| `il/statutes/income-tax-ordinance/section-121b.yaml` | §121ב | מס נוסף — the 3% additional tax on high income and the 2% additional tax on capital-source income |
| `il/statutes/income-tax-ordinance/section-120b.yaml` | §120ב | the annual indexation rule and the §120ב(ה) statutory freeze of the amounts for tax years 2025–2027 |
| `il/statutes/income-tax-ordinance/section-33a.yaml` | §33א | the definition of נקודת זיכוי (credit point) as a nominal 504 ILS indexed under §120א |
| `il/statutes/income-tax-ordinance/section-34.yaml` | §34 | resident credit — two credit points |
| `il/statutes/income-tax-ordinance/section-36.yaml` | §36 | travel-to-work credit — ¼ credit point |
| `il/statutes/income-tax-ordinance/section-36a.yaml` | §36א | woman's credit — ½ credit point |
| `il/statutes/income-tax-ordinance/section-66.yaml` | §66(ג)(4)–(5) | child credit points by age band under separate calculation (חישוב נפרד) |
| `il/statutes/national-insurance-law-1995/section-1.yaml` | חוק הביטוח הלאומי §1 | the הסכום הבסיסי definition, paragraph (2), for child allowance |
| `il/policies/national-insurance-institute/child-allowance-rates.yaml` | ביטוח לאומי publication | the published monthly allowance amounts, effective 1 January 2026 — the only official current-year capture in this pilot |
| `il/statutes/national-insurance-law-1995/section-66.yaml` | §66 | right to child allowance, and its exclusion of parents liable to the ITO §121ב additional tax |
| `il/statutes/national-insurance-law-1995/section-67.yaml` | §67 | which parent a child is counted with |
| `il/statutes/national-insurance-law-1995/section-68.yaml` | §68 | monthly allowance per child, the pre-2003 fourth/fifth-child multipliers, and the §68(ג) income-support increment |
| `il/statutes/composed/worker-with-children-monthly-net-pipeline.yaml` | composed | gross monthly wage → income tax after credit points → §121ב additional tax → child allowance → monthly net |

Every module has a companion `.test.yaml` in which **every** local `#input`
fact is assigned, including the false ones.

## Hebrew is the only authentic language

The encoded source is the Hebrew text. English in this repository — rule names,
summaries, this README — is a working aid and is never the authority. Proof
excerpts are verbatim NFC substrings of the captured Hebrew provision, with
gershayim (״), geresh (׳) and maqaf (־) preserved as captured. Section suffixes
transliterate by ordinal, not by sound: §121ב → `section-121b`, §36א →
`section-36a`.

## Source priority

1. **Knesset national legislation database** (מאגר החקיקה הלאומי) — the official
   registry. The Income Tax Ordinance is `IsraelLawID` 2000944, the National
   Insurance Law 2000198. The database renders client-side and
   `KNS_DocumentIsraelLaw` returns empty over OData, so it is used here as the
   authority for *what the law is and how it was amended*, not as a text source.
2. **Reshumot / ספר החוקים** — official gazette PDFs on `fs.knesset.gov.il`, the
   authentic text of each amending act. Used here to establish effective dates
   and the content of the 2026 bracket amendment.
3. **ספר החוקים הפתוח** on he.wikisource — the consolidation the Knesset database's
   own "לחוק המלא" link points to. Tier: `consolidation-knesset-linked`. This is
   the provision source of record for the pilot, and that is a **secondary
   tier** — recorded as such here, in every module's provenance, and in the PR.
4. **Nevo** (`nevo.co.il`) — commercial consolidation, cross-check only.
5. **רשות המסים** (Tax Authority) and **המוסד לביטוח לאומי** (National Insurance
   Institute) publications under `il/policies/` — the only admissible source for
   current-year regulated amounts.
6. Oracles are never law. See `data/oracles/oracle-index.json`.

Statutes carry no copyright in Israel (Copyright Act 2007 §6). The editorial
apparatus of a consolidation belongs to its publisher; only statutory text is
extracted, and amendment-history brackets are stripped from provision bodies.

## Validation year and the two-year encoding

The pilot validates against **2025**, the year described by the OECD TaxBEN
Israel policy description held in this repository's oracle index. It also
encodes **2026**, because the two differ and the difference is instructive:

- §120ב(ה)(1) froze the indexed amounts for tax years 2025–2027 at their
  1 January 2024 level. The statute says so directly; it is not inferred.
- Separately, the Economic Efficiency Law for budget year 2026 (ס״ח 3511, פרק ג׳,
  ITO amendment 288) *widened the 20% and 31% bands by statute*, effective
  1 January 2026. Frozen indexation and a statutory band change are different
  things, and both are encoded with their own `effective_from`.

## Amounts that are NOT in this repository

The Ordinance states the credit-point value (§33א) and the §121ב additional-tax
threshold as **nominal historical amounts** subject to indexation — 504 ILS and
640,000 ILS respectively — not as current-year figures. This repository does not
compute indexation and does not carry an official current-year capture, so those
current values enter the composed pipeline as **supplied inputs**, and the test
fixtures label where each supplied number came from. See `docs/ENCODING-GAPS.md`.

By contrast, the §121 bracket thresholds *are* stated as current amounts in the
consolidated text and were written into the statute by the 2026 amending act, so
they are encoded as parameters.

The child allowance amounts are **not** in that supplied category. Both years now
come from the National Insurance Institute's own rate page: the live capture for
2026, and the same official page as it stood on 2025-04-20 for 2025, retrieved
from the Internet Archive because the live page no longer states the earlier
amounts. The publisher is the Institute; the archive is only the delivery
channel, and the retrieved bytes carry their own provenance record. Both
snapshots also state the §68(ג) income-support increment — 111 and 113 — which
the statute expresses as 70% of a basic amount this repository has not captured
for either year. That mismatch is recorded, not papered over.

## Corpus anchoring

Proof excerpts quote the captured snapshots, because no signed `il-rulespec-*`
corpus release exists. The Israel ingest does exist as an unmerged branch, so the
re-anchor pass has been run against it read-only: **82 of 100 proof excerpts are
already verbatim in the corpus body.** The remaining 18 are two structural gaps,
not excerpt defects — the corpus has no `il/policy` scope for the Institute's
publication (14 atoms), and it holds only the 2026 expression of §121 while this
pilot's validation year is 2025 (4 atoms). Both are written up in
`docs/ENCODING-GAPS.md` under `corpus-anchor`, together with the seven
`source_sha256` pins that will need repinning and the digests to repin them to.

## Toolchain binding

`.axiom/toolchain.toml` is deliberately **absent**: no signed `il-rulespec-*`
corpus release exists yet, and binding a repository to a release that does not
exist would be a false claim. `.github/workflows/repository-checks.yml` is
structurally the shared validate workflow used by the other jurisdiction repos,
and toolchain binding lands in a dedicated PR after the Israel corpus release is
cut, signed, and registered — never combined with content changes.

Because this pilot is **hand-authored** rather than encoder-produced, the shared
generated-content guard is pinned off. That is a pilot property and is stated
here rather than hidden.

**CI is red on `pilot-v0`, on purpose.** The shared workflow fails with

```
RuleSpec toolchain error: a regular .axiom/toolchain.toml is required
```

because it is fail-closed on the toolchain binding, and that binding cannot
honestly exist before the Israel corpus release is cut and signed. The check is
behaving correctly; making it green would mean either pinning a release that does
not exist or weakening the gate, and neither is acceptable. What the pilot could
verify locally, it verified — see `docs/ENCODING-GAPS.md`,
`validators-not-run-as-shipped`, for the commands and their results.

## Context

Chartered 2026-09-06 for a bounded Israel proof of concept. Lineage:
a PolicyEngine Israel hackathon run with the Prime Minister's Office and
digital.gov.il on 2023-07-06 encoded municipal tax reduction and
discharged-soldier credits; this repository is the Axiom-native successor.
See `docs/encoding-charter.md`.
