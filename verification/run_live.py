"""Checkpointed StudioNet matrix. Uses only the two local test wallets."""
import base64
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from genlayer_py import create_account, create_client
from genlayer_py.abi import calldata
from genlayer_py.abi.transactions import serialize
from genlayer_py.chains import studionet

ROOT = Path(__file__).resolve().parents[1]
ADDRESS = os.environ.get("AWARDTRACE_CONTRACT_ADDRESS", "")
RPC = "https://studio.genlayer.com/api"
OCID = "ocds-b5fd17-9b2e0c20-6781-471b-8b29-c2d639187ed0"
RELEASE = "a55ff105-de10-4260-b843-e16e40642436"
DIGEST = "88049adca6e69542352867906d1b234cf3f698e36121db02e20892cecf2f278a"
TEST_ENV = ROOT.parent / "EvidenceBasedGrantEscrow" / ".env.lifecycle"
PRIVATE = ROOT / ".private" / ("live-" + ADDRESS.lower() + ".json")
PUBLIC = ROOT / "verification" / ("live-" + ADDRESS.lower() + ".json")


def rpc(method, params):
    if method not in {"eth_chainId", "eth_getBalance", "eth_getTransactionByHash", "gen_getContractCode", "gen_call"}:
        raise RuntimeError("RPC_METHOD_NOT_ALLOWED")
    last = None
    for attempt in range(5):
        try:
            response = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=60)
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                raise RuntimeError(str(data["error"]))
            return data["result"]
        except (requests.RequestException, ValueError) as error:
            last = error
            if attempt < 4:
                time.sleep(3 * (attempt + 1))
    raise RuntimeError("RPC_READ_UNAVAILABLE:" + str(last))


def view(method, args=None, sender="0x0000000000000000000000000000000000000001"):
    encoded = serialize([calldata.encode({"method": method, "args": args or []}), b"\x00"])
    raw = rpc("gen_call", [{"type": "read", "to": ADDRESS, "from": sender, "value": "0x0",
                            "data": encoded, "transaction_hash_variant": "latest-final"}])
    return str(calldata.decode(bytes.fromhex(raw.removeprefix("0x"))))


def keys():
    values = {}
    for raw in TEST_ENV.read_text(encoding="utf-8").splitlines():
        if raw.strip() and not raw.lstrip().startswith("#") and "=" in raw:
            key, value = raw.split("=", 1)
            values[key.strip()] = value.strip()
    result = [os.environ.get("WALLET_A_PRIVATE_KEY") or values.get("WALLET_A_PRIVATE_KEY"),
              os.environ.get("WALLET_B_PRIVATE_KEY") or values.get("WALLET_B_PRIVATE_KEY")]
    if not all(result):
        raise RuntimeError("TWO_LOCAL_TEST_KEYS_REQUIRED")
    return result


def tx_return(tx):
    receipts = (tx.get("consensus_data") or {}).get("leader_receipt") or []
    receipts = [receipts] if isinstance(receipts, dict) else receipts
    leaders = [item for item in receipts if item.get("mode") == "leader"]
    if not leaders or leaders[-1].get("execution_result") != "SUCCESS":
        raise RuntimeError("LEADER_EXECUTION_FAILED")
    result = leaders[-1].get("result")
    raw = base64.b64decode(result["raw"] if isinstance(result, dict) else result)
    if not raw or raw[0] != 0:
        raise RuntimeError("CONTRACT_EXECUTION_ERROR")
    return str(calldata.decode(raw[1:]))


