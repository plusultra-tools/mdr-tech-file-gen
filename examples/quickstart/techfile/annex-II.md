# Technical Documentation — Annex II
## SmartGlucose Predictor v1.0 (Class IIa)

**Device ID:** SGP-001
**Manufacturer:** GlucoTech GmbH
**Version:** 1.0
**Generated:** 2026-05-15T08:52:42Z by mdr-tech-file-gen v0.1.0

> **Disclaimer:** This document is a generated skeleton. All `[TODO]` placeholders
> must be completed by a qualified regulatory professional before submission to a
> Notified Body or Competent Authority. This tool does not constitute regulatory advice.
>
> **MDR reference:** Regulation (EU) 2017/745, Annex II — Technical Documentation
> (OJ L 117, 5.5.2017). Full text at: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0745

---

## §1 Device Description and Specification

### §1.1 Device description and specification (MDR Annex II §1.1)

| Field | Value |
| --- | --- |
| Device Name | SmartGlucose Predictor v1.0 |
| Device ID | SGP-001 |
| Version | 1.0 |
| Manufacturer | GlucoTech GmbH |
| Risk Class | Class IIa (MDR Annex VIII) |
| Classification Rule(s) | Rule 11 |
| Software Device (MDSW) | Yes |

#### Intended Use

Intended to predict blood glucose level trends in adults (≥18 years) with Type 1 or Type 2 diabetes mellitus, using continuous glucose monitor (CGM) readings and patient-reported meal data. The software provides predictive alerts to help the patient and their supervising healthcare professional take proactive action to avoid hyperglycaemia and hypoglycaemia. Not intended for acute hypoglycaemia management or autonomous insulin dosing decisions without HCP oversight.


#### Intended Users

- healthcare professional
- layperson (patient under HCP supervision)

#### Intended Environments

- home care
- ambulatory care
- primary care clinic

#### Contraindications

- Not for use in patients under 18 years of age (paediatric population not validated).
- Not validated for use during pregnancy.
- Not a substitute for clinical blood glucose measurement by certified laboratory methods.
- Do not use to make autonomous insulin dosing decisions without HCP consultation.

**Standards pointers for §1.1:**
- **ISO 14971:2019 §3.1** — Intended use definition *(Defines 'intended use' as a cornerstone of the risk management process.)*- **IEC 62304:2006+A1:2015 §4.3** — Software safety class assignment *(Safety class (A/B/C) must be documented based on severity of hazardous situations.)*- **IEC 62366-1:2015+A1:2020 §5.1** — Intended use and user population *(Usability engineering requires intended user, use environment, and use context specification.)*- **MDCG 2021-24 §4** — Guidance on classification of MDR devices *(MDCG guidance document on classification rules (non-binding, public).)*
---

### §1.2 Reference to previous and similar generations (MDR Annex II §1.2)

[TODO: List previous versions of this device and similar devices on the market. For each,
provide: device name, manufacturer, version, key technical differences, and reference to
comparative technical data. If this is a first-in-class device, state that explicitly and
provide market landscape data.]

**Standards pointers for §1.2:**
- **ISO 14971:2019 §4.2** — Risk management file continuity *(Risk management file should reference known risks from prior generations.)*- **MDCG 2020-6 §4** — Clinical evaluation of similar devices *(MDCG guidance on clinical evaluation (public document).)*
---

## §2 Information to be Supplied by the Manufacturer (MDR Annex II §2)

### §2.1 Labelling

[TODO: Attach labelling sample(s) and confirm compliance with MDR Art. 10(11) and Annex I §23.
Symbols must comply with ISO 15223-1:2021.]

### §2.2 Instructions for Use (IFU)

[TODO: Attach the IFU draft and confirm it covers:
- Device identification and description
- Intended purpose and indications for use
- Contraindications: see §1.1- Warnings and precautions
- Description of side effects and undesirable effects
- User instructions and step-by-step operating procedure
- Information regarding the safe disposal of the device and its packaging
- Date of issue or latest revision of the IFU]

### §2.3 UDI Assignment

