"""Tests for mdr_techfile.audit — SHA-256 chain."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from mdr_techfile.audit import (
    AUDIT_FILENAME,
    sha256_file,
    sha256_text,
    write_audit_chain,
)


class TestSha256Text:
    def test_known_hash(self) -> None:
        # SHA-256 of empty string
        assert sha256_text("") == hashlib.sha256(b"").hexdigest()

    def test_known_content(self) -> None:
        text = "hello world"
        expected = hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert sha256_text(text) == expected

    def test_returns_lowercase_hex(self) -> None:
        digest = sha256_text("test")
        assert digest == digest.lower()
        assert len(digest) == 64


class TestSha256File:
    def test_hash_small_file(self, tmp_path: Path) -> None:
        content = b"some content"
        f = tmp_path / "f.txt"
        f.write_bytes(content)
        expected = hashlib.sha256(content).hexdigest()
        assert sha256_file(f) == expected

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            sha256_file(tmp_path / "missing.txt")

    def test_empty_file(self, tmp_path: Path) -> None:
        f = tmp_path / "empty.txt"
        f.write_bytes(b"")
        assert sha256_file(f) == hashlib.sha256(b"").hexdigest()


class TestWriteAuditChain:
    def test_writes_audit_file(self, tmp_path: Path) -> None:
        f1 = tmp_path / "annex-II.md"
        f2 = tmp_path / "annex-III.md"
        f1.write_text("annex two content", encoding="utf-8")
        f2.write_text("annex three content", encoding="utf-8")
        audit_path = write_audit_chain(tmp_path, [f1, f2])
        assert audit_path.exists()
        assert audit_path.name == AUDIT_FILENAME

    def test_audit_content_has_two_hash_lines(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.md"
        f2 = tmp_path / "b.md"
        f1.write_text("aaa", encoding="utf-8")
        f2.write_text("bbb", encoding="utf-8")
        audit_path = write_audit_chain(tmp_path, [f1, f2])
        # Hash lines are non-empty and do NOT start with the '#' provenance marker.
        lines = [
            ln
            for ln in audit_path.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")
        ]
        assert len(lines) == 2

    def test_audit_line_format(self, tmp_path: Path) -> None:
        f = tmp_path / "doc.md"
        content = "test content"
        f.write_text(content, encoding="utf-8")
        audit_path = write_audit_chain(tmp_path, [f])
        # Skip the '# tool_version: ...' header line.
        hash_lines = [
            ln
            for ln in audit_path.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")
        ]
        assert len(hash_lines) == 1
        parts = hash_lines[0].split("  ", 1)
        assert len(parts) == 2
        assert len(parts[0]) == 64  # SHA-256 hex
        assert "doc.md" in parts[1]

    def test_hash_matches_file_content(self, tmp_path: Path) -> None:
        content = "deterministic content"
        f = tmp_path / "out.md"
        f.write_text(content, encoding="utf-8")
        write_audit_chain(tmp_path, [f])
        hash_lines = [
            ln
            for ln in (tmp_path / AUDIT_FILENAME).read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")
        ]
        recorded_hash = hash_lines[0].split("  ")[0]
        assert recorded_hash == hashlib.sha256(content.encode("utf-8")).hexdigest()

    def test_empty_file_list_emits_header_only(self, tmp_path: Path) -> None:
        audit_path = write_audit_chain(tmp_path, [])
        assert audit_path.exists()
        text = audit_path.read_text(encoding="utf-8")
        # No hash lines, but the provenance header is still present.
        hash_lines = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
        assert hash_lines == []
        assert "tool_version" in text

    def test_provenance_header_includes_tool_version(self, tmp_path: Path) -> None:
        f = tmp_path / "x.md"
        f.write_text("xx", encoding="utf-8")
        write_audit_chain(tmp_path, [f], tool_version="9.9.9")
        text = (tmp_path / AUDIT_FILENAME).read_text(encoding="utf-8")
        assert "# tool_version: mdr-tech-file-gen 9.9.9" in text

    def test_provenance_header_includes_spec_sha(self, tmp_path: Path) -> None:
        f = tmp_path / "y.md"
        f.write_text("yy", encoding="utf-8")
        spec = tmp_path / "device.yaml"
        spec.write_text("id: X\n", encoding="utf-8")
        write_audit_chain(tmp_path, [f], spec_path=spec)
        text = (tmp_path / AUDIT_FILENAME).read_text(encoding="utf-8")
        assert "# spec_sha256:" in text
        assert "device.yaml" in text
