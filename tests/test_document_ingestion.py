"""Unit & Integration Tests for Document Ingestion Subsystem (Stage 1)."""

import pytest
from pathlib import Path

from src.system_config import SYSTEM_CONFIG
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from src.document_ingestion.handshake_section_router import _heuristic_section_router


@pytest.fixture
def tls_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc5246.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


@pytest.fixture
def kerberos_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc4120.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


@pytest.fixture
def mib_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc2358.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def test_header_filter_accepts_tls(tls_rfc_text: str):
    res = filter_rfc_header(tls_rfc_text)
    assert res.is_eligible is True
    assert res.rfc_id == "RFC 5246"
    assert "Transport Layer Security" in (res.title or "")
    assert res.category == "Standards Track"


def test_header_filter_accepts_kerberos(kerberos_rfc_text: str):
    res = filter_rfc_header(kerberos_rfc_text)
    assert res.is_eligible is True
    assert res.rfc_id == "RFC 4120"
    assert "Kerberos" in (res.title or "")


def test_header_filter_rejects_mib(mib_rfc_text: str):
    res = filter_rfc_header(mib_rfc_text)
    assert res.is_eligible is False
    assert any(term in res.disqualification_reason.lower() for term in ["mib", "managed objects"])


def test_header_filter_rejects_short_stub():
    res = filter_rfc_header("Short administrative stub.\n" * 10)
    assert res.is_eligible is False
    assert "too short" in res.disqualification_reason.lower()


def test_toc_parser_tls5246(tls_rfc_text: str):
    entries = parse_table_of_contents(tls_rfc_text)
    assert len(entries) >= 70
    section_map = {e.section_id: e.title for e in entries}

    assert "7.3" in section_map
    assert "Handshake Protocol Overview" in section_map["7.3"]
    assert "7.4" in section_map
    assert "Handshake Protocol" in section_map["7.4"]


def test_toc_parser_kerberos4120(kerberos_rfc_text: str):
    entries = parse_table_of_contents(kerberos_rfc_text)
    assert len(entries) >= 100
    section_map = {e.section_id: e.title for e in entries}

    assert "3.1" in section_map
    assert "The Authentication Service Exchange" in section_map["3.1"]


def test_verbatim_slicer_tls_handshake(tls_rfc_text: str):
    slice_text = slice_verbatim_sections(tls_rfc_text, ["7.3"])
    lines = slice_text.splitlines()

    # Starts with section header
    assert lines[0].startswith("7.3.  Handshake Protocol Overview")
    # Contains client hello ladder diagram
    assert "ClientHello" in slice_text
    assert "ServerHello" in slice_text
    # Does not contain page break markers
    assert "\x0c" not in slice_text
    assert "[Page 33]" not in slice_text


def test_heuristic_section_router_tls(tls_rfc_text: str):
    entries = parse_table_of_contents(tls_rfc_text)
    selected = _heuristic_section_router(entries)
    assert "7.3" in selected or "7.4" in selected
