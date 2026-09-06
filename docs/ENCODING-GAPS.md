# Encoding gaps

Everything this pilot does not do, could not verify from primary law, or verified
against something weaker. Divergences from a reference are recorded here as
`unexplained` with both numbers; no issue is ever filed against an external
reference.

## How the content was produced, and what is provisional about that

### `bootstrap-encoder-ref` — the encoder is a local build, not a released one
Every atomic module here was produced by `axiom-encode encode <citation> --backend codex
--apply`, but not by a released axiom-encode. The pinned ref hard-requires a **signed corpus
release** for the jurisdiction it is encoding, and no `il-rulespec-*` release exists. The only
refs that can encode without one predate the current engine CLI. The encoder used is therefore
**0.2.1197.4**: ref `55beb160` (the last ref that reads roots from
`AXIOM_RULESPEC_REPO_ROOTS`) plus four fixes made in this pilot, with a deliberately four-part
version so it can never be read as an upstream three-part release. Every apply manifest
records the exact commit sha as well as the version.

Two consequences, both harness-only and both disclosed:
* A shim translates `AXIOM_RULESPEC_REPO_ROOTS` into the engine's `--rulespec-root` flags and
  stages the generated artifact at its canonical path before compiling — which is what
  axiom-encode 0.2.1695 does in-process.
* `axiom-encode validate` and `proof-validate` cannot run as shipped; see
  `validators-not-run-as-shipped`.
**Resolution:** re-encode every citation at the pinned ref after the release
`il-rulespec-2026-09-06` is cut, signed and registered, and diff the output against what is
here.

### `manifests-locally-signed` — the apply manifests carry a throwaway signature
Apply manifests are HMAC-SHA256 signed under key id `axiom-encode-apply-v1`. The key used here
was generated locally for this pilot, is not committed, and is known to no shared keyring. The
manifests are therefore honest records of what ran — run id, model, encoder commit, prompt
digest, applied-file digests, and the chain of superseded runs — but their signatures verify
against nothing anyone else holds. This is exactly why
`.github/workflows/repository-checks.yml` keeps `run-generated-guard: false`, and why the
workflow says so in a comment rather than leaving it unexplained.
**Resolution:** the Path R re-encode at the pinned ref produces manifests signed with the real
key, and turns the guard on in that same PR.

### `encoder-hebrew-fixes-pending-upstream` — five encoder fixes live only in this bootstrap
Each was found by a module that came out wrong, and each is a defect in code that had only
ever seen Latin-script statutes. They must be ported to axiom-encode main:

| commit | subject |
|---|---|
| `195b0f9d` | Ground the numerals Hebrew statutes print with a maqaf or a fraction slash |
| `b7500e26` | Read Hebrew numerals, and stop escaping the alphabet a statute is written in |
| `6e8cfabb` | Read a fraction slash the way the page it came from set it |
| `dc7baa16` | Count a Hebrew teen as one number, not as the ten inside it |
| `c08cb0c0` | Stop an encoding from landing in escapes the model chose to write |

What they do, concretely: detach the maqaf (U+05BE) so `מ־84,120` parses as 84120 rather than
120; read the Hebrew ordinals and cardinals a statute spells as words (`שתי`, `שלושה`,
`הילד הרביעי`) so the grounding gate can find a number the provision never prints as a digit;
read `21⁄2` — the flattening of a printed 2½, integer part glued to the numerator across the
Unicode fraction slash — as 2.5 rather than as 10.5; stop `yaml.safe_dump(...,
allow_unicode=False)` from turning every summary and proof excerpt into `\uXXXX`; and undo the
same escaping where the MODEL chose it, which the fourth fix did not reach because `--apply`
copies the model's bytes verbatim.

