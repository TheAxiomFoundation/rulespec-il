# Sources and provenance

## The official registry, and why it is not the text source

The Knesset **מאגר החקיקה הלאומי** (national legislation database) is the official
registry of Israeli primary legislation. For the two pilot instruments:

| Instrument | `IsraelLawID` | Status |
|---|---|---|
| פקודת מס הכנסה [נוסח חדש] | 2000944 | תקף |
| חוק הביטוח הלאומי [נוסח משולב], התשנ״ה–1995 | 2000198 | תקף |

The database exposes an OData interface (`KNS_IsraelLaw`, `KNS_DocumentIsraelLaw`).
`KNS_IsraelLaw` resolves both instruments and their amendment tables. **`KNS_DocumentIsraelLaw`
returns empty for both**, and the consolidated "נוסח מלא" is served by a
client-rendered SharePoint application that returns a JavaScript shell to a
plain HTTP client. So the registry is used here as the authority for *what the
law is, which amendments touched it, and where each amending act was published*
— not as a text source.

The database's own "לחוק המלא" link points at **ספר החוקים הפתוח** on
he.wikisource. That is why the Wikisource consolidation, and not Nevo, is the
provision source of record for this pilot.

## Source tiers

1. `official-gazette` — **רשומות / ספר החוקים** PDFs on `fs.knesset.gov.il`. The
   authentic published text of an amending act. Authoritative for content and
   for effective dates.
2. `consolidation-knesset-linked` — **ספר החוקים הפתוח** (he.wikisource). A
   volunteer consolidation, linked from the Knesset database as the full text.
   Provision source of record for this pilot. **Secondary tier**, stated as such
   everywhere it is relied on.
3. `consolidation-secondary` — **Nevo** (`nevo.co.il`). Commercial consolidation,
   cross-check only.
4. `policy-publication` — **רשות המסים** and **המוסד לביטוח לאומי** publications.
   The only admissible source for current-year regulated amounts.
5. `reference` — comparison material (OECD TaxBEN and similar). Never law.

Statutory text carries no copyright in Israel: Copyright Act 2007 §6 excludes
"חוקים" and other edicts of government. A consolidation's editorial apparatus —
amendment-history brackets like `[תיקון: תשמ״ה־3]`, cross-reference styling,
comparison tables — belongs to its publisher and is stripped from provision
bodies. Amendment history is preserved as provision metadata, not as text.

## Snapshots behind the pilot encodings

| File | Tier | URL | sha256 | Retrieved (UTC) |
|---|---|---|---|---|
| `ito-wikisource.html` | consolidation-knesset-linked | `https://he.wikisource.org/wiki/פקודת_מס_הכנסה` | `87535c2b8cd8aa50b27d32301dc2ddd768390ef64e9fb4f391c3e65fe99dc228` | 2026-09-06T11:41:55Z |
| `ito-wikisource-2025-rev2971879.html` | consolidation-knesset-linked | `https://he.wikisource.org/w/index.php?oldid=2971879` (rev of 2025-12-31T17:00:31Z) | `33e8ef54f1f72af98991cd1b540466007a4dc81c42d79c09cb742c03468592f3` | 2026-09-06T11:48:00Z |
| `nii-law-wikisource.html` | consolidation-knesset-linked | `https://he.wikisource.org/wiki/חוק_הביטוח_הלאומי` | `7dbaaa757912c71b361381640d2578bf2c6ab52f2002817b85d677c2267f0715` | 2026-09-06T11:41:55Z |
| `amend-2026-economic-efficiency-law-sefer-hachukim-3511.pdf` | official-gazette | `https://fs.knesset.gov.il/25/law/25_lsr_12846863.pdf` | `4196057aa7d796bf64935647f4f3e3d02511fa00eaa215dc5ad914601b4e6583` | 2026-09-06T11:41:55Z |
| `ito-nevo.html` | consolidation-secondary | `https://www.nevo.co.il/law_html/law01/255_001.htm` | `fe4abf24f639f5270f73095129b87cfcbe750249287576b89becf1e1df1378dd` | 2026-09-06T11:41:55Z |
| `btl-child-allowance-rates.html` | policy-publication | `https://www.btl.gov.il/benefits/children/Pages/שיעורי הקצבה.aspx` | `4bbf76244b622d4925e88cab0193dd4df56c8a1f59961c24122bee72dbb63785` | 2026-09-06T12:10:00Z |

