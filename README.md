# AwardTrace

AwardTrace is a GenLayer dApp that creates a criterion-level, append-only trace between an official public-procurement notice and its published award reasoning. It does **not** decide legality, fairness, corruption, or value for money.

## Architecture

This is a temporal evidence ledger, not a one-shot document reviewer. A steward first commits an official release identity and raw-byte digest, criteria are anchored, an award release is bound later, and an independent caller can trigger a criterion-by-criterion intelligent assessment. Corrections become child revisions; earlier revisions remain readable.

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
- AI output: one bounded pipe-delimited relation vector, independently re-executed by validators. Criterion IDs, source locator, identity flag, amendment flag, trace JSON, and summary are derived deterministically.
- Synthetic fixtures: unit tests only, never represented as live authority.

## Roles

- Primary wallet: deploys the contract only.
- Test wallet A: procurement steward; creates the watch, anchors criteria, binds the award, appends corrections, and freezes.
- Test wallet B: independent public auditor; invokes the permissionless assessment and verifies public readback.

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

The current verified result is 18 passing Python tests, a successful static production build, and two finalized StudioNet journals with authoritative readback.

## Deploy and operate

1. Deploy [`contracts/AwardTrace.py`](contracts/AwardTrace.py) in GenLayer Studio with the primary wallet.
2. Paste the resulting address into the frontend; it is stored only in local browser storage.
3. Connect test wallet A and run create/anchor/bind.
4. Connect test wallet B and run assessment; record the finalized transaction and authoritative state readback.
5. Reconnect test wallet A for correction/freeze operations.
6. Add only real Explorer URLs and transaction hashes to the evidence packet.

See [`docs/VERIFICATION_GUIDE.md`](docs/VERIFICATION_GUIDE.md), [`docs/TEST_RESOURCE_MANIFEST.md`](docs/TEST_RESOURCE_MANIFEST.md), [`docs/EVIDENCE_PACKET.md`](docs/EVIDENCE_PACKET.md), and the clickable [`verification/LIVE_RESULTS.md`](verification/LIVE_RESULTS.md) on-chain transaction index.

## Current deployment truth

The verified StudioNet deployment is `0x3587E5d4cc060718a4b7E4b2aA77A6AcC7f44aC1`. The frontend defaults to public evidence watch `3`; users may still enter another deployment or watch. The submitted evidence journals contain only finalized transactions with authoritative post-transaction readback.

Live frontend: https://awardtrace.pages.dev