The fifth is the one worth reading before the next non-Latin jurisdiction. Three rounds on NII
§68 established that the escaping is not a property of one model — gpt-5.6-terra copied an
escaped target on ITO §121, and gpt-6-astra escaped §68 from scratch with no escaped target to
copy — so no findings file fixes it and the fix has to be in the apply path. It rewrites
`\uXXXX` escapes of non-ASCII characters back to the characters, before the copy, so the
generated file, the manifest's `generated_output_sha256` and the installed file all carry the
same bytes; it refuses to rewrite unless both forms parse and parse to the same value; and it
leaves escapes of ASCII characters alone.

All five are no-ops for a Latin-script module, so nothing already upstream changes.
`eeef33be` is the version bump that unblocks `--apply` after the first of them.
**Resolution:** open the five as PRs against axiom-encode main with their unit tests.

### `encoder-model-mix` — two models, recorded per citation
Most citations were encoded by `gpt-5.6-terra`; the harder ones needed `gpt-6-astra`, and the
apply manifest for each says which. The model is part of the provenance, not an implementation
detail, which is why the manifest carries it. Three places where the difference was decisive:

* **ITO §66.** terra returned `module.status: entity_not_supported` with `rules: []` — the
  claim that the section needs marriage and child-parent relations the entity surface does not
  have. astra encoded the same provision as thirty-six rules that compile and pass CI.
* **ITO §121ב.** Two terra rounds against the same findings file reproduced the same defect:
  proof excerpts containing `...`, which is a substring of nothing. astra fixed both on the
  first round.
* **NII §66.** Two terra rounds produced the right atom shape with no `excerpt` key at all.
  astra quoted both limbs.

The reverse also happened, which is why the split is not "astra for everything": on NII §68
astra restructured the module well and escaped seventy-seven lines of Hebrew, and terra wrote
it readably. Neither model is reliably better at serialising a non-Latin script; both had to be
told, in a findings file, what was wrong.

### `repair-rounds-are-findings-files-not-edits`
No YAML in `il/statutes/` was edited by hand. Where a generated module was wrong, the defect
was written up as a findings file under `ops/il-lane/encoder-regen-v2/review/` in the lane
repository and handed back to the encoder with `--allow-context`, which places it in the
workspace as `context/external/<name>`. Two things learned doing that, recorded because they
will recur:
* When the existing target in the workspace is itself a thin encoding, the model anchors on it
  and reproduces it. Deleting the target before a re-encode is what makes a genuine re-encode
  happen.
* A findings file has to be in place BEFORE the round starts; appending to it while a round is
  running changes nothing for that round.

### `parameter-only-modules-carry-no-companion-cases`
ITO §33א and NII §1 have empty companion files. That is not an omission: the encoder empties
them. `_try_repair_generated_parameter_only_companion_tests_for_apply` in `axiom_encode.cli`
deletes the cases of any module whose rules are ALL `kind: parameter` and whose cases assert
only those parameters, on the view that a case restating a constant proves nothing the module
does not already say. Findings files cannot change it — the repair is deterministic and runs on
every apply.

The consequence, stated plainly: **the 504 ILS credit point and the 150 / 188 / 140 child-
allowance base amounts are not exercised by a companion case in their own modules.** They are
exercised where they are consumed: the composed pipeline's fixtures assert the §1 base amounts
through `statutory_nominal_monthly_child_allowance_ils`, and every proof atom on those
parameters is checked verbatim against the corpus body.
**Resolution:** upstream, decide whether a parameter module should keep a value case; this
pilot does not work around the repair.

## Source and provenance

### `source-tier` — the provision source of record is a secondary consolidation
The Knesset national legislation database serves consolidated text through a
client-rendered application, and `KNS_DocumentIsraelLaw` returns empty over
OData for both pilot instruments. The corpus ingest therefore captured ספר החוקים
הפתוח (he.wikisource) — the consolidation the Knesset database itself links to as
"לחוק המלא". Tier `consolidation-knesset-linked`, which is **secondary**.
**Resolution:** capture the Knesset "נוסח מלא" PDFs through a real browser, re-ingest, and
re-encode.

