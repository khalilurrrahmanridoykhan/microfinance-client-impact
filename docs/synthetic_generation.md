# Synthetic Dataset Generation

CI2 generates a linked client-impact dataset with a deterministic random seed. The default
configuration creates 100 synthetic clients and writes CSV tables to `data/synthetic/`.

```sh
make synth
```

The generator currently creates:

- clients, households and businesses;
- loans, other debts and savings at baseline and follow-up;
- outcome, wellbeing and agency survey records;
- complaints; and
- voluntary dropout events.

The generator uses only coarse categories and synthetic identifiers. It does not represent
real people, real institutions or Bangladesh's actual borrowers. The relationships and
outcomes are assumptions designed to exercise the analytics pipeline.

## Reproducibility

The default seed is `20260922`. Calling `generate_dataset` with the same
`SyntheticConfig(seed=..., clients=...)` produces the same records. Changing the seed is
appropriate for sensitivity checks, but published results must record the seed and config.

## Validation

Generation validates table presence, unique client IDs, foreign-key-like client links,
positive financial values, household sizes and agency-score ranges. CI2 tests also verify
same-seed determinism and rejection of an unknown client link.

Generated CSV files are ignored by Git. Do not force-add them unless a later release
explicitly documents why a generated fixture is needed.