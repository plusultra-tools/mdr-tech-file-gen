"""Tests for mdr_techfile.cli — CLI entrypoint."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from mdr_techfile.cli import main


def _minimal_spec_data() -> dict:  # type: ignore[type-arg]
    return {
        "id": "SGP-001",
        "name": "SmartGlucose Predictor v1.0",
        "manufacturer": "GlucoTech GmbH",
        "version": "1.0",
        "intended_use": (
            "Predict blood glucose trends in adults with diabetes. "
            "For use by patients under HCP supervision."
        ),
        "intended_users": ["healthcare professional", "layperson"],
        "intended_environments": ["home care", "ambulatory care"],
        "risk_class": "IIa",
        "classification_rules_applied": ["Rule 11"],
        "software": True,
        "lifecycle": {
            "iec62304_safety_class": "B",
            "version_control_system": "git 2.x",
        },
        "soup_register": [
            {
                "name": "numpy",
                "version": "1.26.4",
                "purpose": "Numerical computation.",
                "anomaly_list_reviewed": True,
            }
        ],
        "contraindications": ["Not for use under 18."],
        "clinical_claims": ["Predicts glucose trends with MARD ≤15%."],
        "notified_body": "TÜV SÜD",
    }


def _write_spec(tmp_path: Path, data: dict) -> Path:  # type: ignore[type-arg]
    p = tmp_path / "device.yaml"
    p.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")
    return p


class TestValidateCommand:
    def test_valid_spec_exits_0(self, tmp_path: Path) -> None:
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        rc = main(["validate", "--spec", str(spec_path)])
        assert rc == 0

    def test_missing_file_exits_1(self, tmp_path: Path) -> None:
        rc = main(["validate", "--spec", str(tmp_path / "missing.yaml")])
        assert rc == 1

    def test_invalid_spec_exits_1(self, tmp_path: Path) -> None:
        data = _minimal_spec_data()
        del data["name"]
        spec_path = _write_spec(tmp_path, data)
        rc = main(["validate", "--spec", str(spec_path)])
        assert rc == 1


class TestScaffoldCommand:
    def test_scaffold_both_creates_files(self, tmp_path: Path) -> None:
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        out_dir = tmp_path / "techfile"
        rc = main([
            "scaffold",
            "--spec", str(spec_path),
            "--annex", "both",
            "--out", str(out_dir),
        ])
        assert rc == 0
        assert (out_dir / "annex-II.md").exists()
        assert (out_dir / "annex-III.md").exists()
        assert (out_dir / "checklist.md").exists()
        assert (out_dir / "standards-matrix.md").exists()
        assert (out_dir / "audit.sha256").exists()

    def test_scaffold_annex_ii_only(self, tmp_path: Path) -> None:
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        out_dir = tmp_path / "ii-only"
        rc = main([
            "scaffold",
            "--spec", str(spec_path),
            "--annex", "II",
            "--out", str(out_dir),
        ])
        assert rc == 0
        assert (out_dir / "annex-II.md").exists()
        assert not (out_dir / "annex-III.md").exists()

    def test_scaffold_annex_iii_only(self, tmp_path: Path) -> None:
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        out_dir = tmp_path / "iii-only"
        rc = main([
            "scaffold",
            "--spec", str(spec_path),
            "--annex", "III",
            "--out", str(out_dir),
        ])
        assert rc == 0
        assert (out_dir / "annex-III.md").exists()
        assert not (out_dir / "annex-II.md").exists()

    def test_scaffold_no_standards_pointers(self, tmp_path: Path) -> None:
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        out_dir = tmp_path / "no-ptrs"
        rc = main([
            "scaffold",
            "--spec", str(spec_path),
            "--no-standards-pointers",
            "--out", str(out_dir),
        ])
        assert rc == 0
        assert (out_dir / "annex-II.md").exists()
        # standards-matrix.md should NOT be written without pointers
        assert not (out_dir / "standards-matrix.md").exists()

    def test_scaffold_missing_spec_exits_1(self, tmp_path: Path) -> None:
        rc = main([
            "scaffold",
            "--spec", str(tmp_path / "missing.yaml"),
            "--out", str(tmp_path / "out"),
        ])
        assert rc == 1

    def test_annex2_contains_device_name(self, tmp_path: Path) -> None:
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        out_dir = tmp_path / "out"
        main(["scaffold", "--spec", str(spec_path), "--annex", "II", "--out", str(out_dir)])
        content = (out_dir / "annex-II.md").read_text(encoding="utf-8")
        assert "SmartGlucose Predictor" in content

    def test_audit_chain_hashes_match(self, tmp_path: Path) -> None:
        import hashlib
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        out_dir = tmp_path / "out"
        main(["scaffold", "--spec", str(spec_path), "--out", str(out_dir)])
        audit_text = (out_dir / "audit.sha256").read_text(encoding="utf-8")
        for line in audit_text.splitlines():
            if not line.strip():
                continue
            digest, rel_name = line.split("  ", 1)
            file_path = out_dir / rel_name.strip()
            if file_path.exists():
                actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
                assert actual == digest, f"Hash mismatch for {rel_name}"


class TestManifestCommand:
    def test_manifest_to_stdout(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        rc = main(["manifest", "--spec", str(spec_path)])
        assert rc == 0
        captured = capsys.readouterr()
        manifest = json.loads(captured.out)
        assert manifest["device"] == "SmartGlucose Predictor v1.0"
        assert manifest["risk_class"] == "IIa"
        assert isinstance(manifest["sections"], list)
        assert len(manifest["sections"]) > 0

    def test_manifest_to_file(self, tmp_path: Path) -> None:
        spec_path = _write_spec(tmp_path, _minimal_spec_data())
        out_path = tmp_path / "manifest.json"
        rc = main(["manifest", "--spec", str(spec_path), "--out", str(out_path)])
        assert rc == 0
        assert out_path.exists()
        data = json.loads(out_path.read_text(encoding="utf-8"))
        assert "sections" in data

    def test_manifest_missing_spec_exits_1(self, tmp_path: Path) -> None:
        rc = main(["manifest", "--spec", str(tmp_path / "missing.yaml")])
        assert rc == 1
