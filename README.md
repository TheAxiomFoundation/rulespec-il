# rulespec-il

Israel RuleSpec source registry — **bounded pilot**.

> **This is a pilot, not coverage.** Three instruments, a handful of sections, one
> composed capstone. Nothing here is certified, complete, or fit for
> administrative use. The app lists it publicly (`.axiom/registry.toml`), as a
> bounded, uncertified pilot.

## How this content was produced

**All atomic modules are encoder-generated.** Each was produced by
`axiom-encode encode <corpus citation> --backend codex --apply` against the Israel
corpus ingest, and each carries an apply manifest under `.axiom/encoding-manifests/`
recording the run id, the model, the encoder version and commit, the prompt digest, the
sha256 of every applied file, and the chain of superseded runs behind it. The encoder
is a **local bootstrap build of axiom-encode ref `55beb160`** carrying five fixes for
Hebrew source text, listed in `docs/ENCODING-GAPS.md` under
`encoder-hebrew-fixes-pending-upstream`. The fixes were made as the pilot ran, so the
manifests carry versions from `0.2.1197` to `0.2.1197.5` — each one records the exact
version and commit sha of the build that produced it. Repair rounds were driven by
written findings files, never by editing the YAML.

The one file that is not encoder-generated is the composed pipeline,
`il/statutes/composed/worker-with-children-monthly-net-pipeline.yaml`. A composition is
**assembled**: it declares imports of rules the encoder produced and the wiring between
them. It states no statutory quantity the atomic modules do not already carry. It does
carry one statutory *condition* the modules cannot supply in this shape — NII §65(א)'s
`ובלבד שהילד נמצא בישראל ולא מלאו לו 18 שנים`, which has to be asked once per child — with
a verbatim proof atom against the provision. `docs/ENCODING-GAPS.md`,
`nii-section-65-child-definition-partial`, says what that costs.

## What is encoded

A deliberately small, end-to-end-testable slice chosen so a reader can check every number
against the Hebrew statute:

| Module | Provision | What it encodes | Rules | Encoder run |
|---|---|---|---|---|
| `il/statutes/income-tax-ordinance/section-121.yaml` | §121 | the individual rate schedule — the §121(א) general bands and the §121(ב)(1) reduced bands for earned income (הכנסה מיגיעה אישית), withdrawn by §121(ב)(2) where acceptable books were not kept | 10 | `f9f8d0e4` / gpt-6-astra |
| `il/statutes/income-tax-ordinance/section-121b.yaml` | §121ב | מס נוסף — the 3% additional tax above 640,000 ILS and the 2% additional tax on capital-source income, with the §121ב(ה) definition that separates the two bases | 10 | `17f7e7e7` / gpt-6-astra |
| `il/statutes/income-tax-ordinance/section-120b.yaml` | §120ב | the §120ב(ה)(1) suspension of indexation for tax years 2025–2027. The indexation mechanism itself is NOT encoded | 1 | `44dee41d` / gpt-5.6-terra |
| `il/statutes/income-tax-ordinance/section-33a.yaml` | פקודת מס הכנסה §33א | the definition of נקודת זיכוי — a nominal 504 ILS a tax year, index-linked under §120א — and the §33א(2) pension-point divisor | 2 | `e27027ce` / gpt-5.6-terra |
| `il/statutes/income-tax-ordinance/section-34.yaml` | §34 | the resident credit — two credit points for an individual resident in Israel in the tax year | 2 | `5283d2a1` / gpt-5.6-terra |
| `il/statutes/income-tax-ordinance/section-36.yaml` | §36 | the travel-to-work credit — ¼ of a credit point | 4 | `71a86074` / gpt-5.6-terra |
| `il/statutes/income-tax-ordinance/section-36a.yaml` | §36א | the woman's credit — ½ a credit point | 2 | `3c640046` / gpt-5.6-terra |
| `il/statutes/income-tax-ordinance/section-66.yaml` | §66 | separate calculation (חישוב נפרד) for a non-registered spouse, and the §66(ג)(4)(א) and §66(ג)(5) child credit-point ladders by age band | 36 | `565292ca` / gpt-6-astra |
| `il/statutes/national-insurance-law-1995/section-1.yaml` | חוק הביטוח הלאומי §1 | the הסכום הבסיסי definition, paragraph (2) — the child-allowance base amounts | 3 | `cc386cda` / gpt-5.6-terra |
| `il/statutes/national-insurance-law-1995/section-66.yaml` | §66 | the right to a monthly child allowance, and its exclusion of a parent liable to the ITO §121ב additional tax | 1 | `4a2c295e` / gpt-6-astra |
| `il/statutes/national-insurance-law-1995/section-67.yaml` | §67 | which parent a child is counted with — §67(ב)'s father limb and its `זולת אם` exception, the natural/other-parent limb with its `והם מבוטחים` condition, and §67(א)'s one-parent-at-a-time limit | 3 | `d1f0cc50` / gpt-6-astra |
| `il/statutes/national-insurance-law-1995/section-68.yaml` | §68 | the monthly allowance per child, the pre-June-2003 fourth/fifth-child multipliers, and the §68(ג) income-support increment | 8 | `bbcab920` / gpt-5.6-terra |
| `il/statutes/national-insurance-law-1995/section-334.yaml` | §334 | מדרגת הגבייה המופחתת — the reduced collection bracket, 7,522 ILS updated each 1 January by the price-index ratio (2026–2028) or the average-wage ratio (from 2029), and §334(ב)'s deeming of a statutory-salary holder as an employee | 6 | `7674bd8a` / gpt-6-astra |
| `il/statutes/national-insurance-law-1995/section-337.yaml` | §337 | the §337(א)(1) monthly contribution for an employee: the לוח י׳ טור ג׳ total rates (5.55% / 14.6% in 2025–2026) on the income up to the bracket and above it. That is employer and employee together, not the employee's own deduction (טור ד׳), whatever the output name `employee_monthly_insurance_contributions` suggests | 2 | `1f07bdc9` / gpt-6-astra, imports re-pinned by `repair-proof-import-hashes` |
| `il/statutes/national-insurance-law-1995/section-342.yaml` | §342 | the §342(א) self-payer judgment, the §342(ד) multiple-employer shortfall and refund, and §342(ג)(2)'s cessation age for a man (70). The §342(ג)(1) employee deduction itself is deferred by the encoder, for want of Schedule A1 Part D (`docs/ENCODING-GAPS.md`, `nii-schedule-a1-part-d-not-encoded`) | 4 | `ba681bc7` / gpt-6-astra |
| `il/statutes/national-insurance-law-1995/section-348.yaml` | §348 | the §348(א) maximum on the income contributions are levied on, and the §348(א1) exclusion of small non-work income | 4 | `acd42bb2` / gpt-6-astra, imports re-pinned by `repair-proof-import-hashes` |
| `il/statutes/national-insurance-law-1995/schedule-j/sign-1.yaml` | לוח י׳ | the contribution and deduction rate table (טור ג׳ and ד׳), by branch and in total, for employees, the self-employed and others, with its dated temporary rates. טור ה׳, the Treasury allocation, is deferred as a rate, because its heading prints no unit; its figures are kept as printed | 19 | `1d4a7a99` / gpt-6-astra |
| `il/statutes/national-insurance-law-1995/schedule-k/sign-1.yaml` | לוח י״א | the maximum and minimum insurable income; the employee's monthly maximum is five times basic amount 3 | 9 | `2a7325d6` / gpt-6-astra |
| `il/statutes/national-health-insurance-law-1994/section-14.yaml` | חוק ביטוח בריאות ממלכתי §14 | the employee's health insurance contribution withheld by the employer: 3.23% up to the §341 reduced amount (§14(ו1)) and 5.17% above it (§14(ב)(1)), with the §14(ז)–(ז1) exemptions, the §14(ה) pensioner schedule that displaces it, and the §14(ז2) temporary inclusion of §350א(א)-exempt income | 13 | `9c1e3dfa` / gpt-6-astra |
| `il/statutes/composed/worker-with-children-monthly-net-pipeline.yaml` | composed | gross monthly wage → income tax after credit points → §121ב additional tax → child allowance, counted over the children NII §65(א) admits → monthly net → less the NII §342 deduction and the health §14 contribution, on the wage up to the לוח י״א maximum → monthly take-home pay before pension contributions | 54 | assembled, not encoded |

Every module that reads a fact has a companion `.test.yaml` in which **every** local
`#input` fact is assigned, including the false ones. The two modules that read none —
§33א and NII §1, which are nothing but the amounts their provisions print — have an empty
companion file, because the encoder deterministically empties the companion file of a
parameter-only module. Those amounts are exercised where they are consumed, in the composed
pipeline's fixtures. See `docs/ENCODING-GAPS.md`,
`parameter-only-modules-carry-no-companion-cases`.

