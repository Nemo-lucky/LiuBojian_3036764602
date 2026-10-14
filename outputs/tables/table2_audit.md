# Table 2: descriptive statistics and publication comparison

The displayed CSV contains state means, standard errors, available sample sizes and NJ-minus-PA t statistics. FTE = full-time workers + managers + 0.5 x part-time workers. Missing employment components remain missing. Permanent closures have zero follow-up FTE; temporary closures remain missing in the baseline. Meal price is soda + fries + entree; any missing component makes the total missing.

Each variable uses its own available observations. Exact-wage indicators follow the author's SAS convention: divide by all surveyed stores, with missing wages contributing zero to that indicator only. Figure 1 uses a different denominator. SE = sample SD / sqrt(N); the state contrast uses sqrt(SE_NJ^2 + SE_PA^2).

The established audit checks 88 published cells, with 82 matching at the paper's displayed precision. Six differences remain:
- Row 3a t: -0.1 versus -0.2.
- Row 3e NJ mean: 85.5% versus 85.2%.
- Row 3e NJ SE: 1.9 versus 2.0.
- Row 3e t: 36.4 versus 36.1.
- Row 3f t: 5.1 versus 5.0.
- Row 3g t: -0.6 versus -0.8.

A diagnostic treatment of renovation store SHEET 65 can match the row 3e mean and SE, but not its published t. This is not a verified original rule and is not used to change the baseline. Other discrepancies remain unresolved; rounding alone is not an established explanation. The historical course-to-author raw-data comparison matched all values and missing positions; the main workflow can run without that optional archive.

Descriptive state differences do not establish a causal employment effect. Download the numeric CSV for full precision; the browser table rounds numeric entries to three decimal places.

## Current generated results

The tables below are generated from this run. Interpretation notes describe the assigned course dataset; consult the numeric files for full precision.

### Unmatched published cells

| row | metric | calculated | calculated_display | published | digits | matches |
| --- | --- | --- | --- | --- | --- | --- |
| 3a | t | -0.128252 | -0.1 | -0.2 | 1 | False |
| 3e | nj_mean | 85.4985 | 85.5 | 85.2 | 1 | False |
| 3e | t | 36.3848 | 36.4 | 36.1 | 1 | False |
| 3e | nj_se | 1.93834 | 1.9 | 2 | 1 | False |
| 3f | t | 5.07835 | 5.1 | 5 | 1 | False |
| 3g | t | -0.649206 | -0.6 | -0.8 | 1 | False |

### Alternative t calculations

| row | published_t | baseline_welch_t | pooled_t | population_variance_t |
| --- | --- | --- | --- | --- |
| 3a | -0.2 | -0.128252 | -0.119492 | -0.128943 |
| 3e | 36.1 | 36.3848 | 20.9597 | 36.4927 |
| 3f | 5 | 5.07835 | 4.72612 | 5.10815 |
| 3g | -0.8 | -0.649206 | -0.673168 | -0.652838 |

### Renovation-store diagnostic only; baseline unchanged

| nj_mean | nj_se | t |
| --- | --- | --- |
| 85.1964 | 1.95496 | 36.0374 |
