from pathlib import Path
import importlib
import json
import sys
from unittest.mock import patch

from gltest.direct import VMContext, create_address, deploy_contract

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "AwardTrace.py"
OCID = "ocds-b5fd17-test-object-001"
RELEASE = "a55ff105-de10-4260-b843-e16e40642436"
AWARD_RELEASE = "award-release-001"
DIGEST = "1" * 64


def deploy():
    owner, award, correction, outsider = (create_address("owner"), create_address("award"),
                                          create_address("correction"), create_address("outsider"))
    vm = VMContext(owner)
    with patch("os.unlink", lambda _path: None):
        with vm.activate():
            contract = deploy_contract(CONTRACT, vm)
            proxy = contract._instance.create_watch.__globals__["gl"]
            _ = proxy.nondet
            _ = proxy.vm
    sdk_root = str(Path(proxy._cached_gl.__file__).resolve().parents[2])
    if sdk_root not in sys.path:
        sys.path.insert(0, sdk_root)
    importlib.import_module("genlayer")
    return vm, contract, owner, award, correction, outsider


def address(value):
    if isinstance(value, bytes):
        return "0x" + value.hex()
    value = str(value)
    return "0x" + value[5:] if value.startswith("addr#") else value


def sync(vm, contract):
    proxy = contract._instance.create_watch.__globals__["gl"]
    sender = vm.sender
    message = proxy.message
    if isinstance(sender, bytes):
        sender = type(message.sender_address)(sender)
    proxy._cached_gl.message = message._replace(sender_address=sender, origin_address=sender,
                                                 value=type(message.value)(vm.value))
    proxy._cached_gl.message_raw["sender_address"] = sender
    proxy._cached_gl.message_raw["origin_address"] = sender


def criteria():
    return [{"criterion_id": "C1", "text": "Service quality and delivery resilience", "weight_band": "HIGH",
             "source_pointer": "/releases/0/tender/awardCriteriaDetails"},
            {"criterion_id": "C2", "text": "Whole-life cost", "weight_band": "MEDIUM",
             "source_pointer": "/releases/0/tender/documents/0/description"}]


def trace(relation="ADDRESSED", reference="/releases/0/awards/0/rationale"):
    return [{"criterion_id": "C1", "award_reference": reference, "award_excerpt": "Quality evidence scored strongly", "relation": relation,
             "amendment_controls": False, "identity_consistent": True},
            {"criterion_id": "C2", "award_reference": "/releases/0/awards/0/description", "award_excerpt": "Price and quality were balanced", "relation": "ADDRESSED",
             "amendment_controls": False, "identity_consistent": True}]


def create(vm, contract, award, correction):
    with vm.activate():
        sync(vm, contract)
        return contract.create_watch(OCID, RELEASE, DIGEST, address(award), address(correction))


def test_create_validation_and_owner_binding():
    vm, contract, owner, award, correction, _ = deploy()
    with vm.activate():
        sync(vm, contract)
        assert contract.create_watch("bad ocid", RELEASE, DIGEST, address(award), address(correction)) == "INVALID_WATCH"
    assert create(vm, contract, award, correction) == "0"
    record = json.loads(contract.get_watch("0"))
    assert record["owner"].lower() == ("0x" + bytes(owner).hex()).lower()
    assert record["status"] == "MONITORING"


def test_owner_only_anchor_and_retry_no_mutation():
    vm, contract, _, award, correction, outsider = deploy()
    create(vm, contract, award, correction)
    with vm.prank(outsider), vm.activate():
        sync(vm, contract)
        assert contract.anchor_criteria("0") == "TENDER_PUBLISHER_ONLY"
    with vm.activate(), patch.object(contract._instance, "_criteria_consensus", return_value={"source_status": "UNAVAILABLE"}):
        sync(vm, contract)
        assert contract.anchor_criteria("0") == "SOURCE_RETRYABLE"
        assert json.loads(contract.get_watch("0"))["status"] == "MONITORING"


