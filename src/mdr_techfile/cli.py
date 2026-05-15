"""CLI entrypoint: ``mdr-techfile``.

Subcommands:
  scaffold  — render Annex II / III / both + standards-matrix + checklist + audit chain
  validate  — validate device spec YAML (Pydantic), exit 0 if valid
  manifest  — dump the standards pointer table as a citation manifest

Usage:
  mdr-techfile scaffold --spec device.yaml --out techfile/
  mdr-techfile validate --spec device.yaml
  mdr-techfile manifest --spec device.yaml
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from mdr_techfile import __version__


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mdr-techfile",
        description=(
            "YAML device spec → CE-MDR Annex II/III technical file skeleton. "
            "Regulation (EU) 2017/745 scaffolder for SaMD startups."
        ),
    )
    p.add_argument("--version", action="version", version=f"mdr-tech-file-gen {__version__}")

    sub = p.add_subparsers(dest="command", required=True)

    # ── scaffold ─────────────────────────────────────────────────────────────
    sc = sub.add_parser(
        "scaffold",
        help="Render technical file skeleton from a device spec YAML.",
    )
    sc.add_argument(
        "--spec",
        required=True,
        metavar="PATH",
        help="Path to the device spec YAML file.",
    )
    sc.add_argument(
        "--annex",
        choices=["II", "III", "both"],
        default="both",
        help="Which annex(es) to render (default: both).",
    )
    sc.add_argument(
        "--out",
        default="tech-file",
        metavar="DIR",
        help="Output directory (default: tech-file/).",
    )
    sc.add_argument(
        "--standards-pointers",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include ISO/IEC standard clause pointers in output (default: on).",
    )

    # ── validate ─────────────────────────────────────────────────────────────
    va = sub.add_parser(
        "validate",
        help="Validate device spec YAML against the Pydantic schema. Exits 0 if valid.",
    )
    va.add_argument(
        "--spec",
        required=True,
        metavar="PATH",
        help="Path to the device spec YAML file.",
    )

    # ── manifest ─────────────────────────────────────────────────────────────
    ma = sub.add_parser(
        "manifest",
        help=(
            "Dump the standards pointer citation manifest as JSON. "
            "Shows which standards each generated section cites."
        ),
    )
    ma.add_argument(
        "--spec",
        required=True,
        metavar="PATH",
        help="Path to the device spec YAML (used to filter applicable pointers).",
    )
    ma.add_argument(
        "--out",
        default=None,
        metavar="PATH",
        help="Write manifest JSON to this file instead of stdout.",
    )

    return p


def _cmd_scaffold(args: argparse.Namespace) -> int:
    from mdr_techfile.annex2 import render_annex2, render_standards_matrix
    from mdr_techfile.annex3 import render_annex3
    from mdr_techfile.audit import write_audit_chain
    from mdr_techfile.checklist import build_checklist, checklist_to_markdown
    from mdr_techfile.spec import load_spec

    try:
        spec = load_spec(args.spec)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    out = Path(args.out).resolve()
    cwd = Path.cwd().resolve()
    # Refuse to write outside the current working directory unless the user
    # opts in via an absolute path. Relative `../` segments that escape the
    # cwd are silently dangerous in CI contexts where the spec might be
    # attacker-controlled.
    if not args.out.startswith(("/", "\\")) and ":" not in args.out[:3]:
        try:
            out.relative_to(cwd)
        except ValueError:
            print(
                f"ERROR: --out '{args.out}' resolves to '{out}', which escapes "
                f"the current working directory '{cwd}'. Pass an absolute path "
                f"if you really intended to write there.",
                file=sys.stderr,
            )
            return 1
    out.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []

    if args.annex in ("II", "both"):
        annex2_md = render_annex2(spec, include_standards_pointers=args.standards_pointers)
        annex2_path = out / "annex-II.md"
        annex2_path.write_text(annex2_md, encoding="utf-8")
        written.append(annex2_path)
        print(f"  Wrote: {annex2_path}")

        if args.standards_pointers:
            matrix_md = render_standards_matrix(spec)
            matrix_path = out / "standards-matrix.md"
            matrix_path.write_text(matrix_md, encoding="utf-8")
            written.append(matrix_path)
            print(f"  Wrote: {matrix_path}")

        checklist_items = build_checklist(spec)
        checklist_md = checklist_to_markdown(checklist_items, spec)
        checklist_path = out / "checklist.md"
        checklist_path.write_text(checklist_md, encoding="utf-8")
        written.append(checklist_path)
        print(f"  Wrote: {checklist_path}")

    if args.annex in ("III", "both"):
        annex3_md = render_annex3(spec, include_standards_pointers=args.standards_pointers)
        annex3_path = out / "annex-III.md"
        annex3_path.write_text(annex3_md, encoding="utf-8")
        written.append(annex3_path)
        print(f"  Wrote: {annex3_path}")

    if written:
        audit_path = write_audit_chain(
            out, written, tool_version=__version__, spec_path=Path(args.spec)
        )
        print(f"  Wrote: {audit_path}")

    filled = sum(
        1 for item in (build_checklist(spec) if args.annex in ("II", "both") else [])
        if item.status.value == "filled"
    )
    total = len(build_checklist(spec)) if args.annex in ("II", "both") else 0

    print(f"\nOK: scaffolded {len(written)} file(s) to {out}/")
    if total:
        print(f"    Checklist: {filled}/{total} items pre-filled from spec.")
        print("    Review checklist.md and complete all [TODO] items before NB submission.")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    from pydantic import ValidationError

    from mdr_techfile.spec import load_spec

    try:
        spec = load_spec(args.spec)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ValidationError as e:
        print(f"INVALID: {args.spec}", file=sys.stderr)
        for err in e.errors():
            loc = " -> ".join(str(x) for x in err["loc"])
            print(f"  [{loc}] {err['msg']}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"VALID: {args.spec}")
    print(f"  Device: {spec.name} (Class {spec.risk_class.value})")
    print(f"  Manufacturer: {spec.manufacturer}")
    print(f"  Software: {'Yes' if spec.software else 'No'}")
    if spec.software and spec.lifecycle:
        print(f"  IEC 62304 safety class: {spec.lifecycle.iec62304_safety_class.value}")
    print(f"  SOUP entries: {len(spec.soup_register)}")
    print(f"  Clinical claims: {len(spec.clinical_claims)}")
    return 0


def _cmd_manifest(args: argparse.Namespace) -> int:
    from mdr_techfile.spec import load_spec
    from mdr_techfile.standards import load_all_pointers, pointers_for_spec

    try:
        spec = load_spec(args.spec)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    all_p = load_all_pointers()
    filtered = pointers_for_spec(
        all_p, software=spec.software, risk_class=spec.risk_class.value
    )

    manifest = {
        "device": spec.name,
        "device_id": spec.id,
        "risk_class": spec.risk_class.value,
        "software": spec.software,
        "sections": [
            {
                "section": sec.section,
                "title": sec.title,
                "pointers": [
                    {
                        "standard_id": p.standard_id,
                        "clause": p.clause,
                        "topic": p.topic,
                        "applicability": p.applicability,
                        "note": p.note,
                    }
                    for p in sec.pointers
                ],
            }
            for sec in filtered
        ],
    }

    manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(manifest_json + "\n", encoding="utf-8")
        print(f"Manifest written to: {out_path}")
    else:
        print(manifest_json)

    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``mdr-techfile`` CLI."""
    args = _build_parser().parse_args(argv)

    if args.command == "scaffold":
        return _cmd_scaffold(args)
    if args.command == "validate":
        return _cmd_validate(args)
    if args.command == "manifest":
        return _cmd_manifest(args)

    print(f"ERROR: unknown command {args.command!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
