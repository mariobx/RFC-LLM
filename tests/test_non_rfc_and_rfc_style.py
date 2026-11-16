"""Tests for non-RFC global standards ingestion, $0 de-bloater, book splitter, and --rfc-style pairing."""

import json
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch

import pymupdf

from src.cost_tracker import PipelineCostTracker
from src.visualizer.server import hydrate_tab_payload
from src.document_ingestion.pdf_and_book_splitter import split_books_directory
from src.document_ingestion.programmatic_debloater import debloat_protocol_slice
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.document_ingestion.rfc_style_distiller import compute_text_sha256, synthesize_or_load_rfc_style_slice
from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from src.logging_config import PipelineMetricsCSVLogger


def test_programmatic_debloater_strips_noise_preserves_ladders_and_fields():
    raw = "\n".join([
        "3GPP TS 33.501 V18.0.0",
        "Page 12 of 48",
        "4.2 Handshake Overview ............................ 19",
        "4.2 Authentication Flow",
        "The UE sends SUCI with    RAND   and   AUTN      tokens.",
        "   UE ---> AUSF: enc(K_ausf, RAND, AUTN)",
        "\x0c",
        "CCSDS 355.0-B-2 Page 4-1",
        "The CK_SUCI key is derived via HMAC-SHA-256(K, SQN XOR AK).",
        "",
        "",
        "",
        "Change History",
        "2023-01 Rev 1 Editorial cleanup",
        "Acknowledgements",
        "Many thanks to committee.",
    ])
    cleaned, stats = debloat_protocol_slice(raw, is_non_rfc=True)

    assert "Page 12 of 48" not in cleaned
    assert "CCSDS 355.0-B-2 Page 4-1" not in cleaned
    assert "3GPP TS 33.501" not in cleaned
    assert "Change History" not in cleaned
    assert "Editorial cleanup" not in cleaned
    assert "4.2 Handshake Overview ............................ 19" not in cleaned
    assert "   UE ---> AUSF: enc(K_ausf, RAND, AUTN)" in cleaned
    assert "CK_SUCI" in cleaned and "RAND" in cleaned and "AUTN" in cleaned
    assert stats["saved_pct"] > 10.0


def test_non_rfc_header_filter_accepts_global_standards_and_preserves_ietf_rejects():
    body_lines = [
        f"Step {i}: Initiator computes HMAC session key and nonce exchange for OTAR rekeying."
        for i in range(1, 70)
    ]
    ccsds_dossier = "\n".join([
        "Document-ID: CCSDS-355.0-B-2",
        "Source-Organization: CCSDS",
        "Category: Standards Track",
        "Protocol-Title: SDLS Security Architecture and Extended Procedures - Over-the-Air Rekeying (OTAR)",
        "",
        "Abstract",
        "   Defines interactive cryptographic OTAR session key rekeying and authentication.",
        "",
        "Table of Contents",
        "   4.1 OTAR Protocol Exchange",
        "",
    ] + body_lines)

    res = filter_rfc_header(ccsds_dossier)
    assert res.is_eligible is True
    assert res.rfc_id == "CCSDS-355.0-B-2"
    assert "OTAR" in (res.title or "")

    ietf_arch = "\n".join([
        "Network Working Group",
        "Request for Comments: 9999",
        "Category: Informational",
        "",
        "                     Security Architecture Guidelines",
        "",
        "Abstract",
        "   This document discusses high-level security architecture considerations.",
    ] + [f"Line {i} general architectural discussion." for i in range(70)])

    res_ietf = filter_rfc_header(ietf_arch)
    assert res_ietf.is_eligible is False


def test_toc_and_slicer_non_rfc_long_section():
    sec2_body = [f"Line {i}: UE verifies MAC and computes RES* using K_seaf." for i in range(1, 750)]
    sec2_body[300] = "3GPP TS 33.501 V18.0.0"
    sec2_body[301] = "Page 45 of 90"
    doc = "\n".join([
        "Document-ID: 3GPP-TS-33.501",
        "Category: Standards Track",
        "",
        "Table of Contents",
        "   1  Scope .................................................... 5",
        "   2  5G AKA Authentication Procedure .......................... 6",
        "   3  Security Context Handling ................................ 40",
        "",
        "1  Scope",
        "Scope text here.",
        "2  5G AKA Authentication Procedure",
        *sec2_body,
        "3  Security Context Handling",
        "Trailing section text.",
    ])
    toc = parse_table_of_contents(doc)
    assert any(e.section_id == "2" for e in toc)
    sliced = slice_verbatim_sections(doc, ["2"])
    assert "Line 720: UE verifies MAC" in sliced
    assert "3GPP TS 33.501 V18.0.0" not in sliced
    assert "Page 45 of 90" not in sliced
    assert "Trailing section text." not in sliced


