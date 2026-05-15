"""Audit chain module.

Produces ``audit.sha256`` — a line-separated hash manifest of every generated
output file. Pattern mirrors the audit chain used in other plusUltra tools.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

AUDIT_FILENAME = "audit.sha256"


def sha256_file(path: Path) -> str:
    """Return the SHA-256 hex digest of a file's content.

    Args:
        path: Path to the file to hash.

    Returns:
        Lowercase hex-encoded SHA-256 digest.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found for hashing: {path}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def sha256_text(text: str) -> str:
    """Return the SHA-256 hex digest of a UTF-8 encoded string.

    Args:
        text: The string to hash.

    Returns:
        Lowercase hex-encoded SHA-256 digest.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_audit_chain(
    output_dir: Path,
    file_paths: list[Path],
    *,
    tool_version: str | None = None,
    spec_path: Path | None = None,
) -> Path:
    """Write ``audit.sha256`` containing provenance + one hash line per file.

    The file begins with two ``# `` provenance lines (tool version and the
    SHA-256 of the source spec) so two builds of the same generator on the
    same spec are bit-for-bit reproducible — and a different generator
    version or a different spec is visible in the chain. The provenance
    lines are not part of the file-hash assertion; they precede it.

    Args:
        output_dir: Directory where ``audit.sha256`` will be written and where
            relative paths are computed from.
        file_paths: Ordered list of files to hash.
        tool_version: Generator version string. If None, the running package
            version is auto-detected.
        spec_path: Path to the source device spec YAML. Its SHA-256 is recorded
            in the provenance header. If None, no spec line is written.

    Returns:
        Path to the written ``audit.sha256`` file.

    Raises:
        FileNotFoundError: If any path in *file_paths* does not exist.
    """
    header_lines: list[str] = []
    if tool_version is None:
        try:
            from mdr_techfile import __version__ as _v

            tool_version = _v
        except Exception:  # pragma: no cover — defensive
            tool_version = "unknown"
    header_lines.append(f"# tool_version: mdr-tech-file-gen {tool_version}")
    if spec_path is not None and spec_path.exists():
        header_lines.append(f"# spec_sha256: {sha256_file(spec_path)}  {spec_path.name}")

    lines: list[str] = []
    for fp in file_paths:
        digest = sha256_file(fp)
        try:
            rel = fp.relative_to(output_dir)
        except ValueError:
            rel = fp  # fall back to absolute if outside output_dir
        lines.append(f"{digest}  {rel}")
    audit_text = "\n".join(header_lines + lines) + "\n"
    audit_path = output_dir / AUDIT_FILENAME
    audit_path.write_text(audit_text, encoding="utf-8")
    return audit_path
