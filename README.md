# Microfinance Client Impact and Responsible Lending Analytics

A reproducible analytics project for studying client wellbeing, financial health, inclusion and responsible lending in microfinance.

## Scope

This project focuses on the client side of microfinance:

- household and business outcomes;
- savings and emergency resilience;
- debt-service burden and multiple borrowing;
- gender, inclusion and decision-making agency;
- satisfaction, complaints and dropout; and
- responsible-lending support signals.

It is separate from the Kisti microfinance portfolio project, which focuses on MFI-level performance, repayment, PAR, branch productivity and portfolio mechanics.

## Data boundary

The project begins with synthetic data and documented public aggregate sources. It does not contain or accept real client records, names, national IDs, phone numbers, addresses, applications or field submissions. Synthetic findings are not evidence about real borrowers.

The dashboard and analysis are for program learning and safeguards. They must not be used as automatic loan approval, rejection or pricing decisions.

## Status

CI0 foundation, CI1 indicator/source specification, CI2 synthetic client-impact dataset
generation and CI3 data-quality reporting are complete. CI4 descriptive outcome analytics,
aggregate reporting, uncertainty intervals and follow-up coverage are now available. Next:
CI5 responsible-lending and financial-health analytics are now available. Next: add client
voice and complaint analysis.

## Quick start

Requires Python 3.11 or newer.

```sh
make setup
make test
make lint
make synth  # write the seeded synthetic tables to data/synthetic/
make quality  # write results/generated/data-quality.json
make outcomes  # write results/generated/outcomes.json
make uncertainty  # write results/generated/uncertainty.json
make financial-health  # write results/generated/financial-health.json
```

## Repository standards

This is a public repository maintained solely by `khalilurrrahmanridoykhan`. Commits and releases must contain no co-author trailers and no automated-author attribution. See the project plan in `plan/Microfinance/` for the complete public-repository, ethics and release requirements.

## Planned outputs

- tested synthetic client-impact dataset;
- indicator and data-quality reports;
- client outcome and financial-health analysis;
- inclusion, client-voice and responsible-lending reports; and
- an accessible dashboard with provenance and limitations.

## License

Apache License 2.0. See [LICENSE](LICENSE).
