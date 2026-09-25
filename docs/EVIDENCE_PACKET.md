# Evidence packet

This file is intentionally honest about what exists now and what must be captured after deployment.

## Verified now

- Contract source: `contracts/AwardTrace.py`
- Direct/static test suite: 15 passing tests
- GenVM source checks: compile, lint, and typecheck pass
- Frontend: production build passes and imports `genlayer-js`
- Source adapter: fixed Contracts Finder single-release origin; no arbitrary positive-evidence URL
- Observed official source identity and digest: `docs/TEST_RESOURCE_MANIFEST.md`

## Pending user-controlled StudioNet evidence

| Evidence | Required value |
|---|---|
| Superseded contract | `0xD9879234feCD421740896028adE31f42f5f2120A` — source parity passed, but live `anchor_criteria` reached `CONSENSUS_FAILED`; do not submit as successful deployment |
| Superseded contract | `0x513718Aa8600AC79dA3d5809341C8Def3cf6D025` — source parity, anchor and award binding passed; AI assessment reached `CONSENSUS_FAILED` because validators independently invoked AI; do not submit as complete |
| Superseded contract | `0x38a69DefF9612b88F1D0E01C50A0Ea410c17687d` — source parity, anchor and award binding passed; schema-only custom validators still failed assessment consensus and did not meet the semantic proof obligation; do not submit as complete |
| Superseded contract | `0x4179B6864E930b609409dD9cD678F2c1d9441a56` — semantic consensus reached `MAJORITY_AGREE`, but execution returned `INVALID_TRACE_SCHEMA` because structured JSON was object-wrapped; no revision was created |
| Replacement contract | `PENDING_PRIMARY_WALLET_REDEPLOYMENT` |
| Source commit | `PENDING_GIT_COMMIT` |
| Deploy transaction | `PENDING` |
| Wallet A happy-path transactions | `PENDING` |
| Wallet B assessment transaction | `PENDING` |
| Failure/adversarial transactions | `PENDING` |
| Finalized authoritative readback | `PENDING` |
| Live frontend URL | `PENDING_PUBLICATION` |

Do not replace a pending field with a transaction that only finalized transport. Confirm method return and state readback first. Do not claim test fixtures as live source evidence.
