# Uncertainty and Follow-up Coverage

CI4 reports percentile bootstrap intervals around synthetic median changes and makes survey
coverage visible.

```sh
make uncertainty
```

The report includes:

- median-change estimates and percentile intervals for income, business profit and savings;
- the bootstrap confidence level, resample count and seed;
- baseline, follow-up and paired counts for wellbeing, outcome and savings tables; and
- follow-up and paired coverage rates.

The interval describes sampling variability under the synthetic observations. It does not
correct for generator assumptions, measurement error, non-response bias or causal
confounding. A paired coverage rate below 1.0 means that the outcome calculation describes
only clients observed in both rounds.

The report is aggregate-only and marked synthetic. It must not be interpreted as evidence
that borrowing caused an observed change or as a basis for an individual credit decision.