### `no-signed-corpus-release` — the pilot is anchored to an ingest branch
Every proof excerpt here resolves against the Israel corpus ingest
(`axiom-corpus`, branch `ingest/il-taxben-pilot`), which is the source of record for provision
text: the encoder read the provisions from it, and the excerpts are verbatim NFC substrings of
its bodies. What does not exist is a **signed, immutable release**. Until
`il-rulespec-2026-09-06` is cut, signed and registered, an excerpt is checked against a branch
that can still be edited.
**Resolution:** cut and sign the release, bind `.axiom/toolchain.toml` to it in a dedicated
PR, and re-run the shipped validators.

### `no-source-sha256-pins` — the modules pin a citation path, not a digest
Each module declares `source_verification.corpus_citation_path` and no `source_sha256`. That
is what the encoder writes when it resolves a citation out of a corpus checkout rather than
out of a signed release: there is no release digest to pin to. `axiom-encode
check-source-staleness`, the only command that reads a pin, therefore has nothing to check
here.
**Resolution:** the pins arrive with the release, in the toolchain PR.

### `validators-not-run-as-shipped` — `validate` and `proof-validate` are gated
Both require `.axiom/toolchain.toml` and a signed corpus release, neither of which can
honestly exist yet. What WAS run, with the commands, is in the pull request body and
reproduced by `ops/il-lane/encoder-regen-v2/checks/`:
* the encoder's own `axiom-encode test` over every companion file, against an engine build
  carrying the ILS currency seed;
* `axiom_encode.harness.proof_validator.validate_rulespec_proofs` with
  `require_policy_proofs=True`, from the PINNED validator ref, invoked directly with the
  corpus ingest bodies as `source_texts` — the same validator CI will run, differing only in
  where the provision text comes from;
* `find_missing_money_proof_atoms` from the same ref.
Every module was additionally gated by the encoder before it was written: `--apply` installs a
file only after the full ValidatorPipeline — compile plus CI plus proof validation — passes on
it inside a policy overlay, and a module that fails is refused with
`apply=blocked_validation:<the failing check>`. Several run logs show `ci=no` on the raw
generation followed by `outcome=apply_applied`: that is the encoder's own deterministic repair
pass fixing the generation and the repaired file then passing the overlay gate. Each repair is
named in the run log (`apply=auto_repaired_<name>:<rules>`).
**Resolution:** run all three as shipped after the toolchain PR.

### `effective-from-is-not-commencement`
Most module versions carry `effective_from: 0001-01-01`. That is the encoder saying the
captured consolidation states no commencement date for the provision — the consolidations
carry amendment *lists* but no commencement clauses. It is **not** a claim that the rule has
been in force since the year 1. It IS, however, a rule that will answer a request for any
earlier year with the current text, which is why review round 1 rejected it for ITO §121.

Three modules are dated properly, from the gazette rather than from the consolidation:
* **ITO §121** — every version `2026-01-01`. The bands are the text as replaced by ITO
  amendment 288: ס״ח 3511 of י״ג בניסן התשפ״ו, פרק ג׳ "ריווח מדרגות מס הכנסה", §5, whose §6
  reads `תחילתו של פרק זה ביום י״ב בטבת התשפ״ו (1 בינואר 2026) והוא יחול על הכנסה שהופקה או
  נצמחה ביום האמור או לאחריו`. The act is captured
  (`amend-2026-economic-efficiency-law-sefer-hachukim-3511.pdf`, sha256 `4196057a…`) and
  listed in `docs/sources-and-provenance.md`. A request for 2025 now finds no version in
  force rather than being answered with the 2026 schedule, which is the correct behaviour:
  the pre-288 amounts are not in this repository's corpus.
* **the composed pipeline** — every version `2026-01-01`, because it imports §121 and so
  cannot answer an earlier period however its own rules are dated.
