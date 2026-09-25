# Verification guide

## Contract review

Deploy the exact bytes of `contracts/AwardTrace.py`. Record the deployed address, deployment transaction, source commit, and SHA-256 of the source file. A different deployed source is not evidence for this repository.

## Live two-wallet flow

Use the primary wallet only for deployment. Do not use it for the lifecycle below.

1. Wallet A calls `create_watch(ocid, criteria_release_id, criteria_sha256)`.
2. Wait for `FINALIZED`, then call `get_watch(0)` and confirm `MONITORING` and Wallet A ownership.
3. Wallet A calls `anchor_criteria(0)`. Confirm return `CRITERIA_ANCHORED`, then read back `CRITERIA_ANCHORED` plus a non-empty criteria array.
4. Wallet A calls `bind_award(0, award_release_id, award_sha256)`. Confirm `AWARD_BOUND` by authoritative readback.
5. Wallet B calls the permissionless `assess_award(0)`. Confirm `TRACE_OPEN`, `revision_count = 1`, and load revision `0`.
6. Verify every locked criterion appears exactly once in the trace, and that the displayed summary equals the deterministic relation matrix.
7. Wallet A may call `append_correction` with a later official release. Confirm revision `1` points to parent `0`; revision `0` remains unchanged.
8. Wallet A calls `freeze_trace(0)`. Confirm `FROZEN`; further correction must return `CORRECTION_NOT_APPENDABLE`.

## Failure and adversarial paths

- Wrong digest: must return `INTEGRITY_FAILURE`; state remains unchanged.
- Wrong OCID in fetched release: must return `IDENTITY_FAILURE`; state remains unchanged.
- Source unavailable/oversized/invalid: must return `SOURCE_RETRYABLE`; state remains unchanged.
- Wallet B attempts owner-only anchor/bind/correction/freeze: must return `OWNER_ONLY`.
- Assess before award binding: must return `AWARD_NOT_ASSESSABLE`.
- Duplicate or missing criterion, unknown relation, changed reference, or non-boolean control field: validators reject the nondeterministic result.
- Freeze before an accepted trace: must return `TRACE_NOT_FREEZABLE`.

Transaction finality alone is not success. Evidence is complete only after the return/result and authoritative contract state are read back and match the intended transition.