[TODO: Assign UDI-DI and Basic UDI-DI via your UDI issuing entity. Register in EUDAMED
before placing the device on the market. Reference: MDR Art. 27 and MDR Annex VI Part C.]

**Standards pointers for §2:**
- **ISO 15223-1:2021 §5** — Symbols for medical devices *(Normative symbols for labels and accompanying documents.)*- **IEC 62366-1:2015+A1:2020 §5.9** — Instructions for Use (IFU) content *(Usability specification includes IFU content and format requirements.)*- **EUDAMED UDI guidance §3** — UDI-DI and UDI-PI assignment *(UDI assignment rules; refer to EUDAMED actor registration guidance.)*
---

## §3 Design and Manufacturing Information (MDR Annex II §3)

### §3.1 Design Overview

[TODO: Provide a summary of the design, including:
- System architecture (block diagram or description)
- Key design decisions and rationale
- Functional description of all major components
- Interface descriptions (hardware, software, user interfaces)]

### §3.2 Software Architecture (IEC 62304)

**IEC 62304 Software Safety Class:** B

[TODO: Attach or reference:
- Software development plan (IEC 62304:2006+A1:2015 §5.1)
- Software architecture document (IEC 62304:2006+A1:2015 §5.3)
- Software configuration management plan (IEC 62304:2006+A1:2015 §8)]

**Version Control System:** git 2.44
**Change Control SOP:** SOP-CC-001 v2.0

### §3.3 SOUP Register (IEC 62304:2006+A1:2015 §8.1.2)

| Component | Version | Purpose | Anomaly List Reviewed |
| --- | --- | --- | --- |
| numpy | 1.26.4 | Numerical array operations for glucose trend signal processing. | Yes |
| scikit-learn | 1.4.1 | Machine learning model training and inference for trend prediction. | No — TODO |
| pandas | 2.2.1 | Tabular data processing for CGM reading ingestion. | Yes |
| Flask | 3.0.3 | REST API layer for mobile-app integration. | No — TODO |


**Standards pointers for §3:**
- **ISO 13485:2016 §7.3** — Design and development process *(Design control requirements including design inputs, outputs, review, verification, validation.)*- **IEC 62304:2006+A1:2015 §5.1-5.7** — Software development lifecycle activities *(Software development planning, architecture, unit testing, integration, and release activities.)*- **IEC 62304:2006+A1:2015 §8** — Software configuration management *(Configuration management process for SOUP and software items.)*
---

## §4 General Safety and Performance Requirements (GSPR) Checklist (MDR Annex II §4, Annex I)

> Complete the GSPR checklist table below. Each row corresponds to one MDR Annex I requirement.
> For each requirement: mark applicability (Yes/No/N/A), reference the evidence document, and
> record the harmonised standard(s) applied. See `checklist.md` for the auto-derived status overview.

| Annex I Requirement | Applicable? | Evidence Document Reference | Harmonised Standard |
| --- | --- | --- | --- |
| §1 — General requirements: devices shall achieve intended performance | [TODO] | [TODO: ref] | ISO 14971:2019 §4-9 |
| §2 — Risk management: benefit shall outweigh residual risks | [TODO] | [TODO: risk mgmt file ref] | ISO 14971:2019 §5-7 |
| §3 — State of the art | [TODO] | [TODO: ref] | — |
| §4 — Precautionary measures: known and foreseeable misuse | [TODO] | [TODO: ref] | IEC 62366-1:2015 §5.4 |
| §5 — Durability and reliability | [TODO] | [TODO: ref] | — |
| §6 — Transport and storage | [TODO] | [TODO: ref] | — |
| §7 — Combination products (if applicable) | [TODO] | N/A | — |
| §8 — Performance and ergonomic design | [TODO] | [TODO: ref] | IEC 62366-1:2015 §5 |
| §9 — Chemical, physical, biological properties | N/A (software) | N/A | ISO 10993-1:2018 |
| §10 — Infection and microbial contamination | N/A (software) | N/A | — |
| §11 — Construction and environmental properties | [TODO] | [TODO: ref] | — |
| §12 — Devices with measuring function | [TODO] | [TODO: ref] | — |
| §13 — Protection against radiation | N/A (software) | N/A | — |
| §14 — Active devices (general) | Yes | [TODO: ref] | IEC 62304:2006+A1:2015 §5 |
| §15 — Active implantable devices | N/A | N/A | — |
| §16 — Connection to external energy source | [TODO] | [TODO: ref] | — |
| §17 — Software devices (SaMD/MDSW) | Yes | [TODO: software V&V ref] | IEC 62304:2006+A1:2015; MDCG 2019-11; MDCG 2019-16 |
| §18 — Active devices intended for therapy | [TODO] | [TODO: ref] | — |
| §19 — Particular requirements for active implantable devices | N/A | N/A | — |
| §20 — Protection against mechanical risks | N/A (software) | N/A | — |
| §21 — Protection against thermal risks | N/A (software) | N/A | — |
| §22 — Protection against risks from energies | [TODO] | [TODO: ref] | — |
| §23 — Information supplied by the manufacturer | Yes | See §2 above | ISO 15223-1:2021 |