* **ITO §120ב** — `2025-01-01`, because §120ב(ה)(1) names the tax years it suspends
  indexation for.

`tests/test_fixture_periods_are_in_force.py` is the standing guard: no companion case, in any
module, may be dated before the commencement of a rule it asserts — including rules in other
modules it imports.
**Resolution:** take commencement from the gazette act for every remaining amendment and
version those modules the same way.

### `corpus-holds-one-expression-per-provision`
The Israel ingest holds a single expression of each provision: the Income Tax Ordinance as of
2026-06-08 and the National Insurance Law as of 2026-06-15, each the consolidation's own
"נוסח עדכני נכון ליום" date. **This pilot therefore speaks for the current text and cannot
speak for an earlier year.** The consequence that matters is ITO §121: the bands encoded here
— 84,120 / 120,720 / 228,000 / 301,200 / 560,280 — are the text as replaced by ITO amendment
288 with effect from 1 January 2026. The 2025 schedule (193,800 / 269,280 in the middle bands)
is a different text and is not in the corpus, so no fixture in this repository computes a 2025
liability, and the OECD TaxBEN Israel 2025 table is not a like-for-like comparison for the
middle of the schedule. Since review round 1 the §121 module *says* so: its versions commence
2026-01-01 and an earlier request finds no version in force. See
`effective-from-is-not-commencement`.
**Resolution:** ingest the earlier expressions and encode the years separately.

## Divergences from references

### `child-allowance-surtax-exclusion-vs-oecd` — `unexplained`, and it matters
The captured consolidated text of NII §66 (amendment תשע״ג־3) reads, in full:

> הורה מבוטח זכאי לקצבת ילדים חודשית לפי פרק זה בעד כל ילד, למעט הורה מבוטח שיש לו הכנסה החייבת במס נוסף כמשמעותה בסעיף 121ב לפקודת מס הכנסה.

— an insured parent is entitled for each child, **except** an insured parent with income
liable to the ITO §121ב additional tax.

The OECD TaxBEN Israel description says of the same benefit: "It is not means-tested and not
taxable" (§4.1.4).

These cannot both describe the same operative rule. Nothing in the captured material resolves
it: whether the exclusion was ever brought into force, suspended, or is administered
differently cannot be determined from the snapshots, and the pilot does not have the amending
act's commencement clause. `unexplained`.

The pilot **encodes what the captured statutory text says**, and the composed pipeline's
high-earner fixture turns on it. That fixture demonstrates the encoded provision, not a
verified description of what the National Insurance Institute pays. Do not present it as the
latter.
**Resolution:** obtain the commencement and implementation history of תשע״ג־3 from the gazette
and from an Institute publication.

### `additional-tax-threshold-is-the-statute-s-nominal-figure`
ITO §121ב prints 640,000 ILS, and that is what this repository encodes and what the composed
pipeline applies. The current-year threshold is higher — the Ordinance index-links it under a
mechanism this repository does not implement — so a household between the nominal and the
indexed threshold is shown as liable here when it would not be in the year. The hand-authored
predecessor of this pilot supplied 721,560 for 2025, inferring it from the OECD TaxBEN
schedule's 50% top band read as 47% plus this section's 3%. That inference is **not** made
here: the encoder's module has no threshold input, so the pipeline applies the printed figure
and claims nothing about the indexed one.
**Resolution:** capture a Tax Authority עדכון סכומים notice and encode the current threshold
as a policy amount.

### `nii-68c-increment-not-reconcilable-with-the-published-figure` — `unexplained`
NII §68(ג) states the income-support addition as 70% of the §1(2)(ג) basic amount, which
§1(2)(ג) states nominally as 140 — so the statute, taken alone, gives 98. The National
Insurance Institute publishes the resulting increment directly as 111 (2025) and 113 (2026).
The statutory formula is encoded; the published figures are not in this repository, because a
policy capture is not encoder-generated content and this pilot carries only encoder-generated
content plus the composition. The two cannot be reconciled without an official §1(2)(ג) basic
amount, which has not been captured for either year. `unexplained`.

