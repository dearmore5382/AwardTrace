# Evidence packet

This file is intentionally honest about what exists now and what must be captured after deployment.

## Verified now

- Contract source: `contracts/AwardTrace.py`
- Direct/static test suite: 14 passing tests
- GenVM source checks: compile, lint, and typecheck pass
- Frontend: production build passes and imports `genlayer-js`
- Source adapter: fixed Contracts Finder single-release origin; no arbitrary positive-evidence URL
- Observed official source identity and digest: `docs/TEST_RESOURCE_MANIFEST.md`

## Pending user-controlled StudioNet evidence

| Evidence | Required value |
|---|---|
| Contract address | `PENDING_PRIMARY_WALLET_DEPLOYMENT` |
| Source commit | `PENDING_GIT_COMMIT` |
| Deploy transaction | `PENDING` |
| Wallet A happy-path transactions | `PENDING` |
| Wallet B assessment transaction | `PENDING` |
| Failure/adversarial transactions | `PENDING` |
| Finalized authoritative readback | `PENDING` |
| Live frontend URL | `PENDING_PUBLICATION` |

Do not replace a pending field with a transaction that only finalized transport. Confirm method return and state readback first. Do not claim test fixtures as live source evidence.
