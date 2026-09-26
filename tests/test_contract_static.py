from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "contracts" / "AwardTrace.py").read_text(encoding="utf-8")


def test_header_ascii_and_ast():
    assert SOURCE.startswith("# v0.2.16\n# { \"Depends\":")
    SOURCE.encode("ascii")
    ast.parse(SOURCE)


def test_official_source_is_derived_not_arbitrary():
    assert "contractsfinder.service.gov.uk/Published/Notice/releases/" in SOURCE
    assert "def _release_url" in SOURCE
    assert "url:" not in SOURCE


def test_append_only_revision_surface():
    for name in ("create_watch", "anchor_criteria", "bind_award", "assess_award", "append_correction", "freeze_trace"):
        assert "def " + name in SOURCE
    assert "revision_parents" in SOURCE
    assert "revision_traces" in SOURCE


def test_no_money_or_direct_ai_verdict_surface():
    lowered = SOURCE.lower()
    assert "emit_transfer" not in lowered
    assert "payable" not in lowered
    assert "gl.nondet.exec_prompt" in SOURCE
    assert "def _derive" in SOURCE


def test_criteria_are_deterministic_and_trace_is_audited():
    assert "def _criteria_from_release" in SOURCE
    assert "def _parse_relation_line" in SOURCE
    assert "gl.vm.run_nondet_unsafe" in SOURCE
    assert "pipe-delimited line" in SOURCE
    assert 'response_format="json"' not in SOURCE


def test_missing_criteria_is_normalized_by_leader_and_validator():
    assert SOURCE.count('{"source_status": "CRITERIA_NOT_PUBLISHED"}') >= 2
    assert "except Exception:" in SOURCE
