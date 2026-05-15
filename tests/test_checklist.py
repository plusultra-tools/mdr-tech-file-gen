"""Tests for mdr_techfile.checklist — Annex II checklist generator."""
from __future__ import annotations

from mdr_techfile.checklist import (
    ChecklistItem,
    ChecklistStatus,
    build_checklist,
    checklist_to_markdown,
)
from mdr_techfile.spec import DeviceSpec, Iec62304SafetyClass, RiskClass, SoftwareLifecycle


class TestBuildChecklist:
    def test_returns_list(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        assert isinstance(items, list)
        assert len(items) > 0
        assert all(isinstance(i, ChecklistItem) for i in items)

    def test_section_1_1_filled_for_complete_spec(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        s11 = next(i for i in items if i.section == "Annex II §1.1")
        assert s11.status == ChecklistStatus.FILLED

    def test_software_lifecycle_filled_for_samd(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        lc = next((i for i in items if i.section == "IEC 62304 Software Lifecycle"), None)
        assert lc is not None
        assert lc.status == ChecklistStatus.FILLED

    def test_software_lifecycle_na_for_hardware(self, hardware_class_i: DeviceSpec) -> None:
        items = build_checklist(hardware_class_i)
        lc = next((i for i in items if i.section == "IEC 62304 Software Lifecycle"), None)
        assert lc is not None
        assert lc.status == ChecklistStatus.NA

    def test_pmcf_na_for_class_i(self, hardware_class_i: DeviceSpec) -> None:
        items = build_checklist(hardware_class_i)
        pmcf = next((i for i in items if "PMCF" in i.title), None)
        assert pmcf is not None
        assert pmcf.status == ChecklistStatus.NA

    def test_pmcf_todo_for_class_iia(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        pmcf = next((i for i in items if "PMCF" in i.title), None)
        assert pmcf is not None
        assert pmcf.status == ChecklistStatus.TODO

    def test_notified_body_item_for_class_iii(self, samd_class_iii: DeviceSpec) -> None:
        items = build_checklist(samd_class_iii)
        nb = next((i for i in items if "Notified Body" in i.title), None)
        assert nb is not None
        assert nb.status == ChecklistStatus.FILLED  # notified_body is set

    def test_notified_body_todo_when_unset(self) -> None:
        spec = DeviceSpec(
            id="X",
            name="X",
            manufacturer="X",
            intended_use="X",
            intended_users=["healthcare professional"],
            intended_environments=["hospital"],
            risk_class=RiskClass.III,
            classification_rules_applied=["Rule 11"],
            software=True,
            lifecycle=SoftwareLifecycle(iec62304_safety_class=Iec62304SafetyClass.C),
            notified_body=None,
        )
        items = build_checklist(spec)
        nb = next((i for i in items if "Notified Body" in i.title), None)
        assert nb is not None
        assert nb.status == ChecklistStatus.TODO

    def test_no_nb_item_for_class_i(self, hardware_class_i: DeviceSpec) -> None:
        items = build_checklist(hardware_class_i)
        nb_items = [i for i in items if "Notified Body" in i.title]
        assert len(nb_items) == 0

    def test_clinical_claims_status(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        ce = next(i for i in items if "Clinical evaluation" in i.title)
        assert ce.status == ChecklistStatus.FILLED

    def test_clinical_eval_todo_without_claims(self, hardware_class_i: DeviceSpec) -> None:
        items = build_checklist(hardware_class_i)
        ce = next(i for i in items if "Clinical evaluation" in i.title)
        assert ce.status == ChecklistStatus.TODO


class TestChecklistToMarkdown:
    def test_markdown_contains_table(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        md = checklist_to_markdown(items, samd_class_iia)
        assert "| MDR Section |" in md
        assert "| --- |" in md

    def test_markdown_contains_device_name(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        md = checklist_to_markdown(items, samd_class_iia)
        assert samd_class_iia.name in md

    def test_markdown_contains_status_symbols(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        md = checklist_to_markdown(items, samd_class_iia)
        assert "filled" in md
        assert "TODO" in md

    def test_markdown_returns_string(self, samd_class_iia: DeviceSpec) -> None:
        items = build_checklist(samd_class_iia)
        md = checklist_to_markdown(items, samd_class_iia)
        assert isinstance(md, str)
        assert len(md) > 100
