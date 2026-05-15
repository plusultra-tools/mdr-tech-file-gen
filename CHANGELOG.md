# Changelog

All notable changes to this project will be documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned for v0.2
- Introduce a real `data/mdr_clauses.yaml` with verbatim Annex II + III clause
  text from EUR-Lex Regulation (EU) 2017/745 (today the tool ships citation
  pointers only — no verbatim text file exists).
- Cross-link manifest entries to the EUR-Lex CELEX URL for each cited paragraph.
- `--format docx` to emit `.docx` for Notified Body submission (Notified Bodies
  primarily work in Word/PDF, not Markdown).

### Planned for v0.3
- Real GSPR (Annex I §1–§23) applicability generator from the device spec
  (today the GSPR §4 section is a static placeholder table — same rows for
  every device, every cell `[TODO]`).
- ISO 14971 risk-table template with structured hazard / harm / control rows.
- SOUP register CSV emitter (IEC 62304 §8.1.2).

### Planned for v0.4
- Hosted CI validator MVP. Pricing TBD pending demand validation.

## [0.1.0] - 2026-05-14

### Added
- Initial release: `scaffold`, `validate`, `manifest` CLI subcommands.
- Pydantic v2 schema for `device.yaml` (device class, intended use, risk class,
  IEC 62304 software safety class, SOUP register, intended users, clinical claims).
- **3 Jinja2 templates** aligned with MDR Annex II + Annex III sections:
  `annex-II.md.j2`, `annex-III.md.j2`, `standards-matrix.md.j2`.
- `data/standards_pointers.yaml` — citation pointer metadata (standard ID, clause,
  topic, applicability note). NOT verbatim clause text; that is on the roadmap
  for v0.2.
- Fixture device YAML (`examples/quickstart/device-spec.yaml`) — a Class IIa SaMD
  clinical-decision-support device, used by the smoke test.
- pytest matrix on py3.10/3.11/3.12 + CLI smoke test in CI.
- MIT license, SECURITY.md disclosure policy, kill-gate decision criteria.

### Known limitations (v0.1)
- Most evidence sections render as `[TODO]` placeholders. This is a
  scaffolding tool, NOT a finished technical-file generator.
- No PyPI release yet — install from source via `pip install git+https://...`.
- GSPR §4 table is a static placeholder; real spec→Annex I mapping is v0.3.
- Citations are pointers, not verbatim clause text; verbatim is v0.2.
- Output is Markdown only; DOCX/PDF for Notified Body submission is v0.2.
