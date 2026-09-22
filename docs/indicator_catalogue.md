# Indicator Catalogue

All indicators must document their numerator, denominator, time period, missing-data
handling, subgroup limitations and interpretation before appearing in results. CI2 will
generate the synthetic client-level fields used by the indicators below.

| Indicator | Formula | Planned source | Interpretation limit |
|---|---|---|---|
| Debt-service ratio | Monthly debt payments / monthly household income | Synthetic, CI2 | A screening signal, not a credit decision |
| Income change | Follow-up income - baseline income | Synthetic, CI2 | Descriptive change; not automatically causal |
| Income growth rate | (Follow-up income - baseline income) / baseline income | Synthetic, CI2 | Undefined when baseline income is zero |
| Business profit change | Follow-up profit - baseline profit | Synthetic, CI2 | Requires comparable reporting periods |
| Business survival rate | Businesses operating at follow-up / financed businesses observed | Synthetic, CI2 | Sensitive to loss to follow-up |
| Employment change | Follow-up workers - baseline workers | Synthetic, CI2 | Self-reported or modelled employment may be noisy |
| Savings change | Follow-up savings balance - baseline savings balance | Synthetic, CI2 | Does not measure total household wealth |
| Emergency savings coverage | Savings balance / average monthly essential expenses | Synthetic, CI2 | Depends on the essential-expense definition |
| Multiple-borrowing rate | Clients with two or more lenders / active clients | Synthetic, CI2 | Requires complete lender reporting |
| Debt-recycling rate | Clients using new borrowing to repay old debt / surveyed borrowers | Synthetic, CI2 | Based on reported loan use |
| Essential-spending reduction | Clients reporting reduced essential spending / respondents | Synthetic, CI2 | Subject to recall and non-response bias |
| Food-security score change | Follow-up score - baseline score | Synthetic, CI2 | The score requires a documented instrument |
| Women loan-control score | Reported control over loan use, scaled 0 to 1 | Synthetic, CI2 | Captures reported agency, not all power dynamics |
| Women income-control score | Reported control over business income, scaled 0 to 1 | Synthetic, CI2 | Do not compare small groups without suppression |
| Satisfaction score | Mean valid satisfaction response | Synthetic, CI2 | Response rates must be displayed |
| Complaint rate | Complaints / active clients, usually per 1,000 | Synthetic, CI2 | More complaints can also indicate better access to reporting |
| Complaint resolution rate | Resolved complaints / closed complaints | Synthetic, CI2 | Open cases need a separate count |
| Median resolution time | Median days from complaint to resolution | Synthetic, CI2 | Exclude unresolved cases and report them separately |
| Voluntary-exit rate | Voluntary exits / active clients at period start | Synthetic, CI2 | Exit reason may be missing or misclassified |
| Support-review flag rate | Clients meeting configured support flags / assessed clients | Synthetic, CI2 | Thresholds are assumptions, not universal standards |
