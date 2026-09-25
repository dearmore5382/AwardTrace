# Evidence packet

This file distinguishes completed StudioNet evidence from claims the current public source cannot support.

## Verified now

- Contract source: `contracts/AwardTrace.py`
- Direct/static test suite: 18 passing tests
- GenVM source checks: compile, lint, and typecheck pass
- Frontend: production build passes and imports `genlayer-js`
- Source adapter: fixed Contracts Finder single-release origin; no arbitrary positive-evidence URL
- Observed official source identity and digest: `docs/TEST_RESOURCE_MANIFEST.md`

## Completed StudioNet evidence

- Contract: `0x3587E5d4cc060718a4b7E4b2aA77A6AcC7f44aC1`
- Deployed source SHA-256: `cfb26686b4802d3874b18e021d23e8cf05deb26f7a9a8c75e64618fd8293c1dd`
- Base lifecycle journal: `verification/live-0x3587e5d4cc060718a4b7e4b2aa77a6acc7f44ac1.json` (`10/10` readback verified)
- Extended journal: `verification/extended-0x3587e5d4cc060718a4b7e4b2aa77a6acc7f44ac1.json` (`10/10` readback verified)
- Happy path: create, anchor, bind, independent auditor assessment, freeze.
- Integrity failure: transaction `0x211da5bf0059fb03096577a2068b5d9a3ee48401fea1985e5ecdbc9a929efcbc` returned `INTEGRITY_FAILURE`; watch `1` remained `MONITORING`.
- Identity failure: transaction `0x0e3388e25c945d1ebea1e9334c8f527a7a2e3c042d595b194d63b5de42201982` returned `IDENTITY_FAILURE`; watch `2` remained `MONITORING`.
- Revision lineage: transaction `0x5e81699781e78fc7a4b3a64bccf6b8d62336e82eaae0617bf7c1733364e2a2a4` created revision `1`; authoritative readback proves parent `0` and count `2`.
- Final freeze: transaction `0x686fb9ce97c4acea96283f238effa19b73f0168990df20f3e3d559907ca87239`; watch `3` is `FROZEN`.
- UI verification: localhost loaded contract state for watch `3` and displayed `FULLY_TRACED`, `FROZEN`, three `ADDRESSED` rows, and canonical `Revision 1`, matching authoritative readback.

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
| Source commit | `PENDING_GIT_COMMIT` |
| Deploy transaction | `PENDING` |
| Wallet A happy-path transactions | Recorded in both verification journals |
| Wallet B assessment transaction | `0x002cb9c3393d365c8303a65340e7d830e6693473c62c3dfc049bd2c4ad8c133c` |
| Failure/adversarial transactions | Recorded in both verification journals |
| Finalized authoritative readback | Watches `0` and `3` frozen; journals contain per-step readback |
| Live frontend URL | `PENDING_PUBLICATION` |

Do not replace a pending field with a transaction that only finalized transport. Confirm method return and state readback first. Do not claim test fixtures as live source evidence.
