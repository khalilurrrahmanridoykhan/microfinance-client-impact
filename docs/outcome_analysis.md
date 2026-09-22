# Client Outcome Analysis

CI4 compares paired baseline and follow-up synthetic observations for the same client.
It calculates income, business-profit, savings and food-security changes, business survival,
and essential-expense reduction.

```sh
make outcomes
```

The output contains aggregate summaries overall and by gender and district. It does not
publish client-level rows. The result is explicitly marked `synthetic` and uses the
interpretation label `descriptive paired change; not automatically causal`.

## Interpretation

- A positive median change is a descriptive change in this generated dataset.
- Subgroup differences are associations within the synthetic population.
- Business survival is sensitive to follow-up loss and the generator's assumptions.
- Essential-expense reduction is a potential financial-stress signal, not proof of harm.
- No result should be used to approve, reject or price an individual loan.

CI4's next extension is uncertainty and attrition reporting. Causal methods remain out of
scope until a defensible comparison design and appropriate data are available.