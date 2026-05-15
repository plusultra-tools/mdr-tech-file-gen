"""Annex III renderer.

Loads the Jinja2 template and renders the MDR Annex III post-market surveillance
documentation skeleton from a validated :class:`~mdr_techfile.spec.DeviceSpec`.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from mdr_techfile import __version__
from mdr_techfile.spec import DeviceSpec
from mdr_techfile.standards import load_all_pointers, pointers_for_spec

_TEMPLATES_DIR = Path(__file__).parent / "templates"
_ANNEX3_TEMPLATE = "annex-III.md.j2"


def _jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(_TEMPLATES_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def render_annex3(
    spec: DeviceSpec,
    include_standards_pointers: bool = True,
    timestamp_iso: str | None = None,
) -> str:
    """Render the Annex III Markdown skeleton from a device spec.

    Args:
        spec: Validated device specification.
        include_standards_pointers: If False, omit standards pointer sections.
        timestamp_iso: Override generation timestamp (for deterministic tests).

    Returns:
        Rendered Markdown string.
    """
    all_p = load_all_pointers()
    filtered = (
        pointers_for_spec(all_p, software=spec.software, risk_class=spec.risk_class.value)
        if include_standards_pointers
        else []
    )
    ts = timestamp_iso or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    env = _jinja_env()
    tmpl = env.get_template(_ANNEX3_TEMPLATE)
    return tmpl.render(
        spec=spec,
        pointers=filtered,
        generated_at=ts,
        tool_version=__version__,
    )
