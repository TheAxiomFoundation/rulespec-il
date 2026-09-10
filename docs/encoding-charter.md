# Encoding charter

Chartered 2026-09-06 as a bounded Israel proof of concept.

## Why Israel

- **Existing institutional relationship.** A PolicyEngine Israel hackathon was
  run with the Prime Minister's Office and digital.gov.il on 2023-07-06,
  encoding municipal tax reduction (הנחה בארנונה) and discharged-soldier
  credits; a session with Finance Ministry leadership followed on 2023-09-21.
  This repository is the Axiom-native successor to that work.
- **A genuinely non-Latin, right-to-left test of the stack.** Denmark proved a
  non-English pilot; Hebrew adds RTL text, gershayim and geresh inside statutory
  citations, and Hebrew-letter section suffixes that need an ordinal
  transliteration convention rather than a phonetic one.
- **A compact, checkable slice.** The individual rate schedule and the child
  allowance are small enough that a reader can verify every encoded number
  against the statute in an afternoon, and they interact: the National
  Insurance Law conditions the child allowance on the Income Tax Ordinance's
  additional tax.

## Sequence

1. **Source snapshots.** Capture the Ordinance and the National Insurance Law
   from the consolidation the Knesset database links to, plus the gazette PDFs
   of the amending acts that matter for the encoded years. Every snapshot
   carries URL, retrieval time in UTC, sha256, and a tier.
2. **Corpus ingestion.** Land the snapshots in axiom-corpus under
   `il/statute/...` with signed ingest manifests from a clean root checkout.
   Corpus PRs are merge-commit, never squash.
3. **Release cut.** Publish an immutable signed `il-rulespec-*` release from
   corpus main.
4. **Toolchain binding.** Dedicated gated PR adding `.axiom/toolchain.toml` and
   repinning the shared validate workflow. Never combined with content changes.
5. **Encoding.** Every atomic module in this repository is produced by the
   supervised encoder — `axiom-encode encode <corpus citation> --backend codex
   --apply` — and carries an apply manifest under `.axiom/encoding-manifests/`.
   Hand-written YAML is never a module. The only hand work is a findings file
   handed back to the encoder for a repair round, and the composed pipeline,
   which is assembled rather than encoded.

Step 3 has not completed. The pilot therefore encodes from, and validates
against, the corpus ingest branch rather than a signed release; the encoder used
is a local bootstrap build, because the pinned ref refuses to run without one;
and the apply manifests are signed with a throwaway local key, which is why the
shared generated-content guard stays off until the release exists. Each of those
is written up in `docs/ENCODING-GAPS.md` rather than papered over.

## Deliberately out of scope

National Insurance and health contributions (§335 NII Law, §14 Health Insurance
Law), the pension-contribution credit, שכר מינימום interactions, מס הכנסה שלילי
(EITC), and every other instrument. A pilot that quietly grows into a claim of
coverage is worse than a pilot that stays small.