What the published figures DO settle: the OECD TaxBEN Israel description gives the special
basic amount as 153 ("0.7*153 or ILS 107"), and 0.7 × 153 = 107.1, which cannot reach the
Institute's published 111 under any rounding convention. The reference figure is inconsistent
with the publisher's own number and is used nowhere here.
**Resolution:** capture the Institute's published §1(2)(ג) basic amount, or its rounding rule,
for each year, as an `il/policy` corpus scope, and encode it from there.

## Amounts supplied rather than encoded

The Ordinance and the National Insurance Law state several amounts as NOMINAL figures under an
indexation mechanism this repository does not implement. Every nominal figure IS encoded, with
a proof. What is not here is any **current-year** figure: no Tax Authority עדכון סכומים notice
and no National Insurance Institute rate table has been ingested into the corpus, and this
repository carries no hand-made capture. The composed pipeline therefore takes the current
values as inputs, and every fixture states where its number came from. None is law as stated
here.

| Input | Statute's nominal figure, encoded | Supplied value in the fixtures | Where it came from |
|---|---|---|---|
| `credit_point_value_for_tax_year_ils` | ITO §33א: 504 ILS (`tax_credit_point_amount`) | 2,904 | OECD TaxBEN Israel 2025 — a reference, not a source of law |
| `current_basic_amount_first_and_fifth_plus_ils` | NII §1(2)(א): 150 ILS (`child_allowance_first_and_fifth_onward_base_amount`) | 173 | the National Insurance Institute's published rate table, effective 01.01.2026, read during this pilot and NOT carried in this repository |
| `current_basic_amount_second_third_fourth_ils` | NII §1(2)(ב): 188 ILS (`child_allowance_second_third_and_fourth_base_amount`) | 219 | the same table |

The composed pipeline reports `statutory_nominal_monthly_child_allowance_ils` alongside
`monthly_child_allowance_ils` precisely so the distance between the statute's printed figure
and the amount actually paid is visible in every fixture rather than quietly closed.

### `credit-point-current-value-not-captured`
ITO §33א states the credit point as 504 ILS a year, index-linked under §120א. The current
value is not in the statute and no Tax Authority עדכון סכומים notice has been captured
(gov.il refuses a plain HTTP client).
**Resolution:** fetch the notice through a real browser, ingest it as an `il/policy` scope,
and encode it.

