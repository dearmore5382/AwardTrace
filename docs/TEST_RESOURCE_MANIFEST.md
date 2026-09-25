# Test resource manifest

## Official observed resource

| Field | Value |
|---|---|
| Authority | UK Cabinet Office — Contracts Finder |
| Transport | OCDS single-release JSON endpoint |
| OCID | `ocds-b5fd17-9b2e0c20-6781-471b-8b29-c2d639187ed0` |
| Release GUID | `a55ff105-de10-4260-b843-e16e40642436` |
| Derived URL | `https://www.contractsfinder.service.gov.uk/Published/Notice/releases/a55ff105-de10-4260-b843-e16e40642436.json` |
| Observed HTTP status | `200` |
| Observed content type | `application/json` |
| Observed raw length | `8491` bytes |
| Observed SHA-256 | `88049adca6e69542352867906d1b234cf3f698e36121db02e20892cecf2f278a` |
| Observation date | `2026-09-25` |
| OCDS release tag | `award` |

This is a point-in-time observation, not an assertion that the endpoint is immutable. The contract re-fetches the derived URL and requires exact raw-byte digest and OCID agreement before positive mutation. If the authority changes the representation, the old digest fails closed.

This sample is suitable for demonstrating official-source binding, parser behavior, assessment, and readback. Because it is already tagged `award`, it is **not** evidence of a real prospective pre-award anchor. A submission claiming the prospective property must use an earlier tender release and a later award release for the same OCID, with both raw digests recorded.

## Fixture classification

The in-memory objects in `tests/test_contract_direct.py` are synthetic fixtures for state-machine and parser tests. They are explicitly not live-world ground truth and are not submission evidence for source availability or semantic correctness.
