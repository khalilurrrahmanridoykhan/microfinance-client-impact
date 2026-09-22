# Public Source Review

## Review status

No public source has been approved or downloaded yet. The empty `data/source-manifest.json` is intentional. A source may be added only after its licence or terms, field coverage, geography, year, sensitivity and publication limits are recorded.

## Candidate source families

| Candidate | Possible use | Review questions | Current decision |
|---|---|---|---|
| Global Findex | Financial inclusion context and selected country-level comparisons | Are the required country/year fields available? What are the reuse terms? | Review before use |
| Bangladesh Bureau of Statistics household surveys | Household income, expenditure or welfare context | Is the microdata accessible? Are the fields comparable to the project outcomes? Are access conditions satisfied? | Review before use |
| Bangladesh Bank publications | Financial inclusion and financial-system context | Does the publication provide relevant aggregate indicators and reuse terms? | Review before use |
| Microcredit Regulatory Authority aggregate reports | MFI-sector context and non-client aggregates | Is the metric relevant without duplicating Kisti? Does it describe institutions rather than clients? | Review before use |
| Public responsible-finance surveys | Client-protection or satisfaction context | Is the questionnaire documented? Are respondent-level data and licence terms suitable? | Review before use |

## Approval checklist

Before adding a source to `data/source-manifest.json`, record:

- publisher and exact title;
- URL or access route;
- publication and retrieval dates;
- licence or terms of use;
- geography and population represented;
- survey or administrative year;
- fields used and their definitions;
- whether data is aggregate or respondent-level;
- privacy and re-identification risks;
- missingness and comparability limits; and
- whether raw files may be redistributed.

## Source boundary

Public aggregate sources provide context and cannot be used to claim individual client impact. Any respondent-level public source must retain its original population definition and must not be silently combined with the synthetic population. Each output will name its source layer.
