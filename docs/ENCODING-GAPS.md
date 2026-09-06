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

### `corpus-anchor` — citation paths are not corpus-anchored, and the re-anchor pass has been run against the ingest branch
No `il-rulespec-*` corpus release exists. Each module's
`source_verification.source_sha256` is the sha256 of the captured snapshot's
provision text, not of a corpus provision.

The Israel ingest now exists as an unmerged, unsigned branch
(`axiom-corpus` `ingest/il-taxben-pilot`, 1,414 provisions), so the re-anchor
pass this gap asks for has been RUN against it, read-only, by
`ops/il-lane/extract/reanchor_check.py`. Result:

```
atoms checked: 130   re-anchored OK: 92   path-missing: 34   text-missing: 4
```

**92 of 130 proof excerpts are already verbatim NFC substrings of the corpus
body.** The 38 that are not fall into three groups, none of which an excerpt
edit can honestly fix:

* **28 atoms — `il/policy/...` is not in the Israel corpus scope.** Both policy
  modules — `child-allowance-rates.yaml` and `contribution-rates.yaml` — cite
  `il/policy/national-insurance-institute/…`, and the Israel ingest is
  statute-only. The path SHAPE is the org-wide precedent — `policy` is
  a first-class corpus `DocumentClass` and the corpus maps the RuleSpec
  `policies/` bucket to a `policy` citation bucket, exactly as
  `ug/policy/mglsd-scg/sage-handbook` and `rw/policy/loda-vup/...` do — so
  nothing here needs renaming. The publication simply has not been ingested.
  **Resolution:** ingest the four captured National Insurance Institute snapshots
  as an `il/policy` scope.

* **6 atoms — the National Health Insurance Law is not in the corpus at all.**
  See `health-insurance-law-not-in-corpus` below.

* **4 atoms — the corpus holds one expression of ITO §121, and it is the 2026
  one.** `il/statute/income-tax-ordinance/section-121` has `expression_date`
  2026-06-08 and the amendment-288 amounts (228,000 / 301,200). This pilot's
  validation year is 2025, whose §121 states 193,800 / 269,280, and that text
  lives only in the Wikisource rev-2971879 snapshot. The four atoms are on
  `versions[0]`, the version that speaks for 2025.

  **A shorter excerpt was considered and rejected.** Three of the four could be
  trimmed until they coincidentally match the 2026 body — `rate_fourth_band`'s
  `עד 269,280 שקלים חדשים – 31%` shortens to `שקלים חדשים – 31%`, which is
  verbatim in both years. That would turn the re-anchor number green while
  making an atom that speaks for 2025 prove itself against 2026 text describing
  a different band. Making a gate pass by weakening what the proof asserts is
  the failure mode this repository exists to avoid, so the excerpts are
  unchanged and the gap is recorded instead.
  **Resolution:** the corpus ingests the 2025 expression of §121.

One atom in this class WAS repaired, because it was a genuine excerpt bug rather
than a missing expression: §121ב(א)'s excerpt straddled a space that only this
pilot's extractor writes (`640,000 שקלים חדשים , בשיעור`, where the corpus reads
`640,000 שקלים חדשים, בשיעור`). Splitting it into the charge and the rate keeps
the whole obligation proved and is verbatim in both renderings.

#### `source-sha256-pins-will-need-repinning` — 7 modules, digests known
`axiom-encode validate` and `proof-validate` never read `source_sha256`. One
command does: `axiom-encode check-source-staleness`, which compares the pin to
`sha256(corpus_row.body.encode("utf-8"))` — the raw stored body, no NFC pass, no
heading (`corpus_resolver._sha256_text`, and `source_hash.check_staleness`).

Against the ingest branch, 6 modules already match byte-for-byte and 7 do not:

| module | pinned | corpus body |
|---|---|---|
| ITO §34, §36, §36א; NII §66, §67, לוח י׳ | — | **match** |
| ITO §33א | `e72f45b6e51f…` | `c9bc12dcdd1a…` |
| ITO §66 | `7b9a686f8137…` | `53e658c5b3dd…` |
| ITO §120ב | `d77a820b8e0e…` | `879d9901d1ec…` |
| ITO §121 | `7f8d61ff2d52…` | `e4f23cdd08d5…` |
| ITO §121ב | `8a9665a0acb2…` | `116f2d6ace2f…` |
| NII §1 | `cf5a4206e0ac…` | `18f37b3824a8…` |
| NII §68 | `7e16e68531d2…` | `3bbeb6872e24…` |
| composed capstone | none declared | `590fa971feee…` |

The differences are the two rendering conventions
`ops/il-lane/RULES-LANE-HANDOFF.md` predicted — consecutive subsection markers
on one line, and a space stranded before punctuation by note removal — not
content differences. The pins are deliberately NOT being changed to the corpus
digests now: the ingest branch is unmerged, unsigned and still being edited, so
pinning to it would claim verification against something that can still change,
and the snapshot digests are the honest record of what this encoding was actually
made from.
**Resolution:** repin all seven in the same PR that adds `.axiom/toolchain.toml`,
after the release is signed and registered. The pass is mechanical from here.

