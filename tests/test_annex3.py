"""Tests for mdr_techfile.annex3 — Annex III renderer."""
from __future__ import annotations

from mdr_techfile.annex3 import render_annex3
from mdr_techfile.spec import DeviceSpec

FIXED_TS = "2026-01-01T00:00:00Z"


class TestRenderAnnex3:
    def test_basic_structure(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex3(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "# Technical Documentation — Annex III" in md
        assert "Post-Market Surveillance" in md
        assert samd_class_iia.name in md

    def test_psur_section_for_class_iia(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex3(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "PSUR" in md or "Periodic Safety Update" in md
        assert "Art. 86" in md

    def test_sspr_for_class_i(self, hardware_class_i: DeviceSpec) -> None:
        md = render_annex3(hardware_class_i, timestamp_iso=FIXED_TS)
        assert "Art. 85" in md or "SSPR" in md

    def test_pmcf_section_present_for_class_iia(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex3(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "PMCF" in md
        assert "Annex XIV" in md

    def test_pmcf_na_note_for_class_i(self, hardware_class_i: DeviceSpec) -> None:
        md = render_annex3(hardware_class_i, timestamp_iso=FIXED_TS)
        # For Class I the template explains PMCF is not mandatory
        assert "PMCF" in md  # the heading is still there
        assert "not mandatory" in md

    def test_class_iii_psur_annual(self, samd_class_iii: DeviceSpec) -> None:
        md = render_annex3(samd_class_iii, timestamp_iso=FIXED_TS)
        assert "Annually" in md or "annually" in md

    def test_clinical_claims_in_pmcf(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex3(samd_class_iia, timestamp_iso=FIXED_TS)
        # The clinical claim should appear in the PMCF objectives
        assert "blood glucose" in md.lower() or "MARD" in md

    def test_no_standards_pointers_flag(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex3(
            samd_class_iia,
            include_standards_pointers=False,
            timestamp_iso=FIXED_TS,
        )
        assert "Post-Market Surveillance" in md

    def test_mdr_disclaimer_present(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex3(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "Regulation (EU) 2017/745" in md

    def test_vigilance_section_present(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex3(samd_class_iia, timestamp_iso=FIXED_TS)
        assert "Vigilance" in md or "Art. 87" in md

    def test_timestamp_injected(self, samd_class_iia: DeviceSpec) -> None:
        md = render_annex3(samd_class_iia, timestamp_iso=FIXED_TS)
        assert FIXED_TS in md
