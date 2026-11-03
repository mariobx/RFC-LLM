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


def test_cost_tracker_per_role_and_batch_telemetry():
    """Verify `PipelineCostTracker` accurately computes per-role (`router`, `extraction`,
    `query`, `repair`) and batch USD costs and token counts, and emits `cost_updated` events.
    """
    import pytest
    from src.cost_tracker import PipelineCostTracker
    from src.pipeline_events import GLOBAL_EVENT_BUS

    tracker = PipelineCostTracker()
    tracker._catalog_fetched = True  # Use deterministic fallback table in unit tests

    captured_events = []
    GLOBAL_EVENT_BUS.subscribe(captured_events.append)
    try:
        tracker.start_rfc(
            rfc_id="RFC 9999",
            router_model="nous/z-ai/glm-5.3-flash",
            extraction_model="nous/openai/gpt-6.1-terra",
            query_model="nous/anthropic/claude-haiku-5.5",
            repair_model="nous/google/gemini-3.7-flash",
        )

        # 1. Router call: 1,000 prompt + 200 completion on glm-5.3-flash ($0.12/1M in, $0.40/1M out)
        resp_router = {
            "usage": {"prompt_tokens": 1000, "completion_tokens": 200}
        }
        tracker.record_llm_call(resp_router, role="router", model_name="nous/z-ai/glm-5.3-flash", stage=1)

        # 2. Extraction call: 5,000 prompt + 1,000 completion on gpt-6.1-terra ($1.00/1M in, $5.00/1M out)
        resp_extract = {
            "usage": {"prompt_tokens": 5000, "completion_tokens": 1000}
        }
        tracker.record_llm_call(resp_extract, role="extraction", model_name="nous/openai/gpt-6.1-terra", stage=2)

        # 3. Query call: 2,000 prompt + 500 completion on claude-haiku-5.5 ($0.10/1M in, $0.50/1M out)
        resp_query = {
            "usage": {"prompt_tokens": 2000, "completion_tokens": 500}
        }
        tracker.record_llm_call(resp_query, role="query", model_name="nous/anthropic/claude-haiku-5.5", stage=5)

        # 4. Repair call: 4,000 prompt + 1,000 completion on gemini-3.7-flash ($0.75/1M in, $3.75/1M out)
        resp_repair = {
            "usage": {"prompt_tokens": 4000, "completion_tokens": 1000}
        }
        rfc_summary = tracker.record_llm_call(
            resp_repair, role="repair", model_name="nous/google/gemini-3.7-flash", stage=5
        )

        assert rfc_summary["total_calls"] == 4
        assert rfc_summary["total_tokens"] == (1200 + 6000 + 2500 + 5000)
        assert rfc_summary["roles"]["router"]["cost_usd"] == pytest.approx(0.0002, rel=1e-4)
        assert rfc_summary["roles"]["extraction"]["cost_usd"] == pytest.approx(0.0100, rel=1e-4)
        assert rfc_summary["roles"]["query"]["cost_usd"] == pytest.approx(0.00045, rel=1e-4)
        assert rfc_summary["roles"]["repair"]["cost_usd"] == pytest.approx(0.00675, rel=1e-4)
        assert rfc_summary["total_cost_usd"] == pytest.approx(0.0174, rel=1e-4)

        cli_line = tracker.format_cli_summary(rfc_summary, prefix="RFC Run Cost")
        assert "RFC Run Cost: $0.0174" in cli_line
        assert "Extraction: $0.0100" in cli_line
        assert "Repair: $0.006" in cli_line

        cost_evts = [e for e in captured_events if e.event_type == "cost_updated"]
        assert len(cost_evts) == 4
        assert cost_evts[-1].data["rfc_cost"]["total_cost_usd"] == pytest.approx(0.0174, rel=1e-4)
    finally:
        GLOBAL_EVENT_BUS.unsubscribe(captured_events.append)