### `indexation-mechanism-not-encoded`
ITO §120ב(א) is the annual indexation itself — "ב־1 בינואר של כל שנת מס יתואמו תקרות ההכנסה,
סכומי נקודת זיכוי ונקודת קיצבה" — and it is NOT encoded. The module carries only the §120ב(ה)(1)
judgment that indexation is suspended for tax years 2025 to 2027, which is the part that
matters for reading a frozen nominal amount. §120ב(ב) (the cost-of-living-agreement
adjustment), §120ב(ד) (the Minister's rounding rules) and §120ב(ה)(2) (the 2028 catch-up) are
not encoded either. Nothing in this repository computes an indexed amount from a nominal one,
which is why every current-year amount above is supplied rather than derived.
**Resolution:** encode §120ב(א)–(ד) and drive it from a captured index series.

## Narrowings inside the encoded sections

### `ito-section-66-what-is-and-is-not-executable`
§66 is the largest module in the pilot and the one that took the most rounds. What it
executes: the §66(א)(1) separate-calculation judgment for a non-registered spouse, including
the pension limb and its five-preceding-years alternative and the §66(א)(1)(א)–(ג) conditions
on a shared income source; the §66(ג)(1) composition of §34's and §36's credit points into the
separate calculation; and both child credit-point ladders, §66(ג)(4)(א) for the woman and
§66(ג)(5) for the man, as a named parameter per printed figure plus an age-band selector.

What it defers, each with a reason written into the module rather than into this file:
§66(א)(2) allocation of non-personal-exertion income between spouses; §66(א)(3) attribution of
a child's income to the registered spouse; §66(ב) separately calculated property income;
§66(ג)(1)'s remaining deductions and reliefs (§§35, 45A, 47, 47A, 121A, 10, 11); §66(ג)(2)'s
favoured-individual half point, which needs §37; §66(ג)(3)'s registered-spouse pension points,
which need §40(א); and §66(ג)(4)'s reference into §36א's own mechanics.

### `ito-section-66-birth-and-maturity-year-come-from-section-40`
§66(ג)(4)(א) defines ”שנת לידה“ and ”שנת בגרות“ by reference to §40(ב)(3), which this pilot
does not encode. Birth year and maturity year are therefore child-level Boolean facts
(`child_is_in_birth_year`, `child_is_in_maturity_year`, `child_is_before_maturity_year`)
rather than being derived from a date of birth. The module says so in a `deferred_outputs`
entry and does not invent an age from which to infer a maturity year.

### `ito-section-66-c-4-a1-election-not-applied`
§66(ג)(4)(א1) lets the mother elect to take one of a child's birth-year credit points in the
following tax year instead. The module encodes the deferrable point as a parameter and names
its own woman's selector `woman_child_credit_points_before_birth_year_election` to say plainly
that the election has not been applied; applying it needs the same mother and child connected
across two tax years, which this pilot's entity surface cannot express. The composed pipeline
allots the birth-year points in the birth year.

### `ito-section-40-not-encoded`
§40(א) (נקודות קיצבה for children, paid by the National Insurance Institute under §109 of the
1968 Law) and §40(ב) (the single-parent credit-point schedule) are not encoded. A single-parent
household therefore cannot be computed by this pilot, and the OECD TaxBEN "single parent tax
credit" of one additional point is outside its scope.

### `ito-section-121-reduced-rates-apply-to-income-not-to-a-person` — CLOSED
Was: §121(ב)(1) applies the reduced rates to "הכנסה חייבת בשנת המס מיגיעה אישית" — to income of
that character — and §121(ב)(2) withdraws them from income for which acceptable books were not
kept. Both are properties of INCOME, and the hand-authored predecessor of this pilot collapsed
them into one person-level switch, so a taxpayer with both personal-exertion and other income
was taxed wholly on one schedule.

Closed by the encoder. `il/statutes/income-tax-ordinance/section-121.yaml` derives
`reduced_rate_taxable_income` — the part of taxable income the reduced rates reach — from the
personal-exertion amount, extended to all income where the individual has reached sixty, less
the part of each requiring books that were not kept, and applies the general schedule to the
whole while crediting back the reduced-rate part. Its own fixtures exercise mixed income and
the books exception on each side. The composed pipeline supplies an employee's whole wage as
personal-exertion income, so no fixture there exercises the split, but the module does.

Review round 1 additionally found the composition classifying that wage under §121ב(ה)'s
paragraph (2) — personal-exertion income that is NOT §2(1)/(2) income — while setting the
paragraph (1) category to zero. A salary is `השתכרות או ריווח מעבודה`, ITO §2(2)(א), so it is
paragraph (1) income. The two assignments are now the other way round. §121ב subtracts both
categories identically, so no computed figure changed; the classification did.

### `ito-section-121b-subsections-b-to-e-not-encoded`
Only §121ב(א) and §121ב(א1) are encoded, plus the §121ב(ה) definitional split that separates
capital-source income from §2(1)/(2) and personal-exertion income. §121ב(ב) (no §91(ד)
advances on income bearing the additional tax), §121ב(ג) (notwithstanding any enactment) and
§121ב(ד) (the §8(ג) spreading rule) are not. The 5,385,285 ILS residential-dwelling threshold
IS encoded as a parameter, but nothing consumes it: the module's `deferred_outputs` record
that the §9(ג2) exemption interaction it belongs to is out of reach.

### `nii-section-1-paragraphs-1-and-3`
Only paragraph (2) of the הסכום הבסיסי definition is encoded — the one that governs the child
allowance. Paragraphs (1) and (3), covering maternity, work-injury, disability and residual
benefits, are not, nor is the update mechanism that follows them.

### `nii-section-68-repealed-and-unencoded-subsections`
§68(א), §68(ב) and §68(ג) are encoded. §68(ב)(1) and §68(ד)–(יא) are empty or repealed in the
captured expression and are not encoded.

### `nii-section-67-relations-are-facts`
§67 decides which parent a child is counted with. The encoding takes the household shape as
Boolean facts about one child and one "current" insured parent
(`child_has_two_parents`, `current_insured_parent_is_father`, `child_is_with_mother_alone`,
`child_has_natural_and_other_parent`, `child_is_with_current_insured_parent`) rather than as
relations between entities, because this pilot declares no Child entity. The section is
encoded and tested in its own module; the composed pipeline does not apply it (below).

### `credit-conditions-are-inputs-not-derived`
ITO §34 ("יחיד שהיה תושב ישראל בשנת המס"), §36 ("יחיד תושב ישראל") and §36א ("אשה") each state
a condition that enters as a Boolean input rather than being derived. Residence in particular
is not modelled: the Ordinance's §1 residence definition is not encoded. §36א states no
residence requirement and the encoding does not add one.

### `composed-capstone-bounds`
The composed pipeline is bounded to: at most two children; one earner; separate calculation
(חישוב נפרד) assumed elected, which is what makes §66(ג)(4)–(5) apply. The per-child age-band
selection is written twice — `child_1_credit_points` and `child_2_credit_points` — for two
reasons: the pilot declares no Child entity and uses no relation aggregation, and §66's own
per-child selector reads a parameter table that the engine can key only once per person per
period (`evaluate_parameter`: "parameter `{name}` is indexed; query it through a derived
rule"). Every point VALUE in those two rules is imported from the §66 module; none is retyped.
The correct shape is a Child entity with `sum(children.credit_points)`, which is out of scope
here.

Annual tax is divided by twelve for presentation. That is NOT a model of the monthly
ניכוי במקור deduction rules, which are not encoded.

### `composed-capstone-does-not-apply-nii-67-or-68b-c`
The pipeline wires NII §66 (entitlement), §65(א)'s definition of ”ילד“, and the §68(א)/§1(2)
birth-order structure. It does NOT apply §67 — it assumes every counted child falls in the
modelled parent's count — and it does not apply §68(ב) (pre-June-2003 multipliers) or §68(ג)
(the income-support increment); no fixture is on income support or has a child born before
June 2003. §67 and §68 are encoded and tested in their own modules.

### `nii-section-65-child-definition-partial`
Review round 1 found the capstone counting every supplied child for the monthly allowance
regardless of age, so a 19-year-old drew 219 ILS a month that NII §65(א) does not allow. The
pipeline now derives `child_N_is_a_child_under_section_65` from the child's age and presence,
against the section's own words — `ובלבד שהילד נמצא בישראל ולא מלאו לו 18 שנים` — and reads
the §68(א)/§1(2) birth-order amounts against `children_in_parent_child_count` rather than
against `number_of_children`. That keeps the monthly allowance count separate from the annual
ITO §66(ג) credit-point ladder, which has its own age bands and asks nothing about presence.

What is still partial:
* **§65 is not encoded as a module.** It is the definition section for the whole
  child-allowance chapter, and no `il/statutes/national-insurance-law-1995/section-65.yaml`
  exists. The condition is applied inside the composition, with a verbatim proof atom against
  the provision, because the pilot declares no Child entity and the test has to be asked once
  per child — the same constraint that makes `child_N_credit_points` repeat the §66(ג) ladder.
* **the definition's other limb is not modelled.** §65(א) also admits a child the insured
  maintains without being its parent, on conditions set in regulations that are not in the
  corpus.
* **§65(ב) is not modelled.** A child out of Israel for up to three months is still treated as
  in Israel, and the Institute may extend that. `child_N_is_present_in_israel` is supplied as
  a conclusion for the month; the three-month arithmetic is not computed.
* **age is supplied annually and read monthly.** `child_N_age_years` is one number for the
  case, so a child that turns 18 mid-year changes state at the start of the modelled month
  rather than on its birthday.
**Resolution:** encode §65 through the encoder and give the composition a Child entity, so the
definition is imported per child instead of repeated.

### `no-contributions-so-net-is-not-take-home-pay`
The employee's National Insurance and health contributions are not encoded, so
`monthly_net_income_ils` is net of income tax and inclusive of child allowance ONLY. **It is
not take-home pay and must not be presented as such.**

Half of that is a corpus gap rather than a choice. Israel splits the employee's payroll
deduction between two acts: the National Insurance Law's own rate table (לוח י׳,
`il/statute/national-insurance-law-1995/schedule-j/sign-1`, which IS in the corpus ingest) and
the National Health Insurance Law 1994 §14, which **is not in the corpus at all** — the Israel
ingest carries exactly two instruments, `income-tax-ordinance` (686 provisions) and
`national-insurance-law-1995` (728). Encoding one without the other would produce a figure that
looks even more like take-home pay than a figure that deducts neither, so this repository
deducts neither and says so.
**Resolution:** ingest the National Health Insurance Law 1994, encode §14 and לוח י׳, and wire
both into the pipeline in the same change.

Also not encoded: the pension-contribution credit (§45א), מס הכנסה שלילי (EITC), ITO §40's
single-parent and נקודות קיצבה schedules, and every other instrument.

## Oracles

### `no-executable-oracle`
Nothing in this repository is machine-compared against an external model.
`oracle-coverage-pending.yaml` declares a ceiling of 0 rather than overstating coverage. The
OECD TaxBEN Israel description is a narrative policy description read by a human; the TaxBEN
web calculator and the Tax Authority simulator (`secapp.taxes.gov.il/srsimulatorNZ`, linked
from the consolidated text of §121) are candidate oracles and are NOT wired. No fixture here
was produced by any of them.

A hand comparison against the TaxBEN description WAS done, and is reported in full in the pull
request. What it found:

* **Agrees**: the 84,120 and 120,720 bracket edges; the 560,280 edge at which 47% begins; the
  rates 10 / 14 / 20 / 31 / 35 / 47; the 2.25 basic credit points, which this encoding reaches
  as §34's two plus §36's quarter from two separate provisions; §36א's further half point for a
  woman; and every rung of both §66(ג) child ladders — 2.5 / 4.5 / 3.5 / 2.5 in the early
  years, then 2 for the mother against 1 for the father, and 0.5 against nothing in the
  maturity year.
* **Differs**: the 20%→31% and 31%→35% edges (TaxBEN 193,800 / 269,280, encoded 228,000 /
  301,200), because ITO amendment 288 widened those bands with effect from 1 January 2026 and
  the corpus holds only that expression; and the point at which the additional tax begins
  (TaxBEN's 50% band above 721,560, encoded from the 640,000 §121ב prints), because nothing
  here computes indexation.

Every difference is a fact about the statute or about what the corpus holds, not a defect in
either the description or the encoding — see `corpus-holds-one-expression-per-provision` and
`additional-tax-threshold-is-the-statute-s-nominal-figure`. The credit-point VALUE (2,904) is
absent from that comparison on purpose: it is supplied FROM TaxBEN, and a number taken from a
reference cannot then check the encoding.