def test_happy_lifecycle_append_only_and_freeze():
    vm, contract, _, award, correction, outsider = deploy()
    create(vm, contract, award, correction)
    with vm.activate(), patch.object(contract._instance, "_criteria_consensus", return_value={"source_status": "VERIFIED", "criteria": criteria(), "released_at": "2026-01-01T00:00:00Z"}):
        sync(vm, contract)
        assert contract.anchor_criteria("0") == "CRITERIA_ANCHORED"
    with vm.prank(award), vm.activate():
        sync(vm, contract)
        assert contract.bind_award("0", AWARD_RELEASE, DIGEST) == "AWARD_BOUND"
    with vm.prank(outsider), vm.activate(), patch.object(contract._instance, "_trace_consensus", return_value={"source_status": "VERIFIED", "trace": trace(), "released_at": "2026-02-01T00:00:00Z"}):
        sync(vm, contract)
        assert contract.assess_award("0") == "FULLY_TRACED"
    with vm.prank(correction), vm.activate(), patch.object(contract._instance, "_trace_consensus", return_value={"source_status": "VERIFIED", "trace": trace(), "released_at": "2026-03-01T00:00:00Z"}):
        sync(vm, contract)
        assert contract.append_correction("0", "correction-001", DIGEST) == "FULLY_TRACED"
    with vm.activate():
        sync(vm, contract)
        assert contract.freeze_trace("0") == "TRACE_FROZEN"
    first = json.loads(contract.get_revision("0", "0"))
    second = json.loads(contract.get_revision("0", "1"))
    assert first["parent"] == "" and second["parent"] == "0"
    assert first["trace"] == trace()


def test_wrong_digest_closes_no_positive_state():
    vm, contract, _, award, correction, _ = deploy()
    create(vm, contract, award, correction)
    with vm.activate(), patch.object(contract._instance, "_criteria_consensus", return_value={"source_status": "INTEGRITY_FAILURE"}):
        sync(vm, contract)
        assert contract.anchor_criteria("0") == "INTEGRITY_FAILURE"
        assert json.loads(contract.get_watch("0"))["status"] == "MONITORING"


def test_deterministic_summary_matrix():
    module = deploy()[1]._instance.create_watch.__globals__
    derive = module["_derive"]
    assert derive(trace()) == "FULLY_TRACED"
    assert derive(trace("OMITTED")) == "GAPS_PRESENT"
    assert derive(trace("CONTRADICTED")) == "PUBLISHED_CONFLICT"
    assert derive(trace("UNCLEAR")) == "INSUFFICIENT_OFFICIAL_EVIDENCE"


def test_trace_parser_binds_every_consequential_field():
    module = deploy()[1]._instance.create_watch.__globals__
    parser = module["_parse_trace"]
    locked = criteria()
    assert parser(trace(), locked) != parser(trace(reference="/releases/0/awards/0/description"), locked)
    changed = trace()
    changed[0]["amendment_controls"] = True
    assert parser(trace(), locked) != parser(changed, locked)
    assert parser({"trace": trace()}, locked) == parser(trace(), locked)


def test_relation_line_is_bounded_and_ordered():
    module = deploy()[1]._instance.create_watch.__globals__
    parser = module["_parse_relation_line"]
    locked = criteria()
    passages = [{"pointer": "/releases/0/awards/0/rationale", "excerpt": "Quality evidence scored strongly"}]
    assert parser("ADDRESSED@P0|UNCLEAR@NONE", locked, passages) == [{"relation": "ADDRESSED", "citation": "P0"}, {"relation": "UNCLEAR", "citation": "NONE"}]
    for invalid in ("ADDRESSED", "ADDRESSED@NONE|YES", "ADDRESSED@P0|UNCLEAR@NONE\nextra", {"trace": []}):
        try:
            parser(invalid, locked, passages)
            assert False, "invalid relation output must fail"
        except Exception:
            pass


