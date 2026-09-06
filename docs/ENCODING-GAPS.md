# Encoding gaps

Everything this pilot does not do, could not verify from primary law, or verified
against something weaker. Divergences from a reference are recorded here as
`unexplained` with both numbers; no issue is ever filed against an external
reference.

## Source and provenance

### `source-tier` — the provision source of record is a secondary consolidation
The Knesset national legislation database serves consolidated text through a
client-rendered application, and `KNS_DocumentIsraelLaw` returns empty over
OData for both pilot instruments. The pilot therefore encodes from ספר החוקים
הפתוח (he.wikisource) — the consolidation the Knesset database itself links to as
"לחוק המלא". Tier `consolidation-knesset-linked`, which is **secondary**.
**Resolution:** capture the Knesset "נוסח מלא" PDFs through a real browser and
re-anchor every module.

### `corpus-anchor` — citation paths are not corpus-anchored
No `il-rulespec-*` corpus release exists. Each module's
`source_verification.source_sha256` is the sha256 of the captured snapshot's
provision text, not of a corpus provision, and the `corpus_citation_path` values
name paths the corpus does not yet contain.
**Resolution:** re-anchor pass after the Israel ingest lands and the release is
signed and registered.

### `validators-not-run-as-shipped` — `validate` and `proof-validate` are gated
`axiom-encode validate` and `axiom-encode proof-validate` both require
`.axiom/toolchain.toml` and a signed corpus release, neither of which can
honestly exist yet. What WAS run, and what it proves:
* `axiom-encode test` — all 73 companion cases pass against an engine build
  carrying the ILS currency seed.
* `axiom_encode.harness.proof_validator.validate_rulespec_proofs` with
  `require_policy_proofs=True`, invoked directly with the captured provision
  texts as `source_texts` — 91 proof atoms checked across 14 modules, all pass,
  plus 19 atoms re-checked against the specific expression their version speaks
  for (see `proof-check-concatenates-expressions-except-where-pinned`).
* `find_missing_money_proof_atoms` — 0 missing money atoms across 14 modules.
The validator code is the same; only the source of the provision text differs.
**Resolution:** run both commands as shipped after the toolchain PR.

### `effective-from-dates-are-pilot-scope-not-commencement`
Every module version carries `effective_from: 2025-01-01` unless a captured
gazette act establishes a later date. **That is the earliest date this pilot
speaks for, not a commencement date.** §34, §36 and §36א have been in the
Ordinance for decades; §68's multipliers date from 2003 and §1(2)'s figures are
nominal to 2015. None of that is encoded, because the captured consolidations
carry amendment LISTS but no commencement clauses, and asserting a historical
`effective_from` would state something the sources do not support. An earlier
draft of this pilot did assert such dates; they were removed.
**Resolution:** take commencement from the gazette act for each amendment and
version the modules properly.

### `proof-check-concatenates-expressions-except-where-pinned`
`ops/il-lane/extract/proofcheck.py` builds `source_texts` by concatenating every
captured expression of a citation path, so an excerpt validates if it appears in
ANY expression of that provision. For ITO §121, which has two captured
expressions, that is weaker than the real gate. The script therefore runs a
second, explicit pass asserting that atoms on `versions[0]` appear in the 2025
expression and atoms on `versions[1]` in the current one (19 atoms). No other
module has more than one captured expression.

### `gazette-effective-date-not-a-proof-atom`
The 2026 `effective_from` dates rest on ס״ח 3511 פרק ג׳ §6
("תחילתו של פרק זה ביום י״ב בטבת התשפ״ו (1 בינואר 2026)"), which is captured as a
PDF. Extracting its text yields bidi-interleaved output in which digits are
displaced, so no excerpt from it can meet the verbatim standard. No
`effective_period` proof atom cites it; the justification lives in the module
summaries and in `docs/sources-and-provenance.md`.
**Resolution:** OCR the gazette PDF single-block RTL-aware, as the Ethiopia lane
did, and add the atom.