def test_pdf_and_book_splitter_multicore_and_pdf(tmp_path: Path):
    pdf_path = tmp_path / "matter_multi_protocol.pdf"
    doc = pymupdf.open()

    def _add_pages(title_line: str, body_items: list[str]):
        page = doc.new_page()
        page.insert_text((50, 60), title_line + "\n" + "\n".join(body_items), fontsize=9)

    pase_lines = [
        f"{i}. Client and Responder exchange nonce, SPAKE2+ public key, HMAC, and derive session key."
        for i in range(1, 35)
    ]
    case_lines = [
        f"{i}. Initiator sends Sigma1 ephemeral ECDH key, certificate, signature, and session key confirmation."
        for i in range(1, 35)
    ]
    filler_lines = [f"Appendix editorial line {i} thanking contributors." for i in range(1, 35)]

    _add_pages(
        "Table of Contents",
        [
            "1  Introduction ........................................ 2",
            "2  PASE Password Authenticated Session Establishment ... 3",
            "3  CASE Certificate Authenticated Session Establishment  4",
            "4  Change History ...................................... 5",
        ] + [f"Background sentence {i}." for i in range(25)],
    )
    _add_pages("1  Introduction", [f"General introduction paragraph {i}." for i in range(25)])
    _add_pages("2  PASE Password Authenticated Session Establishment", pase_lines + [f"More PASE spec {i}." for i in range(25)])
    _add_pages("3  CASE Certificate Authenticated Session Establishment", case_lines + [f"More CASE spec {i}." for i in range(25)])
    # Push total line count well past 950 to exercise multi-protocol splitting mode
    for k in range(18):
        _add_pages(f"3.{k+1} CASE Cipher Details", [f"Protocol cipher message nonce key agreement line {m}" for m in range(45)])
    _add_pages("4  Change History", filler_lines)
    doc.set_toc([
        [1, "1. Introduction", 2],
        [1, "2. PASE Password Authenticated Session Establishment", 3],
        [1, "3. CASE Certificate Authenticated Session Establishment", 4],
        [1, "4. Change History", 23],
    ])
    doc.save(str(pdf_path))
    doc.close()

    md_path = tmp_path / "custom_aead_handshake.md"
    md_path.write_text(
        "\n".join([
            "# Custom Device Pairing Handshake",
            "## 1. Pairing Exchange",
            "Protocol message exchange using Diffie-Hellman ephemeral key, signature, certificate, and nonce:",
        ] + [
            f"Step {i}: Initiator sends handshake nonce and authenticates session key via HMAC signature."
            for i in range(1, 45)
        ]),
        encoding="utf-8",
    )

    out_dir = tmp_path / "split_out"
    res = split_books_directory([pdf_path, md_path], output_dir=out_dir, workers=2, use_llm=False)

    assert res["input_files_scanned"] == 2
    assert res["emitted_protocols_count"] >= 3
    emitted_names = [Path(e["path"]).name for e in res["emitted_files"]]
    assert any("pase" in n for n in emitted_names)
    assert any("case" in n for n in emitted_names)
    assert not any("change_history" in n for n in emitted_names)
    assert (out_dir / "INDEX.csv").exists()
    for item in res["emitted_files"]:
        txt = Path(item["path"]).read_text(encoding="utf-8")
        assert filter_rfc_header(txt).is_eligible is True


