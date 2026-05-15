"""Tests for mdr_techfile.spec — DeviceSpec schema validation."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from mdr_techfile.spec import (
    DeviceSpec,
    Iec62304SafetyClass,
    RiskClass,
    load_spec,
)


def _write_yaml(tmp_path: Path, data: dict) -> Path:  # type: ignore[type-arg]
    p = tmp_path / "spec.yaml"
    p.write_text(yaml.dump(data), encoding="utf-8")
    return p


class TestDeviceSpecValidation:
    def test_valid_software_device(self, samd_class_iia: DeviceSpec) -> None:
        assert samd_class_iia.name == "SmartGlucose Predictor v1.0"
        assert samd_class_iia.risk_class == RiskClass.IIA
        assert samd_class_iia.software is True
        assert samd_class_iia.lifecycle is not None
        assert samd_class_iia.lifecycle.iec62304_safety_class == Iec62304SafetyClass.B

    def test_valid_hardware_device(self, hardware_class_i: DeviceSpec) -> None:
        assert hardware_class_i.software is False
        assert hardware_class_i.lifecycle is None
        assert hardware_class_i.risk_class == RiskClass.I

    def test_software_requires_lifecycle(self) -> None:
        with pytest.raises(Exception):
            DeviceSpec(
                id="BAD-001",
                name="Bad Device",
                manufacturer="Acme",
                intended_use="Test.",
                intended_users=["layperson"],
                intended_environments=["home"],
                risk_class=RiskClass.IIA,
                classification_rules_applied=["Rule 11"],
                software=True,
                lifecycle=None,  # must fail
            )

    def test_risk_class_enum_values(self) -> None:
        for val, expected in [
            ("I", RiskClass.I),
            ("IIa", RiskClass.IIA),
            ("IIb", RiskClass.IIB),
            ("III", RiskClass.III),
        ]:
            spec = DeviceSpec(
                id="X",
                name="X",
                manufacturer="X",
                intended_use="X",
                intended_users=["healthcare professional"],
                intended_environments=["hospital"],
                risk_class=val,  # type: ignore[arg-type]
                classification_rules_applied=["Rule 1"],
                software=False,
            )
            assert spec.risk_class == expected

    def test_invalid_risk_class_raises(self) -> None:
        with pytest.raises(Exception):
            DeviceSpec(
                id="X",
                name="X",
                manufacturer="X",
                intended_use="X",
                intended_users=["healthcare professional"],
                intended_environments=["hospital"],
                risk_class="IV",  # type: ignore[arg-type]
                classification_rules_applied=["Rule 1"],
                software=False,
            )

    def test_soup_register_parsed(self, samd_class_iia: DeviceSpec) -> None:
        assert len(samd_class_iia.soup_register) == 2
        assert samd_class_iia.soup_register[0].name == "numpy"
        assert samd_class_iia.soup_register[0].anomaly_list_reviewed is True
        assert samd_class_iia.soup_register[1].anomaly_list_reviewed is False

    def test_optional_fields_default(self) -> None:
        spec = DeviceSpec(
            id="MIN-001",
            name="Minimal Device",
            manufacturer="Minimal Co.",
            intended_use="Test use.",
            intended_users=["healthcare professional"],
            intended_environments=["hospital"],
            risk_class=RiskClass.I,
            classification_rules_applied=["Rule 1"],
            software=False,
        )
        assert spec.contraindications == []
        assert spec.clinical_claims == []
        assert spec.soup_register == []
        assert spec.notified_body is None
        assert spec.udi_di is None


class TestLoadSpec:
    def test_load_valid_yaml(self, tmp_path: Path, samd_class_iia: DeviceSpec) -> None:
        # model_dump(mode='json') serializes enums as their string values
        import json
        data = json.loads(samd_class_iia.model_dump_json())
        p = _write_yaml(tmp_path, data)
        loaded = load_spec(p)
        assert loaded.id == samd_class_iia.id
        assert loaded.name == samd_class_iia.name
        assert loaded.risk_class == samd_class_iia.risk_class

    def test_load_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_spec(tmp_path / "nonexistent.yaml")

    def test_load_non_mapping_yaml(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text("- item1\n- item2\n", encoding="utf-8")
        with pytest.raises(ValueError, match="must be a YAML mapping"):
            load_spec(p)

    def test_load_missing_required_field(self, tmp_path: Path) -> None:
        data = {
            "id": "X",
            # name is missing
            "manufacturer": "X",
            "intended_use": "X",
            "intended_users": ["professional"],
            "intended_environments": ["hospital"],
            "risk_class": "I",
            "classification_rules_applied": ["Rule 1"],
            "software": False,
        }
        p = _write_yaml(tmp_path, data)
        with pytest.raises(Exception):
            load_spec(p)
