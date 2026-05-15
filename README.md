# mdr-tech-file-gen

[![tests](https://github.com/plusultra-tools/mdr-tech-file-gen/actions/workflows/test.yml/badge.svg)](https://github.com/plusultra-tools/mdr-tech-file-gen/actions/workflows/test.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![python: 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![status: v0.1 pre-release](https://img.shields.io/badge/status-v0.1%20pre--release-orange.svg)](CHANGELOG.md)

**YAML device spec → CE-MDR Annex II/III technical file scaffolding in one command.** Pure-Python CLI that reads a typed `device.yaml`, validates it against a Pydantic schema, and renders an Annex II/III technical-file skeleton — an engineering team starting point for MDR Annex II/III scaffolding, NOT a finished submission. Most evidence sections ship as `[TODO]` placeholders the manufacturer must complete.

```bash
# v0.1: install from source (PyPI release pending)
pip install git+https://github.com/plusultra-tools/mdr-tech-file-gen.git
mdr-techfile scaffold --spec device.yaml --out techfile/
```

---

## Why this exists

Solo-founder med-device / SaMD startups in the EU have three options for assembling the Annex II/III technical file Regulation (EU) 2017/745 demands:

1. **Hire a regulatory consultant** — €5,000–€15,000 for the first draft, plus retainer. Outside the budget when you're still pre-revenue.
2. **Buy a template pack** — [Advisera](https://advisera.com/13485academy/) sells one for €700+. [OpenRegulatory](https://openregulatory.com/) gives away Word/Markdown templates for free, no strings attached, and is the de-facto reference for the bootstrapped end of the market.
3. **Write it from scratch** — six weeks of regex-and-Google before a Notified Body will look at you.

`mdr-tech-file-gen` is the structured / CI-friendly upgrade to option 2. OpenRegulatory templates are excellent prose, but they are static Word docs — you can't diff them in code review, you can't generate them from a single source of truth, you can't fail a pipeline when a required section is missing, and you can't reference them from issue trackers.

This tool takes a single `device.yaml` (intended use, risk class, IEC 62304 software safety class, SOUP register, intended users, clinical claims) and renders Annex II + Annex III scaffolding as Markdown plus a `manifest.json` that MDR-cross-references each generated section to the relevant Annex II/III paragraphs and ISO/IEC standards (verbatim EUR-Lex clause text is on the roadmap — v0.2). You commit the YAML and the generated skeleton to git, you iterate the YAML, you regenerate. The manufacturer fills in the substantive evidence; the tool keeps the structure honest.

## What it does

1. `pip install git+https://github.com/plusultra-tools/mdr-tech-file-gen.git` — pure Python, no Java, no MS Word. (PyPI release pending.)
2. `mdr-techfile scaffold --spec device.yaml --out techfile/` — renders Annex II + Annex III Markdown skeletons + a `standards-matrix.md` + a `checklist.md` + a `manifest.json` + an `audit.sha256` chain.
3. `mdr-techfile validate --spec device.yaml` — checks the YAML against the Pydantic schema. Exits 0 if valid, 1 with a structured error list if not. Designed for CI.
4. `mdr-techfile manifest --spec device.yaml` — dumps the citation pointer mapping (each generated section → MDR Annex II/III paragraphs + ISO 14971/IEC 62304/IEC 62366 standard clauses), so a reviewer can audit which clauses each section is meant to address. Note: pointers are citation metadata; verbatim EUR-Lex clause text is roadmap (v0.2).

## What gets generated

`scaffold` writes **3 Jinja2-rendered Markdown files** plus a checklist, a JSON manifest, and an audit hash chain:

- **`annex-II.md`** — Annex II technical-documentation skeleton with the following headings inside one document, aligned with MDR Annex II (technical documentation):
  1. Device description and specification — Annex II §1.1
  2. Reference to previous and similar generations of the device — Annex II §1.2
  3. Information to be supplied by the manufacturer (labelling, IFU, UDI) — Annex II §2
  4. Design and manufacturing information — Annex II §3
  5. General safety and performance requirements (GSPR) — Annex II §4, Annex I *(static placeholder table in v0.1; spec→GSPR mapping is roadmap v0.3)*
  6. Benefit-risk analysis and risk management file — Annex II §5, ISO 14971:2019
  7. Software lifecycle file (SaMD only) — IEC 62304:2006+A1:2015, MDCG 2019-11, MDCG 2019-16
  8. Usability engineering file — IEC 62366-1:2015+A1:2020
  9. Biological and clinical safety / materials — ISO 10993 series
  10. Product verification and validation — Annex II §6
  11. Clinical evaluation — Annex II §6.1, MDR Article 61, MDCG 2020-6, MDCG 2020-13
- **`annex-III.md`** — Annex III post-market surveillance skeleton (post-market surveillance plan, PMCF plan, Declaration of Conformity pointers) — Annex III, MDR Articles 83–86, Annex XIV Part B, Annex IV.
- **`standards-matrix.md`** — table mapping each section to the ISO/IEC standards it cites.
- **`checklist.md`** — structural completeness checklist derived from the spec.
- **`manifest.json`** — machine-readable citation pointer manifest.
- **`audit.sha256`** — SHA-256 chain of all generated files for tamper-evidence.

Each section currently ships with a citation pointer to the MDR clause + ISO/IEC standard it addresses. Verbatim EUR-Lex clause text is on the roadmap (v0.2). Most evidence rows ship as `[TODO]` — this is a scaffold, not a finished file.

## What it does NOT do

- **NOT a regulatory consultant.** It generates structure and citations. It does not write your clinical evaluation. It does not assess your risk file.
- **NOT legal advice.** Use of this tool does not establish a regulatory affairs relationship. The output is a starting skeleton; a competent regulatory professional must review the completed file before submission.
- **NOT a substitute for Notified Body conformity assessment.** For Class IIa, IIb, III devices, a Notified Body assessment is mandatory under MDR. This tool helps you prepare the documentation the NB will audit; it does not replace the audit.
- **NOT QMS software.** It does not implement ISO 13485 quality management processes. Plug it into your existing QMS (Greenlight Guru, Matrix, Qualio, Notion + git, whatever).
- **NOT MDR-certified itself.** The tool is not a medical device. It is a documentation scaffolder.

## Pricing

- **CLI: MIT licensed, free forever.** Source on GitHub.
- A hosted CI integration is on the roadmap (pricing TBD pending demand validation). No paid tier is shipped today.

## Comparison to adjacent tooling

- **[OpenRegulatory](https://openregulatory.com/) templates** — excellent free Word/Markdown prose templates, community-edited, very respected in the bootstrapped MDR space. `mdr-tech-file-gen` is the schema-driven / git-native sibling: same target audience, different ergonomics. We cite OpenRegulatory in our docs and recommend reading their templates alongside the generated skeleton.
- **[Advisera 13485 toolkit](https://advisera.com/13485academy/)** — €700+ for a polished pack with consulting hours bolted on. Better fit when you already have a budget; ours is the no-budget path.
- **[Matrix Requirements](https://matrixreq.com/) / [Greenlight Guru](https://www.greenlight.guru/) / [Qualio](https://www.qualio.com/)** — full eQMS platforms, €2K–€20K/year, way past where most solo founders start. Complementary later; competitive too early.

## Roadmap

- **v0.1 (this release)** — Pydantic spec schema, 3 Jinja2 templates (annex-II, annex-III, standards-matrix), `scaffold` / `validate` / `manifest` CLI, fixture device YAML, smoke-test in CI. PyPI release pending.
- **v0.2** — Verbatim MDR Annex II + III clause text from EUR-Lex Regulation (EU) 2017/745 (today citations are pointer metadata only, NOT verbatim clause text). `--format docx` exporter for Notified Body submission.
- **v0.3** — GSPR checklist generator: real spec→Annex I §1–§23 applicability mapping (today the GSPR table is a static placeholder). ISO 14971 risk-table template with structured hazard/harm/control rows. SOUP register CSV emitter.
- **v0.4** — Hosted CI validator MVP. Pricing to be determined after demand validation.
- **v1.0** — Wire-format stability for the manifest schema; semver guarantees.

## Audience

- Class I / IIa solo-founder med-device and SaMD startups in the EU.
- Bootstrapped digital-health teams shipping under MDR who can't justify €5K+ consultant fees pre-revenue.
- Regulatory-conscious open-source health-tech projects that want their documentation in git, not in a Word doc on someone's laptop.
- Distribution channels: `r/medicaldevices`, `r/IndieBiotech`, `r/SaaS`, Hacker News (`Show HN`), `awesome-mdr` GitHub lists, the OpenRegulatory community Slack, LinkedIn regulatory-affairs groups.

## Contributing

Open an issue with a real `device.yaml` that fails to scaffold, or a section that doesn't map cleanly to your device class. PRs welcome — especially for additional standard references (ISO 13485:2016, ISO 14155:2020, ISO 27001 for SaMD security) and template polish.

## License

MIT. See [LICENSE](LICENSE).

## Disclaimer

This tool is provided as-is. It does not constitute regulatory or legal advice. Compliance with Regulation (EU) 2017/745 (MDR) and the harmonised standards remains the sole responsibility of the device manufacturer.