def test_snowball_error_classification_and_15s_timeout():
    """Verify default CPSA compile timeout is 15s and `is_snowball_state_error` strictly
    isolates state-space snowball errors from ordinary compiler/roletran diagnostics.
    """
    from src.system_config import SYSTEM_CONFIG
    from src.verification_engine.snowball_autopsy import (
        inject_herald_options_into_scm,
        is_snowball_state_error,
    )

    assert SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS == 15

    # Snowball state errors -> True
    assert is_snowball_state_error(
        "MITRE CPSA compilation timed out after 15 seconds (state-space explosion / infinite strand loop)"
    )
    assert is_snowball_state_error("cpsa4: Step limit exceeded")
    assert is_snowball_state_error("cpsa4: Strand bound exceeded")
    assert is_snowball_state_error("cpsa4: Heap exhausted;")

    # Every other compiler/roletran/syntax error -> False
    assert not is_snowball_state_error("cpsa4: Identifier foo unknown")
    assert not is_snowball_state_error("roletran: Received term cannot be fully destructured")
    assert not is_snowball_state_error("cpsa4: Malformed encryption term")
    assert not is_snowball_state_error("cpsa4: Sort mismatch in defstrand")
    assert not is_snowball_state_error("")
    assert not is_snowball_state_error(None)

    # Herald flag injection into .scm
    scm_in = '(herald "Test Protocol" (algebra diffie-hellman))\n\n(defprotocol p diffie-hellman)'
    scm_out = inject_herald_options_into_scm(scm_in, ["try-old-strands", "check-nonces"])
    assert '(herald "Test Protocol" (algebra diffie-hellman) (try-old-strands) (check-nonces))' in scm_out


def test_snowball_tier1_herald_portfolio_and_non_snowball_bypass(tmp_path):
    """Verify non-snowball errors bypass Tier 1/Tier 2 immediately, whereas snowball errors
    trigger the Tier 1 deterministic herald search-order portfolio and persist winning flags.
    """
    import pytest
    from src.verification_engine.mitre_build_orchestrator import (
        CPSABuildError,
        execute_mitre_make_build,
    )

    scm_file = tmp_path / "proto.scm"
    scm_file.write_text('(herald "Proto")\n(defprotocol proto basic)\n', encoding="utf-8")

    # 1. Non-snowball error -> must NOT run Tier 1 portfolio (only 1 call to _run_make_with_hard_timeout)
    with patch("src.verification_engine.mitre_build_orchestrator._ensure_cpsa_makefile"), \
         patch(
             "src.verification_engine.mitre_build_orchestrator._run_make_with_hard_timeout",
             return_value=(2, "", "cpsa4: Identifier bad_var unknown"),
         ) as mock_make:
        with pytest.raises(CPSABuildError) as exc_info:
            execute_mitre_make_build(scm_file, tmp_path, build_full_graph=False)
        assert "Identifier bad_var unknown" in str(exc_info.value)
        assert mock_make.call_count == 1

    # 2. Snowball error on Pass 0 -> Tier 1 Strategy #1 (`--try-old-strands`) resolves it!
    call_counter = {"n": 0}

    def _fake_make_side_effect(cmd, cwd, env, timeout_seconds):
        call_counter["n"] += 1
        if call_counter["n"] == 1:
            raise CPSABuildError(
                "MITRE CPSA compilation timed out after 15 seconds (state-space explosion / infinite strand loop)"
            )
        # Strategy #1 (`--try-old-strands`) succeeds and writes expected build artifacts
        (cwd / "proto.txt").write_text("(defskeleton proto (shape))", encoding="utf-8")
        (cwd / "proto_shapes.txt").write_text("(defskeleton proto (shape))", encoding="utf-8")
        (cwd / "proto_shapes.xhtml").write_text("<html/>", encoding="utf-8")
        return (0, "ok", "")

    with patch("src.verification_engine.mitre_build_orchestrator._ensure_cpsa_makefile"), \
         patch(
             "src.verification_engine.mitre_build_orchestrator._run_make_with_hard_timeout",
             side_effect=_fake_make_side_effect,
         ):
        artifacts = execute_mitre_make_build(scm_file, tmp_path, build_full_graph=False)
        assert artifacts.winning_herald_options == ["try-old-strands"]
        assert "(try-old-strands)" in scm_file.read_text(encoding="utf-8")


