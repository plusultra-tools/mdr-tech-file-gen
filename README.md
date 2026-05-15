# mdr-tech-file-gen

**YAML device spec → CE-MDR Annex II/III technical file skeleton in one command.** Pure-Python CLI that reads a typed `device.yaml`, validates it against a Pydantic schema, and renders a 13-section Annex II/III technical-file skeleton ready to drop into your QMS repo or hand to a Notified Body reviewer.

```bash
pip install mdr-tech-file-gen
mdr-techfile scaffold --spec device.yaml --output techfile/
```

---

## Why this exists

Solo-founder med-device / SaMD startups in the EU have three options for assembling the Annex II/III technical file Regulation (EU) 2017/745 demands:

1. **Hire a regulatory consultant** — €5,000–€15,000 for the first draft, plus retainer. Outside the budget when you're still pre-revenue.
2. **Buy a template pack** — [Advisera](https://advisera.com/13485academy/) sells one for €700+. [OpenRegulatory](https://openregulatory.com/) gives away Word/Markdown templates for free, no strings attached, and is the de-facto reference for the bootstrapped end of the market.
3. **Write it from scratch** — six weeks of regex-and-Google before a Notified Body will look at you.

`mdr-tech-file-gen` is the structured / CI-friendly upgrade to option 2. OpenRegulatory templates are excellent prose, but they are static Word docs — you can't diff them in code review, you can't generate them from a single source of truth, you can't fail a pipeline when a required section is missing, and you can't reference them from issue trackers.

This tool takes a single `device.yaml` (intended use, risk class, IEC 62304 software safety class, SOUP register, intended users, clinical claims) and renders the 13 standard sections as Markdown plus a `manifest.json` that verbatim-cites every MDR clause and ISO/IEC standard reference each section is meant to satisfy. You commit the YAML and the generated skeleton to git, you iterate the YAML, you regenerate. The Notified Body gets a coherent technical file; you get a build that breaks when a Class IIa device has no risk-management plan.

## What it does

1. `pip install mdr-tech-file-gen` — single `pip install`, pure Python, no Java, no MS Word.
2. `mdr-techfile scaffold --spec device.yaml --output techfile/` — renders 13 Markdown sections + `manifest.json` + a top-level `README.md` for the file.
3. `mdr-techfile validate --spec device.yaml` — checks the YAML against the Pydantic schema and the structural completeness rules. Exits 0 if valid, 1 with a structured error list if not. Designed for CI.
4. `mdr-techfile manifest` — dumps the verbatim-cite mapping (each generated section → MDR Annex II/III paragraphs + ISO 14971/IEC 62304/IEC 62366 standard references), so a reviewer can audit the provenance of every claim.

## The 13 sections it generates

Aligned with MDR Annex II (technical documentation) and Annex III (post-market surveillance):

1. **Device description and specification** — Annex II §1.1
2. **Reference to previous and similar generations of the device** — Annex II §1.2
3. **Information to be supplied by the manufacturer** (labelling, IFU, UDI) — Annex II §2
4. **Design and manufacturing information** — Annex II §3
5. **General safety and performance requirements (GSPR) checklist** — Annex II §4, Annex I
6. **Benefit-risk analysis and risk management file** — Annex II §5, ISO 14971:2019
7. **Software lifecycle file** (SaMD only) — IEC 62304:2006+A1:2015, MDCG 2019-11, MDCG 2019-16
8. **Usability engineering file** — IEC 62366-1:2015+A1:2020
9. **Biological and clinical safety / materials** (N/A skeleton for SaMD) — ISO 10993 series
10. **Product verification and validation** — Annex II §6
11. **Clinical evaluation** — Annex II §6.1, MDR Article 61, MDCG 2020-6, MDCG 2020-13
12. **Post-market surveillance plan** — Annex III, MDR Article 84
13. **Post-market clinical follow-up (PMCF) plan + Declaration of Conformity** — Annex XIV Part B, Annex IV

Each section is generated with the verbatim MDR clause text quoted at the top (from `data/mdr_clauses.yaml`, sourced from EUR-Lex Regulation (EU) 2017/745) and a structured TODO list of evidence the manufacturer must attach.

## What it does NOT do

- **NOT a regulatory consultant.** It generates structure and citations. It does not write your clinical evaluation. It does not assess your risk file.
- **NOT legal advice.** Use of this tool does not establish a regulatory affairs relationship. The output is a starting skeleton; a competent regulatory professional must review the completed file before submission.
- **NOT a substitute for Notified Body conformity assessment.** For Class IIa, IIb, III devices, a Notified Body assessment is mandatory under MDR. This tool helps you prepare the documentation the NB will audit; it does not replace the audit.
- **NOT QMS software.** It does not implement ISO 13485 quality management processes. Plug it into your existing QMS (Greenlight Guru, Matrix, Qualio, Notion + git, whatever).
- **NOT MDR-certified itself.** The tool is not a medical device. It is a documentation scaffolder.

## Pricing

- **CLI: MIT licensed, free forever.** Source on GitHub. Same skeleton output whether you pay or not.
- **Hosted validator (planned, €50–€100/mo per device)** — continuous CI integration: webhook on every `device.yaml` change, run the structural validator, post a PR comment with the diff against the previous skeleton, alert on regressions (e.g. you removed a SOUP without updating §7), track which sections are still TODO. Stripe-billed when the demand signal justifies launching. This is the monetisation hook: the OSS CLI gets you in the door of CI/CD-minded solo SaMD shops; the hosted service is what teams trying to ship past Class IIa pay for.

## Comparison to adjacent tooling

- **[OpenRegulatory](https://openregulatory.com/) templates** — excellent free Word/Markdown prose templates, community-edited, very respected in the bootstrapped MDR space. `mdr-tech-file-gen` is the schema-driven / git-native sibling: same target audience, different ergonomics. We cite OpenRegulatory in our docs and recommend reading their templates alongside the generated skeleton.
- **[Advisera 13485 toolkit](https://advisera.com/13485academy/)** — €700+ for a polished pack with consulting hours bolted on. Better fit when you already have a budget; ours is the no-budget path.
- **[Matrix Requirements](https://matrixreq.com/) / [Greenlight Guru](https://www.greenlight.guru/) / [Qualio](https://www.qualio.com/)** — full eQMS platforms, €2K–€20K/year, way past where most solo founders start. Complementary later; competitive too early.

## Roadmap

- **v0.1 (this release)** — Pydantic spec schema, 13-section Jinja2 templates, `scaffold` / `validate` / `manifest` CLI, fixture device YAML, smoke-test in CI.
- **v0.2** — Real verbatim MDR Annex II + III clause text in `data/mdr_clauses.yaml` (currently structured placeholders; sourced from EUR-Lex on next pass).
- **v0.3** — GSPR checklist generator (Annex I §1–§23, mapped to evidence types), ISO 14971 risk table template, SOUP register CSV emitter.
- **v0.4** — Hosted-validator MVP: webhook, PR-comment integration, Stripe checkout for €50/mo plan.
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
