# Encoding gaps

Everything this pilot does not do, could not verify, or verified against
something weaker than primary law. Divergences from a reference are recorded
here as `unexplained` with both numbers; no issue is ever filed against an
external reference.

## Structural gaps (scaffold)

### `source-tier` — the provision source of record is a secondary consolidation
The Knesset national legislation database serves the consolidated text through a
client-rendered application; `KNS_DocumentIsraelLaw` returns empty over OData.
The pilot therefore encodes from ספר החוקים הפתוח (he.wikisource), the
consolidation the Knesset database itself links to as "לחוק המלא". Tier
`consolidation-knesset-linked` — secondary. Effective dates and amendment
content are taken from the official gazette PDFs where they matter.
**Resolution:** capture the Knesset "נוסח מלא" PDFs through a real browser and
re-anchor.

### `corpus-anchor` — citation paths are not yet corpus-anchored
No `il-rulespec-*` corpus release exists. Module
`source_verification.source_sha256` values are hashes of the captured snapshot's
provision text, not of a corpus provision, and `corpus_citation_path` values
name paths that the corpus does not yet contain.
**Resolution:** re-anchor pass after the Israel ingest lands and the release is
signed and registered.

### `no-executable-oracle` — nothing is machine-compared
The OECD TaxBEN Israel description is a narrative policy description read by a
human, not a model run. The TaxBEN web calculator and the Tax Authority
simulator are candidate oracles and are **not wired**. No fixture in this
repository was produced by any of them.