def test_rfc_style_shared_stem_pairing_and_zero_cost_cache_hit(tmp_path: Path):
    cache_dir = tmp_path / "paired_slices"
    run1_dir = tmp_path / "run1" / "ts33501"
    run2_dir = tmp_path / "run2" / "ts33501"
    src_file = tmp_path / "ts33501_aka.txt"
    verbatim = "\n".join([
        "3GPP TS 33.501 V18.0.0",
        "Page 12 of 50",
        "6.1.3.2 Authentication Procedure",
        "UE -> SEAF: SUCI, RAND, AUTN, RES*, K_ausf, K_seaf HMAC check.",
    ] + [f"Detail line {i}: nonce RAND and AUTN check with K_ausf." for i in range(25)])
    src_file.write_text(verbatim, encoding="utf-8")

    fake_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="```text\n1. Overview\nUE ---> SEAF: SUCI\n```"))],
        usage=SimpleNamespace(prompt_tokens=120, completion_tokens=40, total_tokens=160),
    )

    with patch("src.document_ingestion.rfc_style_distiller.litellm.completion", return_value=fake_resp) as mock_comp:
        style1, meta1 = synthesize_or_load_rfc_style_slice(
            stem="3GPP TS 33.501__aka",
            doc_id="3GPP-33.501",
            protocol_name="5G AKA",
            verbatim_slice=verbatim,
            source_file=src_file,
            selected_sections=["6.1.3.2"],
            run_output_dir=run1_dir,
            paired_dir=cache_dir,
            model="nous/anthropic/claude-haiku-5.5",
        )
        assert mock_comp.call_count == 1
        assert meta1["cache_hit"] is False
        stem = meta1["stem"]
        assert (cache_dir / stem / f"{stem}__verbatim.txt").read_text(encoding="utf-8") == verbatim
        assert (cache_dir / stem / f"{stem}__debloated.txt").exists()
        assert (cache_dir / stem / f"{stem}__rfc_style.txt").exists()
        assert (run1_dir / f"{stem}_slices" / f"{stem}__verbatim.txt").exists()
        assert (run1_dir / f"{stem}_slices" / f"{stem}__debloated.txt").exists()
        assert (run1_dir / f"{stem}_slices" / f"{stem}__rfc_style.txt").exists()
        assert not (cache_dir / f"{stem}__rfc_style.txt").exists()
        assert not (run1_dir / f"{stem}__rfc_style.txt").exists()
        assert f"Verbatim-Companion: {stem}__verbatim.txt" in style1
        assert f"Verbatim-SHA256: {compute_text_sha256(verbatim)}" in style1
        assert (cache_dir / "PAIRED_INDEX.csv").exists()

        # Second call into different run dir MUST hit $0.00 SHA-256 cache
        style2, meta2 = synthesize_or_load_rfc_style_slice(
            stem="3GPP TS 33.501__aka",
            doc_id="3GPP-33.501",
            protocol_name="5G AKA",
            verbatim_slice=verbatim,
            source_file=src_file,
            selected_sections=["6.1.3.2"],
            run_output_dir=run2_dir,
            paired_dir=cache_dir,
            model="nous/anthropic/claude-haiku-5.5",
        )
        assert mock_comp.call_count == 1
        assert meta2["cache_hit"] is True
        assert style2 == style1
        assert (run2_dir / f"{stem}_slices" / f"{stem}__rfc_style.txt").exists()

        # refresh=True forces regeneration
        _, meta3 = synthesize_or_load_rfc_style_slice(
            stem="3GPP TS 33.501__aka",
            doc_id="3GPP-33.501",
            protocol_name="5G AKA",
            verbatim_slice=verbatim,
            source_file=src_file,
            selected_sections=["6.1.3.2"],
            run_output_dir=run2_dir,
            paired_dir=cache_dir,
            model="nous/anthropic/claude-haiku-5.5",
            refresh=True,
        )
        assert mock_comp.call_count == 2
        assert meta3["cache_hit"] is False


def test_cost_tracker_distiller_role_and_67_col_csv():
    assert len(PipelineMetricsCSVLogger.CSV_HEADER) == 67
    ct = PipelineCostTracker()
    ct.start_rfc("TEST-PROTO", router_model="nous/anthropic/claude-haiku-5.5", distiller_model="nous/anthropic/claude-haiku-5.5")
    resp = SimpleNamespace(usage=SimpleNamespace(prompt_tokens=1000, completion_tokens=500, total_tokens=1500))
    ct.record_llm_call(resp, role="distiller", model_name="nous/anthropic/claude-haiku-5.5", stage=1)
    summary = ct.get_current_rfc_summary()
    assert summary["roles"]["distiller"]["calls"] == 1
    assert summary["roles"]["distiller"]["cost_usd"] > 0.0
    cli_line = ct.format_cli_summary(summary)
    assert "Distiller:" in cli_line


