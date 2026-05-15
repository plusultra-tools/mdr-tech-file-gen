"""Device specification schema.

Pydantic v2 model for the ``device.yaml`` input file. Validates the device
identity, risk classification, software lifecycle data, intended-use context,
and optional SOUP register entries required to render the technical file.
"""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise ImportError("PyYAML is required: pip install pyyaml") from exc

from pydantic import BaseModel, Field, field_validator


class RiskClass(str, Enum):
    """MDR Annex VIII device risk classification."""

    I = "I"  # noqa: E741
    IIA = "IIa"
    IIB = "IIb"
    III = "III"


class Iec62304SafetyClass(str, Enum):
    """IEC 62304:2006+A1:2015 software safety class (§4.3)."""

    A = "A"
    B = "B"
    C = "C"


class SoftwareLifecycle(BaseModel):
    """IEC 62304 lifecycle metadata block."""

    iec62304_safety_class: Iec62304SafetyClass = Field(
        description="Software safety class per IEC 62304:2006+A1:2015 §4.3."
    )
    version_control_system: str | None = Field(
        default=None,
        description="VCS in use (e.g. 'git 2.x', 'SVN'). Informative only.",
    )
    change_control_sop: str | None = Field(
        default=None,
        description="Reference to the change-control SOP document ID.",
    )


class SoupEntry(BaseModel):
    """SOUP (Software of Unknown Provenance) register entry per IEC 62304 §8.1.2."""

    name: str = Field(description="SOUP component name.")
    version: str = Field(description="Exact version string.")
    purpose: str = Field(description="Functional purpose in the device software.")
    anomaly_list_reviewed: bool = Field(
        default=False,
        description="Whether known anomaly list has been reviewed (IEC 62304 §8.1.2).",
    )


class DeviceSpec(BaseModel):
    """
    Top-level device specification.

    Maps to the ``device.yaml`` file supplied by the user. All fields that drive
    section presence in the generated technical file are required; optional fields
    enrich the generated content but do not gate rendering.
    """

    id: str = Field(description="Unique device identifier (e.g. DOC-001).")
    name: str = Field(description="Commercial/trade name of the device.")
    manufacturer: str = Field(description="Legal manufacturer name.")
    version: str = Field(
        default="1.0",
        description="Device hardware/software version string.",
    )
    intended_use: str = Field(
        description=(
            "Plain-language statement of the intended use as it will appear in the "
            "Instructions for Use (IFU). Must cover intended patient population, "
            "clinical indication, and intended user(s)."
        )
    )
    intended_users: list[str] = Field(
        description=(
            "Intended user categories (e.g. ['healthcare professional', 'layperson'])."
        )
    )
    intended_environments: list[str] = Field(
        description=(
            "Intended environments of use "
            "(e.g. ['hospital ICU', 'home care', 'ambulatory care'])."
        )
    )
    risk_class: RiskClass = Field(
        description="MDR risk class per Annex VIII: I, IIa, IIb, or III."
    )
    classification_rules_applied: list[str] = Field(
        min_length=1,
        description=(
            "MDR Annex VIII classification rules that justify the risk class "
            "(e.g. ['Rule 11', 'Rule 22']). At least one rule must be provided."
        ),
    )
    software: bool = Field(
        default=False,
        description="True if the device is (or incorporates) medical device software (MDSW/SaMD).",
    )
    lifecycle: SoftwareLifecycle | None = Field(
        default=None,
        description="IEC 62304 lifecycle metadata. Required when software=true.",
    )
    soup_register: list[SoupEntry] = Field(
        default_factory=list,
        description="SOUP register. Populate when software=true.",
    )
    contraindications: list[str] = Field(
        default_factory=list,
        description="Contraindications as a list of plain-language statements.",
    )
    clinical_claims: list[str] = Field(
        default_factory=list,
        description="Clinical performance/benefit claims to be substantiated.",
    )
    notified_body: str | None = Field(
        default=None,
        description="Notified Body name (e.g. 'TÜV SÜD') if selected.",
    )
    udi_di: str | None = Field(
        default=None,
        description="UDI-DI (Device Identifier) if already assigned.",
    )
    basic_udi_di: str | None = Field(
        default=None,
        description="Basic UDI-DI if already assigned.",
    )
    eudamed_registration_id: str | None = Field(
        default=None,
        description="EUDAMED SRN / registration ID if already obtained.",
    )

    @field_validator("lifecycle")
    @classmethod
    def lifecycle_required_for_software(
        cls, v: SoftwareLifecycle | None, info: Any
    ) -> SoftwareLifecycle | None:
        """Lifecycle block is required when software=True."""
        # info.data may not yet have 'software' if validation order differs; guard
        if info.data.get("software") is True and v is None:
            raise ValueError(
                "lifecycle must be provided when software=True "
                "(IEC 62304:2006+A1:2015 §4.3 requires safety class assignment)."
            )
        return v


# Hard cap on the raw YAML size we are willing to read. Defends against
# billion-laughs anchors, runaway anchors / aliases, and accidental
# multi-gigabyte input files in CI pipelines. 1 MiB is ~10x the size of
# any realistic device.yaml we have seen.
MAX_SPEC_BYTES = 1_000_000


def load_spec(path: str | Path) -> DeviceSpec:
    """Load and validate a device specification YAML file.

    Args:
        path: Path to the YAML spec file.

    Returns:
        A validated :class:`DeviceSpec` instance.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError: If the YAML is missing required fields, exceeds
            :data:`MAX_SPEC_BYTES`, or fails Pydantic validation.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Device spec not found: {p}")
    size = p.stat().st_size
    if size > MAX_SPEC_BYTES:
        raise ValueError(
            f"Device spec is too large: {size} bytes > {MAX_SPEC_BYTES} byte cap. "
            "Refusing to parse to avoid YAML-bomb / OOM risk. "
            "Split or trim the spec, or raise MAX_SPEC_BYTES if you really need to."
        )
    with p.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    if not isinstance(raw, dict):
        raise ValueError(
            f"Device spec must be a YAML mapping, got: {type(raw).__name__}"
        )
    return DeviceSpec.model_validate(raw)
