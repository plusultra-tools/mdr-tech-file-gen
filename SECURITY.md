# Security policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | yes       |
| < 0.1   | no        |

## Reporting a vulnerability

Email **plusultra.dev@proton.me** with subject `[mdr-tech-file-gen] security`. Do **not** open a public GitHub issue for security findings.

Expected response: acknowledgement within 72 hours, triage within 7 days, fix or mitigation within 30 days for high-severity issues.

## Threat model

`mdr-tech-file-gen` is a local CLI that parses user-supplied YAML and renders Markdown via Jinja2. Trust boundaries:

- **Input YAML** is assumed potentially adversarial. `safe_load` is used (no Python-object construction). Pydantic v2 validates the schema before any rendering touches the spec.
- **Jinja2 autoescape** is enabled for HTML/XML output paths; Markdown output is treated as plain text. The CLI does not execute spec-supplied template code.
- **No network calls** are made by v0.1. The bundled `data/mdr_clauses.yaml` is a static snapshot from EUR-Lex; updating it requires a code change, not a runtime fetch.

## Regulatory disclaimer (not a security issue, but load-bearing)

This tool is **not a medical device**. It generates documentation skeletons. It does not:

- Provide regulatory advice.
- Replace a Notified Body conformity assessment.
- Guarantee that the generated skeleton, once completed by the manufacturer, will satisfy any specific Notified Body's audit.

Manufacturers remain solely responsible for MDR compliance under Regulation (EU) 2017/745.

## Out-of-scope

- Denial-of-service via extremely large YAML inputs (we recommend a 10 MB input cap in your CI).
- Side-channel attacks on validation timing.
- Anything involving a hosted service surface (v0.1 is CLI-only).
