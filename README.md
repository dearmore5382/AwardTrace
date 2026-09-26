# AwardTrace

AwardTrace is a GenLayer intelligent contract and browser workflow that joins a published TED competition notice to its later award notice, locks the real evaluation criteria, and creates a cited criterion-level trace of the published award evidence.

## v5 architecture

- Source: EU Publications Office TED Search API v3; no user-supplied URL.
- Identity: publication number, award-to-tender `previous-notice-id-proc`, and shared award/correction `procedure-identifier`.
- Phases: `cn-*` tender, `can-*` award, and `can-modif` correction are enforced independently.
- Actors: the evidence curator registers/binds sources; a distinct assigned auditor triggers consequential assessment.
- Ordering: award and correction dates must advance; the same publication number cannot be reused across roles.
- Consensus: validators independently fetch the same TED record and repeat bounded assessment.
- Evidence: actual published criteria, rationale-only citations, modification passages, raw API-response SHA-256 and append-only revisions.

## Verified live source chain

- Procedure: `c7a1e838-29fc-420d-a45a-8b3c2b2ebdd1`
- Tender: [`470710-2023`](https://ted.europa.eu/en/notice/-/detail/470710-2023), published 2023-08-02
- Award: [`1424-2024`](https://ted.europa.eu/en/notice/-/detail/1424-2024), published 2024-01-02
- Correction: [`538997-2024`](https://ted.europa.eu/en/notice/-/detail/538997-2024), published 2024-09-09

The award references the tender, publishes an actual criterion and a rationale passage. The later correction shares the award procedure and publishes a modification passage. See [the resource manifest](docs/TEST_RESOURCE_MANIFEST.md).

## Contract flow

1. Curator calls `create_case(procedure_id, tender_notice, auditor)`.
2. Curator calls `anchor_tender(case_id)`; validators verify the independent tender release.
3. Curator calls `bind_award(case_id, award_notice)`.
4. Assigned auditor calls `assess_award(case_id)`; validators extract published criteria and permit citations only from rationale-specific TED fields.
5. Curator may bind a later official correction; auditor assesses it as a new revision.
6. Curator freezes the append-only trace.

## Verification

```bash
pytest -q
npm run lint
npm run build
```

Production v5.2 contract: [`0xa966526ce2c7B79E7Be4561FdF27a29090cB8dFd`](https://explorer-studio.genlayer.com/address/0xa966526ce2c7B79E7Be4561FdF27a29090cB8dFd). Exact source parity was verified against [`contracts/AwardTrace.py`](contracts/AwardTrace.py): `19,591` bytes, SHA-256 `96e60855a7d7e73de793e00a15f8a0b3cde6c462a1c2281553dbd459e4335c6d`. The finalized 16-step StudioNet matrix completed on case `1`, including award and correction consensus, two-wallet authorization failures, notice-role reuse failures, append-only revisions, freeze, and authoritative readback. See [`verification/LIVE_RESULTS.md`](verification/LIVE_RESULTS.md). Older deployments are superseded.

See [`docs/RULES_APPLICATION.md`](docs/RULES_APPLICATION.md) for the repository-wide rule audit and the evidence gate that must be met before submission.

AwardTrace reports what the published notices evidence. It does not claim legality, fairness, value for money, or absence of corruption.
