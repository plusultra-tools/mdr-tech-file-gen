# Changelog

All notable changes to this project will be documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned for v0.2
- Replace structured-placeholder MDR clause text in `data/mdr_clauses.yaml` with
  the verbatim wording from EUR-Lex Regulation (EU) 2017/745.
- Cross-link manifest entries to the EUR-Lex CELEX URL for each cited paragraph.
- `--format word` to emit `.docx` instead of Markdown for Notified Body submission.

### Planned for v0.3
- GSPR (General Safety and Performance Requirements) checklist generator,
  mapping every Annex I clause to an evidence type the spec must declare.
- ISO 14971 risk-table template with structured hazard / harm / control rows.
- SOUP register CSV emitter (IEC 62304 §8.1.2).

### Planned for v0.4
- Hosted validator MVP: webhook integration, PR-comment diff against previous
  skeleton, Stripe checkout for the €50/mo plan.

## [0.1.0] - 2026-05-14

### Added
- Initial release: `scaffold`, `validate`, `manifest` CLI subcommands.
- Pydantic v2 schema for `device.yaml` (device class, intended use, risk class,
  IEC 62304 software safety class, SOUP register, intended users, clinical claims).
- 13 Jinja2 templates aligned with MDR Annex II + Annex III sections.
- `data/mdr_clauses.yaml` with structured placeholders for every cited clause
  (verbatim wording pending v0.2 EUR-Lex pass).
- Fixture device YAML (`tests/fixtures/sample_device.yaml`) — a Class IIa SaMD
  clinical-decision-support device, used by the smoke test.
- pytest matrix on py3.10/3.11/3.12 + CLI smoke test in CI.
- MIT license, SECURITY.md disclosure policy, kill-gate decision criteria.
