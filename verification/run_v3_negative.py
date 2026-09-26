"""Run the reviewer-requested v3 negative-source matrix with two local test wallets."""
import json
import os
import time
from datetime import datetime, timezone

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

from verification.run_live import ROOT, DIGEST, OCID, RELEASE, keys, rpc, save, tx_return, view

ADDRESS = os.environ.get("AWARDTRACE_CONTRACT_ADDRESS", "")
CORRECTION_ROLE = "0x1111111111111111111111111111111111111111"


def wait_final(hash_value: str) -> tuple[str, dict]:
    deadline = time.monotonic() + 1200
    while time.monotonic() < deadline:
        transaction = rpc("eth_getTransactionByHash", [hash_value])
        if transaction and transaction.get("status") == "FINALIZED":
            if transaction.get("result_name") != "MAJORITY_AGREE":
                raise RuntimeError("CONSENSUS_FAILED")
            return tx_return(transaction), transaction
        time.sleep(5)
    raise RuntimeError("FINALITY_TIMEOUT")


def main() -> None:
    if len(ADDRESS) != 42:
        raise RuntimeError("AWARDTRACE_CONTRACT_ADDRESS_REQUIRED")
    secrets = keys()
    accounts = [create_account(account_private_key="0x" + secret.removeprefix("0x")) for secret in secrets]
    del secrets
    tender, award = accounts
    clients = [create_client(chain=studionet, account=account) for account in accounts]
    watch_id = str(int(view("get_counts", sender=tender.address)))
    plan = [
        ("H1-create-role-separated-watch", 0, "create_watch",
         [OCID, RELEASE, DIGEST, award.address, CORRECTION_ROLE], watch_id),
        ("A1-award-wallet-cannot-anchor", 1, "anchor_criteria", [watch_id], "TENDER_PUBLISHER_ONLY"),
        ("F1-premature-assessment", 1, "assess_award", [watch_id], "AWARD_NOT_ASSESSABLE"),
        ("F2-no-published-criteria", 0, "anchor_criteria", [watch_id], "CRITERIA_NOT_PUBLISHED"),
    ]
    path = ROOT / "verification" / ("v3-negative-" + ADDRESS.lower() + ".json")
    record = {"contract": ADDRESS, "network": "StudioNet", "schema": "role-separated-cited-procurement-trace-v1",
              "started_at": datetime.now(timezone.utc).isoformat(), "watch_id": watch_id,
              "actors": {"tender": tender.address, "award": award.address, "correction_reserved": CORRECTION_ROLE},
              "source": {"ocid": OCID, "release_id": RELEASE, "sha256": DIGEST}, "steps": [], "complete": False}
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    for step_id, actor_index, method, args, expected in plan:
        hash_value = str(clients[actor_index].write_contract(address=ADDRESS, function_name=method,
                                                             args=args, value=0, leader_only=False))
        actual, _ = wait_final(hash_value)
        if actual != expected:
            raise RuntimeError(step_id + ":UNEXPECTED_RETURN:" + actual)
        state = json.loads(view("get_watch", [watch_id], sender=award.address))
        record["steps"].append({"id": step_id, "actor": accounts[actor_index].address, "method": method,
                                "hash": hash_value, "explorer": "https://explorer-studio.genlayer.com/tx/" + hash_value,
                                "return": actual, "state_after": state, "status": "READBACK_VERIFIED"})
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record["steps"][-1]), flush=True)
    record["final_watch"] = json.loads(view("get_watch", [watch_id], sender=award.address))
    record["complete"] = True
    record["completed_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete": True, "watch_id": watch_id, "steps": len(record["steps"])}))


if __name__ == "__main__":
    main()