def test_snowball_tier2_autopsy_report_and_tier3_prompt_isolation():
    """Verify `analyze_snowball_trace_text` extracts the exact repeating `(added-strand ...)`
    operation, critical term, and cloned primed variables, and `repair_protocol_specification`
    injects Tier 3 snowball directives ONLY on snowball errors.
    """
    from src.verification_engine.snowball_autopsy import analyze_snowball_trace_text

    sample_snowball_txt = """
(herald "Looping Protocol")
(defprotocol loop_proto basic)
(defskeleton loop_proto
  (vars (n data) (a b name) (ch chan))
  (defstrand init 2 (n n) (a a) (b b) (ch ch))
  (label 0)
  (unrealized (0 1))
  (comment "POV 1 (Initiator)"))

(defskeleton loop_proto
  (vars (n n-0 data) (a b a-0 b-0 name) (ch ch-0 chan))
  (defstrand init 2 (n n) (a a) (b b) (ch ch))
  (defstrand resp 2 (n n-0) (a a-0) (b b-0) (ch ch-0))
  (operation encryption-test (added-strand resp 2) (enc n-0 a-0 (ltk a-0 b-0)) (0 1))
  (label 1)
  (parent 0)
  (unrealized (1 0)))

(defskeleton loop_proto
  (vars (n n-0 n-1 data) (a b a-0 b-0 a-1 b-1 name) (ch ch-0 ch-1 chan))
  (defstrand init 2 (n n) (a a) (b b) (ch ch))
  (defstrand resp 2 (n n-0) (a a-0) (b b-0) (ch ch-0))
  (defstrand resp 2 (n n-1) (a a-1) (b b-1) (ch ch-1))
  (operation encryption-test (added-strand resp 2) (enc n-1 a-1 (ltk a-1 b-1)) (1 0))
  (label 2)
  (parent 1)
  (unrealized (2 0)))
"""
    report = analyze_snowball_trace_text(sample_snowball_txt)
    assert "CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT" in report
    assert "resp (height 2): 2x" in report
    assert "encryption-test" in report
    assert "(added-strand resp 2)" in report
    assert "(enc n-* a-* (ltk a-* b-*))" in report
    assert "a:name (cloned 2x as a-0..a-1)" in report
    assert "DOMAIN-SEPARATE EVERY `(enc ...)` AND `(hash ...)` TERM" in report

    # Verify Tier 3 prompt injection is strictly isolated to snowball errors
    spec = _make_sample_spec()
    mock_repair_resp = MagicMock()
    mock_repair_resp.choices = [MagicMock(message=MagicMock(content=spec.model_dump_json()))]

    captured_prompts = []

    def _capture_completion(**kwargs):
        captured_prompts.append(kwargs["messages"][1]["content"])
        return mock_repair_resp

    with patch("src.verification_engine.compiler_diagnostic_repair.run_agentic_cpsa_searcher", return_value="KB Rules"), \
         patch("src.verification_engine.compiler_diagnostic_repair.litellm.completion", side_effect=_capture_completion):
        # Normal error -> NO Tier-3 snowball block in prompt
        repair_protocol_specification(
            failing_spec=spec,
            error_diagnostic="Cannot build (enc n (pubk b))",
            verbatim_slice="RFC slice",
            failure_stage="solver",
            use_agentic_searcher=False,
        )
        assert "MANDATORY TIER-3 SNOWBALL STATE RECOVERY PROTOCOL" not in captured_prompts[-1]

        # Snowball error -> Tier-3 snowball block IS in prompt
        repair_protocol_specification(
            failing_spec=spec,
            error_diagnostic=f"MITRE CPSA compilation timed out after 15 seconds\n\n{report}",
            verbatim_slice="RFC slice",
            failure_stage="solver",
            use_agentic_searcher=False,
        )
        assert "MANDATORY TIER-3 SNOWBALL STATE RECOVERY PROTOCOL" in captured_prompts[-1]
        assert "CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT" in captured_prompts[-1]