**Standards pointers for §4:**
- **ISO 14971:2019 §5-7** — Risk management: hazard identification, estimation, evaluation *(Risk analysis, evaluation, and control measures mapping to GSPR §1.)*- **IEC 62366-1:2015+A1:2020 §5** — Usability engineering process *(Usability process evidence maps to GSPR §5 (use error risks).)*- **IEC 62304:2006+A1:2015 §5.1-5.8** — Software verification and validation *(V&V activities map to GSPR §17 (software for medical devices).)*- **ISO 27001:2022 §6.1** — Information security risk treatment *(Cybersecurity risk treatment for MDSW (GSPR §17.2, MDCG 2019-16).)*- **ISO 10993-1:2018 §4-6** — Biological safety evaluation framework *(Applies to hardware contact materials; N/A skeleton for pure-software devices.)*
---

## §5 Benefit-Risk Analysis and Risk Management File (MDR Annex II §5)

> Reference: MDR Art. 10(2), Annex I §1-8, ISO 14971:2019

[TODO: Attach or reference the ISO 14971:2019 risk management file. This section must demonstrate:
1. Risk management plan (ISO 14971:2019 §4.4)
2. Risk analysis — identification of characteristics related to safety (§4.3)
3. Hazard identification and estimation of associated risks (§5-6)
4. Risk evaluation and risk control measures (§7-8)
5. Evaluation of residual risks (§9)
6. Benefit-risk determination: overall residual risks acceptable in light of clinical benefits
7. Risk management review and sign-off

Risk management file reference: [TODO: Document ID and version]]

### Clinical Claims Requiring Benefit Evidence

- Predicts blood glucose trends ≥30 minutes ahead with mean absolute relative difference (MARD) ≤15% in the target population.
- Reduces time-in-hypoglycaemia by ≥20% versus standard CGM alone (clinical study reference: SGP-CL-001).

[TODO: For each claim above, attach or reference the clinical evidence substantiating
the claimed benefit used in the benefit-risk analysis.]

**Standards pointers for §5:**
- **ISO 14971:2019 §4-9** — Full risk management process *(Risk management plan, risk analysis, evaluation, control, residual risk, benefit-risk.)*- **ISO 14971:2019 Annex A** — Guidance on risk management *(Informative annex on risk management principles and terminology.)*- **MDCG 2019-11 §4** — Guidance on qualifying and classifying MDSW *(MDCG guidance on SaMD qualification (public document).)*
---

## §6 Product Verification and Validation (MDR Annex II §6)

[TODO: Provide or reference:
- Verification protocols and results (does the product meet design outputs?)
- Validation protocols and results (does the product meet user needs and intended use?)
- For SaMD: software test documentation per IEC 62304:2006+A1:2015 §5.6-5.8
- For usability: summative evaluation report per IEC 62366-1:2015 §5.10]

**Standards pointers for §6:**
- **ISO 13485:2016 §7.3.6-7.3.7** — Design verification and validation *(Design V&V records, protocols, and reports.)*- **IEC 62304:2006+A1:2015 §5.6-5.7** — Software integration testing and system testing *(Software integration test plan and results; system test records.)*- **IEC 62366-1:2015+A1:2020 §5.10** — Summative usability evaluation *(Formative and summative usability study reports.)*
### §6.1 Clinical Evaluation (MDR Annex II §6.1, MDR Art. 61)

