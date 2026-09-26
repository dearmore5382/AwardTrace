from pathlib import Path
import importlib
import json
import sys
from unittest.mock import patch

import pytest
from gltest.direct import VMContext, create_address, deploy_contract

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "AwardTrace.py"
PROCEDURE = "f78fe5bc-095c-4053-a1de-8c63d1154e15"


def address(value):
    return "0x" + bytes(value).hex() if isinstance(value, bytes) else str(value).replace("addr#", "0x")


def deploy():
    owner, auditor, outsider = create_address("owner"), create_address("auditor"), create_address("outsider")
    vm = VMContext(owner)
    with patch("os.unlink", lambda _path: None), vm.activate():
        contract = deploy_contract(CONTRACT, vm)
        proxy = contract._instance.create_case.__globals__["gl"]
        _ = proxy.nondet; _ = proxy.vm
    sdk_root = str(Path(proxy._cached_gl.__file__).resolve().parents[2])
    if sdk_root not in sys.path: sys.path.insert(0, sdk_root)
    importlib.import_module("genlayer")
    return vm, contract, owner, auditor, outsider


def sync(vm, contract):
    proxy = contract._instance.create_case.__globals__["gl"]
    sender, message = vm.sender, proxy.message
    if isinstance(sender, bytes): sender = type(message.sender_address)(sender)
    proxy._cached_gl.message = message._replace(sender_address=sender, origin_address=sender,
                                                  value=type(message.value)(vm.value))
    proxy._cached_gl.message_raw["sender_address"] = sender
    proxy._cached_gl.message_raw["origin_address"] = sender


def criteria():
    return [{"criterion_id":"C1", "type":"PRICE", "text":"Price", "weight":"per-exa",
             "source_pointer":"award-criterion-name-lot/0"}]


def trace(relation="ADDRESSED"):
    return [{"criterion_id":"C1", "relation":relation,
             "award_reference":"award-criterion-order-justification-lot/0",
             "award_excerpt":"Lowest price is the sole criterion because requirements are fixed."}]


def test_parser_extracts_real_eforms_fields_and_phases():
    module = deploy()[1]._instance.create_case.__globals__
    notice = {"award-criterion-name-lot":{"deu":["Preis"]},
              "award-criterion-description-lot":{"deu":["Preis"]},
              "award-criterion-type-lot":["price"], "notice-type":"cn-standard"}
    assert module["_criteria"](notice)[0]["text"] == "Preis"
    assert module["_phase"](notice) == "TENDER"
    assert module["_phase"]({"notice-type":"can-standard"}) == "AWARD"
    assert module["_phase"]({"notice-type":"can-modif"}) == "CORRECTION"


def test_relation_parser_and_summary_are_fail_closed():
    module = deploy()[1]._instance.create_case.__globals__
    assert module["_relations"]({"relations":[" addressed "]}, 1) == ["ADDRESSED"]
    with pytest.raises(Exception): module["_relations"]({"relations":["SUPPORTED"]}, 1)
    with pytest.raises(Exception): module["_relations"]({"relations":[], "reason":"extra"}, 1)
    assert module["_derive"](trace("CONTRADICTED")) == "PUBLISHED_CONFLICT"
    assert module["_derive"](trace("ADDRESSED")) == "FULLY_TRACED"
    assert module["_derive"](trace("OMITTED")) == "GAPS_PRESENT"
    assert module["_derive"](trace("UNCLEAR")) == "INSUFFICIENT_OFFICIAL_EVIDENCE"


def test_only_rationale_and_modification_fields_can_be_cited():
    module = deploy()[1]._instance.create_case.__globals__
    notice = {"award-criterion-name-lot":{"eng":["Price"]}, "winner-name":["Supplier"],
              "award-criterion-order-justification-lot":{"eng":["Lowest price is justified by fixed specifications."]},
              "modification-description":{"eng":["Unit prices were amended."]}}
    award = module["_passages"](notice, "AWARD")
    correction = module["_passages"](notice, "CORRECTION")
    assert [item["pointer"] for item in award] == ["award-criterion-order-justification-lot/0"]
    assert [item["pointer"] for item in correction] == ["modification-description/0"]


