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
| Replacement contract | `PENDING_PRIMARY_WALLET_REDEPLOYMENT` |
| Source commit | `PENDING_GIT_COMMIT` |
| Deploy transaction | `PENDING` |
| Wallet A happy-path transactions | `PENDING` |
| Wallet B assessment transaction | `PENDING` |
| Failure/adversarial transactions | `PENDING` |
| Finalized authoritative readback | `PENDING` |
| Live frontend URL | `PENDING_PUBLICATION` |

Do not replace a pending field with a transaction that only finalized transport. Confirm method return and state readback first. Do not claim test fixtures as live source evidence.
