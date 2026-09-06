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
  texts as `source_texts` — 88 proof atoms checked across 14 modules, all pass.
* `find_missing_money_proof_atoms` — 0 missing money atoms across 14 modules.
The validator code is the same; only the source of the provision text differs.
**Resolution:** run both commands as shipped after the toolchain PR.

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

### `child-allowance-special-basic-amount-2025` — `unexplained`
Two figures for the §1(2)(ג) special basic amount in 2025:
* **153** — OECD TaxBEN Israel description ("0.7*153 or ILS 107").
* **158** — the Wikisource editorial annotation on the same definition.
The pilot's 2025 §68(ג) fixture supplies **153** and labels it as the TaxBEN
reference. Neither figure comes from an official publication. `unexplained`.
**Resolution:** capture the National Insurance Institute's published special
basic amount for 2025.

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
| `current_basic_amount_*` (2026) | §1(2): 150 / 188 / 140 ILS | 173 / 219 | **official** — the captured ביטוח לאומי publication, effective 01.01.2026 |
| `current_basic_amount_*` (2025) | §1(2): 150 / 188 / 140 ILS | 169 / 214 / 153 | OECD TaxBEN Israel 2025 — a reference |

### `credit-point-current-value-not-captured`
§33א states the credit point as 504 ILS a year, index-linked under §120א. The
current value is not in the statute and no Tax Authority עדכון סכומים notice was
captured (gov.il refuses a plain HTTP client). `il/policies/` therefore holds a
National Insurance Institute capture but no Tax Authority capture.
**Resolution:** fetch the Tax Authority notice through a real browser and add an
`il/policies/tax-authority/` module.

### `child-allowance-2025-amounts-not-officially-captured`
The captured National Insurance Institute page states amounts "(החל מ- 01.01.2026)"
only. The 2025 amounts used in fixtures are the OECD TaxBEN figures.
**Resolution:** capture the Institute's 2025 table.

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

### `child-allowance-2026-special-basic-amount-not-captured`
The captured Institute publication gives the per-child amounts but no special
basic amount for §1(2)(ג)/§68(ג). The 2026 fixtures therefore supply the NOMINAL
statutory 140 — a figure this repository encodes as a parameter — and none of
them exercises §68(ג), so it is inert there. It is **not** an amount payable, and
it is deliberately not the Wikisource editorial annotation (162), because taking a
current-year amount from editorial apparatus is forbidden by `AGENTS.md`.

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
