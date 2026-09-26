from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "contracts" / "AwardTrace.py").read_text(encoding="utf-8")


def test_header_ascii_and_ast():
    assert SOURCE.startswith('# v0.2.16\n# { "Depends":')
    SOURCE.encode("ascii")
    ast.parse(SOURCE)


def test_ted_adapter_is_fixed_and_query_is_derived():
    assert "https://api.ted.europa.eu/v3/notices/search" in SOURCE
    assert '"query": "publication-number = " + number' in SOURCE
    assert 'method="POST"' in SOURCE
    assert "procedure-identifier" in SOURCE


def test_two_party_phase_separated_surface():
    for name in ("create_case", "anchor_tender", "bind_award", "assess_award",
                 "append_correction", "assess_correction", "freeze_trace"):
        assert "def " + name in SOURCE
    assert "CURATOR_ONLY" in SOURCE
    assert "AUDITOR_ONLY" in SOURCE
    assert "WRONG_NOTICE_PHASE" in SOURCE
    assert "NOTICE_ROLE_REUSE" in SOURCE


def test_consensus_and_bounded_ai_output():
    assert "gl.vm.run_nondet(" in SOURCE
    assert SOURCE.count("gl.vm.run_nondet(") >= 2
    assert "def _parse_relations" in SOURCE
    assert "UNCITED_CONSEQUENTIAL_RELATION" in SOURCE
    assert 'fields = ("award-criterion-order-justification-lot"' in SOURCE
    assert '"modification-description"' in SOURCE
    assert '"winner-name", "winner-decision-date"' not in SOURCE.split("def _passages", 1)[1].split("def _phase", 1)[0]
    assert "def _derive" in SOURCE
    assert "json.loads(proposal.calldata) == json.loads(evaluate())" not in SOURCE


def test_no_money_or_arbitrary_source_surface():
    lowered = SOURCE.lower()
    assert "emit_transfer" not in lowered
    assert "payable" not in lowered
    assert "url: str" not in SOURCE
