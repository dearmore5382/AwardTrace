# Repository rule application

Status: **CONTRACT_DEPLOYED_VERIFIED**. Exact-source deployment and the complete two-wallet contract matrix are verified. Production frontend redeployment/readback remains a separate gate.

## Applied to the contract

- The consequential assessment still uses `gl.nondet.exec_prompt`; AwardTrace is not a deterministic contract disguised as an intelligent contract.
- Model output is bounded to one JSON object containing relation enums only. Criteria, official passages, citations, chronology, roles, state transitions, revision lineage, and summaries are contract-derived.
- Validators independently fetch the fixed TED Search API resource and compare the source binding, publication date, criteria, passages, and relation enums. Free-form wording is not a consensus field.
- TED content is treated as untrusted evidence in the prompt. An unavailable, malformed, oversized, wrong-procedure, wrong-phase, criteria-free, or rationale-free source cannot create a positive trace.
- Tender, award, and correction are distinct roles with chronological and reuse guards. Corrections create append-only revisions rather than overwriting the award trace.
- The contract imports only the workspace-compatible `json` and `typing` modules beyond `genlayer`. HTTP response hashes were removed from contract execution; the deployment runner remains responsible for exact deployed-source SHA-256 parity.
- Public writes use explicit curator/auditor authorization. Every successful transition has a corresponding authoritative view.

## Applied to testing and evidence

- Direct Mode covers role separation, happy path state transitions, chronology failure, role reuse, bounded output rejection, cited-field allowlisting, correction lineage, and freeze behavior.
- Static tests enforce the fixed TED endpoint, bounded JSON output, consensus fields, absence of arbitrary URL/money surfaces, and compatibility imports.
- A finalized transaction is not labeled successful without its return value and post-write contract readback.
- Prior deployments and journals remain audit history and are explicitly marked superseded. They are not evidence for the current source hash.

## Live evidence completed

- Exact deployed-source SHA-256 parity for `0xa966526ce2c7B79E7Be4561FdF27a29090cB8dFd`.
- Sixteen finalized steps on case `1`, with method return and post-write readback for every step.
- Real TED tender, award, and correction releases; award and correction assessments both reached validator consensus and created append-only revisions.
- Authorization, premature action, notice reuse, and post-freeze rejection paths.

## Still required before submission

1. Run validator differential tests for every consequential relation and retain raw GenVM/consensus evidence.
2. Redeploy the frontend with the verified address and case `1`, then demonstrate that every displayed status, revision, citation, and transaction link matches authoritative readback.
3. Keep the delayed case `0` creation caused by an RPC `502` out of the canonical evidence path; case `1` is the complete journal.
