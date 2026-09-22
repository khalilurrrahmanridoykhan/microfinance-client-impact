# Evaluation Design and Causal Readiness

CI7 makes the project's evaluation status explicit through:

```sh
make evaluation
```

The output checks for an `evaluation_group` field with at least two groups and for repeated
outcome observations. The current generated data has no evaluation group, so the report
correctly returns `causal_ready: false` and lists the missing design requirement.

The available before/after result is labeled `paired descriptive change`. It describes the
synthetic observations only and does not establish that borrowing caused the change.

## Future comparison design

If a suitable public or explicitly simulated comparison population is introduced, document:

- treatment definition and treatment date;
- comparison-group eligibility and why it is credible;
- baseline covariates and balance checks;
- outcome timing and follow-up windows;
- attrition and missing-data handling;
- placebo or pre-trend diagnostics; and
- the estimand, uncertainty method and prohibited interpretations.

Until those requirements are met, use descriptive language such as `reported change` and
`associated with`, not `impact` or `caused`.