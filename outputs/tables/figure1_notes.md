# Figure 1: starting wage distributions

The figure reconstructs each state's wage distribution before and after the policy. Each distribution excludes only missing wages for its own state and wave; it does not require complete employment data or two valid wage observations for the same store. Percentages sum to 100% within each state and wave.

Bins are 10 cents wide and include their lower endpoint: [4.20, 4.30), [4.30, 4.40), and so on. The last bin includes all wages at or above 5.50. The graph labels that tail 5.50+ rather than the original 5.55. Integer-cent binning and independent interval counts check the classification.

For the course data, valid wage counts are NJ 314 and PA 76 before the policy, and NJ 318 and PA 71 afterward. In post-policy NJ, 284/318 = 89.31% are in [5.00, 5.10). Table 2 instead counts wages exactly equal to 5.05: 283/331 = 85.5%, using all surveyed NJ stores. These percentages measure different events with different denominators.

Post-policy NJ wages concentrate near the new minimum, while PA remains more dispersed. The panels use different y-axis scales. Bin boundaries and upper-tail handling are explicit reconstruction choices: exact bar-by-bar agreement with the original figure has not been verified. Marginal distributions do not show individual wage transitions or identify an employment effect.

## Current generated results

The tables below are generated from this run. Interpretation notes describe the assigned course dataset; consult the numeric files for full precision.

### Sample and denominator checks

| wave | state | surveyed | valid_wages | missing_wages | minimum | maximum | high_tail_n | percent_total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NJ | 331 | 314 | 17 | 4.25 | 5.75 | 9 | 100 |
| 1 | PA | 79 | 76 | 3 | 4.25 | 5.5 | 2 | 100 |
| 2 | NJ | 331 | 318 | 13 | 5 | 5.75 | 11 | 100 |
| 2 | PA | 79 | 71 | 8 | 4.25 | 6.25 | 1 | 100 |

### Bin counts and percentages

