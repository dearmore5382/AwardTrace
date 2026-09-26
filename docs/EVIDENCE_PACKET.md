# Evidence packet

> Archived v3 evidence. The active architecture is TED eForms v4. Do not submit the v3 deployment or Contracts Finder journals as current happy-path evidence.

This file distinguishes completed StudioNet evidence from claims the current public source cannot support.

## Verified now

- Contract source: `contracts/AwardTrace.py`
- Direct/static test suite: 18 passing tests
- GenVM source checks: compile, lint, and typecheck pass
- Frontend: production build passes and imports `genlayer-js`
- Source adapter: fixed Contracts Finder single-release origin; no arbitrary positive-evidence URL
- Observed official source identity and digest: `docs/TEST_RESOURCE_MANIFEST.md`

## Superseded StudioNet evidence

- Contract: `0x3587E5d4cc060718a4b7E4b2aA77A6AcC7f44aC1`
- Deployed source SHA-256: `cfb26686b4802d3874b18e021d23e8cf05deb26f7a9a8c75e64618fd8293c1dd`
- Base lifecycle journal: `verification/live-0x3587e5d4cc060718a4b7e4b2aa77a6acc7f44ac1.json` (`10/10` readback verified)
- Extended journal: `verification/extended-0x3587e5d4cc060718a4b7e4b2aa77a6acc7f44ac1.json` (`10/10` readback verified)
- Clickable live transaction index: [`verification/LIVE_RESULTS.md`](../verification/LIVE_RESULTS.md)
- These transactions verify the prior v2 mechanics only. They do not satisfy the new reviewer request because the same release was reused and the source does not publish actual evaluation criteria or substantive award-rationale passages.
- Integrity failure: transaction `0x211da5bf0059fb03096577a2068b5d9a3ee48401fea1985e5ecdbc9a929efcbc` returned `INTEGRITY_FAILURE`; watch `1` remained `MONITORING`.
- Identity failure: transaction `0x0e3388e25c945d1ebea1e9334c8f527a7a2e3c042d595b194d63b5de42201982` returned `IDENTITY_FAILURE`; watch `2` remained `MONITORING`.
- Revision lineage: transaction `0x5e81699781e78fc7a4b3a64bccf6b8d62336e82eaae0617bf7c1733364e2a2a4` created revision `1`; authoritative readback proves parent `0` and count `2`.
- Final freeze: transaction `0x686fb9ce97c4acea96283f238effa19b73f0168990df20f3e3d559907ca87239`; watch `3` is `FROZEN`.
- UI verification: localhost loaded contract state for watch `3` and displayed `FULLY_TRACED`, `FROZEN`, three `ADDRESSED` rows, and canonical `Revision 1`, matching authoritative readback.

## Required replacement evidence

- Verified v3 deployment: `0x2Fc5df47d11D2c7cf1bB569DD646E676E65810E1`; exact source parity passed (`27,288` bytes, SHA-256 `07f28df9bcb0d9dbd42ee327ce160d8c18ffa938f8c91757d8d5b075d47c3c57`), chain `61999`, version/schema readback passed, initial watch count `0`.
- Finalized v3 negative journal: [`verification/v3-negative-0x2fc5df47d11d2c7cf1bb569dd646e676e65810e1.json`](../verification/v3-negative-0x2fc5df47d11d2c7cf1bb569dd646e676e65810e1.json), four of four steps readback verified.

- New v3 deployment with exact source parity and `get_contract_version` readback.
- Three distinct publisher addresses assigned at watch creation.
- Separate tender and award release GUIDs for the same OCID, with award timestamp later than tender.
- Tender source must publish actual evaluation criteria; each stored criterion must include a JSON pointer.
- Award source must publish substantive rationale; every `ADDRESSED` or `CONTRADICTED` relation must store its JSON pointer and excerpt.
- Negative finalized transactions for role violation, release-role reuse, non-chronological release, missing criteria, and missing rationale.
- If a correction is claimed, a third distinct release and correction-publisher transaction, later than the award.
- Browser readback matching the new authoritative state and transaction journal.

## Explicit limitation

The selected Contracts Finder OCID currently exposes one release URL. Its public history describes updates, but does not expose independent immutable raw-byte snapshots for those earlier updates. Consequently, the journals prove integrity rejection, identity rejection, permissions, state-machine guards, consensus, append-only revision mechanics, and UI/readback parity. They do **not** claim a real semantic `PUBLISHED_CONFLICT` between two independent same-OCID official snapshots. Reusing the same release for revision `1` proves lineage mechanics only.

## Deployment history

| Evidence | Required value |
|---|---|
| Superseded contract | `0xD9879234feCD421740896028adE31f42f5f2120A` — source parity passed, but live `anchor_criteria` reached `CONSENSUS_FAILED`; do not submit as successful deployment |
| Superseded contract | `0x513718Aa8600AC79dA3d5809341C8Def3cf6D025` — source parity, anchor and award binding passed; AI assessment reached `CONSENSUS_FAILED` because validators independently invoked AI; do not submit as complete |
| Superseded contract | `0x38a69DefF9612b88F1D0E01C50A0Ea410c17687d` — source parity, anchor and award binding passed; schema-only custom validators still failed assessment consensus and did not meet the semantic proof obligation; do not submit as complete |
| Superseded contract | `0x4179B6864E930b609409dD9cD678F2c1d9441a56` — semantic consensus reached `MAJORITY_AGREE`, but execution returned `INVALID_TRACE_SCHEMA` because structured JSON was object-wrapped; no revision was created |
| Replacement contract | `0x3587E5d4cc060718a4b7E4b2aA77A6AcC7f44aC1` |
| Source commit | `e709236` — verified contract and E2E evidence publication |
| Deploy transaction | `PENDING` |
| Wallet A happy-path transactions | Recorded in both verification journals |
| Wallet B assessment transaction | `0x002cb9c3393d365c8303a65340e7d830e6693473c62c3dfc049bd2c4ad8c133c` |
| Failure/adversarial transactions | Recorded in both verification journals |
| Finalized authoritative readback | Watches `0` and `3` frozen; journals contain per-step readback |
| Live frontend URL | `https://awardtrace.pages.dev` — HTTP 200 and verified contract address embedded in the production build |

Do not replace a pending field with a transaction that only finalized transport. Confirm method return and state readback first. Do not claim test fixtures as live source evidence.
