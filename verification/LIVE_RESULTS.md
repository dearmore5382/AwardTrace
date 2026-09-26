# AwardTrace live StudioNet E2E results

> **Superseded evidence:** these transactions belong to the prior contract schema. They remain published for audit history, but they do not satisfy the reviewer request for distinct tender/award/correction releases, actual published evaluation criteria, or cited award-rationale passages. Do not submit them as v3 evidence.

## Current v3 negative-source evidence

- Contract: [`0x2Fc5…10E1`](https://explorer-studio.genlayer.com/address/0x2Fc5df47d11D2c7cf1bB569DD646E676E65810E1)
- Source parity: exact byte match (`27,288` bytes), SHA-256 `07f28df9bcb0d9dbd42ee327ce160d8c18ffa938f8c91757d8d5b075d47c3c57`
- Machine journal: [`v3-negative-0x2fc5…json`](v3-negative-0x2fc5df47d11d2c7cf1bb569dd646e676e65810e1.json)

| Step | Verified return | Authoritative state | Explorer |
|---|---|---|---|
| Create role-separated watch `0` | `0` | Three distinct roles stored; `MONITORING` | [`0xb307…bca2`](https://explorer-studio.genlayer.com/tx/0xb30750298efda216b3314bb89d4f7c35af984ae7be7ca2c0a208e182fb32bca2) |
| Award wallet attempts tender anchor | `TENDER_PUBLISHER_ONLY` | Watch unchanged | [`0x48e6…44b9`](https://explorer-studio.genlayer.com/tx/0x48e617ae059c82f307c291e393a590281d29e78b05edb918a73217fd267f44b9) |
| Premature award assessment | `AWARD_NOT_ASSESSABLE` | Watch unchanged | [`0x8be4…1544`](https://explorer-studio.genlayer.com/tx/0x8be4c1d576d4fcf4e62d457e217d7a40bbb5ebbc7a76a4cb7077e51343a71544) |
| Official source lacks published criteria | `CRITERIA_NOT_PUBLISHED` | No criteria stored; remained `MONITORING` | [`0xc5e0…c803`](https://explorer-studio.genlayer.com/tx/0xc5e08ab33331e7483276b796eaa1d50bb322f0d89a2ba4add96ffabd9090c803) |

This v3 evidence proves deployment parity, explicit role separation, premature-state rejection, and fail-closed handling of a real official source that does not publish evaluation criteria. It is not positive tender-to-award trace evidence.

This is the human-readable index for the machine-readable journals in this directory. Every transaction below finalized on StudioNet and is linked directly to GenLayer Studio Explorer. A transaction is marked verified only when its method return and authoritative post-transaction contract readback matched the expected result.

## Deployment under test

- Contract: [`0x3587E5…f44aC1`](https://explorer-studio.genlayer.com/address/0x3587E5d4cc060718a4b7E4b2aA77A6AcC7f44aC1)
- Exact source SHA-256: `cfb26686b4802d3874b18e021d23e8cf05deb26f7a9a8c75e64618fd8293c1dd`
- Steward wallet: `0x736A168247e3f0C52F7907c9a8fDac572DF9c8bB`
- Independent auditor wallet: `0xA63DE24e30C88FB1019E8956654730316e36eDBE`
- Machine-readable base journal: [`live-0x3587…json`](live-0x3587e5d4cc060718a4b7e4b2aa77a6acc7f44ac1.json)
- Machine-readable extended journal: [`extended-0x3587…json`](extended-0x3587e5d4cc060718a4b7e4b2aa77a6acc7f44ac1.json)

## Base lifecycle and adversarial authorization

| Step | Actor | Verified method result | Authoritative state after | Explorer |
|---|---|---|---|---|
| Reject invalid watch | Steward | `INVALID_WATCH` | No watch created | [`0x06df…b740`](https://explorer-studio.genlayer.com/tx/0x06dfc159ff662bf2569fe2a30c3b068ed7e83bfb8d7e1f2821574e2b11afb740) |
| Create watch `0` | Steward | `0` | `MONITORING` | [`0x0b40…3561`](https://explorer-studio.genlayer.com/tx/0x0b40fc7c7466bbe04aa275c80e06cb9e46ba9359571ed31ca19b41f126913561) |
| Auditor attempts owner-only anchor | Auditor | `OWNER_ONLY` | Remained `MONITORING` | [`0x5232…1b48`](https://explorer-studio.genlayer.com/tx/0x5232f097ed79127180dd3e6a36aac50c504796ede794956f69d35fc589e81b48) |
| Premature assessment | Auditor | `AWARD_NOT_ASSESSABLE` | Remained `MONITORING` | [`0x1fc9…aaed`](https://explorer-studio.genlayer.com/tx/0x1fc9e29481dee812d42d96c6f395661f762a4bafa1234da25d85904ae339aaed) |
| Anchor authenticated criteria | Steward | `CRITERIA_ANCHORED` | Three criteria locked | [`0x037a…4c3`](https://explorer-studio.genlayer.com/tx/0x037a469cede948bfeb729a13cdff77133fab9c55b995464b462ebf62e54734c3) |
| Bind authenticated award | Steward | `AWARD_BOUND` | `AWARD_BOUND` | [`0x17aa…4fe8`](https://explorer-studio.genlayer.com/tx/0x17aaeab410ea2861b8700e20d9e3bdb1fdb33e621cd9b1b762b068ddac7c4fe8) |
| Independent assessment | Auditor | `FULLY_TRACED` | `TRACE_OPEN`, revision `0` | [`0x002c…133c`](https://explorer-studio.genlayer.com/tx/0x002cb9c3393d365c8303a65340e7d830e6693473c62c3dfc049bd2c4ad8c133c) |
| Auditor attempts owner-only correction | Auditor | `OWNER_ONLY` | Revision `0` unchanged | [`0xb56b…104d`](https://explorer-studio.genlayer.com/tx/0xb56b93af6b932bd08ad9ce4032af57de69631fa6b695d24c3d0062022abe104d) |
| Freeze accepted trace | Steward | `TRACE_FROZEN` | `FROZEN` | [`0xea67…6bae`](https://explorer-studio.genlayer.com/tx/0xea67715ac850a809115bbe71e8b30caf3bb7a94cfb3a9f97d8a548d585d66bae) |
| Reject correction after freeze | Steward | `CORRECTION_NOT_APPENDABLE` | Remained `FROZEN` | [`0x794c…9868`](https://explorer-studio.genlayer.com/tx/0x794c46372f39d7ff47f6cc17da955e1d647d9df62b0aa40e19a618ce9b689868) |

## Integrity, identity, revision, and final-freeze evidence

| Step | Actor | Verified method result | Authoritative state after | Explorer |
|---|---|---|---|---|
| Create wrong-digest watch `1` | Steward | `1` | `MONITORING` | [`0x9f04…0c22`](https://explorer-studio.genlayer.com/tx/0x9f0495e9c33b5dfc6907cdcaa7a1c7aa176002c7a53e55d8de75966b94390c22) |
| Reject wrong digest | Steward | `INTEGRITY_FAILURE` | Watch `1` remained `MONITORING` | [`0x211d…fcbc`](https://explorer-studio.genlayer.com/tx/0x211da5bf0059fb03096577a2068b5d9a3ee48401fea1985e5ecdbc9a929efcbc) |
| Create wrong-identity watch `2` | Steward | `2` | `MONITORING` | [`0xd46d…7fdc`](https://explorer-studio.genlayer.com/tx/0xd46d8525e1f7aa27f6ad4511095f81ecf0271e6e761421d361fe6839e4cf7fdc) |
| Reject wrong OCID | Steward | `IDENTITY_FAILURE` | Watch `2` remained `MONITORING` | [`0x0e33…1982`](https://explorer-studio.genlayer.com/tx/0x0e3388e25c945d1ebea1e9334c8f527a7a2e3c042d595b194d63b5de42201982) |
| Create revision watch `3` | Steward | `3` | `MONITORING` | [`0x0c75…aee6`](https://explorer-studio.genlayer.com/tx/0x0c758523b00f9a0a3dec2af009f662f2711b3ccf89e57a49f52f8880b947aee6) |
| Anchor authenticated criteria | Steward | `CRITERIA_ANCHORED` | Three criteria locked | [`0x13a4…a649`](https://explorer-studio.genlayer.com/tx/0x13a42cfb8c9c36bf16ebe5a8ae67e87a0d70a61b4594f3211c922d39c0bda649) |
| Bind authenticated award | Steward | `AWARD_BOUND` | `AWARD_BOUND` | [`0x4204…6755`](https://explorer-studio.genlayer.com/tx/0x420490687f932f23cc2c2d2d961e4d6b932b7902e87e350c0e421525895a6755) |
| Independent assessment | Auditor | `FULLY_TRACED` | `TRACE_OPEN`, revision `0` | [`0xd032…097`](https://explorer-studio.genlayer.com/tx/0xd0320b3f1a39af642d417ffee4991e22168934b1f2706077064e54c2cee98097) |
| Append authenticated revision | Steward | `FULLY_TRACED` | Revision `1`, parent `0` | [`0x5e81…a2a4`](https://explorer-studio.genlayer.com/tx/0x5e81699781e78fc7a4b3a64bccf6b8d62336e82eaae0617bf7c1733364e2a2a4) |
| Freeze canonical trace | Steward | `TRACE_FROZEN` | Watch `3` is `FROZEN`, revision count `2` | [`0x686f…239`](https://explorer-studio.genlayer.com/tx/0x686fb9ce97c4acea96283f238effa19b73f0168990df20f3e3d559907ca87239) |

## Final readback parity

The live frontend defaults to watch `3`. Its verified production view matches the journal's authoritative readback:

- status: `FROZEN`
- canonical revision: `1`
- revision count: `2`
- summary: `FULLY_TRACED`
- relations: `C1 ADDRESSED`, `C2 ADDRESSED`, `C3 ADDRESSED`

## Evidence boundary

These transactions prove finalized execution, exact-source integrity rejection, OCID identity rejection, role separation, bounded assessment, revision linkage, final freezing, and UI/readback parity. The selected official endpoint exposes one current award-tagged release, so this evidence does not claim a real prospective pre-award anchor or a semantic conflict between two independent historical official snapshots.
