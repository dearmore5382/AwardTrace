# TED eForms live resource manifest

| Field | Tender | Award |
|---|---|---|
| Authority | EU Publications Office / TED | EU Publications Office / TED |
| Publication number | `616030-2024` | `4-2025` |
| Notice type | `cn-standard` | `can-standard` |
| Publication date | `2024-10-11` | `2025-01-02` |
| Procedure ID | `f78fe5bc-095c-4053-a1de-8c63d1154e15` | same |
| Official page | https://ted.europa.eu/en/notice/-/detail/616030-2024 | https://ted.europa.eu/en/notice/-/detail/4-2025 |

The tender and award expose actual eForms award-criterion names, descriptions and types. The award also exposes winner and decision-date fields. The contract retrieves each record through anonymous `POST https://api.ted.europa.eu/v3/notices/search`, using a deterministic publication-number query and a fixed field allowlist. It requires exactly one result, the expected procedure ID, the expected phase and increasing publication dates. Validators repeat the same fetch; the raw response SHA-256 is retained as audit metadata.

Local fixtures test parsers and adversarial cases only. They are never accepted as live ground truth.
