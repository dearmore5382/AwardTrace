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
DIGEST = "1" * 64


def deploy():
    owner, outsider = create_address("owner"), create_address("outsider")
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
    return vm, contract, owner, outsider


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
    return [{"criterion_id": "C1", "text": "Service quality and delivery resilience", "weight_band": "HIGH"},
            {"criterion_id": "C2", "text": "Whole-life cost", "weight_band": "MEDIUM"}]


def trace(relation="ADDRESSED", reference="award.rationale[0]"):
    return [{"criterion_id": "C1", "award_reference": reference, "relation": relation,
             "amendment_controls": False, "identity_consistent": True},
            {"criterion_id": "C2", "award_reference": "award.rationale[1]", "relation": "ADDRESSED",
             "amendment_controls": False, "identity_consistent": True}]


def create(vm, contract):
    with vm.activate():
        sync(vm, contract)
        return contract.create_watch(OCID, RELEASE, DIGEST)


def test_create_validation_and_owner_binding():
    vm, contract, owner, _ = deploy()
    with vm.activate():
        sync(vm, contract)
        assert contract.create_watch("bad ocid", RELEASE, DIGEST) == "INVALID_WATCH"
    assert create(vm, contract) == "0"
    record = json.loads(contract.get_watch("0"))
    assert record["owner"].lower() == ("0x" + bytes(owner).hex()).lower()
    assert record["status"] == "MONITORING"


def test_owner_only_anchor_and_retry_no_mutation():
    vm, contract, _, outsider = deploy()
    create(vm, contract)
    with vm.prank(outsider), vm.activate():
        sync(vm, contract)
        assert contract.anchor_criteria("0") == "OWNER_ONLY"
    with vm.activate(), patch.object(contract._instance, "_criteria_consensus", return_value={"source_status": "UNAVAILABLE"}):
        sync(vm, contract)
        assert contract.anchor_criteria("0") == "SOURCE_RETRYABLE"
        assert json.loads(contract.get_watch("0"))["status"] == "MONITORING"


def test_happy_lifecycle_append_only_and_freeze():
    vm, contract, _, _ = deploy()
    create(vm, contract)
    with vm.activate(), patch.object(contract._instance, "_criteria_consensus", return_value={"source_status": "VERIFIED", "criteria": criteria()}):
        sync(vm, contract)
        assert contract.anchor_criteria("0") == "CRITERIA_ANCHORED"
        assert contract.bind_award("0", RELEASE, DIGEST) == "AWARD_BOUND"
    with vm.activate(), patch.object(contract._instance, "_trace_consensus", return_value={"source_status": "VERIFIED", "trace": trace()}):
        sync(vm, contract)
        assert contract.assess_award("0") == "FULLY_TRACED"
        assert contract.append_correction("0", "correction-001", DIGEST) == "FULLY_TRACED"
        assert contract.freeze_trace("0") == "TRACE_FROZEN"
    first = json.loads(contract.get_revision("0", "0"))
    second = json.loads(contract.get_revision("0", "1"))
    assert first["parent"] == "" and second["parent"] == "0"
    assert first["trace"] == trace()


def test_wrong_digest_closes_no_positive_state():
    vm, contract, _, _ = deploy()
    create(vm, contract)
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
    assert parser(trace(), locked) != parser(trace(reference="different passage"), locked)
    changed = trace()
    changed[0]["amendment_controls"] = True
    assert parser(trace(), locked) != parser(changed, locked)
    assert parser({"trace": trace()}, locked) == parser(trace(), locked)


def test_relation_line_is_bounded_and_ordered():
    module = deploy()[1]._instance.create_watch.__globals__
    parser = module["_parse_relation_line"]
    locked = criteria()
    assert parser("ADDRESSED|UNCLEAR", locked) == ["ADDRESSED", "UNCLEAR"]
    for invalid in ("ADDRESSED", "ADDRESSED|YES", "ADDRESSED|UNCLEAR\nextra", {"trace": []}):
        try:
            parser(invalid, locked)
            assert False, "invalid relation output must fail"
        except Exception:
            pass


def test_trace_metadata_is_derived_not_model_authored():
    module = deploy()[1]._instance.create_watch.__globals__
    built = module["_trace_from_relations"](criteria(), ["ADDRESSED", "OMITTED"],
                                             {"amendments": [{"id": "a1"}]})
    assert [item["criterion_id"] for item in built] == ["C1", "C2"]
    assert [item["relation"] for item in built] == ["ADDRESSED", "OMITTED"]
    assert all(item["award_reference"] == "releases[0]" for item in built)
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
    vm, contract, _, _ = deploy()
    create(vm, contract)
    with vm.activate():
        sync(vm, contract)
        assert contract.bind_award("0", RELEASE, DIGEST) == "AWARD_NOT_BINDABLE"
        assert contract.assess_award("0") == "AWARD_NOT_ASSESSABLE"
        assert contract.freeze_trace("0") == "TRACE_NOT_FREEZABLE"