## Hebrew is the only authentic language

The encoded source is the Hebrew text. English in this repository — rule names,
summaries, this README — is a working aid and is never the authority. Proof
excerpts are verbatim NFC substrings of the captured Hebrew provision, with
gershayim (״), geresh (׳) and maqaf (־) preserved as captured. Section suffixes
transliterate by ordinal, not by sound: §121ב → `section-121b`, §36א →
`section-36a`.

Getting the encoder to read Hebrew at all took five fixes to it, each found by a module
that came out wrong: a maqaf glued to a digit (`מ־84,120` parsed as 120), the Unicode
fraction slash a printed `2½` flattens to (`21⁄2` parsed as twenty-one halves), Hebrew
numerals spelled as words (`שתי`, `שלושה`, `הילד הרביעי`), a `yaml.safe_dump` that
escaped every non-Latin character out of the file, and — separately — the same escaping
where the *model* chose to write it, which `--apply` copies verbatim and so no findings
file can reach. See `docs/ENCODING-GAPS.md`.

## Source priority

1. **Knesset national legislation database** (מאגר החקיקה הלאומי) — the official
   registry. The Income Tax Ordinance is `IsraelLawID` 2000944, the National
   Insurance Law 2000198, the National Health Insurance Law 2000111. The database renders client-side and
   `KNS_DocumentIsraelLaw` returns empty over OData, so it is used here as the
   authority for *what the law is and how it was amended*, not as a text source.
2. **Reshumot / ספר החוקים** — official gazette PDFs on `fs.knesset.gov.il`, the
   authentic text of each amending act. Used here to establish effective dates
   and the content of the 2026 bracket amendment.
