# Carrd landing-page copy — mdr-tech-file-gen

## Hero

**YAML device spec → CE-MDR technical file skeleton in one command.**

`mdr-techfile scaffold --spec device.yaml --output techfile/` — 13 Annex II/III sections, MDR clauses verbatim-cited, ready for git review. Pure Python, MIT-licensed, no consultant gatekeeping.

[Install from PyPI →](https://pypi.org/project/mdr-tech-file-gen/) · [GitHub →](https://github.com/plusultra/mdr-tech-file-gen)

---

## Sub-hero (one paragraph)

OpenRegulatory's free Word templates are the bootstrapped MDR community's gold standard for written prose. `mdr-tech-file-gen` is the schema-driven sibling: one `device.yaml` becomes a 13-section Markdown skeleton with MDR Annex II/III paragraphs and ISO 14971 / IEC 62304 / IEC 62366 references quoted inline. Diff it in code review. Fail the build when a Class IIa device has no risk management plan. MIT-licensed CLI; hosted CI validator planned at €50–100/mo per device.

---

## Three-card row

**Git-native.** YAML in, Markdown + JSON manifest out. The technical file lives in your repo, gets reviewed in PRs, regenerates on every spec change. No `.docx` round-tripping.

**Citation-honest.** Every section quotes the MDR Annex II/III paragraph that mandates it (verbatim from EUR-Lex Reg. (EU) 2017/745, full text pending v0.2 pass) plus the ISO/IEC standard reference a Notified Body will expect. Auditable provenance.

**Consultant-priced-out friendly.** Solo SaMD shops can't justify €5–15K for a regulatory consultant pre-revenue. This is the no-budget on-ramp. Free CLI; pay only when you want the hosted CI integration.

---

## Audience CTA

Building a Class I / IIa medical-device or SaMD startup in the EU?

[Tell me what section your audit failed on →](mailto:plusultra.dev@proton.me?subject=mdr-tech-file-gen)

---

## Honest disclaimer

Not a regulatory consultant. Not legal advice. Not a substitute for Notified Body conformity assessment. A starting skeleton, not a finished file. Read the README before you assume anything else.

---

## Footer

MIT-licensed. Adjacent to (and recommends) [OpenRegulatory](https://openregulatory.com/) free templates. Built for `r/medicaldevices`, `r/IndieBiotech`, OpenRegulatory Slack, LinkedIn regulatory-affairs groups. v0.1 ships the CLI surface, the schema, and 13 templates with structured-placeholder MDR text; v0.2 swaps in verbatim EUR-Lex text.
