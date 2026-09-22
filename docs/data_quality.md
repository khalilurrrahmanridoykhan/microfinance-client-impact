# Data Quality Report

CI3 provides two checks for the synthetic dataset:

```sh
make synth
make quality
```

`make quality` regenerates the default seeded dataset in memory, validates its table
presence, client links, required financial values and score ranges, then writes
`results/generated/data-quality.json`.

The report contains:

- `ok`: whether any validation errors were found;
- `table_counts`: record count by expected table;
- `error_count` and `errors`: integrity and range failures; and
- `warning_count` and `warnings`: missing values or empty-table warnings.

Optional agency scores for non-women clients are represented as null and are intentionally
not treated as errors. Any future optional field must be documented in the data dictionary
before the validator permits it.

The generated report is ignored by Git because it is reproducible output. A future release
may commit a fixture only if the seed, configuration and purpose are documented.