### `validators-not-run-as-shipped` — `validate` and `proof-validate` are gated
`axiom-encode validate` and `axiom-encode proof-validate` both require
`.axiom/toolchain.toml` and a signed corpus release, neither of which can
honestly exist yet. What WAS run, and what it proves:
* `axiom-encode test` — all 119 companion cases pass against an engine build
  carrying the ILS currency seed.
* `axiom_encode.harness.proof_validator.validate_rulespec_proofs` with
  `require_policy_proofs=True`, invoked directly with the captured provision
  texts as `source_texts` — 130 proof atoms checked across 17 modules, all pass,
  plus 47 atoms re-checked against the specific expression their version speaks
  for (see `proof-check-concatenates-expressions-except-where-pinned`).
* `find_missing_money_proof_atoms` — 0 missing money atoms across 17 modules.
* `ops/il-lane/extract/reanchor_check.py` — the same excerpts re-checked against
  the axiom-corpus Israel ingest branch; see `corpus-anchor`.
The validator code is the same; only the source of the provision text differs.

One thing running them as shipped would NOT add: neither `validate` nor
`proof-validate` reads `source_verification.source_sha256` at all. The only
command that checks a pin is `check-source-staleness`. If pin integrity is
supposed to be gated for this pilot, that command has to be wired in explicitly —
see `source-sha256-pins-will-need-repinning`.
**Resolution:** run all three commands as shipped after the toolchain PR.

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
ANY expression of that provision. Three citation paths have two captured
expressions each — ITO §121 (2025 and current), the National Insurance Institute
child-allowance page and its contribution-rate page (2025 and 2026 for both) —
and for those, concatenation is weaker than the real gate. The script therefore runs a second, explicit pass asserting that
atoms on `versions[0]` appear in the earlier expression and atoms on
`versions[1]` in the later one (33 atoms). No other module has more than one
captured expression.

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
§67 and §68 have their own modules and their own fixtures, but "fully encoded"
would be too strong: §67(ב)'s natural/other-parent limb is folded into one
Boolean (below), §65 eligibility is not modelled at all, and §68(ד)–(יא) are
empty or repealed in the captured expression.

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
The composed capstone is bounded to: at most two children; one earner; separate
calculation assumed elected. BOTH credit-point ladders are carried — §66(ג)(4)
for the mother and §66(ג)(5) for the father — and selected on
`taxpayer_is_a_woman`; an earlier revision of this entry said the mother's
schedule only, which stopped being true when the father fixture was corrected. The per-child
age-band selection is written twice (`child_1_credit_points`,
`child_2_credit_points`) because the pilot declares no Child entity and uses no
relation aggregation; the correct shape is a Child entity with
`sum(children.credit_points)`. Annual tax is divided by twelve for presentation
and is NOT a model of the monthly ניכוי במקור deduction rules.

### `capstone-net-is-not-take-home-pay` — narrower than it was, still not take-home pay
This entry previously read "National Insurance and health contributions are not
encoded". They now are, for the employee: `monthly_net_income_ils` is net of
income tax, net of the employee's national insurance contribution (לוח י׳) and
net of the employee's health insurance contribution (§14), and inclusive of the
child allowance.

It is still **not take-home pay**. The employer's contributions are not modelled;
neither is the pension-contribution credit, nor מס הכנסה שלילי (EITC), nor any
other instrument; and the annual tax is divided by twelve for presentation rather
than computed under the monthly ניכוי במקור rules. See
`contribution-scope-is-the-employee-only`.

