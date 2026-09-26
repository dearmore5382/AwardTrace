# AwardTrace

AwardTrace is a GenLayer dApp that creates a criterion-level, append-only trace between an official public-procurement notice and its published award reasoning. It does **not** decide legality, fairness, corruption, or value for money.

## Architecture

This is a temporal evidence ledger, not a one-shot document reviewer. A tender publisher commits a tender release whose actual published evaluation criteria are extracted with source pointers. A distinct award publisher binds a later award release. An independent caller can then trigger a criterion-by-criterion assessment whose consequential relations cite exact published award-rationale passages. A third correction publisher can append later corrections; earlier revisions remain readable.

```text
official release -> exact-byte verification -> criteria anchor
                                             |
official award  -> exact-byte verification -> criterion trace -> revision chain -> freeze
```

## Trust and source boundary

- Authority: UK Cabinet Office Contracts Finder OCDS release service.
- Positive evidence URL: derived by the contract from a validated release GUID; callers cannot supply arbitrary URLs.
- Binding: OCID + release GUID + raw response SHA-256 + contract state.
- Source outage: returns `SOURCE_RETRYABLE` and does not create positive state.
- Digest or OCID mismatch: returns an explicit integrity/identity failure and does not create positive state.
- AI output: one bounded relation/citation vector, independently re-executed by validators. Criterion IDs, tender source pointers, cited award excerpts, identity flag, amendment flag, trace JSON, and summary are validated or derived deterministically.
- Role and chronology guards: tender, award, and correction publishers are distinct; releases cannot be reused across roles; award/correction timestamps must advance.
- Synthetic fixtures: unit tests only, never represented as live authority.

## Roles

- Primary wallet: deploys the contract only.
- Tender publisher: creates the watch and anchors published criteria.
- Award publisher: binds the independent later award release.
- Correction publisher: appends an independent later correction release.
- Public auditor: invokes the permissionless assessment and verifies public readback.

Private keys are never committed or bundled into the frontend. The browser uses an injected wallet and `genlayer-js`.

## State machine

`MONITORING -> CRITERIA_ANCHORED -> AWARD_BOUND -> TRACE_OPEN -> FROZEN`

Each assessed correction creates a new immutable revision with a parent pointer. Summary values are `FULLY_TRACED`, `GAPS_PRESENT`, `PUBLISHED_CONFLICT`, `INSUFFICIENT_OFFICIAL_EVIDENCE`, or `IDENTITY_CONFLICT`.

## Verify locally

```powershell
python -m pytest -q
python -m py_compile contracts\AwardTrace.py
genvm-lint check contracts\AwardTrace.py
genvm-lint typecheck contracts\AwardTrace.py
npm run build
```

The reviewer-requested v3 source currently passes 21 Python tests, GenVM lint, and a production frontend build. A new StudioNet deployment and new role-separated live evidence are still required before resubmission.

## Deploy and operate

1. Deploy [`contracts/AwardTrace.py`](contracts/AwardTrace.py) in GenLayer Studio with the primary wallet.
2. Paste the resulting address into the frontend; it is stored only in local browser storage.
3. Connect test wallet A and run create/anchor/bind.
4. Connect test wallet B and run assessment; record the finalized transaction and authoritative state readback.
5. Reconnect test wallet A for correction/freeze operations.
6. Add only real Explorer URLs and transaction hashes to the evidence packet.

See [`docs/VERIFICATION_GUIDE.md`](docs/VERIFICATION_GUIDE.md), [`docs/TEST_RESOURCE_MANIFEST.md`](docs/TEST_RESOURCE_MANIFEST.md), [`docs/EVIDENCE_PACKET.md`](docs/EVIDENCE_PACKET.md), and the clickable [`verification/LIVE_RESULTS.md`](verification/LIVE_RESULTS.md) on-chain transaction index.

## Current deployment truth

The v3 StudioNet deployment is `0xc710672c3B2815Ba0cc945Ff86260cdB591B0BaB`. Its deployed bytes exactly match `contracts/AwardTrace.py` (`27,050` bytes, SHA-256 `9fa542c9e939345470afb74c744f955499efe7b92a5acb0c16063f7e45dbe724`) and `get_contract_version` returns schema `role-separated-cited-procurement-trace-v1`, version `3`. The prior deployment `0x3587E5d4cc060718a4b7E4b2aA77A6AcC7f44aC1` is superseded. New role-separated live evidence is still required before resubmission.

Live frontend: https://awardtrace.pages.dev