def test_trace_metadata_is_derived_not_model_authored():
    module = deploy()[1]._instance.create_watch.__globals__
    passages = [{"pointer": "/releases/0/awards/0/rationale", "excerpt": "Quality evidence scored strongly"}]
    built = module["_trace_from_relations"](criteria(), [{"relation": "ADDRESSED", "citation": "P0"}, {"relation": "OMITTED", "citation": "NONE"}],
                                             {"amendments": [{"id": "a1"}]}, passages)
    assert [item["criterion_id"] for item in built] == ["C1", "C2"]
    assert [item["relation"] for item in built] == ["ADDRESSED", "OMITTED"]
    assert built[0]["award_reference"] == "/releases/0/awards/0/rationale" and built[1]["award_reference"] == ""
    assert all(item["identity_consistent"] is True for item in built)
    assert all(item["amendment_controls"] is True for item in built)


def test_trace_parser_rejects_wrapper_key_injection():
    module = deploy()[1]._instance.create_watch.__globals__
    parser = module["_parse_trace"]
    try:
        parser({"trace": trace(), "verdict": "FULLY_TRACED"}, criteria())
        assert False, "wrapper key injection must fail"
    except Exception:
        pass


def test_duplicate_and_wrong_state_guards():
    vm, contract, _, award, correction, _ = deploy()
    create(vm, contract, award, correction)
    with vm.prank(award), vm.activate():
        sync(vm, contract)
        assert contract.bind_award("0", AWARD_RELEASE, DIGEST) == "AWARD_NOT_BINDABLE"
        assert contract.assess_award("0") == "AWARD_NOT_ASSESSABLE"
    with vm.activate():
        sync(vm, contract)
        assert contract.freeze_trace("0") == "TRACE_NOT_FREEZABLE"


def test_extracts_only_published_criteria_with_source_pointers():
    module = deploy()[1]._instance.create_watch.__globals__
    release = {"tender": {"awardCriteriaDetails": "Quality 60%; price 40%",
                          "documents": [{"documentType": "evaluationCriteria",
                                         "description": "Technical method statement scoring"}]}}
    extracted = module["_criteria_from_release"](release)
    assert [item["text"] for item in extracted] == ["Quality 60%; price 40%", "Technical method statement scoring"]
    assert all(item["source_pointer"].startswith("/releases/0/tender/") for item in extracted)
    try:
        module["_criteria_from_release"]({"tender": {"title": "Scope is not evaluation criteria"}})
        assert False, "scope text must not be promoted into evaluation criteria"
    except Exception:
        pass


def test_award_rationale_passages_are_pointer_bound():
    module = deploy()[1]._instance.create_watch.__globals__
    passages = module["_award_passages"]({"awards": [{"rationale": "Highest combined quality score",
                                                        "documents": [{"description": "Evaluation panel report"}]}]})
    assert passages == [{"pointer": "/releases/0/awards/0/rationale", "excerpt": "Highest combined quality score"},
                        {"pointer": "/releases/0/awards/0/documents/0/description", "excerpt": "Evaluation panel report"}]


def test_release_role_reuse_and_chronology_fail_closed():
    vm, contract, _, award, correction, outsider = deploy()
    create(vm, contract, award, correction)
    with vm.activate(), patch.object(contract._instance, "_criteria_consensus", return_value={"source_status": "VERIFIED", "criteria": criteria(), "released_at": "2026-02-01T00:00:00Z"}):
        sync(vm, contract)
        assert contract.anchor_criteria("0") == "CRITERIA_ANCHORED"
    with vm.prank(award), vm.activate():
        sync(vm, contract)
        assert contract.bind_award("0", RELEASE, DIGEST) == "RELEASE_ROLE_REUSE"
        assert contract.bind_award("0", AWARD_RELEASE, DIGEST) == "AWARD_BOUND"
    with vm.prank(outsider), vm.activate(), patch.object(contract._instance, "_trace_consensus", return_value={"source_status": "VERIFIED", "trace": trace(), "released_at": "2026-01-01T00:00:00Z"}):
        sync(vm, contract)
        assert contract.assess_award("0") == "NON_CHRONOLOGICAL_RELEASE"
        assert json.loads(contract.get_watch("0"))["status"] == "AWARD_BOUND"
