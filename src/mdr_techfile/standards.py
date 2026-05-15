"""Standards pointer table.

Maps (MDR Annex II section, DeviceSpec field) to ISO/IEC standard clause pointers.

IMPORTANT: This module contains ONLY standard identifiers and clause numbers.
It does NOT reproduce verbatim text from copyrighted ISO/IEC standards.
All content is limited to citation data: standard ID, year, amendment, clause number.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise ImportError("PyYAML is required: pip install pyyaml") from exc

_DATA_FILE = Path(__file__).parent / "data" / "standards_pointers.yaml"


@dataclass(frozen=True)
class StandardPointer:
    """A citation pointer to a specific clause of a harmonised standard."""

    standard_id: str
    """E.g. 'ISO 14971:2019'."""
    clause: str
    """E.g. '§5' or '§5.1-5.7' or '§4.3'."""
    topic: str
    """Human-readable topic label."""
    applicability: str = "always"
    """'always' | 'if_software' | 'if_class_iib_iii' | 'if_sterile'."""
    note: str = ""
    """Short explanatory note (max ~120 chars). No verbatim ISO/IEC text."""


@dataclass
class SectionPointers:
    """All standard pointers relevant to one MDR Annex II section."""

    section: str
    """E.g. 'Annex II §1.1' or 'Annex III §1'."""
    title: str
    pointers: list[StandardPointer] = field(default_factory=list)


def _load_raw() -> list[dict[str, object]]:
    with _DATA_FILE.open(encoding="utf-8") as fh:
        raw: object = yaml.safe_load(fh)
    if not isinstance(raw, list):
        raise ValueError(f"standards_pointers.yaml must be a list, got {type(raw)}")
    result: list[dict[str, object]] = []
    for item in raw:
        if isinstance(item, dict):
            result.append(item)
    return result


def load_all_pointers() -> list[SectionPointers]:
    """Load the full pointer table from ``data/standards_pointers.yaml``."""
    raw = _load_raw()
    result: list[SectionPointers] = []
    for entry in raw:
        raw_pointers = entry.get("pointers", [])
        pointer_list: list[dict[str, str]] = (
            raw_pointers if isinstance(raw_pointers, list) else []
        )
        pointers = [StandardPointer(**p) for p in pointer_list]
        result.append(
            SectionPointers(
                section=str(entry["section"]),
                title=str(entry["title"]),
                pointers=pointers,
            )
        )
    return result


def pointers_for_spec(
    all_pointers: Sequence[SectionPointers],
    software: bool = False,
    risk_class: str = "IIa",
) -> list[SectionPointers]:
    """Filter pointer table to entries applicable to the given device spec.

    Args:
        all_pointers: Full pointer list from :func:`load_all_pointers`.
        software: True if the device is a SaMD/MDSW.
        risk_class: MDR risk class string ('I', 'IIa', 'IIb', 'III').

    Returns:
        Filtered list where only applicable pointers remain.
    """
    high_risk = risk_class in ("IIb", "III")
    filtered: list[SectionPointers] = []
    for sec in all_pointers:
        keep: list[StandardPointer] = []
        for p in sec.pointers:
            if p.applicability == "always":
                keep.append(p)
            elif p.applicability == "if_software" and software:
                keep.append(p)
            elif p.applicability == "if_class_iib_iii" and high_risk:
                keep.append(p)
        if keep:
            filtered.append(
                SectionPointers(section=sec.section, title=sec.title, pointers=keep)
            )
    return filtered
