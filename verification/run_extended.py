"""Additional real-source StudioNet evidence: integrity, identity and revision lineage."""
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

from run_live import rpc, view, keys, tx_return, OCID, RELEASE, DIGEST

ROOT = Path(__file__).resolve().parents[1]
ADDRESS = os.environ.get("AWARDTRACE_CONTRACT_ADDRESS", "")
PUBLIC = ROOT / "verification" / ("extended-" + ADDRESS.lower() + ".json")
WRONG_OCID = "ocds-b5fd17-00000000-0000-4000-8000-000000000000"
WRONG_DIGEST = DIGEST[:-1] + ("0" if DIGEST[-1] != "0" else "1")


def main():
    if not ADDRESS.startswith("0x") or len(ADDRESS) != 42:
        raise RuntimeError("AWARDTRACE_CONTRACT_ADDRESS_REQUIRED")
    local = (ROOT / "contracts" / "AwardTrace.py").read_bytes()
    import base64
    if base64.b64decode(rpc("gen_getContractCode", [ADDRESS])) != local:
        raise RuntimeError("SOURCE_PARITY_FAILED")
    private_keys = keys()
    accounts = [create_account(account_private_key="0x" + value.removeprefix("0x")) for value in private_keys]
    del private_keys
    steward, auditor = accounts
    clients = {account.address.lower(): create_client(chain=studionet, account=account) for account in accounts}
    start = int(view("get_counts", sender=steward.address))
    integrity_watch, identity_watch, revision_watch = str(start), str(start + 1), str(start + 2)
    plan = [
        ("D1-create-wrong-digest", steward.address, "create_watch", [OCID, RELEASE, WRONG_DIGEST], integrity_watch, [integrity_watch]),
        ("D2-anchor-wrong-digest", steward.address, "anchor_criteria", [integrity_watch], integrity_watch, ["INTEGRITY_FAILURE"]),
        ("I1-create-wrong-identity", steward.address, "create_watch", [WRONG_OCID, RELEASE, DIGEST], identity_watch, [identity_watch]),
        ("I2-anchor-wrong-identity", steward.address, "anchor_criteria", [identity_watch], identity_watch, ["IDENTITY_FAILURE"]),
        ("R1-create", steward.address, "create_watch", [OCID, RELEASE, DIGEST], revision_watch, [revision_watch]),
        ("R2-anchor", steward.address, "anchor_criteria", [revision_watch], revision_watch, ["CRITERIA_ANCHORED"]),
        ("R3-bind", steward.address, "bind_award", [revision_watch, RELEASE, DIGEST], revision_watch, ["AWARD_BOUND"]),
        ("R4-auditor-assess", auditor.address, "assess_award", [revision_watch], revision_watch,
         ["FULLY_TRACED", "GAPS_PRESENT", "PUBLISHED_CONFLICT", "INSUFFICIENT_OFFICIAL_EVIDENCE", "IDENTITY_CONFLICT"]),
        ("R5-append-authenticated-revision", steward.address, "append_correction", [revision_watch, RELEASE, DIGEST], revision_watch,
         ["FULLY_TRACED", "GAPS_PRESENT", "PUBLISHED_CONFLICT", "INSUFFICIENT_OFFICIAL_EVIDENCE", "IDENTITY_CONFLICT"]),
        ("R6-freeze", steward.address, "freeze_trace", [revision_watch], revision_watch, ["TRACE_FROZEN"]),
    ]
    record = {"contract": ADDRESS, "network": "StudioNet", "source_sha256": hashlib.sha256(local).hexdigest(),
              "official_source": {"ocid": OCID, "release": RELEASE, "sha256": DIGEST},
              "started_at": datetime.now(timezone.utc).isoformat(), "steps": [], "complete": False}
    PUBLIC.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    for step_id, actor, method, args, watch_id, allowed in plan:
        tx_hash = str(clients[actor.lower()].write_contract(address=ADDRESS, function_name=method,
                                                            args=args, value=0, leader_only=False))
        print(json.dumps({"id": step_id, "hash": tx_hash, "status": "SUBMITTED"}), flush=True)
        deadline = time.monotonic() + 1200
        while time.monotonic() < deadline:
            tx = rpc("eth_getTransactionByHash", [tx_hash])
            if tx and tx.get("status") == "FINALIZED":
                if tx.get("result_name") != "MAJORITY_AGREE":
                    raise RuntimeError(step_id + ":CONSENSUS_FAILED")
                actual = tx_return(tx)
                if actual not in allowed:
                    raise RuntimeError(step_id + ":UNEXPECTED_RETURN:" + actual)
                state = view("get_watch", [watch_id], sender=auditor.address)
                item = {"id": step_id, "actor": actor, "method": method, "hash": tx_hash,
                        "return": actual, "state_after": state, "status": "READBACK_VERIFIED"}
                record["steps"].append(item)
                PUBLIC.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                print(json.dumps(item), flush=True)
                break
            time.sleep(5)
        else:
            raise RuntimeError(step_id + ":FINALITY_TIMEOUT")
    final_watch = json.loads(view("get_watch", [revision_watch], sender=auditor.address))
    revision_zero = json.loads(view("get_revision", [revision_watch, "0"], sender=auditor.address))
    revision_one = json.loads(view("get_revision", [revision_watch, "1"], sender=auditor.address))
    if final_watch["status"] != "FROZEN" or final_watch["revision_count"] != 2 or revision_one["parent"] != "0":
        raise RuntimeError("REVISION_READBACK_MISMATCH")
    record.update({"integrity_watch": integrity_watch, "identity_watch": identity_watch,
                   "revision_watch": revision_watch, "final_watch": final_watch,
                   "revision_zero": revision_zero, "revision_one": revision_one,
                   "complete": True, "completed_at": datetime.now(timezone.utc).isoformat(),
                   "semantic_conflict_proven": False,
                   "semantic_conflict_note": "The official OCID exposes one current release URL; no independent same-OCID conflicting byte snapshot was available."})
    PUBLIC.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete": True, "steps": len(record["steps"]), "revision_watch": revision_watch}))


if __name__ == "__main__":
    main()
