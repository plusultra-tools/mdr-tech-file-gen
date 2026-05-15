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

    def test_audit_content_has_two_lines(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.md"
        f2 = tmp_path / "b.md"
        f1.write_text("aaa", encoding="utf-8")
        f2.write_text("bbb", encoding="utf-8")
        audit_path = write_audit_chain(tmp_path, [f1, f2])
        lines = [ln for ln in audit_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        assert len(lines) == 2

    def test_audit_line_format(self, tmp_path: Path) -> None:
        f = tmp_path / "doc.md"
        content = "test content"
        f.write_text(content, encoding="utf-8")
        audit_path = write_audit_chain(tmp_path, [f])
        line = audit_path.read_text(encoding="utf-8").strip()
        parts = line.split("  ", 1)
        assert len(parts) == 2
        assert len(parts[0]) == 64  # SHA-256 hex
        assert "doc.md" in parts[1]

    def test_hash_matches_file_content(self, tmp_path: Path) -> None:
        content = "deterministic content"
        f = tmp_path / "out.md"
        f.write_text(content, encoding="utf-8")
        write_audit_chain(tmp_path, [f])
        audit_line = (tmp_path / AUDIT_FILENAME).read_text(encoding="utf-8").strip()
        recorded_hash = audit_line.split("  ")[0]
        assert recorded_hash == hashlib.sha256(content.encode("utf-8")).hexdigest()

    def test_empty_file_list(self, tmp_path: Path) -> None:
        audit_path = write_audit_chain(tmp_path, [])
        assert audit_path.exists()
        assert audit_path.read_text(encoding="utf-8") == "\n"
