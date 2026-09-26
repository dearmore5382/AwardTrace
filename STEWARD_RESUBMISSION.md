# AwardTrace — steward resubmission record

## What changed

AwardTrace was rebuilt around three distinct, chronologically ordered EU Publications Office TED releases rather than a reused release or a fixture. The deployed intelligent contract now verifies the tender, binds a later award, extracts the actual published evaluation criterion, cites only published award-rationale fields, appends a later correction as a new immutable revision, and requires an independently assigned auditor wallet to perform both semantic assessments.

The model has a deliberately narrow role: it returns one bounded relation enum per criterion as structured JSON. Contract code derives source identity, criteria, citations, chronology, authorization, revision lineage, summaries, and all state transitions. Validators independently fetch the fixed TED endpoint and compare every consequential source and assessment field. Unavailable, malformed, wrong-phase, wrong-procedure, criteria-free, or rationale-free sources cannot create a positive trace.

## Verified production configuration

| Item | Verified value |
|---|---|
| Frontend | https://awardtrace.pages.dev |
| GitHub | https://github.com/dearmore5382/AwardTrace |
| Contract | https://explorer-studio.genlayer.com/address/0xa966526ce2c7B79E7Be4561FdF27a29090cB8dFd |
| Network | GenLayer StudioNet |
| Contract source | `contracts/AwardTrace.py` |
| Source size | `19,591` bytes |
| Source SHA-256 | `96e60855a7d7e73de793e00a15f8a0b3cde6c462a1c2281553dbd459e4335c6d` |
| Schema | `ted-three-release-cited-rationale-v1` |
| Canonical case | `1` |
| Final state | `FROZEN` |
| Revisions | `2` (`0` award, `1` correction) |

The deployed bytecode source was downloaded from StudioNet and compared byte-for-byte with the repository source before any lifecycle transaction was accepted as evidence.

## Real published source chain