[TODO: Attach or reference the Clinical Evaluation Report (CER). The CER must cover:
1. Identification of applicable GSPRs requiring clinical data (MDR Annex I §1, §8)
2. Clinical data sources: literature search protocol and results, clinical investigation data (if any)
3. Equivalence assessment (if claiming equivalence: technical, biological, clinical equivalence per MDCG 2020-13)
4. Clinical evaluation of safety and performance
5. Residual risks and uncertainties requiring PMCF

CER reference: [TODO: Document ID and version]]

**Standards pointers for §6.1:**
- **MDCG 2020-6 rev.2 §4-6** — Clinical evaluation report (CER) structure *(MDCG guidance on clinical evaluation methodology (public document).)*- **MDCG 2020-13 §3** — Clinical evaluation equivalence assessment *(MDCG guidance on equivalence claims (public document).)*
---

## §7 Post-Market Surveillance Documentation (see Annex III)

See `annex-III.md` for the PMS plan and PMCF plan.

---

## Appendix A: Software Lifecycle File (IEC 62304:2006+A1:2015)

**IEC 62304 Safety Class:** B

[TODO: Reference or attach:
- Software development plan (§5.1)
- Software requirements specification (§5.2)
- Software architecture document (§5.3)
- Software unit design, implementation, and unit test records (§5.4-5.5)
- Software integration test records (§5.6)
- Software system test records (§5.7)
- Software release records (§5.8)
- Problem resolution process records (§9)]

### SOUP Register Summary

| SOUP | Version | Safety-Critical Purpose | Anomaly List |
| --- | --- | --- | --- |
| numpy | 1.26.4 | Numerical array operations for glucose trend signal processing. | Reviewed |
| scikit-learn | 1.4.1 | Machine learning model training and inference for trend prediction. | [TODO: review] |
| pandas | 2.2.1 | Tabular data processing for CGM reading ingestion. | Reviewed |
| Flask | 3.0.3 | REST API layer for mobile-app integration. | [TODO: review] |

**Standards pointers:**
- **IEC 62304:2006+A1:2015 §5.1** — Software development planning *(Software development plan content requirements.)*- **IEC 62304:2006+A1:2015 §5.2** — Software requirements analysis *(Software requirements specification activities.)*- **IEC 62304:2006+A1:2015 §5.3** — Software architectural design *(Software architecture documentation requirements.)*- **IEC 62304:2006+A1:2015 §5.4-5.5** — Software detailed design and unit implementation *(Unit implementation and verification records.)*- **IEC 62304:2006+A1:2015 §8.1.2** — SOUP identification and hazard analysis *(SOUP register: name, version, anomaly list review status.)*- **MDCG 2019-16 §4** — Cybersecurity for MDSW *(MDCG guidance on cybersecurity requirements (public document).)*
---

## Appendix B: Usability Engineering File (IEC 62366-1:2015+A1:2020)

[TODO: Reference or attach:
- Intended use specification (§5.1) — see §1.1 above
- User profile and use environment specification (§5.1)
- Use-related risk analysis (§5.4)
- Formative evaluation records (§5.7-5.9)
- Summative usability evaluation protocol and report (§5.10)]

**Standards pointers:**
- **IEC 62366-1:2015+A1:2020 §5.1-5.4** — Use specification and known use problems *(Intended use, user profile, use environment, use-related hazard analysis.)*- **IEC 62366-1:2015+A1:2020 §5.7-5.9** — Formative evaluation and IFU review *(Formative evaluation records and IFU content requirements.)*- **IEC 62366-1:2015+A1:2020 §5.10** — Summative evaluation *(Summative usability evaluation protocol and results.)*
---

*End of Annex II Technical Documentation skeleton for SmartGlucose Predictor v1.0.*
*Generated by mdr-tech-file-gen v0.1.0 on 2026-05-15T08:52:42Z.*
*Review and complete all [TODO] items before Notified Body submission.*