## Source defects and divergences

### `section-121-a-2-defective-2025-expression` — a real transcription error
The captured Wikisource expressions of §121(א)(2) for tax year 2025 read:

> על כל שקל חדש מ־560,280 שקלים חדשים עד 542,160 שקלים חדשים – 35%

The lower bound exceeds the upper bound, and 560,280 is elsewhere the point at
which the 47% rate begins. The defect is present in both the 2025-12-31 revision
(oldid=2971879) and the 2024-12-31 revision (oldid=2897076), so it is longstanding
rather than a one-off edit. The current text, as replaced wholesale by ITO
amendment 288, is internally consistent
("מ־301,201 שקלים חדשים עד 560,280 שקלים חדשים – 35%").

Consequence: the 35%/47% boundary is NOT a parameter. It enters
`il/statutes/income-tax-ordinance/section-121.yaml` as the supplied input
`thirty_five_percent_band_upper_ils` (560,280 in every fixture), so that no proof
atom is attached to text that does not support the value.
Two independent things corroborate 560,280 as the 2025 boundary without being
usable as proof: the OECD TaxBEN Israel 2025 table (47% from 560,280), and a
comparison table in the Wikisource page itself giving 2024–2025 as
"269,281 עד 560,280 | 35%" and "מעל 721,560 | 3% מס נוסף". The latter is the
publisher's **editorial apparatus**, not provision text, and this repository
strips editorial apparatus from proof bodies — so it corroborates the reading
and the supplied 721,560 surtax threshold, but neither may ground a proof atom.
**Resolution:** confirm the 2025 boundary from the Knesset consolidated text or a
Tax Authority עדכון סכומים notice, then encode it as a parameter.

### `child-allowance-surtax-exclusion-vs-oecd` — `unexplained`, and it matters
The captured consolidated text of NII §66 (amendment תשע״ג־3) reads:

> הורה מבוטח זכאי לקצבת ילדים חודשית לפי פרק זה בעד כל ילד, למעט הורה מבוטח שיש לו הכנסה החייבת במס נוסף כמשמעותה בסעיף 121ב לפקודת מס הכנסה.

— an insured parent is entitled for each child, **except** an insured parent with
income liable to the ITO §121ב additional tax.

The OECD TaxBEN Israel description says of the same benefit: "It is not
means-tested and not taxable" (§4.1.4: "The benefit is not means-tested").

These cannot both describe the same operative rule. Nothing in the captured
material resolves it: whether the exclusion was ever brought into force,
suspended, or is administered differently cannot be determined from the
snapshots, and the pilot does not have the amending act's commencement clause.
`unexplained`.

The pilot **encodes what the captured statutory text says**, and the composed
capstone's high-earner fixture turns on it. That fixture demonstrates the
encoded provision, not a verified description of what the National Insurance
Institute pays. Do not present it as the latter.
**Resolution:** obtain the commencement and implementation history of תשע״ג־3
from the gazette and from an Institute publication.

### `nii-68c-published-increment-vs-encoded-formula` — `unexplained`
NII §68(ג) states the income-support addition as a formula:

> תיווסף לקצבת הילדים המשתלמת לו בעד הילד השלישי ובעד הילד הרביעי שבמנין ילדיו תוספת בסכום השווה ל־70% מן הסכום הבסיסי הקבוע בפסקה (2)(ג) שבהגדרה ”הסכום הבסיסי“

— 70% of the §1(2)(ג) basic amount, which §1(2)(ג) states nominally as 140.

The National Insurance Institute publishes the *result* directly, in both
captured snapshots of its own rate page:

> התוספת משולמת עבור הילד השלישי והרביעי במשפחה בסך 111 ש"ח לכל ילד.  (2025)
> התוספת משולמת עבור הילד השלישי והרביעי במשפחה בסך 113 ש"ח לכל ילד.  (2026)