def test_visualizer_hydrate_tab_payload_returns_paired_slices(tmp_path: Path):
    proto_dir = tmp_path / "ms_nrpc_test"
    slices_dir = proto_dir / "ms_nrpc_test_slices"
    slices_dir.mkdir(parents=True)
    (proto_dir / "verbatim_slice.txt").write_text("RAW VERBATIM TEXT", encoding="utf-8")
    (slices_dir / "ms_nrpc_test__verbatim.txt").write_text("RAW VERBATIM TEXT", encoding="utf-8")
    (slices_dir / "ms_nrpc_test__debloated.txt").write_text("DEBLOATED TEXT", encoding="utf-8")
    (slices_dir / "ms_nrpc_test__rfc_style.txt").write_text("RFC STYLE TEXT", encoding="utf-8")
    traj_path = proto_dir / "ms_nrpc_test_trajectory.json"
    traj_path.write_text(
        json.dumps({
            "rfc_metadata": {
                "rfc_id": "MS-NRPC",
                "rfc_title": "Netlogon Remote Protocol",
                "verbatim_rfc_slice": "RAW VERBATIM TEXT",
                "debloated_rfc_slice": "DEBLOATED TEXT",
                "rfc_style_slice": "RFC STYLE TEXT",
                "paired_stem": "ms_nrpc_test",
            },
            "stage2_initial_extraction": {},
            "stage5_preflight_gate": {},
            "stage6_cpsa4_solver": {},
            "quality_assessment": {"quality_tier": "GOLD"},
            "final_verified_output": {},
        }),
        encoding="utf-8",
    )

    payload = hydrate_tab_payload({
        "tab_index": 1,
        "rfc_id": "MS-NRPC",
        "rfc_dir": str(proto_dir),
        "trajectory_path": str(traj_path),
        "status": "VERIFIED",
    })
    assert payload["verbatim_slice"] == "RAW VERBATIM TEXT"
    assert payload["debloated_slice"] == "DEBLOATED TEXT"
    assert payload["rfc_style_slice"] == "RFC STYLE TEXT"
    assert payload["paired_stem"] == "ms_nrpc_test"

    # Also verify disk fallback hydration from <stem>_slices/ when omitted in trajectory metadata
    traj_path.write_text(
        json.dumps({
            "rfc_metadata": {"rfc_id": "MS-NRPC", "rfc_title": "Netlogon Remote Protocol"},
            "stage2_initial_extraction": {},
            "stage5_preflight_gate": {},
            "stage6_cpsa4_solver": {},
            "quality_assessment": {"quality_tier": "GOLD"},
            "final_verified_output": {},
        }),
        encoding="utf-8",
    )
    fallback_payload = hydrate_tab_payload({
        "tab_index": 1,
        "rfc_id": "MS-NRPC",
        "rfc_dir": str(proto_dir),
        "trajectory_path": str(traj_path),
        "status": "VERIFIED",
    })
    assert fallback_payload["debloated_slice"] == "DEBLOATED TEXT"
    assert fallback_payload["rfc_style_slice"] == "RFC STYLE TEXT"


def test_pdf_space_separated_toc_slicing_and_isolated_page_numbers():
    doc = "\n".join([
        "Document-ID: SIGNAL-X3DH",
        "Protocol-Title: Extended Triple Diffie-Hellman",
        "",
        "Table of Contents",
        "   1  Introduction",
        "   2  Preliminaries",
        "   3  The X3DH protocol",
        "   4  Security considerations",
        "",
        "Contents",
        "1. Introduction  2",
        "2. Preliminaries  2",
        "3. The X3DH protocol  4",
        "4. Security considerations  7",
        "",
        "1. Introduction",
        "This document describes X3DH.",
        "",
        "2. Preliminaries",
        "Roles: Alice, Bob, Server.",
        "",
        "    3",
        "",
        "3. The X3DH protocol",
        "3.1. Overview",
        "Alice fetches prekey bundle and computes DH1 = DH(IKA, SPKB).",
        "",
        "    4",
        "",
        "3.2. Sending the initial message",
        "SK = KDF(DH1 || DH2 || DH3 || DH4).",
        "",
        "4. Security considerations",
        "Identity binding analysis.",
    ])

    toc = parse_table_of_contents(doc)
    assert any(entry.section_id == "3" and "X3DH" in entry.title for entry in toc)

    sliced = slice_verbatim_sections(doc, ["3"])
    assert "3.1. Overview" in sliced
    assert "SK = KDF(DH1 || DH2 || DH3 || DH4)." in sliced
    assert "3. The X3DH protocol  4" not in sliced

    debloated, _ = debloat_protocol_slice(sliced, is_non_rfc=True)
    assert "\n    4\n" not in debloated
    assert "SK = KDF(DH1 || DH2 || DH3 || DH4)." in debloated