| wave | state | bin_index | label | lower_inclusive | upper_exclusive | upper_tail | count | valid_wage_n | percent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NJ | 0 | 4.25 | 4.2 | 4.3 | False | 101 | 314 | 32.1656 |
| 1 | NJ | 1 | 4.35 | 4.3 | 4.4 | False | 12 | 314 | 3.82166 |
| 1 | NJ | 2 | 4.45 | 4.4 | 4.5 | False | 3 | 314 | 0.955414 |
| 1 | NJ | 3 | 4.55 | 4.5 | 4.6 | False | 52 | 314 | 16.5605 |
| 1 | NJ | 4 | 4.65 | 4.6 | 4.7 | False | 20 | 314 | 6.36943 |
| 1 | NJ | 5 | 4.75 | 4.7 | 4.8 | False | 38 | 314 | 12.1019 |
| 1 | NJ | 6 | 4.85 | 4.8 | 4.9 | False | 13 | 314 | 4.14013 |
| 1 | NJ | 7 | 4.95 | 4.9 | 5 | False | 2 | 314 | 0.636943 |
| 1 | NJ | 8 | 5.05 | 5 | 5.1 | False | 50 | 314 | 15.9236 |
| 1 | NJ | 9 | 5.15 | 5.1 | 5.2 | False | 5 | 314 | 1.59236 |
| 1 | NJ | 10 | 5.25 | 5.2 | 5.3 | False | 6 | 314 | 1.91083 |
| 1 | NJ | 11 | 5.35 | 5.3 | 5.4 | False | 2 | 314 | 0.636943 |
| 1 | NJ | 12 | 5.45 | 5.4 | 5.5 | False | 1 | 314 | 0.318471 |
| 1 | NJ | 13 | 5.50+ | 5.5 | - | True | 9 | 314 | 2.86624 |
| 1 | PA | 0 | 4.25 | 4.2 | 4.3 | False | 26 | 76 | 34.2105 |
| 1 | PA | 1 | 4.35 | 4.3 | 4.4 | False | 1 | 76 | 1.31579 |
| 1 | PA | 2 | 4.45 | 4.4 | 4.5 | False | 0 | 76 | 0 |
| 1 | PA | 3 | 4.55 | 4.5 | 4.6 | False | 13 | 76 | 17.1053 |
| 1 | PA | 4 | 4.65 | 4.6 | 4.7 | False | 1 | 76 | 1.31579 |
| 1 | PA | 5 | 4.75 | 4.7 | 4.8 | False | 10 | 76 | 13.1579 |
| 1 | PA | 6 | 4.85 | 4.8 | 4.9 | False | 1 | 76 | 1.31579 |
| 1 | PA | 7 | 4.95 | 4.9 | 5 | False | 0 | 76 | 0 |
| 1 | PA | 8 | 5.05 | 5 | 5.1 | False | 20 | 76 | 26.3158 |
| 1 | PA | 9 | 5.15 | 5.1 | 5.2 | False | 0 | 76 | 0 |
| 1 | PA | 10 | 5.25 | 5.2 | 5.3 | False | 2 | 76 | 2.63158 |
| 1 | PA | 11 | 5.35 | 5.3 | 5.4 | False | 0 | 76 | 0 |
| 1 | PA | 12 | 5.45 | 5.4 | 5.5 | False | 0 | 76 | 0 |
| 1 | PA | 13 | 5.50+ | 5.5 | - | True | 2 | 76 | 2.63158 |
| 2 | NJ | 0 | 4.25 | 4.2 | 4.3 | False | 0 | 318 | 0 |
| 2 | NJ | 1 | 4.35 | 4.3 | 4.4 | False | 0 | 318 | 0 |
| 2 | NJ | 2 | 4.45 | 4.4 | 4.5 | False | 0 | 318 | 0 |
| 2 | NJ | 3 | 4.55 | 4.5 | 4.6 | False | 0 | 318 | 0 |
| 2 | NJ | 4 | 4.65 | 4.6 | 4.7 | False | 0 | 318 | 0 |
| 2 | NJ | 5 | 4.75 | 4.7 | 4.8 | False | 0 | 318 | 0 |
| 2 | NJ | 6 | 4.85 | 4.8 | 4.9 | False | 0 | 318 | 0 |
| 2 | NJ | 7 | 4.95 | 4.9 | 5 | False | 0 | 318 | 0 |
| 2 | NJ | 8 | 5.05 | 5 | 5.1 | False | 284 | 318 | 89.3082 |
| 2 | NJ | 9 | 5.15 | 5.1 | 5.2 | False | 3 | 318 | 0.943396 |
| 2 | NJ | 10 | 5.25 | 5.2 | 5.3 | False | 18 | 318 | 5.66038 |
| 2 | NJ | 11 | 5.35 | 5.3 | 5.4 | False | 1 | 318 | 0.314465 |
| 2 | NJ | 12 | 5.45 | 5.4 | 5.5 | False | 1 | 318 | 0.314465 |
| 2 | NJ | 13 | 5.50+ | 5.5 | - | True | 11 | 318 | 3.45912 |
| 2 | PA | 0 | 4.25 | 4.2 | 4.3 | False | 20 | 71 | 28.169 |
| 2 | PA | 1 | 4.35 | 4.3 | 4.4 | False | 5 | 71 | 7.04225 |
| 2 | PA | 2 | 4.45 | 4.4 | 4.5 | False | 2 | 71 | 2.8169 |
| 2 | PA | 3 | 4.55 | 4.5 | 4.6 | False | 11 | 71 | 15.493 |
| 2 | PA | 4 | 4.65 | 4.6 | 4.7 | False | 0 | 71 | 0 |
| 2 | PA | 5 | 4.75 | 4.7 | 4.8 | False | 14 | 71 | 19.7183 |
| 2 | PA | 6 | 4.85 | 4.8 | 4.9 | False | 0 | 71 | 0 |
| 2 | PA | 7 | 4.95 | 4.9 | 5 | False | 3 | 71 | 4.22535 |
| 2 | PA | 8 | 5.05 | 5 | 5.1 | False | 14 | 71 | 19.7183 |
| 2 | PA | 9 | 5.15 | 5.1 | 5.2 | False | 0 | 71 | 0 |
| 2 | PA | 10 | 5.25 | 5.2 | 5.3 | False | 1 | 71 | 1.40845 |
| 2 | PA | 11 | 5.35 | 5.3 | 5.4 | False | 0 | 71 | 0 |
| 2 | PA | 12 | 5.45 | 5.4 | 5.5 | False | 0 | 71 | 0 |
| 2 | PA | 13 | 5.50+ | 5.5 | - | True | 1 | 71 | 1.40845 |

![figure1.png](../figures/figure1.png)
