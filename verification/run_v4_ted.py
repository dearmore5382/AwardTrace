"""Finalized TED v5 three-release matrix using two local test wallets."""
import base64
import hashlib
import json
import os
import time
from datetime import datetime, timezone

from genlayer_py import create_account, create_client

from run_live import ROOT, rpc, tx_return
from run_live import keys as load_keys

ADDRESS = os.environ.get("AWARDTRACE_CONTRACT_ADDRESS", "")
PROCEDURE = "c7a1e838-29fc-420d-a45a-8b3c2b2ebdd1"
TENDER = "470710-2023"
AWARD = "1424-2024"
CORRECTION = "538997-2024"
EXPLORER = "https://explorer-studio.genlayer.com/tx/"


def view(method, args=None, sender="0x0000000000000000000000000000000000000001"):
    from genlayer_py.abi import calldata
    from genlayer_py.abi.transactions import serialize
    encoded = serialize([calldata.encode({"method": method, "args": args or []}), b"\x00"])
    raw = rpc("gen_call", [{"type": "read", "to": ADDRESS, "from": sender, "value": "0x0",
                            "data": encoded, "transaction_hash_variant": "latest-final"}])
    return str(calldata.decode(bytes.fromhex(raw.removeprefix("0x"))))


def main():
    deployed = base64.b64decode(rpc("gen_getContractCode", [ADDRESS]))
    local = (ROOT / "contracts" / "AwardTrace.py").read_bytes()
    if deployed != local: raise RuntimeError("SOURCE_PARITY_FAILED")
    private_keys = load_keys()
    accounts = [create_account(account_private_key="0x" + key.removeprefix("0x")) for key in private_keys]
    del private_keys
    curator, auditor = accounts
    clients = {a.address.lower(): create_client(chain=__import__("genlayer_py.chains", fromlist=["studionet"]).studionet, account=a) for a in accounts}
    balances = {a.address: int(rpc("eth_getBalance", [a.address, "latest"]), 16) for a in accounts}
    if not all(balances.values()): raise RuntimeError("TEST_WALLET_BALANCE_EMPTY")
    case_id = view("get_counts", sender=curator.address)
    plan = [
        ("F1-invalid-case", curator, "create_case", ["bad", TENDER, auditor.address], "INVALID_CASE", False),
        ("H1-create", curator, "create_case", [PROCEDURE, TENDER, auditor.address], case_id, True),
        ("A1-auditor-cannot-anchor", auditor, "anchor_tender", [case_id], "CURATOR_ONLY", True),
        ("F2-premature-assessment", auditor, "assess_award", [case_id], "AWARD_NOT_ASSESSABLE", True),
        ("H2-anchor-tender", curator, "anchor_tender", [case_id], "TENDER_ANCHORED", True),
        ("F3-reuse-tender-as-award", curator, "bind_award", [case_id, TENDER], "INVALID_AWARD_NOTICE", True),
        ("H3-bind-award", curator, "bind_award", [case_id, AWARD], "AWARD_BOUND", True),
        ("A2-curator-cannot-assess", curator, "assess_award", [case_id], "AUDITOR_ONLY", True),
        ("H4-independent-assessment", auditor, "assess_award", [case_id],
         ("FULLY_TRACED", "GAPS_PRESENT", "PUBLISHED_CONFLICT", "INSUFFICIENT_OFFICIAL_EVIDENCE"), True),
        ("F4-award-reused-as-correction", curator, "append_correction", [case_id, AWARD], "NOTICE_ROLE_REUSE", True),
        ("H5-bind-correction", curator, "append_correction", [case_id, CORRECTION], "CORRECTION_BOUND", True),
        ("A3-curator-cannot-assess-correction", curator, "assess_correction", [case_id], "AUDITOR_ONLY", True),
        ("H6-assess-correction", auditor, "assess_correction", [case_id],
         ("FULLY_TRACED", "GAPS_PRESENT", "PUBLISHED_CONFLICT", "INSUFFICIENT_OFFICIAL_EVIDENCE"), True),
        ("F5-correction-release-reuse", curator, "append_correction", [case_id, CORRECTION], "NOTICE_ROLE_REUSE", True),
        ("H7-freeze", curator, "freeze_trace", [case_id], "TRACE_FROZEN", True),
        ("F6-correction-after-freeze", curator, "append_correction", [case_id, "538998-2024"], "CORRECTION_NOT_APPENDABLE", True),
    ]
    output = {"contract": ADDRESS, "network": "StudioNet", "source_sha256": hashlib.sha256(local).hexdigest(),
              "official_sources": {"procedure_id": PROCEDURE, "tender": TENDER, "award": AWARD, "correction": CORRECTION},
              "wallets": {"curator": curator.address, "auditor": auditor.address}, "balances": balances,
              "case_id": case_id, "started_at": datetime.now(timezone.utc).isoformat(), "steps": [], "complete": False}
    target = ROOT / "verification" / ("v5-ted-" + ADDRESS.lower() + ".json")
    for step_id, actor, method, args, expected, read_case in plan:
        tx_hash = str(clients[actor.address.lower()].write_contract(address=ADDRESS, function_name=method,
                                                                    args=args, value=0, leader_only=False))
        deadline = time.monotonic() + 1500
        while time.monotonic() < deadline:
            tx = rpc("eth_getTransactionByHash", [tx_hash])
            if tx and tx.get("status") == "FINALIZED":
                if tx.get("result_name") != "MAJORITY_AGREE": raise RuntimeError(step_id + ":CONSENSUS_FAILED")
                actual = tx_return(tx)
                allowed = expected if isinstance(expected, tuple) else (expected,)
                if actual not in allowed: raise RuntimeError(step_id + ":UNEXPECTED:" + actual)
                state = json.loads(view("get_case", [case_id], auditor.address)) if read_case else "NOT_CREATED"
                output["steps"].append({"id": step_id, "actor": actor.address, "method": method,
                    "return": actual, "tx_hash": tx_hash, "explorer": EXPLORER + tx_hash, "state_after": state})
                target.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
                print(json.dumps(output["steps"][-1]), flush=True)
                break
            time.sleep(5)
        else: raise RuntimeError(step_id + ":FINALITY_TIMEOUT")
    output["final_case"] = json.loads(view("get_case", [case_id], auditor.address))
    output["final_revisions"] = [json.loads(view("get_revision", [case_id, str(index)], auditor.address))
                                 for index in range(output["final_case"]["revision_count"])]
    output["complete"] = True
    output["completed_at"] = datetime.now(timezone.utc).isoformat()
    target.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete": True, "case_id": case_id, "steps": len(output["steps"]), "file": str(target)}))


if __name__ == "__main__": main()
