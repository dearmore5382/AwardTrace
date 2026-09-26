# Verification guide

> Current v5.2 candidate. Do not reuse the archived v2-v4 transaction journals as proof for this source.

## Contract review

Deploy the exact bytes of `contracts/AwardTrace.py`. Record the deployed address, deployment transaction, source commit, and SHA-256 of the source file. A different deployed source is not evidence for this repository.

## Live two-wallet flow

Use the primary wallet only for deployment. Do not use it for the lifecycle below.

1. Wallet A calls `create_case(procedure_id, tender_notice, wallet_b)` with three distinct official TED releases selected in advance.
2. Wait for `FINALIZED`, verify the method return, then call `get_case(0)` and confirm `SOURCE_REGISTERED`, Wallet A ownership, and Wallet B as auditor.
3. Wallet A calls `anchor_tender(0)`. Confirm return `TENDER_ANCHORED`, a canonical `tender_source_binding`, and authoritative readback.
4. Wallet A calls `bind_award(0, award_notice)`. Confirm `AWARD_BOUND` by authoritative readback.
5. Wallet B calls `assess_award(0)`. Confirm a semantic return, `TRACE_OPEN`, `revision_count = 1`, published criteria, and cited revision `0`.
6. Verify every locked criterion appears exactly once in the trace, and that the displayed summary equals the deterministic relation matrix.
7. Wallet A calls `append_correction` with the later official correction; Wallet B calls `assess_correction`. Confirm revision `1` points to parent `0`; revision `0` remains unchanged.
8. Wallet A calls `freeze_trace(0)`. Confirm `FROZEN`; further correction must return `CORRECTION_NOT_APPENDABLE`.

## Failure and adversarial paths

- Wrong publication identity or procedure: must return `IDENTITY_FAILURE`; state remains unchanged.
- Source unavailable/oversized/invalid: must return `SOURCE_RETRYABLE`; state remains unchanged.
- Wallet B attempts curator-only anchor/bind/correction/freeze: must return `CURATOR_ONLY`.
- Assess before award binding: must return `AWARD_NOT_ASSESSABLE`.
- Wrong relation count, unknown relation, multiline output, or added model prose: validators reject the nondeterministic result.
- Criterion IDs, the authenticated source locator, identity consistency, and explicit amendment-control flag are derived deterministically; the model cannot author them.
- Freeze before an accepted trace: must return `TRACE_NOT_FREEZABLE`.

Transaction finality alone is not success. Evidence is complete only after the return/result and authoritative contract state are read back and match the intended transition.
