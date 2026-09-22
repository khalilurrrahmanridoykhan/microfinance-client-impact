# Inclusion and Client Voice Analysis

CI6 covers two related but distinct views of client experience.

## Gender and inclusion

`make inclusion` reports women borrowers' reported loan-use and income-control scores overall
and by district. Groups below the configured minimum size are marked `suppressed` rather than
published with unstable or potentially identifying results.

The scores describe reported agency in the synthetic survey instrument. They do not measure
all household power dynamics, and subgroup differences are not causal findings.

## Client voice

`make client-voice` reports:

- mean follow-up satisfaction score;
- complaint count and complaints per 1,000 active clients;
- complaint resolution rate and median resolution time;
- voluntary-exit count and rate;
- complaint categories; and
- exit reasons.

Complaint volume can rise when clients have better access to reporting, so a higher rate is
not automatically evidence of worse service. Unresolved complaints are excluded from median
resolution time and retained in the resolution-rate denominator.

Both reports are aggregate-only, marked synthetic and unsuitable for individual client
ranking, credit decisions or claims about real borrowers.