def save(record):
    PRIVATE.parent.mkdir(exist_ok=True)
    PRIVATE.write_text(json.dumps(record, indent=2), encoding="utf-8")
    PUBLIC.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def main():
    if not ADDRESS.startswith("0x") or len(ADDRESS) != 42:
        raise RuntimeError("AWARDTRACE_CONTRACT_ADDRESS_REQUIRED")
    if int(rpc("eth_chainId", []), 16) != 61999:
        raise RuntimeError("WRONG_CHAIN")
    deployed = base64.b64decode(rpc("gen_getContractCode", [ADDRESS]))
    local = (ROOT / "contracts" / "AwardTrace.py").read_bytes()
    if deployed != local:
        raise RuntimeError("SOURCE_PARITY_FAILED")
    source_hash = hashlib.sha256(local).hexdigest()
    secret_keys = keys()
    accounts = [create_account(account_private_key="0x" + key.removeprefix("0x")) for key in secret_keys]
    del secret_keys
    steward, auditor = accounts
    clients = {account.address.lower(): create_client(chain=studionet, account=account) for account in accounts}
    balances = {account.address: int(rpc("eth_getBalance", [account.address, "latest"]), 16) for account in accounts}
    if not all(balances.values()):
        raise RuntimeError("TEST_WALLET_BALANCE_EMPTY")
    count = int(view("get_counts", sender=steward.address))
    watch = str(count)
    plan = [
        {"id": "F1-invalid-watch", "actor": steward.address, "method": "create_watch",
         "args": ["bad ocid", RELEASE, DIGEST], "allowed": ["INVALID_WATCH"]},
        {"id": "H1-create-watch", "actor": steward.address, "method": "create_watch",
         "args": [OCID, RELEASE, DIGEST], "allowed": [watch]},
        {"id": "A1-auditor-anchor", "actor": auditor.address, "method": "anchor_criteria",
         "args": [watch], "allowed": ["OWNER_ONLY"]},
        {"id": "F2-premature-assess", "actor": auditor.address, "method": "assess_award",
         "args": [watch], "allowed": ["AWARD_NOT_ASSESSABLE"]},
        {"id": "H2-anchor-criteria", "actor": steward.address, "method": "anchor_criteria",
         "args": [watch], "allowed": ["CRITERIA_ANCHORED"]},
        {"id": "H3-bind-award", "actor": steward.address, "method": "bind_award",
         "args": [watch, RELEASE, DIGEST], "allowed": ["AWARD_BOUND"]},
        {"id": "H4-auditor-assess", "actor": auditor.address, "method": "assess_award",
         "args": [watch], "allowed": ["FULLY_TRACED", "GAPS_PRESENT", "PUBLISHED_CONFLICT", "INSUFFICIENT_OFFICIAL_EVIDENCE", "IDENTITY_CONFLICT"]},
        {"id": "A2-auditor-correction", "actor": auditor.address, "method": "append_correction",
         "args": [watch, RELEASE, DIGEST], "allowed": ["OWNER_ONLY"]},
        {"id": "H5-freeze", "actor": steward.address, "method": "freeze_trace",
         "args": [watch], "allowed": ["TRACE_FROZEN"]},
        {"id": "F3-correction-after-freeze", "actor": steward.address, "method": "append_correction",
         "args": [watch, RELEASE, DIGEST], "allowed": ["CORRECTION_NOT_APPENDABLE"]},
    ]
    record = {"contract": ADDRESS, "network": "StudioNet", "source_sha256": source_hash,
              "started_at": datetime.now(timezone.utc).isoformat(), "wallets": [a.address for a in accounts],
              "start_count": count, "watch_id": watch, "steps": [], "complete": False}
    save(record)
    for item in plan:
        hash_value = str(clients[item["actor"].lower()].write_contract(address=ADDRESS,
                         function_name=item["method"], args=item["args"], value=0, leader_only=False))
        print(json.dumps({"id": item["id"], "hash": hash_value, "status": "SUBMITTED"}), flush=True)
        deadline = time.monotonic() + 1200
        while time.monotonic() < deadline:
            tx = rpc("eth_getTransactionByHash", [hash_value])
            if tx and tx.get("status") == "FINALIZED":
                if tx.get("result_name") != "MAJORITY_AGREE":
                    raise RuntimeError(item["id"] + ":CONSENSUS_FAILED")
                actual = tx_return(tx)
                if actual not in item["allowed"]:
                    raise RuntimeError(item["id"] + ":UNEXPECTED_RETURN:" + actual)
                state = view("get_watch", [watch], sender=auditor.address) if item["id"] != "F1-invalid-watch" else "NOT_CREATED"
                record["steps"].append({"id": item["id"], "actor": item["actor"], "method": item["method"],
                                        "hash": hash_value, "return": actual, "state_after": state,
                                        "status": "READBACK_VERIFIED"})
                save(record)
                print(json.dumps(record["steps"][-1]), flush=True)
                break
            time.sleep(5)
        else:
            raise RuntimeError(item["id"] + ":FINALITY_TIMEOUT")
    record["final_watch"] = json.loads(view("get_watch", [watch], sender=auditor.address))
    record["final_revision"] = json.loads(view("get_revision", [watch, "0"], sender=auditor.address))
    record["complete"] = True
    record["completed_at"] = datetime.now(timezone.utc).isoformat()
    save(record)
    print(json.dumps({"complete": True, "watch_id": watch, "steps": len(record["steps"])}))


if __name__ == "__main__":
    main()