def test_csv_logger_upsert_overwrites_by_rfc_id_and_logs_all_model_columns(tmp_path):
    """Verify `PipelineMetricsCSVLogger` performs in-place upserts keyed by normalized `rfc_id`,
    increments `run_count`, saves `scm_path` regardless of pass/fail, and logs dedicated columns
    for every model role (`router`, `extraction`, `query`, `repair`).
    """
    import csv
    from src.logging_config import PipelineMetricsCSVLogger

    csv_file = tmp_path / "pipeline_runs.csv"
    logger_csv = PipelineMetricsCSVLogger(csv_path=csv_file)
    assert len(PipelineMetricsCSVLogger.CSV_HEADER) == 48

    scm_file = tmp_path / "mobile_ipv6.scm"
    scm_file.write_text("(herald test)\n(defprotocol p basic)\n", encoding="utf-8")
    traj_file = tmp_path / "mobile_ipv6_trajectory.json"
    shapes_file = tmp_path / "mobile_ipv6_shapes.xhtml"

    fake_cost_1 = {
        "total_calls": 5,
        "total_tokens": 25000,
        "total_cost_usd": 0.045,
        "roles": {
            "router": {"model": "nous/z-ai/glm-5.3", "calls": 2, "total_tokens": 3000, "cost_usd": 0.0012},
            "extraction": {"model": "nous/openai/gpt-6.1-terra", "calls": 1, "total_tokens": 12000, "cost_usd": 0.0280},
            "query": {"model": "nous/anthropic/claude-haiku-5.5", "calls": 1, "total_tokens": 2000, "cost_usd": 0.0008},
            "repair": {"model": "nous/google/gemini-3.7-flash", "calls": 1, "total_tokens": 8000, "cost_usd": 0.0150},
        },
    }

    # 1. First run of RFC 4285 fails in Stage 6, but scm_path is still saved!
    logger_csv.log_run(
        rfc_id="rfc 4285",
        is_eligible=True,
        status="PARTIAL",
        quality_tier="REJECTED",
        protocol_name="Mobile IPv6 Auth",
        message_algebra="basic",
        selected_sections=["5", "5.1"],
        sliced_lines_count=242,
        role_count=3,
        preskeleton_count=3,
        roletran_passed=True,
        solver_passed=False,
        roletran_repairs=1,
        solver_repairs=2,
        searcher_invocations=1,
        duration_seconds=45.2,
        cost_telemetry=fake_cost_1,
        scm_path=scm_file,
        trajectory_json_path=traj_file,
        error_message="Step limit exceeded",
    )

    with open(csv_file, "r", encoding="utf-8") as f:
        rows_1 = list(csv.DictReader(f))
    assert len(rows_1) == 1
    r1 = rows_1[0]
    assert r1["rfc_id"] == "RFC4285"
    assert r1["run_count"] == "1"
    assert r1["status"] == "PARTIAL"
    assert r1["scm_path"] == str(scm_file)
    assert r1["scm_lines_count"] == "2"
    assert r1["router_model"] == "nous/z-ai/glm-5.3"
    assert r1["router_cost_usd"] == "0.001200"
    assert r1["extraction_model"] == "nous/openai/gpt-6.1-terra"
    assert r1["extraction_cost_usd"] == "0.028000"
    assert r1["query_model"] == "nous/anthropic/claude-haiku-5.5"
    assert r1["query_cost_usd"] == "0.000800"
    assert r1["repair_model"] == "nous/google/gemini-3.7-flash"
    assert r1["repair_cost_usd"] == "0.015000"
    assert r1["total_cost_usd"] == "0.045000"

    # 2. Re-run of RFC4285 succeeds -> overwrites existing row in-place and increments run_count to 2!
    logger_csv.log_run(
        rfc_id="RFC4285",
        is_eligible=True,
        status="VERIFIED",
        quality_tier="GOLD",
        protocol_name="Mobile IPv6 Auth",
        message_algebra="basic",
        selected_sections=["5", "5.1"],
        sliced_lines_count=242,
        role_count=3,
        preskeleton_count=3,
        roletran_passed=True,
        solver_passed=True,
        shapes_count=4,
        explored_skeletons_count=18,
        all_povs_multi_strand=True,
        secrecy_proved=True,
        roletran_repairs=0,
        solver_repairs=0,
        herald_options=["try-old-strands"],
        duration_seconds=12.4,
        cost_telemetry=fake_cost_1,
        scm_path=scm_file,
        shapes_xhtml_path=shapes_file,
        trajectory_json_path=traj_file,
        error_message=None,
    )

    with open(csv_file, "r", encoding="utf-8") as f:
        rows_2 = list(csv.DictReader(f))
    assert len(rows_2) == 1  # Overwritten in-place, NOT duplicated!
    r2 = rows_2[0]
    assert r2["rfc_id"] == "RFC4285"
    assert r2["run_count"] == "2"
    assert r2["status"] == "VERIFIED"
    assert r2["quality_tier"] == "GOLD"
    assert r2["zero_shot_passed"] == "True"
    assert r2["herald_options"] == "try-old-strands"
    assert r2["shapes_xhtml_path"] == str(shapes_file)
    assert r2["error_message"] == ""



