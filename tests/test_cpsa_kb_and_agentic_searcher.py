"""Unit & Integration Tests for the CPSA 4.4.9 Knowledge Base, TOC Rebuild Flag,
Agentic Searcher Loop, and Two-Speed Repair Trigger.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.rag_retriever_client import (
    CPSAKnowledgeBase,
    TOC_MD_PATH,
    build_cpsa_kb_index,
    get_cpsa_manual_retriever,
    parse_toc_rebuild_flag,
    run_agentic_cpsa_searcher,
)
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAProtocolRole,
    CPSAProtocolSpecification,
    CPSAPreskeleton,
    CPSAStrandInstance,
    CPSATraceEvent,
    CPSAVariableDeclaration,
    CPSASortEnum,
)
from src.verification_engine.compiler_diagnostic_repair import (
    repair_protocol_specification,
)


def _make_sample_spec() -> CPSAProtocolSpecification:
    return CPSAProtocolSpecification(
        protocol_name="test-proto",
        message_algebra="basic",
        roles=[
            CPSAProtocolRole(
                role_name="init",
                variables=[
                    CPSAVariableDeclaration(name="a", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="b", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                ],
                inputs=["ch", "a", "b"],
                outputs=["n"],
                unique_originating=["n"],
                trace=[
                    CPSATraceEvent(
                        direction="send",
                        channel="ch",
                        message_term=["enc", "n", ["pubk", "b"]],
                    )
                ],
            )
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="test-proto",
                variables=[
                    CPSAVariableDeclaration(name="a", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="b", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                ],
                strands=[
                    CPSAStrandInstance(
                        role_name="init",
                        height=1,
                        variable_mappings=[["a", "a"], ["b", "b"], ["n", "n"]],
                    )
                ],
                non_originating=[["privk", "b"]],
                unique_originating=["n"],
            )
        ],
    )


def test_production_cpsa_kb_completeness_and_toc_flag():
    """Verify that the production `refrences/cpsa_kb/` corpus indexes all 151 .scm examples,
    all core rules/manuals/catalogs, and has `rebuild_toc: false` in `TOC.md`.
    """
    kb = get_cpsa_manual_retriever()
    assert kb is not None
    assert len(kb.scm_examples) == 151
    assert len(kb.sections) >= 400
    assert TOC_MD_PATH.exists()
    assert parse_toc_rebuild_flag(TOC_MD_PATH) is False

    # Verify the 3 official Hackage cpsa-4.4.9 test files are indexed
    for hackage_scm in ("chan-mesg.scm", "dev-subatomic-open-closed.scm", "devlocn.scm"):
        ex = kb.read_scm_example(hackage_scm)
        assert ex is not None, f"Missing Hackage 4.4.9 example {hackage_scm}"
        assert "(defprotocol" in ex["scm_code"]


def test_toc_rebuild_flag_lifecycle_in_isolated_kb(tmp_path: Path):
    """Verify that `rebuild_toc: true` triggers a full rebuild of `TOC.md` and `kb_index.json`
    and automatically flips `rebuild_toc: false`, and that subsequent loads skip rebuilding
    until `rebuild_toc: true` is flipped back.
    """
    kb_dir = tmp_path / "cpsa_kb"
    core_dir = kb_dir / "01_core_rules"
    scm_dir = kb_dir / "03_examples_scm"
    core_dir.mkdir(parents=True)
    scm_dir.mkdir(parents=True)

    (core_dir / "01_test_rules.md").write_text(
        "# Test Rules\n\n## Section Alpha\nAlpha rule about uniq-orig and non-orig in defskeleton.\n",
        encoding="utf-8",
    )
    (scm_dir / "mini_ns.scm").write_text(
        "(herald \"Mini NS\")\n(defprotocol ns basic (defrole init (vars (a b name) (n text)) (trace (send (enc n (pubk b))))))\n",
        encoding="utf-8",
    )

    toc_path = kb_dir / "TOC.md"
    # Before TOC exists, parse_toc_rebuild_flag returns True
    assert parse_toc_rebuild_flag(toc_path) is True

    kb1 = CPSAKnowledgeBase(kb_dir)
    assert len(kb1.sections) == 1
    assert len(kb1.scm_examples) == 1
    # After build, TOC.md exists and rebuild_toc is automatically flipped to False
    assert toc_path.exists()
    assert parse_toc_rebuild_flag(toc_path) is False

    # Add a new markdown file WITHOUT flipping rebuild_toc -> cached kb_index.json is used
    (core_dir / "02_extra_rules.md").write_text(
        "# Extra Rules\n\n## Section Beta\nBeta rule about diffie-hellman rndx and uniq-gen.\n",
        encoding="utf-8",
    )
    kb2 = CPSAKnowledgeBase(kb_dir)
    assert len(kb2.sections) == 1

    # Now flip `rebuild_toc: false` -> `rebuild_toc: true` in TOC.md
    toc_text = toc_path.read_text(encoding="utf-8").replace("rebuild_toc: false", "rebuild_toc: true")
    toc_path.write_text(toc_text, encoding="utf-8")
    assert parse_toc_rebuild_flag(toc_path) is True

    # Loading CPSAKnowledgeBase now rebuilds and resets rebuild_toc to False
    kb3 = CPSAKnowledgeBase(kb_dir)
    assert len(kb3.sections) == 2
    assert parse_toc_rebuild_flag(toc_path) is False


def test_cpsa_kb_four_tools_precision():
    """Verify `read_section`, `search_cpsa_docs`, `find_scm_examples`, and `read_scm_example`."""
    kb = get_cpsa_manual_retriever()
    assert kb is not None

    # Tool 1: read_section
    sec = kb.read_section("01_core_rules/07_compiler_and_solver_error_catalog#1.1-received-term-cannot-be-fully-destructured")
    assert sec is not None
    assert "Received term cannot be fully destructured" in sec["title"]

    # Tool 2: search_cpsa_docs on exact compiler diagnostic
    hits = kb.search_cpsa_docs("Received term cannot be fully destructured", top_k=2, rerank=False)
    assert len(hits) >= 1
    assert "destructured" in hits[0]["title"].lower() or "destructured" in hits[0]["content"].lower()

    # Tool 3: find_scm_examples for diffie-hellman + uniq-gen
    dh_examples = kb.find_scm_examples(algebra="diffie-hellman", keywords=["uniq-gen"], top_k=3)
    assert len(dh_examples) >= 1
    assert all(ex["algebra"] == "diffie-hellman" for ex in dh_examples)

    # Tool 4: read_scm_example
    blanchet = kb.read_scm_example("blanchet.scm")
    assert blanchet is not None
    assert "(defprotocol blanchet basic" in blanchet["scm_code"]


def test_agentic_searcher_multi_tool_loop():
    """Verify `run_agentic_cpsa_searcher` executes structured tool calls and returns
    diagnosis + KB rules + working .scm example.
    """
    spec = _make_sample_spec()
    mock_resp_turn1 = MagicMock()
    mock_resp_turn1.choices = [
        MagicMock(
            message=MagicMock(
                content=json.dumps({
                    "is_final": False,
                    "ast_root_cause": "Nonce n is encrypted under (pubk b) without Responder knowing (privk b).",
                    "actionable_fix": "Add (privk b) to Responder inputs.",
                    "tool_calls": [
                        {
                            "tool": "read_section",
                            "section_id": "01_core_rules/07_compiler_and_solver_error_catalog#1.1-received-term-cannot-be-fully-destructured",
                        },
                        {
                            "tool": "read_scm_example",
                            "filename": "ns.scm",
                        },
                    ],
                })
            )
        )
    ]
    mock_resp_turn2 = MagicMock()
    mock_resp_turn2.choices = [
        MagicMock(
            message=MagicMock(
                content=json.dumps({
                    "is_final": True,
                    "ast_root_cause": "Responder lacks decryption key (privk b) in its inputs list.",
                    "actionable_fix": "Declare (privk b) in role inputs so cpsa4roletran can destructure the recv term.",
                    "tool_calls": [],
                })
            )
        )
    ]

    with patch("src.rag_retriever_client.litellm.completion", side_effect=[mock_resp_turn1, mock_resp_turn2]):
        guidance = run_agentic_cpsa_searcher(
            error_diagnostic="roletran: Received term cannot be fully destructured (enc n (pubk b))",
            failure_stage="roletran",
            failing_spec=spec,
            cycle_detected=True,
        )

    assert "Agentic Searcher AST Diagnosis" in guidance
    assert "Responder lacks decryption key" in guidance
    assert "Received term cannot be fully destructured" in guidance
    assert "ns.scm" in guidance


def test_two_speed_repair_trigger_skips_searcher_on_fast_attempt_and_escalates():
    """Verify `repair_protocol_specification` skips the Agentic Searcher when
    `use_agentic_searcher=False` and invokes it when `use_agentic_searcher=True`.
    """
    spec = _make_sample_spec()
    mock_repair_resp = MagicMock()
    mock_repair_resp.choices = [
        MagicMock(message=MagicMock(content=spec.model_dump_json()))
    ]

    with patch("src.verification_engine.compiler_diagnostic_repair.run_agentic_cpsa_searcher") as mock_searcher, \
         patch("src.verification_engine.compiler_diagnostic_repair.litellm.completion", return_value=mock_repair_resp):
        # Attempt 1: Fast direct repair (use_agentic_searcher=False) -> searcher NOT called
        repaired_1 = repair_protocol_specification(
            failing_spec=spec,
            error_diagnostic="Cannot build (enc n (pubk b))",
            verbatim_slice="RFC slice",
            failure_stage="roletran",
            cycle_detected=False,
            use_agentic_searcher=False,
        )
        assert repaired_1.protocol_name == "test-proto"
        assert mock_searcher.call_count == 0

        # Escalated attempt (use_agentic_searcher=True) -> searcher IS called
        mock_searcher.return_value = "--- Agentic Searcher AST Diagnosis ---\nAdd variable to inputs."
        repaired_2 = repair_protocol_specification(
            failing_spec=spec,
            error_diagnostic="Cannot build (enc n (pubk b))",
            verbatim_slice="RFC slice",
            failure_stage="roletran",
            cycle_detected=False,
            use_agentic_searcher=True,
        )
        assert repaired_2.protocol_name == "test-proto"
        assert mock_searcher.call_count == 1
