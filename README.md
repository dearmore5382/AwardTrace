# AwardTrace

AwardTrace is a GenLayer intelligent contract and browser workflow that joins a published TED competition notice to its later award notice, locks the real evaluation criteria, and creates a cited criterion-level trace of the published award evidence.

## v4 architecture

- Source: EU Publications Office TED Search API v3; no user-supplied URL.
- Identity: publication number plus shared official `procedure-identifier`.
- Phases: `cn-*` tender, `can-*` award, and `can-modif` correction are enforced independently.
- Actors: the evidence curator registers/binds sources; a distinct assigned auditor triggers consequential assessment.
- Ordering: award and correction dates must advance; the same publication number cannot be reused across roles.
- Consensus: validators independently fetch the same TED record and repeat bounded assessment.
- Evidence: raw API-response SHA-256, source pointers, exact cited excerpts, append-only revisions.

## Verified live source pair

- Procedure: `f78fe5bc-095c-4053-a1de-8c63d1154e15`
- Tender: [`616030-2024`](https://ted.europa.eu/en/notice/-/detail/616030-2024), published 2024-10-11
- Award: [`4-2025`](https://ted.europa.eu/en/notice/-/detail/4-2025), published 2025-01-02

Both notices publish real award criteria. The award also publishes winner and decision fields. See [the resource manifest](docs/TEST_RESOURCE_MANIFEST.md).

## Contract flow

1. Curator calls `create_case(procedure_id, tender_notice, auditor)`.
2. Curator calls `anchor_tender(case_id)`; validators retrieve and lock TED criteria.
3. Curator calls `bind_award(case_id, award_notice)`.
4. Assigned auditor calls `assess_award(case_id)`; the resulting trace cites exact TED fields.
5. Curator may bind a later official correction; auditor assesses it as a new revision.
6. Curator freezes the append-only trace.

## Verification

```bash
pytest -q
npm run lint
npm run build
```

Current production deployment: `0x3b5eE5e170D54152f526686Ae13531B00d5F41Df`. Its deployed source exactly matches the repository (`18,576` bytes, SHA-256 `96e3cc7f8489374b83b186767f4daa4aee7bf6528435a6d419346321c597e3ed`). The finalized 11-step matrix covers valid lifecycle, invalid input, premature assessment, role violations, notice-role reuse, comparative consensus, freeze and mutation rejection after freeze. Case `0` finished `FROZEN`; revision `0` is `FULLY_TRACED`.

AwardTrace reports what the published notices evidence. It does not claim legality, fairness, value for money, or absence of corruption.
