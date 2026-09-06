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

The snapshots themselves live in the dispatching workspace
(`ops/il-lane/sources/`) pending corpus ingestion; they are not committed here.
Once the `il-rulespec-*` corpus release exists, each module's
`source_verification.source_sha256` is re-anchored to the corpus provision hash.
Until then the modules carry the snapshot's provision hash and this is recorded
in `docs/ENCODING-GAPS.md`.

## Two revisions of one page, on purpose

The pilot encodes tax years 2025 and 2026, whose §121 bracket amounts differ.
The current Wikisource revision carries the 2026 amounts; the last revision of
calendar 2025 (`oldid=2971879`) carries the 2025 amounts. Both are captured, and
each `effective_from` cites the revision that states its amounts. The *cause* of
the difference is taken from the gazette, not from either consolidation: ס״ח
3511, פרק ג׳ "ריווח מדרגות מס הכנסה", §5 (ITO amendment 288) with §6 setting
תחילה at 1 January 2026.

## Text normalization

NFC. Gershayim (״), geresh (׳) and maqaf (־) are kept exactly as captured —
they appear inside statutory citations (התשנ״ה) and in numeric ranges (מ־301,200),
and normalizing them away would break verbatim proof matching. Bidi control
characters (U+200E, U+200F, U+FEFF) are removed. Language tag `he`.

Section suffixes transliterate by **ordinal**, not by sound: א→a, ב→b, ג→c, ד→d,
ה→e … so §121ב → `section-121b`, §120ב → `section-120b`, §36א → `section-36a`.
Sound-based transliteration would give `121v`/`36alef` and collide across
instruments.
