# Table 2 — replication and comparison

Input: unmodified course `public.csv`.

NJ and PA entries show mean (standard error). N is available in the numeric output. Published values were transcribed from Table 2, printed page 776.

| Row | Variable | Replicated NJ (SE) | Replicated PA (SE) | t | Paper NJ / PA / t |
|---|---|---:|---:|---:|---:|
| 1a | Burger King (%) | 41.1 (2.7) | 44.3 (5.6) | -0.5 | 41.1 / 44.3 / -0.5 |
| 1b | KFC (%) | 20.5 (2.2) | 15.2 (4.1) | 1.2 | 20.5 / 15.2 / 1.2 |
| 1c | Roy Rogers (%) | 24.8 (2.4) | 21.5 (4.7) | 0.6 | 24.8 / 21.5 / 0.6 |
| 1d | Wendy's (%) | 13.6 (1.9) | 19.0 (4.4) | -1.1 | 13.6 / 19.0 / -1.1 |
| 1e | Company-owned (%) | 34.1 (2.6) | 35.4 (5.4) | -0.2 | 34.1 / 35.4 / -0.2 |
| 2a | Before: FTE employment | 20.4 (0.51) | 23.3 (1.35) | -2.0 | 20.4 / 23.3 / -2.0 |
| 2b | Before: full-time employees (% of FTE) | 32.8 (1.3) | 35.0 (2.7) | -0.7 | 32.8 / 35.0 / -0.7 |
| 2c | Before: starting wage ($/hour) | 4.61 (0.02) | 4.63 (0.04) | -0.4 | 4.61 / 4.63 / -0.4 |
| 2d | Before: reported wage = $4.25 (%) | 30.5 (2.5) | 32.9 (5.3) | -0.4 | 30.5 / 32.9 / -0.4 |
| 2e | Before: full meal price ($) | 3.35 (0.04) | 3.04 (0.07) | 4.0 | 3.35 / 3.04 / 4.0 |
| 2f | Before: hours open | 14.4 (0.2) | 14.5 (0.3) | -0.3 | 14.4 / 14.5 / -0.3 |
| 2g | Before: recruiting bonus (%) | 23.6 (2.3) | 29.1 (5.1) | -1.0 | 23.6 / 29.1 / -1.0 |
| 3a | After: FTE employment | 21.0 (0.52) | 21.2 (0.94) | -0.1 | 21.0 / 21.2 / -0.2 |
| 3b | After: full-time employees (% of FTE) | 35.9 (1.4) | 30.4 (2.8) | 1.8 | 35.9 / 30.4 / 1.8 |
| 3c | After: starting wage ($/hour) | 5.08 (0.01) | 4.62 (0.04) | 10.8 | 5.08 / 4.62 / 10.8 |
| 3d | After: reported wage = $4.25 (%) | 0.0 (0.0) | 25.3 (4.9) | — | 0.0 / 25.3 / — |
| 3e | After: reported wage = $5.05 (%) | 85.5 (1.9) | 1.3 (1.3) | 36.4 | 85.2 / 1.3 / 36.1 |
| 3f | After: full meal price ($) | 3.41 (0.04) | 3.03 (0.07) | 5.1 | 3.41 / 3.03 / 5.0 |
| 3g | After: hours open | 14.4 (0.2) | 14.7 (0.3) | -0.6 | 14.4 / 14.7 / -0.8 |
| 3h | After: recruiting bonus (%) | 20.3 (2.3) | 23.4 (4.9) | -0.6 | 20.3 / 23.4 / -0.6 |

## Definitions and sample choices

- FTE = full-time employees + managers + 0.5 × part-time employees. Missing components stay missing.
- Permanent closures have zero follow-up FTE; temporary closures / renovations have missing follow-up FTE.
- Full-time percentage follows author check.sas: 100 × EMPFT / FTE, excluding zero/missing FTE. This is not the full-time share of raw headcount.
- Meal price = soda + fries + entree; a missing component produces a missing total.
- Means otherwise use the available observations separately for each variable, not one globally complete-case sample.
- Wage-equality indicators follow check.sas: proportion of all surveyed stores reporting the target wage. Missing wages contribute zero to this indicator only. The valid-wage denominator alternative is exported separately.
- SE = sample SD / sqrt(N). t uses sqrt(SE_NJ² + SE_PA²); no equal-variance assumption. Row 3d t is omitted in the display as in the paper; the computed t remains in the numeric output.

## Differences at the paper's displayed precision

- 3a t: -0.1, paper -0.2.
- 3e NJ mean: 85.5, paper 85.2.
- 3e t: 36.4, paper 36.1.
- 3f t: 5.1, paper 5.0.
- 3g t: -0.6, paper -0.8.

The 3e NJ difference corresponds to 283/331 stores in the data (85.5%), versus approximately 282/331 in the paper (85.2%). Renovation store SHEET 65 reports WAGE_ST2 = 5.05; classifying its wage indicator as unavailable/false would remove one count. This is a possible explanation, not a verified original-paper coding rule; baseline values are preserved.

These descriptive results alone do not establish a causal policy effect. Employment effects and the ownership extension are examined in the separate stage outputs.

The comparison above covers means and t statistics. The complete audit including published standard errors is in table2_audit_中文.md (82 of 88 published values match at displayed precision).