This repository encodes BOTH: the statutory formula in
`il/statutes/national-insurance-law-1995/section-68.yaml`, and the published
amounts in `il/policies/national-insurance-institute/child-allowance-rates.yaml`.
It cannot reconcile them, because no official §1(2)(ג) basic amount has been
captured for either year. Supplying the nominal 140 gives 0.7 × 140 = 98 against
a published 111 (2025) and 113 (2026). `unexplained`.

What the published figures DO settle: the OECD TaxBEN Israel description gives
the special basic amount as 153 ("0.7*153 or ILS 107"), and 0.7 × 153 = 107.1,
which cannot reach the Institute's published 111 under any rounding convention.
**The reference figure is inconsistent with the publisher's own number**, and is
no longer supplied anywhere in this repository. That conclusion does not depend
on knowing the Institute's rounding rule.

What they do NOT settle: a Wikisource editorial annotation gives 158 for 2025,
and 0.7 × 158 = 110.6, which rounds to 111. That is *consistent with* the
published increment under ordinary rounding — it is not proof, the annotation is
editorial apparatus this repository may not treat as a source for a current
amount, and no fixture uses it. For 2026 the published 113 does not discriminate:
0.7 × 161 = 112.7 and 0.7 × 162 = 113.4 both round to 113.
**Resolution:** capture the Institute's published §1(2)(ג) basic amount, or its
rounding rule, for each year.

## Amounts supplied rather than encoded

The Ordinance and the National Insurance Law state several amounts as NOMINAL
figures under an indexation mechanism this repository does not implement. Where
no official current-year capture exists, the amount is a module input and every
fixture states its provenance. None of these is law as stated here.

| Input | Statute's nominal figure | Supplied value | Where it came from |
|---|---|---|---|
| `credit_point_value_for_tax_year_ils` | §33א: 504 ILS | 2,904 (2025 and 2026) | OECD TaxBEN Israel 2025 — a reference |
| `additional_tax_threshold_for_tax_year_ils` | §121ב: 640,000 ILS | 721,560 (2025) | OECD TaxBEN Israel 2025 — a reference |
| `thirty_five_percent_band_upper_ils` | §121(א)(2), stated as current | 560,280 | current consolidation; supplied because the 2025 expression is defective (above) |
| `current_basic_amount_*` (2026) | §1(2): 150 / 188 ILS | 173 / 219 | **official** — the captured ביטוח לאומי publication, effective 01.01.2026 |
| `current_basic_amount_*` (2025) | §1(2): 150 / 188 ILS | 169 / 214 | **official** — the same publication as it stood 2025-04-20, via the Internet Archive |
| `current_basic_amount_income_support_base_ils` (both years) | §1(2)(ג): 140 ILS | 140 | the statute's own nominal figure. NOT an amount payable; the Institute publishes the resulting increment as 111 (2025) / 113 (2026) |

### `credit-point-current-value-not-captured`
§33א states the credit point as 504 ILS a year, index-linked under §120א. The
current value is not in the statute and no Tax Authority עדכון סכומים notice was
captured (gov.il refuses a plain HTTP client). `il/policies/` therefore holds a
National Insurance Institute capture but no Tax Authority capture.
**Resolution:** fetch the Tax Authority notice through a real browser and add an
`il/policies/tax-authority/` module.

### `child-allowance-2025-amounts-not-officially-captured` — CLOSED
Was: the captured Institute page states amounts "(החל מ- 01.01.2026)" only, so
the 2025 fixtures took 169 / 214 from the OECD TaxBEN description.

Closed by capturing the same official page as it stood on 2025-04-20 from the
Internet Archive, where it states "(החל ב- 01.01.2025)" and the same 169 / 214 /
169 ladder. The publisher is the National Insurance Institute; the archive is the
delivery channel, not the publisher, and the retrieved bytes carry their own
provenance record (sha256
a150c2e4b3237be0b83868fd798e8b00404a41550187645fe95146a5bfaf1287). The 2025
per-child amounts are now official, and the OECD figures for them are unused.