### `nii-section-67-insurance-gate` — a defect found by audit, fixed, and regression-tested
§67's `child_counts_with_this_parent` tested `this_parent_is_insured` only in its
one-parent branch. A consistent input set — two parents, not with the mother
only, this parent is the father, this parent is NOT insured — returned TRUE,
counting a child with an uninsured father. §67(א) ("לא יבוא ילד ... במנין ילדים
של יותר מהורה מבוטח אחד") and §67(ב) ("האב המבוטח") both turn on insurance.

Insurance now gates every branch, and the companion fixtures run all sixteen
combinations of the four Booleans instead of six. The fixture header previously
claimed all combinations were exercised; the gap between that claim and the six
cases is what hid the defect.

### `capstone-derives-the-surtax-exclusion-once`
The capstone gated the allowance on the imported §121ב judgment AND on §66's
`entitled_to_child_allowance`, which reads its own
`parent_has_income_liable_to_additional_tax` input. Two independent sources for
one legal fact, and they could disagree: setting the §66 input TRUE while income
was below the threshold drove the allowance to zero.

§66 now also exposes its opening limb alone,
`parent_is_insured_for_child_allowance`, and the capstone takes the exclusion from
the imported §121ב judgment and the insurance condition from that rule. The stale
input is still ASSIGNED in every capstone fixture, because the harness requires
every input of every module in the graph, but nothing reads it.
`stale_nii_surtax_flag_no_longer_changes_the_allowance_2025` is the regression
test: it is the ordinary two-child fixture with that flag flipped to TRUE, and it
produces the same 383 ILS allowance and the same 14,151.738 net. §66 standalone
still excludes — the fixture asserts `entitled_to_child_allowance: not_holds` —
which is the section doing its job; the composition simply no longer asks it that
question twice.

## Contributions

### `nii-schedule-10-branch-rows-do-not-sum` — the schedule contradicts itself
לוח י׳ states the employee's deduction per insurance branch and then states a
total. In the captured rendering the ten branch figures in the employee's
full-rate column are

> 0.87, –, –, –, 0.07, 0.21, –, 1.86, 0.14, 1.52

which sum to **4.67**, while the schedule's own `סך הכל` row for that column
reads **7.00**. The reduced column does sum correctly (1.04). This repository
encodes the figure the schedule states as the total, which is also the figure the
National Insurance Institute publishes; it does not encode the branch rows.

An earlier draft of this module summed the branch column and would have shipped
4.67% as the employee's national insurance rate. That is recorded here because
the mistake is instructive: the branch breakdown looks like the authoritative
detail and is not.
**Resolution:** determine from the amending acts whether the branch figures or
the total were amended, and by which act. `unexplained` until then.

### `nii-schedule-10-was-dropped-by-the-corpus-adapter` — found here, fixed upstream
When this leg started, `il/statute/national-insurance-law-1995/schedule-j/sign-1`
had a body of 40 characters equal to its own heading, and none of the ten rate
rows was citable: an adapter heuristic treated a block whose only non-note
content is a table as editorial in full — a rule written to suppress ITO §121's
editorial comparison tables, with לוח י׳ as collateral damage. The employee
contribution rates were therefore not provable from the corpus at all.

Reported to the corpus lane in `ops/il-lane/RULES-LANE-TO-CORPUS.md`. It has
since been fixed on the ingest branch, and this module's independently rendered
provision text and the corpus body now agree **byte for byte** — the module's
`source_sha256` is also the sha256 of the corpus body. No action outstanding.

### `health-insurance-law-not-in-corpus`
`il/statutes/national-health-insurance-law-1994/section-14.yaml` encodes an act
the Israel corpus scope does not contain. The ingest has two documents; the
National Health Insurance Law appears in them only as a cross-referenced defined
term. Its 6 proof atoms (5 on §14, 1 on §15) cannot resolve, and the module
carries no corpus-matched `source_sha256`.

The instrument slug `national-health-insurance-law-1994` also extends the fixed
slug list in `ops/il-lane/CITATION-SCHEME.md`. That extension is flagged to the
corpus lane, not assumed.
**Resolution:** ingest חוק ביטוח בריאות ממלכתי, התשנ״ד-1994 (Knesset
IsraelLawID 2000111) as a third document of the Israel scope.

### `published-contribution-grid-starts-in-february-2025`
The Institute's 2025 page dates the whole grid "החל ב- 01.02.2025", and dates the
full national-insurance rate from that day too, so the published grid does not
speak for January 2025. The versions in
`il/policies/national-insurance-institute/contribution-rates.yaml` start
2025-01-01 because that is the earliest date this pilot speaks for — the general
`effective-from-dates-are-pilot-scope-not-commencement` rule — not because the
publication says so. No fixture is in January 2025.
**Resolution:** capture the grid that was in force in January 2025.

### `contribution-thresholds-are-supplied`
Neither threshold is stated as an amount in either Law. לוח י׳ splits the wage at
"מדרגת הגבייה המופחתת כהגדרתה בסעיף 334(א)" and §348(א) caps it at "הסכום המרבי
המתקבל לפי האמור בלוח י״א"; the health side reaches the same two boundaries
through §14(ו1)'s reference to NII §341 and §15(א)'s "כאילו היו דמי ביטוח לאומי".
`reduced_collection_step_ils` and `maximum_monthly_income_for_contributions_ils`
are therefore inputs, supplied from the Institute's published table — 7,522 and
50,695 for 2025, 7,703 and 51,910 for 2026. Those are **official** captures.
§334, §337, §341 and §342 themselves are not encoded.

### `contribution-scope-is-the-employee-only`
Only the employee's own deduction is encoded, for an employed resident between
18 and retirement age. Not encoded: the employer's contribution (7.6% full /
4.51% reduced, published and captured but not modelled, because it is not the
employee's money); the self-employed and not-working columns of לוח י׳;
§14(ג)-(ה1) of the Health Insurance Law; the סכום המינימום floor; the §14(ז)
exemptions; §348(ב)'s minimum-income rule; and §350's exempt income.

### `contribution-rates-agree-with-the-publication` — recorded because agreement is also a result
Unusually for this pilot, the statute and the publication match. The Institute
publishes the employee's national insurance rate as 1.04% reduced and 7% full,
which is exactly the `סך הכל` row of לוח י׳, and the health rate as 3.23% and
5.17%, which is exactly §14(ו1) and §14(ב)(1). Both were encoded from the
statutes and the publication was encoded separately; nothing was reconciled by
hand. The OECD TaxBEN Israel description's employee total of 12.17% is the sum of
the two full rates.

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
