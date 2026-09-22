# Data Dictionary Contract

This contract defines the initial synthetic dataset. It contains no direct identifiers and is not a template for collecting real client records.

| Table | Field | Type | Description | Privacy class |
|---|---|---|---|---|
| clients | `client_id` | string | Stable synthetic identifier | Synthetic identifier |
| clients | `survey_round` | category | `baseline` or `followup` observation context | Synthetic attribute |
| clients | `age_band` | category | Coarse age group, never exact birth date | Sensitive attribute |
| clients | `gender` | category | Self-described or generated analysis group | Sensitive attribute |
| clients | `district` | category | Coarse location for subgroup analysis | Quasi-identifier |
| households | `household_size` | integer | Number of household members | Synthetic attribute |
| households | `monthly_household_income` | number | Reported or generated monthly income | Financial attribute |
| businesses | `business_type` | category | Coarse economic activity | Synthetic attribute |
| businesses | `monthly_revenue` | number | Monthly business revenue | Financial attribute |
| businesses | `monthly_profit` | number | Monthly business profit after costs | Financial attribute |
| loans | `loan_purpose` | category | Productive, emergency, consumption or debt replacement | Financial attribute |
| loans | `loan_cycle` | integer | Borrowing cycle number | Financial attribute |
| loans | `monthly_debt_payment` | number | Total scheduled monthly payment for the project loan | Financial attribute |
| other_debts | `other_lender_count` | integer | Number of additional lenders reported | Financial attribute |
| other_debts | `total_other_lender_debt` | number | Outstanding debt with other lenders | Financial attribute |
| savings | `savings_balance` | number | Synthetic savings balance at observation date | Financial attribute |
| wellbeing_surveys | `food_security_score` | number | Score from the documented synthetic instrument | Sensitive outcome |
| wellbeing_surveys | `essential_expense_reduction` | boolean | Whether essential spending reportedly fell | Sensitive outcome |
| agency_surveys | `women_loan_control_score` | number | Reported control over loan use, from 0 to 1 | Sensitive outcome |
| agency_surveys | `women_income_control_score` | number | Reported control over income, from 0 to 1 | Sensitive outcome |
| outcome_surveys | `business_operating` | boolean | Whether the financed business is operating | Outcome |
| outcome_surveys | `satisfaction_score` | integer | Follow-up satisfaction response on a 1-to-5 scale | Survey response |
| complaints | `complaint_category` | category | Standardized complaint type | Client voice |
| complaints | `resolved_at` | date or null | Resolution date, if resolved | Client voice |
| dropout_events | `exit_reason` | category | Standardized voluntary-exit reason | Client voice |

## Rules

- CI2 must use synthetic IDs and a fixed random seed.
- Exact addresses, phone numbers, national IDs, names and free-text responses are prohibited.
- Dates must use month or quarter precision unless a test specifically requires a day.
- Generator validation must reject negative financial values, invalid score ranges and unknown categories.
- Published outputs should aggregate these fields and suppress small groups.
- Satisfaction scores are synthetic follow-up responses and do not represent a validated real-world survey instrument.