| Role | TED publication | Publication date | Purpose |
|---|---|---|---|
| Tender | [470710-2023](https://ted.europa.eu/en/notice/-/detail/470710-2023) | 2023-08-02 | Independent competition notice |
| Award | [1424-2024](https://ted.europa.eu/en/notice/-/detail/1424-2024) | 2024-01-02 | Result notice with published evaluation criterion and award rationale |
| Correction | [538997-2024](https://ted.europa.eu/en/notice/-/detail/538997-2024) | 2024-09-09 | Later contract modification publication |

AwardTrace verifies the shared procedure identifier `c7a1e838-29fc-420d-a45a-8b3c2b2ebdd1`, release role, distinct publication number, and increasing publication date. The award revision cites `award-criterion-order-justification-lot/0`; the correction revision cites `modification-description/0`.

## Independent roles

- Deployment wallet was used only to deploy the contract.
- Curator: `0x736A168247e3f0C52F7907c9a8fDac572DF9c8bB`
- Independent auditor: `0xA63DE24e30C88FB1019E8956654730316e36eDBE`
- Auditor attempts to perform curator-only actions returned `CURATOR_ONLY` without changing state.
- Curator attempts to perform assessments returned `AUDITOR_ONLY` without changing state.

## Canonical live transactions

| Step | Verified return and readback | Explorer |
|---|---|---|
| Create case `1` | `1`; `SOURCE_REGISTERED` | [0x4a7e…b487](https://explorer-studio.genlayer.com/tx/0x4a7e3d467b220b4d1f2071f66a5800c9fcbc23b3cc90b13497e6259c34bbb487) |
| Reject auditor anchor | `CURATOR_ONLY`; unchanged | [0x1466…7ac2](https://explorer-studio.genlayer.com/tx/0x14667824c27e426bd923451bcef9555f5d0caa2da21fe1daa4f33e95b41a7ac2) |
| Reject premature assessment | `AWARD_NOT_ASSESSABLE`; unchanged | [0x48d0…9896](https://explorer-studio.genlayer.com/tx/0x48d0208be932868e7648407df151eb7eee52c32bf4babbf9a32cdee2e5b49896) |
| Anchor tender | `TENDER_ANCHORED`; bound publication/date | [0xebf7…b1df](https://explorer-studio.genlayer.com/tx/0xebf71220bafe769fb6810b337e3f9bf7a9fdfcb44ad078a2fb7d88c17bafb1df) |
| Reject tender reuse as award | `INVALID_AWARD_NOTICE`; unchanged | [0xd104…ab32](https://explorer-studio.genlayer.com/tx/0xd104385de34ebdaad55c2e8ced52411e9785ffb0f3c90b96f99684661291ab32) |
| Bind award | `AWARD_BOUND` | [0x2850…8ca3](https://explorer-studio.genlayer.com/tx/0x2850700d6a48fa2b7224103a8d338a150bec2d8599aa4936ca416cd7d81c8ca3) |
| Reject curator assessment | `AUDITOR_ONLY`; unchanged | [0x8913…beec](https://explorer-studio.genlayer.com/tx/0x89134981d4ecbd36e8f2d8c75dd01996fa3e410f5b748e8c7c0ed168ffd2beec) |
| Auditor assesses award | `FULLY_TRACED`; revision `0`, `TRACE_OPEN` | [0x1127…be5d](https://explorer-studio.genlayer.com/tx/0x1127402ddb965e9a2609e6e370d82adeedb77b45028e56ff8ac512438f56be5d) |
| Reject award reuse as correction | `NOTICE_ROLE_REUSE`; unchanged | [0x96f7…4514](https://explorer-studio.genlayer.com/tx/0x96f7f4b1c5bc867a5ad1fbf438c4823199a9c7a13fa64c817e2cf045d0084514) |
| Bind correction | `CORRECTION_BOUND` | [0xc0bd…e0a1](https://explorer-studio.genlayer.com/tx/0xc0bd4d1af7ceb33222c77b188f2a07480d4bcec1f943fb5d958df5ae9df4e0a1) |
| Reject curator correction assessment | `AUDITOR_ONLY`; unchanged | [0x9abb…79d1](https://explorer-studio.genlayer.com/tx/0x9abb65b678dc66e445c2614c6f7e3d8b78c98029a6b323a175eebd943da479d1) |
| Auditor assesses correction | `FULLY_TRACED`; revision `1`, parent `0` | [0x2f99…9671](https://explorer-studio.genlayer.com/tx/0x2f99c9fd7148d856c9ca174de2fb76b7f23f373c9f495449fc20d59386739671) |
| Reject correction reuse | `NOTICE_ROLE_REUSE`; unchanged | [0xa29a…e0e3](https://explorer-studio.genlayer.com/tx/0xa29a746fa3307948dee0358bc653aade73e2f8949c6a1191f46eb790f821e0e3) |
| Freeze canonical trace | `TRACE_FROZEN`; `FROZEN`, revision count `2` | [0x096e…c6f5](https://explorer-studio.genlayer.com/tx/0x096e7d4af7839b6ceb255bdcd62afd64d2cafa8cd78b87b5bc42c47dd75dc6f5) |
| Reject post-freeze mutation | `CORRECTION_NOT_APPENDABLE`; unchanged | [0x1aca…1bcc](https://explorer-studio.genlayer.com/tx/0x1aca13b987fb2b6a23dcada01e98fa1d924982b71685589b8ace3ac5be911bcc) |

Each row above was accepted only after `FINALIZED`, `MAJORITY_AGREE`, the expected method return, and authoritative `get_case` readback. Transport finality by itself was not treated as success.

## Frontend verification

The production frontend defaults to the verified contract and case `1`, automatically loads authoritative state, displays the canonical citation trace, and includes persistent Explorer links for the successful lifecycle. At verification time:

- URL returned HTTP `200`.
- Published page asset: `/_next/static/chunks/page-CkZ6VjQy.js`.
- Asset SHA-256: `b45ec216110cb85cdccc328abdca2b5e81868a9cebacca49f16d96e8ed2bbfb7`.
- The production asset contained the exact contract address, source chain, canonical award-assessment transaction, and current source-binding terminology.

## Reproducible evidence

- [Complete 16-step machine journal](verification/v5-ted-0xa966526ce2c7b79e7be4561fdf27a29090cb8dfd.json)
- [Human-readable transaction index](verification/LIVE_RESULTS.md)
- [Production frontend verification](verification/frontend-production.json)
- [Rule-application audit](docs/RULES_APPLICATION.md)
- [Test resource manifest](docs/TEST_RESOURCE_MANIFEST.md)
- [Reviewer verification instructions](docs/VERIFICATION_GUIDE.md)

Local verification: `14/14` Direct Mode/static tests passed, ESLint passed, and the production asset build completed. Tests cover role separation, chronology, notice reuse, correction lineage, freeze behavior, source-field allowlisting, bounded JSON rejection, and deterministic derivation of all four summaries.

## Evidence boundary

The selected real TED chain produced `FULLY_TRACED` for both published award rationale and later price modification. Direct Mode verifies the deterministic `GAPS_PRESENT`, `PUBLISHED_CONFLICT`, and `INSUFFICIENT_OFFICIAL_EVIDENCE` branches, but this submission does not mislabel a fixture as a live published conflict. A live `PUBLISHED_CONFLICT` should only be claimed when an official notice actually contradicts its criterion.

## Text for the “What did you change?” field

Rebuilt AwardTrace around three distinct official TED releases and deployed exact source `96e60855…35c6d` at `0xa966526c…b8dFd`. Validators now fetch the fixed TED API, extract the published criterion and rationale/modification passages, and reach bounded JSON consensus while the contract enforces separate curator/auditor roles, chronology, notice-role non-reuse, cited append-only revisions, and authoritative readback. A 16-step finalized StudioNet matrix completed on case 1: award and correction assessments both created cited revisions, then the trace was frozen; authorization, premature action, reuse, and post-freeze attempts left state unchanged. The production UI now loads case 1 from chain and provides persistent Explorer links. Full machine journal and source/UI parity records are in the repository.