def test_two_wallet_happy_path_and_authorization():
    vm, contract, owner, auditor, outsider = deploy()
    with vm.activate():
        sync(vm, contract)
        assert contract.create_case(PROCEDURE, "616030-2024", address(auditor)) == "0"
        contract._instance._source_consensus = lambda *_: {"source_status":"VERIFIED", "source_binding":"tender",
            "publication_date":"2024-10-11", "criteria":criteria()}
        assert contract.anchor_tender("0") == "TENDER_ANCHORED"
        assert contract.bind_award("0", "4-2025") == "AWARD_BOUND"
    vm.sender = outsider
    with vm.activate():
        sync(vm, contract)
        assert contract.assess_award("0") == "AUDITOR_ONLY"
    vm.sender = auditor
    with vm.activate():
        sync(vm, contract)
        contract._instance._assessment_consensus = lambda *_: {"source_status":"VERIFIED",
            "source_binding":"award", "publication_date":"2025-01-02", "criteria":criteria(), "trace":trace()}
        assert contract.assess_award("0") == "FULLY_TRACED"
    record = json.loads(contract.get_case("0"))
    assert record["status"] == "TRACE_OPEN"
    assert record["revision_count"] == 1
    assert json.loads(contract.get_revision("0", "0"))["summary"] == "FULLY_TRACED"


def test_role_reuse_and_chronology_guards():
    vm, contract, _, auditor, _ = deploy()
    with vm.activate():
        sync(vm, contract)
        assert contract.create_case(PROCEDURE, "616030-2024", address(auditor)) == "0"
        contract._instance._source_consensus = lambda *_: {"source_status":"VERIFIED", "source_binding":"tender",
            "publication_date":"2024-10-11", "criteria":criteria()}
        assert contract.anchor_tender("0") == "TENDER_ANCHORED"
        assert contract.bind_award("0", "616030-2024") == "INVALID_AWARD_NOTICE"
        assert contract.bind_award("0", "4-2025") == "AWARD_BOUND"
    vm.sender = auditor
    with vm.activate():
        sync(vm, contract)
        contract._instance._assessment_consensus = lambda *_: {"source_status":"VERIFIED",
            "source_binding":"award", "publication_date":"2024-01-01", "trace":trace()}
        assert contract.assess_award("0") == "NON_CHRONOLOGICAL_NOTICE"
        assert json.loads(contract.get_case("0"))["revision_count"] == 0


def test_correction_is_distinct_append_only_revision():
    vm, contract, owner, auditor, _ = deploy()
    with vm.activate():
        sync(vm, contract)
        assert contract.create_case(PROCEDURE, "470710-2023", address(auditor)) == "0"
        contract._instance._source_consensus = lambda *_: {"source_status":"VERIFIED", "source_binding":"tender",
            "publication_date":"2023-08-02"}
        assert contract.anchor_tender("0") == "TENDER_ANCHORED"
        assert contract.bind_award("0", "1424-2024") == "AWARD_BOUND"
    vm.sender = auditor
    with vm.activate():
        sync(vm, contract)
        contract._instance._assessment_consensus = lambda *_: {"source_status":"VERIFIED",
            "source_binding":"award", "publication_date":"2024-01-02", "criteria":criteria(), "trace":trace()}
        assert contract.assess_award("0") == "FULLY_TRACED"
    vm.sender = owner
    with vm.activate():
        sync(vm, contract)
        contract._instance._source_consensus = lambda *_: {"source_status":"VERIFIED", "source_binding":"correction",
            "publication_date":"2024-09-09"}
        assert contract.append_correction("0", "538997-2024") == "CORRECTION_BOUND"
        record = json.loads(contract.get_case("0"))
        assert record["award_notice"] == "1424-2024"
        assert record["correction_notice"] == "538997-2024"
    vm.sender = auditor
    with vm.activate():
        sync(vm, contract)
        contract._instance._assessment_consensus = lambda *_: {"source_status":"VERIFIED",
            "source_binding":"correction", "publication_date":"2024-09-09", "criteria":criteria(),
            "trace":trace("OMITTED")}
        assert contract.assess_correction("0") == "GAPS_PRESENT"
        assert json.loads(contract.get_case("0"))["revision_count"] == 2
    vm.sender = owner
    with vm.activate():
        sync(vm, contract)
        assert contract.append_correction("0", "538997-2024") == "NOTICE_ROLE_REUSE"
