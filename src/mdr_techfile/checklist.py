"""Annex II checklist generator.

Derives the status of each Annex II checklist item from the device spec.
Status values:
- 'filled'  — DeviceSpec provides enough data to generate non-empty content.
- 'todo'    — Section is applicable but requires manual completion.
- 'na'      — Section is not applicable to this device class.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from mdr_techfile.spec import DeviceSpec, RiskClass


class ChecklistStatus(str, Enum):
    """Status of a generated checklist item."""

    FILLED = "filled"
    TODO = "todo"
    NA = "na"


@dataclass(frozen=True)
class ChecklistItem:
    """One checklist line item."""

    section: str
    """MDR reference, e.g. 'Annex II §1.1'."""
    title: str
    """Human-readable section title."""
    status: ChecklistStatus
    rationale: str
    """One-line explanation of why this status was assigned."""


def _risk_level(spec: DeviceSpec) -> str:
    """Return 'low', 'medium', or 'high' based on risk class."""
    if spec.risk_class == RiskClass.I:
        return "low"
    if spec.risk_class in (RiskClass.IIA, RiskClass.IIB):
        return "medium"
    return "high"


def build_checklist(spec: DeviceSpec) -> list[ChecklistItem]:
    """Build an Annex II checklist from a validated device spec.

    Args:
        spec: A validated :class:`~mdr_techfile.spec.DeviceSpec` instance.

    Returns:
        Ordered list of :class:`ChecklistItem` covering all Annex II §1-7 sections.
    """
    high = _risk_level(spec) == "high"
    software = spec.software

    items: list[ChecklistItem] = []

    # §1.1 Device description and specification
    if spec.name and spec.intended_use and spec.risk_class:
        items.append(ChecklistItem(
            section="Annex II §1.1",
            title="Device description and specification",
            status=ChecklistStatus.FILLED,
            rationale=(
                f"name={spec.name!r}, risk_class={spec.risk_class.value}, "
                "intended_use provided."
            ),
        ))
    else:
        items.append(ChecklistItem(
            section="Annex II §1.1",
            title="Device description and specification",
            status=ChecklistStatus.TODO,
            rationale="name, risk_class, or intended_use missing from spec.",
        ))

    # §1.2 Previous and similar generations
    items.append(ChecklistItem(
        section="Annex II §1.2",
        title="Reference to previous and similar generations of the device",
        status=ChecklistStatus.TODO,
        rationale=(
            "Manual: list predecessor device versions and comparative technical "
            "characteristics. N/A for first-in-class; state explicitly."
        ),
    ))

    # §2 Information to be supplied by manufacturer
    if spec.udi_di or spec.basic_udi_di:
        items.append(ChecklistItem(
            section="Annex II §2",
            title="Information to be supplied by the manufacturer (labelling, IFU, UDI)",
            status=ChecklistStatus.FILLED,
            rationale=(
                f"UDI-DI={spec.udi_di!r} / basic-UDI-DI={spec.basic_udi_di!r} provided."
            ),
        ))
    else:
        items.append(ChecklistItem(
            section="Annex II §2",
            title="Information to be supplied by the manufacturer (labelling, IFU, UDI)",
            status=ChecklistStatus.TODO,
            rationale=(
                "udi_di and basic_udi_di not yet assigned. "
                "Register in EUDAMED before submission."
            ),
        ))

    # §3 Design and manufacturing information
    if software and spec.lifecycle:
        items.append(ChecklistItem(
            section="Annex II §3",
            title="Design and manufacturing information",
            status=ChecklistStatus.FILLED,
            rationale=(
                f"software=True, IEC 62304 safety class "
                f"{spec.lifecycle.iec62304_safety_class.value} declared."
            ),
        ))
    elif not software:
        items.append(ChecklistItem(
            section="Annex II §3",
            title="Design and manufacturing information",
            status=ChecklistStatus.TODO,
            rationale=(
                "Hardware device: attach design drawings, manufacturing process "
                "description, and quality system certificates."
            ),
        ))
    else:
        items.append(ChecklistItem(
            section="Annex II §3",
            title="Design and manufacturing information",
            status=ChecklistStatus.TODO,
            rationale="software=True but lifecycle block missing; assign IEC 62304 safety class.",
        ))

    # §4 GSPR checklist
    items.append(ChecklistItem(
        section="Annex II §4",
        title="General Safety and Performance Requirements (GSPR) checklist",
        status=ChecklistStatus.TODO,
        rationale=(
            "Manual: complete Annex I §1-23 GSPR table, citing evidence for each "
            "applicable requirement."
        ),
    ))

    # §5 Benefit-risk analysis
    items.append(ChecklistItem(
        section="Annex II §5",
        title="Benefit-risk analysis and risk management file",
        status=ChecklistStatus.TODO,
        rationale=(
            "Manual: attach ISO 14971:2019 risk management file reference. "
            "Pointer to risk management plan and residual risk evaluation required."
        ),
    ))

    # §6 Product verification and validation
    items.append(ChecklistItem(
        section="Annex II §6",
        title="Product verification and validation",
        status=ChecklistStatus.TODO,
        rationale=(
            "Manual: attach V&V protocols and test reports. "
            "IEC 62304 safety class determines test rigour required."
        ),
    ))

    # §6.1 Clinical evaluation
    if spec.clinical_claims:
        items.append(ChecklistItem(
            section="Annex II §6.1",
            title="Clinical evaluation",
            status=ChecklistStatus.FILLED,
            rationale=(
                f"{len(spec.clinical_claims)} clinical claim(s) declared; "
                "each must be substantiated in the Clinical Evaluation Report."
            ),
        ))
    else:
        items.append(ChecklistItem(
            section="Annex II §6.1",
            title="Clinical evaluation",
            status=ChecklistStatus.TODO,
            rationale=(
                "No clinical claims declared in spec. "
                "Clinical evaluation is still mandatory per MDR Art. 61; "
                "state clinical claims or justify equivalence."
            ),
        ))

    # §7 Post-market surveillance plan (Annex III)
    items.append(ChecklistItem(
        section="Annex III §1",
        title="Post-market surveillance plan",
        status=ChecklistStatus.TODO,
        rationale=(
            "Manual: complete PMS plan per MDCG 2022-21. "
            + (
                "PSUR required for Class IIa/IIb/III per MDR Art. 86."
                if spec.risk_class != RiskClass.I
                else (
                    "Post-market surveillance report for Class I per MDR Art. 85: "
                    "'a post-market surveillance report which summarises the results "
                    "and conclusions of the analyses of the post-market surveillance "
                    "data', updated when necessary and made available to authorities "
                    "on request."
                )
            )
        ),
    ))

    # §7.2 PMCF plan
    if spec.risk_class != RiskClass.I:
        items.append(ChecklistItem(
            section="Annex III §2",
            title="Post-market clinical follow-up (PMCF) plan",
            status=ChecklistStatus.TODO,
            rationale=(
                f"Class {spec.risk_class.value}: PMCF plan required per MDR Annex XIV "
                "Part B unless PMCF deemed unnecessary with justification."
            ),
        ))
    else:
        items.append(ChecklistItem(
            section="Annex III §2",
            title="Post-market clinical follow-up (PMCF) plan",
            status=ChecklistStatus.NA,
            rationale="Class I device: PMCF not mandatory unless new or modified device.",
        ))

    # Software lifecycle file (IEC 62304)
    if software and spec.lifecycle:
        items.append(ChecklistItem(
            section="IEC 62304 Software Lifecycle",
            title="Software lifecycle file",
            status=ChecklistStatus.FILLED,
            rationale=(
                f"IEC 62304 safety class {spec.lifecycle.iec62304_safety_class.value} declared. "
                f"SOUP register: {len(spec.soup_register)} entries."
            ),
        ))
    elif software:
        items.append(ChecklistItem(
            section="IEC 62304 Software Lifecycle",
            title="Software lifecycle file",
            status=ChecklistStatus.TODO,
            rationale=(
                "software=True but lifecycle block missing; "
                "complete IEC 62304 safety class assignment."
            ),
        ))
    else:
        items.append(ChecklistItem(
            section="IEC 62304 Software Lifecycle",
            title="Software lifecycle file",
            status=ChecklistStatus.NA,
            rationale="software=False; IEC 62304 lifecycle file not required.",
        ))

    # Usability engineering file (IEC 62366)
    if spec.intended_users and spec.intended_environments:
        items.append(ChecklistItem(
            section="IEC 62366 Usability",
            title="Usability engineering file",
            status=ChecklistStatus.FILLED,
            rationale=(
                f"{len(spec.intended_users)} intended user category(ies) and "
                f"{len(spec.intended_environments)} intended environment(s) declared."
            ),
        ))
    else:
        items.append(ChecklistItem(
            section="IEC 62366 Usability",
            title="Usability engineering file",
            status=ChecklistStatus.TODO,
            rationale=(
                "intended_users or intended_environments not fully specified. "
                "Required for IEC 62366-1:2015 use specification."
            ),
        ))

    # Class IIb/III: Notified Body info
    if high:
        if spec.notified_body:
            items.append(ChecklistItem(
                section="MDR Art. 52",
                title="Notified Body conformity assessment",
                status=ChecklistStatus.FILLED,
                rationale=f"Notified Body declared: {spec.notified_body!r}.",
            ))
        else:
            items.append(ChecklistItem(
                section="MDR Art. 52",
                title="Notified Body conformity assessment",
                status=ChecklistStatus.TODO,
                rationale=(
                    f"Class {spec.risk_class.value} requires Notified Body assessment "
                    "per MDR Art. 52. Assign NB before submission."
                ),
            ))

    return items


def checklist_to_markdown(items: list[ChecklistItem], spec: DeviceSpec) -> str:
    """Render checklist items as a Markdown table.

    Args:
        items: Checklist items from :func:`build_checklist`.
        spec: Device spec for header context.

    Returns:
        Markdown string ready to write to ``checklist.md``.
    """
    status_symbol = {
        ChecklistStatus.FILLED: "✅ filled",
        ChecklistStatus.TODO: "⬜ TODO",
        ChecklistStatus.NA: "N/A",
    }
    lines: list[str] = [
        f"# Annex II Checklist — {spec.name} (Class {spec.risk_class.value})",
        "",
        f"**Device ID:** {spec.id}  ",
        f"**Manufacturer:** {spec.manufacturer}  ",
        f"**Version:** {spec.version}  ",
        "",
        "> Auto-generated by mdr-tech-file-gen. Review each item and complete all TODO entries "
        "before Notified Body submission.",
        "",
        "| MDR Section | Title | Status | Rationale |",
        "| --- | --- | --- | --- |",
    ]
    for item in items:
        sym = status_symbol[item.status]
        # Escape pipe characters in rationale
        rationale = item.rationale.replace("|", "\\|")
        lines.append(f"| {item.section} | {item.title} | {sym} | {rationale} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "*Legend: ✅ filled = spec provides enough data to pre-populate the section; "
        "⬜ TODO = manufacturer must complete manually; N/A = not applicable to this device.*"
    )
    lines.append("")
    return "\n".join(lines)