The last row is the pilot's only official current-amount capture: the National
Insurance Institute's published child allowance table, which states
"(החל מ- 01.01.2026)". It is **not** encoded in this repository. Every module here
is encoder-generated from a corpus citation, and no `il/policy` scope has been
ingested for the Institute's publication, so the current-year child-allowance
amounts enter the composed pipeline as supplied inputs with their provenance
stated in the fixtures. `btl.gov.il` answers a request carrying a browser
User-Agent; `gov.il` (the Tax Authority) does not, so no Tax Authority
עדכון סכומים notice was captured either, and the credit-point value is supplied
the same way.

## From snapshot to corpus to encoding

The snapshots above were ingested into axiom-corpus as
`il/statute/income-tax-ordinance/...` and
`il/statute/national-insurance-law-1995/...` on branch `ingest/il-taxben-pilot`,
1,414 provisions, one expression each: the Ordinance as of 2026-06-08 and the
National Insurance Law as of 2026-06-15. **The corpus is the source of record for
provision text**, and every module in this repository was encoded from a corpus
citation, not from a snapshot file. Every proof excerpt is a verbatim NFC
substring of a corpus body.

The snapshots themselves live in the dispatching workspace
(`ops/il-lane/sources/`); they are not committed here. What is still missing is a
signed, immutable `il-rulespec-*` release: until it exists, the modules declare a
`corpus_citation_path` and no `source_sha256`, because there is no release digest
to pin to. See `docs/ENCODING-GAPS.md`, `no-signed-corpus-release` and
`no-source-sha256-pins`.

## Two revisions of one page, and only one of them is encoded

The §121 bracket amounts differ between tax year 2025 and tax year 2026. The
current Wikisource revision carries the 2026 amounts; the last revision of
calendar 2025 (`oldid=2971879`) carries the 2025 amounts. Both pages are
captured, but **only the 2026 expression was ingested into the corpus, and so
only tax year 2026 is encoded.** The §121 module's versions all commence
2026-01-01 and a request for an earlier period finds no version in force — it is
not answered with the 2026 schedule. The composed pipeline commences on the same
date for the same reason.

The commencement is taken from the gazette, not from either consolidation: ס״ח
3511 of י״ג בניסן התשפ״ו, פרק ג׳ "ריווח מדרגות מס הכנסה", §5 (ITO amendment 288),
whose §6 reads

    תחילתו של פרק זה ביום י״ב בטבת התשפ״ו (1 בינואר 2026) והוא יחול על הכנסה שהופקה או נצמחה ביום האמור או לאחריו

The 2025 revision is retained in the capture set so that the second expression
can be ingested and encoded without re-fetching a page that will have moved on.
See `docs/ENCODING-GAPS.md`, `corpus-holds-one-expression-per-provision` and
`effective-from-is-not-commencement`.

## Text normalization

NFC. Gershayim (״), geresh (׳) and maqaf (־) are kept exactly as captured —
they appear inside statutory citations (התשנ״ה) and in numeric ranges (מ־301,200),
and normalizing them away would break verbatim proof matching. Bidi control
characters (U+200E, U+200F, U+FEFF) are removed. Language tag `he`.

Section suffixes transliterate by **ordinal**, not by sound: א→a, ב→b, ג→c, ד→d,
ה→e … so §121ב → `section-121b`, §120ב → `section-120b`, §36א → `section-36a`.
Sound-based transliteration would give `121v`/`36alef` and collide across
instruments.