### `child-allowance-2026-special-basic-amount-not-captured` — WITHDRAWN, IT WAS WRONG
This repository previously recorded that "the Institute's published table gives
the per-child amounts but no special basic amount". The captured 2026 page does
carry the §68(ג) increment — "התוספת משולמת עבור הילד השלישי והרביעי במשפחה בסך
113 ש\"ח לכל ילד" — in a sentence the first extraction pass dropped before the
provision text was written. The figure was inside the byte-pinned capture the
whole time the repository said it was not captured.

Both years' increments are now extracted by `ops/il-lane/extract/btl_rates.py`
and encoded with verbatim proofs. What remains genuinely uncaptured is the
*basic amount* those increments are 70% of — see
`nii-68c-published-increment-vs-encoded-formula`.

## Narrowings inside the encoded sections

### `ito-section-66-maturity-year-cross-reference`
§66(ג)(4)(א) defines ”שנת לידה“ and ”שנת בגרות“ by reference to §40(ב)(3), which
this pilot does not encode. Birth year and maturity year are therefore Boolean
inputs (`child_is_in_birth_year`, `child_is_in_maturity_year`) rather than being
derived from an age and a date of birth.

### `ito-section-66-scope`
Only §66(ג)(4)(א) and §66(ג)(5) are encoded. §66(א), §66(ב), §66(ג)(1)–(3),
(4א), (5א), (6), and §66(ד)–(ה) are not. §66 applies only where separate
calculation (חישוב נפרד) is elected; the composed fixtures take that election as
given and do not test the election conditions in §66(ד).

### `ito-section-40-not-encoded`
§40(א) (נקודות קיצבה for children, paid by the National Insurance Institute under
§109 of the 1968 Law) and §40(ב) (the single-parent credit-point schedule) are
not encoded. A single-parent household therefore cannot be computed by this
pilot, and the OECD TaxBEN "single parent tax credit" of one additional point is
outside its scope.

### `nii-section-67-second-limb`
§67(ב)'s second limb — a child with one natural parent and one other parent, both
insured, counted with the parent the child is with — is folded into the same
`child_is_with_the_mother_only` input rather than encoded as its own branch,
because the pilot's household shapes do not distinguish it.

### `nii-section-68-repealed-subsections`
§68(ב)(1) and §68(ד)–(יא) are empty or repealed in the captured expression and
are not encoded.

### `nii-section-1-paragraphs-1-and-3`
Only paragraph (2) of the הסכום הבסיסי definition is encoded — the one that
governs the child allowance. Paragraphs (1) and (3), covering maternity,
work-injury, disability and residual benefits, are not.

### `ito-section-121-reduced-rates-are-a-person-level-switch`
§121(ב)(1) applies the reduced rates to "הכנסה חייבת בשנת המס מיגיעה אישית" — to
income of that character — and §121(ב)(2) withdraws them from income for which
acceptable books were not kept. Both are properties of INCOME. The encoding
collapses them into a single person-level switch, `reduced_rates_apply`, so a
taxpayer with both personal-exertion and other income is taxed wholly on one
schedule rather than having the schedules applied to the respective parts.
Every pilot fixture has income of a single character, so none exercises the
difference.
**Resolution:** split the taxable-income input by character and apply each
schedule to its own part.

### `ito-section-121b-subsections-b-to-e-not-encoded`
Only §121ב(א) and §121ב(א1) are encoded. §121ב(ב) (no §91(ד) advances on income
bearing the additional tax), §121ב(ג) (notwithstanding any enactment), §121ב(ד)
(the §8(ג) spreading rule) and §121ב(ה) are not.

