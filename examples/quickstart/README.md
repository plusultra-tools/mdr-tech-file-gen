# Quickstart Example — SmartGlucose Predictor v1.0

This example walks you through generating a complete MDR technical file skeleton
for a fictitious Class IIa SaMD device using `mdr-techfile`.

## Prerequisites

```bash
pip install mdr-tech-file-gen
```

Or from source (from the repo root):

```bash
pip install -e .
```

## 1. Inspect the device spec

Open `device-spec.yaml`. It describes:
- A Class IIa SaMD (classified under MDR Annex VIII Rule 11)
- IEC 62304 Software Safety Class B
- 4 SOUP components (numpy, scikit-learn, pandas, Flask)
- 2 clinical claims requiring substantiation in the CER

## 2. Validate the spec

```bash
mdr-techfile validate --spec examples/quickstart/device-spec.yaml
```

Expected output:
```
VALID: examples/quickstart/device-spec.yaml
  Device: SmartGlucose Predictor v1.0 (Class IIa)
  Manufacturer: GlucoTech GmbH
  Software: Yes
  IEC 62304 safety class: B
  SOUP entries: 4
  Clinical claims: 2
```

## 3. Scaffold the full technical file

```bash
mdr-techfile scaffold \
  --spec examples/quickstart/device-spec.yaml \
  --annex both \
  --out examples/quickstart/techfile/
```

This produces:

```
examples/quickstart/techfile/
├── annex-II.md          # MDR Annex II Technical Documentation skeleton
├── annex-III.md         # MDR Annex III PMS Documentation skeleton
├── checklist.md         # Annex II checklist with auto-derived status
├── standards-matrix.md  # ISO/IEC standards citation matrix
└── audit.sha256         # SHA-256 hash chain of all generated files
```

## 4. Review the checklist

Open `techfile/checklist.md`. Items marked `✅ filled` were pre-populated from
the device spec. Items marked `⬜ TODO` require manual completion before Notified
Body submission.

## 5. Disable standards pointers (optional)

If you want a clean skeleton without the ISO/IEC citation tables:

```bash
mdr-techfile scaffold \
  --spec examples/quickstart/device-spec.yaml \
  --no-standards-pointers \
  --out examples/quickstart/techfile-clean/
```

## 6. Get the citation manifest

```bash
mdr-techfile manifest \
  --spec examples/quickstart/device-spec.yaml \
  --out examples/quickstart/manifest.json
```

The manifest JSON maps each Annex II section to the relevant ISO/IEC standard
clause pointers. Use it to audit the provenance of every generated section.

## 7. Next steps

- Replace all `[TODO]` placeholders in the generated Markdown files.
- Attach or reference your risk management file (ISO 14971:2019) in Annex II §5.
- Complete the GSPR checklist table in Annex II §4.
- Attach your Clinical Evaluation Report (CER) draft in Annex II §6.1.
- Commit the YAML spec and generated skeleton to your QMS git repository.
- Regenerate when the spec changes: `mdr-techfile scaffold --spec device-spec.yaml ...`

## What this tool does NOT do

- Write your clinical evaluation report.
- Complete your risk management file.
- Substitute for advice from a qualified regulatory professional.
- Replace Notified Body conformity assessment (mandatory for Class IIa).
