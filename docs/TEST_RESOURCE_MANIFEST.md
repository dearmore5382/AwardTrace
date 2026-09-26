# TED eForms live resource manifest

| Field | Tender | Award | Correction |
|---|---|---|---|
| Authority | EU Publications Office / TED | EU Publications Office / TED | EU Publications Office / TED |
| Publication number | `470710-2023` | `1424-2024` | `538997-2024` |
| Notice type | `cn-standard` | `can-standard` | `can-modif` |
| Publication date | `2023-08-02` | `2024-01-02` | `2024-09-09` |
| Procedure ID | legacy notice omits this Search API field | `c7a1e838-29fc-420d-a45a-8b3c2b2ebdd1` | same as award |
| Official link | referenced by the award as `previous-notice-id-proc` | explicit previous-notice link to tender | same procedure as award |
| Official page | https://ted.europa.eu/en/notice/-/detail/470710-2023 | https://ted.europa.eu/en/notice/-/detail/1424-2024 | https://ted.europa.eu/en/notice/-/detail/538997-2024 |

The award publishes the actual criterion and an `award-criterion-order-justification-lot` passage explaining why lowest price is the sole criterion. The correction publishes a concrete `modification-description`. The contract retrieves each record through anonymous `POST https://api.ted.europa.eu/v3/notices/search`, using a deterministic publication-number query and a fixed field allowlist. It requires exactly one result, the expected phase, the award's official backwards link to the tender, a shared award/correction procedure ID, three distinct publication numbers and increasing publication dates. Validators repeat the fetch and bounded assessment; raw response SHA-256 values are retained.

Criterion names, descriptions, winner identity and dates are descriptive evidence only. They are deliberately excluded from the rationale citation allowlist and cannot produce a consequential `ADDRESSED` or `CONTRADICTED` relation.

Local fixtures test parsers and adversarial cases only. They are never accepted as live ground truth.