§121ב(ה) is the consequential one. It defines ”הכנסה חייבת ממקור הוני“ by
excluding §2(1)/(2) income and personal-exertion income, and defines ”הכנסה
חייבת“ by reference to §1, §89, §88 and the Land Taxation Law. The module takes
`annual_taxable_income_from_capital_sources_ils` as a **supplied input** instead
of deriving it from that definition, so no fixture can prove the boundary of the
capital-source base. §121ב(ה) also carries a 5,385,285 ILS residential-dwelling
threshold that is not encoded.

### `composed-capstone-does-not-apply-nii-67-or-68b-c`
The capstone wires NII §66 (entitlement) and the §68(א)/§1(2) birth-order
structure. It does NOT apply §67 (whose count a child falls into) — it assumes
both children fall in the modelled parent's count — and it does not apply
§68(ב) (pre-June-2003 multipliers) or §68(ג) (the income-support increment); no
capstone fixture is on income support or has a child born before June 2003.
§67 and §68 are fully encoded and tested in their own modules.

### `ito-section-66-c-4-a1-not-encoded`
§66(ג)(4)(א1) lets the mother elect to have one of her birth-year credit points
counted in the following tax year instead. Not encoded; `child_1_credit_points`
and `child_2_credit_points` always allot the birth-year points in the birth year.

### `additional-tax-threshold-attribution-is-an-inference`
The OECD TaxBEN Israel description never names the §121ב additional tax. Its 2025
schedule ends "560 280 – 721 560 | 47" and "Above 721 560 | 50". Reading that 50%
band as the 47% rate plus this section's 3% — and therefore reading 721,560 as
the 2025 additional-tax threshold — is an **inference made in this repository**,
not something TaxBEN states. The Wikisource page's own editorial comparison table
("מעל 721,560 | 3% מס נוסף") corroborates it and, being editorial apparatus,
cannot ground a proof atom.

### `credit-conditions-are-inputs-not-derived`
§34 ("יחיד שהיה תושב ישראל בשנת המס"), §36 ("יחיד תושב ישראל") and §36א ("אשה")
each state a condition that enters as a Boolean input rather than being derived.
Residence in particular is not modelled: the Ordinance's §1 residence definition
is not encoded. Note that §36א states no residence requirement and the encoding
does not add one.

### `composed-capstone-bounds`
The composed capstone is bounded to: at most two children; one earner; the
mother's §66(ג)(4) schedule; separate calculation assumed elected. The per-child
age-band selection is written twice (`child_1_credit_points`,
`child_2_credit_points`) because the pilot declares no Child entity and uses no
relation aggregation; the correct shape is a Child entity with
`sum(children.credit_points)`. Annual tax is divided by twelve for presentation
and is NOT a model of the monthly ניכוי במקור deduction rules.

### `no-contributions-so-net-is-not-take-home-pay`
National Insurance and health contributions (NII Law §335, Health Insurance Law
§14) are not encoded. `monthly_net_income_ils` is net of income tax and inclusive
of child allowance ONLY. It is not take-home pay and must not be presented as
such. Neither are the pension-contribution credit, מס הכנסה שלילי (EITC), or any
other instrument.

## Oracles

### `no-executable-oracle`
Nothing in this repository is machine-compared against an external model. The
OECD TaxBEN Israel description is a narrative policy description read by a human;
the TaxBEN web calculator and the Tax Authority simulator
(`secapp.taxes.gov.il/srsimulatorNZ`, linked from the consolidated text of §121)
are candidate oracles and are NOT wired. No fixture here was produced by any of
them. `oracle-coverage-pending.yaml` declares a ceiling of 0 rather than
overstating coverage.

Where the 2025 encoding was compared to the TaxBEN description by hand, it
agrees: bracket edges 84,120 / 120,720 / 193,800 / 269,280 / 560,280; rates
10/14/20/31/35/47; the child credit point ladder 2.5 / 4.5 / 3.5 / 2.5 / 2 (mother)
against 1 (father) and 0.5 against 0 in the maturity year; and 2.25 basic points,
which the statute reaches as §34's two points plus §36's quarter point.
