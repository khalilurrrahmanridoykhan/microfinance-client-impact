# Responsible-Lending and Financial-Health Analysis

CI5 calculates descriptive support signals from the synthetic loan, household and other-debt
tables.

```sh
make financial-health
```

## Indicators

- Project debt-service ratio: project monthly payment / monthly household income.
- Estimated other monthly payment: outstanding other-lender debt / 12.
- Total debt-service ratio: project payment plus estimated other payment / monthly income.
- Multiple-borrowing flag: the configured minimum number of other lenders is present.
- Debt-replacement flag: the synthetic loan purpose is `debt_replacement`.
- Support-review flag: one or more transparent signals is present.

The 12-month conversion of other outstanding debt is a synthetic modelling assumption, not a
regulatory standard. It must be sensitivity-tested before any external interpretation.

## Responsible use

These are support signals for human review and client protection. They are not risk scores,
credit decisions, pricing inputs or evidence that a client is irresponsible. The report is
aggregate-only, marked synthetic and includes its threshold assumptions. Subgroup rates must
be interpreted with sample size, missingness and fairness safeguards.