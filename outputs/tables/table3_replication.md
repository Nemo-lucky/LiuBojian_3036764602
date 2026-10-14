# Table 3: employment changes and difference-in-differences

DID = (NJ after - NJ before) - (PA after - PA before). NJ stores are also compared by initial starting wage: low, middle and high wage groups. Row 1 compares pre-policy levels, row 2 post-policy levels, row 3 changes using all available observations in each wave, row 4 paired-store changes, and row 5 paired changes with temporary closures assigned zero follow-up employment as a separate sensitivity check.

For the course data, the paired sample contains 384 stores: NJ 309 and PA 75. The temporary-zero sample contains 388 stores. The paired state DID is 2.75 FTE, SE 1.34, matching the paper at displayed precision. The temporary-zero DID is 2.51, SE 1.35.

The unbalanced-wave observations overlap. Row 3 uses overlap-aware store influence scores with G/(G-1) correction, independently checked using stacked OLS. Missing employment is not filled with zero. The original row 3 SE algorithm is unconfirmed, so this is a transparent reconstruction rather than a claim to reproduce the author's exact method.

The audit checks 80 published estimates and SEs; 66 match and 14 differ. Several differences are row 3 SEs. The current unbalanced DID is 2.753605783, which rounds to 2.75 rather than the published 2.76. The difference cannot simply be attributed to rounding; its original cause remains unverified. No baseline data are altered to force agreement.

Positive relative employment changes depend on comparison-group and trend assumptions. There is only one pre-policy wave and two states, limiting causal and policy-level inference.

## Current generated results

The tables below are generated from this run. Interpretation notes describe the assigned course dataset; consult the numeric files for full precision.

### Employment estimates and SEs

| row | column | estimate | se | published_estimate | published_se |
| --- | --- | --- | --- | --- | --- |
| 1 | PA | 23.3312 | 1.35115 | 23.33 | 1.35 |
| 1 | NJ | 20.4394 | 0.508261 | 20.44 | 0.51 |
| 1 | NJ-PA | -2.89176 | 1.44358 | -2.89 | 1.44 |
| 1 | NJ_low | 19.5567 | 0.774856 | 19.56 | 0.77 |
| 1 | NJ_mid | 20.0807 | 0.841274 | 20.08 | 0.84 |
| 1 | NJ_high | 22.25 | 1.1358 | 22.25 | 1.14 |
| 1 | Low-High | -2.6933 | 1.37493 | -2.69 | 1.37 |
| 1 | Mid-High | -2.16934 | 1.41343 | -2.17 | 1.41 |
| 2 | PA | 21.1656 | 0.943221 | 21.17 | 0.94 |
| 2 | NJ | 21.0274 | 0.520309 | 21.03 | 0.52 |
| 2 | NJ-PA | -0.138155 | 1.07721 | -0.14 | 1.07 |
| 2 | NJ_low | 20.8776 | 1.0059 | 20.88 | 1.01 |
| 2 | NJ_mid | 20.9556 | 0.755608 | 20.96 | 0.76 |
| 2 | NJ_high | 20.2138 | 1.0251 | 20.21 | 1.03 |
| 2 | Low-High | 0.663783 | 1.4362 | 0.67 | 1.44 |
| 2 | Mid-High | 0.741787 | 1.27349 | 0.75 | 1.27 |
| 3 | PA | -2.16558 | 1.22199 | -2.16 | 1.25 |
| 3 | NJ | 0.588021 | 0.472146 | 0.59 | 0.54 |
| 3 | NJ-PA | 2.75361 | 1.31003 | 2.76 | 1.36 |
| 3 | NJ_low | 1.32085 | 0.811592 | 1.32 | 0.95 |
| 3 | NJ_mid | 0.874899 | 0.672801 | 0.87 | 0.84 |
| 3 | NJ_high | -2.03623 | 0.981906 | -2.04 | 1.14 |
| 3 | Low-High | 3.35708 | 1.2739 | 3.36 | 1.48 |
| 3 | Mid-High | 2.91113 | 1.19029 | 2.91 | 1.41 |
| 4 | PA | -2.28333 | 1.25327 | -2.28 | 1.25 |
| 4 | NJ | 0.466667 | 0.480829 | 0.47 | 0.48 |
| 4 | NJ-PA | 2.75 | 1.34234 | 2.75 | 1.34 |
| 4 | NJ_low | 1.20479 | 0.82249 | 1.21 | 0.82 |
| 4 | NJ_mid | 0.709848 | 0.686227 | 0.71 | 0.69 |
| 4 | NJ_high | -2.15672 | 1.00732 | -2.16 | 1.01 |
| 4 | Low-High | 3.3615 | 1.30046 | 3.36 | 1.3 |
| 4 | Mid-High | 2.86656 | 1.21885 | 2.87 | 1.22 |
| 5 | PA | -2.28333 | 1.25327 | -2.28 | 1.25 |
| 5 | NJ | 0.225879 | 0.490979 | 0.23 | 0.49 |
| 5 | NJ-PA | 2.50921 | 1.34601 | 2.51 | 1.35 |
| 5 | NJ_low | 0.897368 | 0.869916 | 0.9 | 0.87 |
| 5 | NJ_mid | 0.49403 | 0.692838 | 0.49 | 0.69 |
| 5 | NJ_high | -2.38971 | 1.01938 | -2.39 | 1.02 |
| 5 | Low-High | 3.28707 | 1.34011 | 3.29 | 1.34 |
| 5 | Mid-High | 2.88374 | 1.23254 | 2.88 | 1.23 |

### Sample counts

| group | all_stores | before_n | after_n | paired_n | temp_zero_paired_n |
| --- | --- | --- | --- | --- | --- |
| PA | 79 | 77 | 77 | 75 | 75 |
| NJ | 331 | 321 | 319 | 309 | 313 |
| NJ_low | 101 | 97 | 98 | 94 | 95 |
| NJ_mid | 140 | 137 | 135 | 132 | 134 |
| NJ_high | 73 | 71 | 69 | 67 | 68 |

### Unmatched published cells

| row | column | metric | value | display | published | matches |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | NJ-PA | se | 1.07721 | 1.08 | 1.07 | False |
| 2 | Low-High | estimate | 0.663783 | 0.66 | 0.67 | False |
| 2 | Mid-High | estimate | 0.741787 | 0.74 | 0.75 | False |
| 3 | PA | estimate | -2.16558 | -2.17 | -2.16 | False |
| 3 | PA | se | 1.22199 | 1.22 | 1.25 | False |
| 3 | NJ | se | 0.472146 | 0.47 | 0.54 | False |
| 3 | NJ-PA | estimate | 2.75361 | 2.75 | 2.76 | False |
| 3 | NJ-PA | se | 1.31003 | 1.31 | 1.36 | False |
| 3 | NJ_low | se | 0.811592 | 0.81 | 0.95 | False |
| 3 | NJ_mid | se | 0.672801 | 0.67 | 0.84 | False |
| 3 | NJ_high | se | 0.981906 | 0.98 | 1.14 | False |
| 3 | Low-High | se | 1.2739 | 1.27 | 1.48 | False |
| 3 | Mid-High | se | 1.19029 | 1.19 | 1.41 | False |
| 4 | NJ_low | estimate | 1.20479 | 1.2 | 1.21 | False |
