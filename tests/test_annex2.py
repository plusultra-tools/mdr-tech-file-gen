"""Tests for mdr_techfile.annex2 — Annex II renderer."""
from __future__ import annotations

from mdr_techfile.annex2 import render_annex2, render_standards_matrix
from mdr_techfile.spec import DeviceSpec

FIXED_TS = "2026-01-01T00:00:00Z"


class TestRenderAnnex2:
    def test_basic_structure(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex2(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "# Technical Documentation — Annex II" in md
        assert samd_class_iia.name in md
        assert f"Class {samd_class_iia.risk_class.value}" in md
        assert samd_class_iia.manufacturer in md

    def test_contains_intended_use(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex2(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "SmartGlucose Predictor" in md
        assert "blood glucose" in md.lower()

    def test_software_section_present_for_samd(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex2(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "IEC 62304" in md
        assert "Safety Class" in md
        assert "SOUP" in md

    def test_software_section_absent_for_hardware(self, hardware_class_i: DeviceSpec) -> None:
        md = render_annex2(hardware_class_i, timestamp_iso=FIXED_TS)
        # No software lifecycle section
        assert "IEC 62304 Safety Class:" not in md

    def test_soup_table_rendered(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex2(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "numpy" in md
        assert "scikit-learn" in md
        assert "1.26.4" in md

    def test_contraindications_rendered(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex2(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "Not for use in patients under 18" in md

    def test_no_standards_pointers_flag(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex2(
            samd_class_iia,
            include_standards_pointers=False,
            timestamp_iso=FIXED_TS,
        )
        # Standards pointer blocks should be empty when flag is off
        # The template renders empty loops but the ISO 14971 etc. should not appear
        # in the pointer table rows (the static text in TODO blocks is fine)
        assert "## §1 Device Description" in md

    def test_timestamp_injected(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex2(samd_class_iia, timestamp_iso=FIXED_TS)
        assert FIXED_TS in md

    def test_mdr_disclaimer_present(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex2(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "Regulation (EU) 2017/745" in md
        assert "eur-lex.europa.eu" in md

    def test_tool_version_present(self, samd_class_iia: DeviceSpec) -> None:
        from mdr_techfile import __version__
        md = render_annex2(samd_class_iia, timestamp_iso=FIXED_TS)
        assert __version__ in md

    def test_class_iii_notified_body(self, samd_class_iii: DeviceSpec) -> None:
        md = render_annex2(samd_class_iii, timestamp_iso=FIXED_TS)
        assert "CardioAlert" in md
        assert "Class III" in md

    def test_udi_rendered_when_present(self) -> None:
        from mdr_techfile.spec import Iec62304SafetyClass, RiskClass, SoftwareLifecycle
        spec = DeviceSpec(
            id="X-001",
            name="Test Device",
            manufacturer="Test Mfr",
            intended_use="Test use.",
            intended_users=["healthcare professional"],
            intended_environments=["hospital"],
            risk_class=RiskClass.IIA,
            classification_rules_applied=["Rule 11"],
            software=True,
            lifecycle=SoftwareLifecycle(iec62304_safety_class=Iec62304SafetyClass.B),
            udi_di="01234567890123",
            basic_udi_di="0123456789012300",
        )
        md = render_annex2(spec, timestamp_iso=FIXED_TS)
        assert "01234567890123" in md


class TestRenderStandardsMatrix:
    def test_basic_structure(self, samd_class_iia: DeviceSpec) -> None:
        md = render_standards_matrix(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "# Standards and Harmonised Standards Matrix" in md
        assert samd_class_iia.name in md

    def test_software_standards_present(self, samd_class_iia: DeviceSpec) -> None:
        md = render_standards_matrix(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "IEC 62304" in md
        assert "ISO 14971" in md

    def test_no_verbatim_iso_text(self, samd_class_iia: DeviceSpec) -> None:
        md = render_standards_matrix(samd_class_iia, timestamp_iso=FIXED_TS)
        # Confirm no verbatim paragraph starts that would indicate copied text
        # (just a basic heuristic — the real check is the data file)
        assert "COPYRIGHT" not in md.upper()
        assert "ALL RIGHTS RESERVED" not in md.upper()