3. **ספר החוקים הפתוח** (the Open Law Book) on he.wikisource — a volunteer project of
   [Hasadna](https://www.hasadna.org.il/openlaw/), and the consolidation the Knesset
   database's own "לחוק המלא" link points to. Tier: `consolidation-knesset-linked`. This is
   the provision source of record for the pilot, and that is a **secondary
   tier** — recorded as such here, in `data/coverage/tax-benefit-source-map.json`
   (`source_tier: consolidation-knesset-linked`) and in the PR. No module records a
   source tier of its own: a module declares a `corpus_citation_path` and nothing about
   the tier of the text behind it, so the tier is a property of the ingest, not of the
   encoding.
4. **Nevo** (`nevo.co.il`) — commercial consolidation, cross-check only.
5. **רשות המסים** (Tax Authority) and **המוסד לביטוח לאומי** (National Insurance
   Institute) publications — the only admissible source for current-year regulated
   amounts. None has been ingested as an `il/policy` corpus scope, so none is encoded
   here; the current-year amounts the composed pipeline uses are **supplied inputs**,
   labelled case by case.
6. Oracles are never law. See `data/oracles/oracle-index.json`.

Statutes carry no copyright in Israel (Copyright Act 2007 §6). The editorial
apparatus of a consolidation belongs to its publisher; only statutory text is
extracted, and amendment-history brackets are stripped from provision bodies.

## What the modules speak for

**Tax year 2026.** ITO §121's bands are the text as replaced by ITO amendment 288, and
the amending act sets its own commencement: ס״ח 3511, פרק ג׳ "ריווח מדרגות מס הכנסה", §6 —
`תחילתו של פרק זה ביום י״ב בטבת התשפ״ו (1 בינואר 2026)`. So every version of the §121
module, and of the composed pipeline that imports it, carries
`effective_from: '2026-01-01'`, and a request for an earlier period finds **no version in
force** rather than being answered with the wrong year's schedule. The 2025 amounts are a
different text that is not in this repository's corpus.

That applies to §121 and to the pipeline, not to the repository: the other modules are
dated `0001-01-01` and their fixtures run in the year each was written for, so of 68
companion cases only the pipeline's 11 and §121's 5 are evaluated in 2026, and §120ב's
run in 2025 and 2028. `docs/ENCODING-GAPS.md`, `effective-from-is-not-commencement`,
records why. `tests/test_fixture_periods_are_in_force.py` holds the line that matters:
no companion case, in any module, may be dated before a rule it **reaches** commences —
including rules reached through a declared import and never named in the case's own
`output` map.

Most other modules carry `effective_from: 0001-01-01` — the encoder's way of saying that
the captured consolidation states no commencement date for the provision it encoded.
**That is not a claim that the rule has always been in force**; the consolidations carry
amendment *lists* but no commencement clauses, and asserting a historical date would
state something the sources do not support. It is a gap, and dating each of them from its
gazette act the way §121 is now dated is the resolution. The exception is ITO §120ב, at
`2025-01-01`, because §120ב(ה)(1) names the tax years it suspends indexation for. See
`docs/ENCODING-GAPS.md`, `effective-from-is-not-commencement`.

## Amounts that are NOT in this repository

The Ordinance states the credit-point value (§33א) as a nominal 504 ILS and the §121ב
additional-tax threshold as a nominal 640,000 ILS, both subject to an indexation
mechanism this repository does not implement, and the National Insurance Law states the
child-allowance basic amounts as a nominal 150 / 188 / 140. All of those nominal figures
ARE encoded, with proofs.

What is not here is any **current-year** figure. The Israel corpus ingest is
statute-only — no `il/policy` scope exists for a Tax Authority עדכון סכומים notice or a
National Insurance Institute rate table — and this repository carries no hand-made
capture either, because every module here is encoder-generated from a corpus citation.
The composed pipeline therefore takes the current credit-point value and the current
child-allowance base amounts as **supplied inputs**, and every fixture states where its
number came from. The §121ב threshold is not supplied at all: the pipeline applies the
statute's own 640,000, which is a narrower claim than an indexed figure would be. See
`docs/ENCODING-GAPS.md`.

The employee contributions add two more supplied amounts, both from the National
Insurance Institute's published tables for 01.01.2026: the reduced collection bracket
(7,703 ILS; NII §334 prints 7,522 and an update formula, which gives 7,702.53 at the
published 2.4% index rise, and the Institute rounds) and basic amount 3 (10,382 ILS),
whose fivefold is the 51,910 ILS monthly maximum of לוח י״א. One bracket figure feeds both
contributions. See `docs/ENCODING-GAPS.md`, `contributions-bracket-and-ceiling-are-supplied`.

## Corpus anchoring

Every proof excerpt in this repository is checked against the Israel corpus: the pilot's
modules against the signed release `il-rulespec-2026-09-06`, which `.axiom/toolchain.toml`
pins, and the contribution modules against the 2026-09-29 scope (axiom-corpus#767). Each
excerpt is a verbatim NFC substring of the corpus body.

**No module pins a digest of the statutory text it encodes.** Each declares
`source_verification.corpus_citation_path` and no `source_sha256`: that is what the encoder
writes when it resolves a citation out of a corpus checkout rather than out of a signed
release, and there is no release digest to pin to yet.

`sha256` values do appear here, in two places, and neither is a digest of statutory text.
In `.axiom/encoding-manifests/` they are digests of the generated module and its companion
file — what the encoder produced. Inside five module YAMLs they are `import.hash` values
pinning the imported RULE definition (`sha256:local` where the import is same-module), so
that a change to an imported rule is detectable by its consumer. Both identify RuleSpec
artifacts. Neither would change if the corpus text did. What anchors an encoding to its text is
therefore the citation path plus the corpus release CI validates against. See
`docs/ENCODING-GAPS.md`, `no-signed-corpus-release` and `no-source-sha256-pins`.

## Toolchain binding

`.axiom/toolchain.toml` binds the repository to the signed corpus release
`il-rulespec-2026-09-06` (rulespec-il#4), and the shared validate workflow checks every
pull request against it. The generated-content guard (`run-generated-guard`) is still
off, for the reason the workflow file gives: the apply manifests were signed with a local
key by a local encoder build (`docs/ENCODING-GAPS.md`, `bootstrap-encoder-ref`).

The contribution modules cite the National Health Insurance Law, which only the
2026-09-29 corpus scope carries (axiom-corpus#767, release `il-rulespec-2026-09-29`).
The toolchain moves to that release in a pull request of its own, which changes nothing
else, before the contribution modules can pass CI. See `docs/ENCODING-GAPS.md`,
`no-signed-corpus-release`.

## Context

Chartered 2026-09-06 for a bounded Israel proof of concept. Lineage:
a PolicyEngine Israel hackathon run with the Prime Minister's Office and
digital.gov.il on 2023-07-06 encoded municipal tax reduction and
discharged-soldier credits; this repository is the Axiom-native successor.
See `docs/encoding-charter.md`.
