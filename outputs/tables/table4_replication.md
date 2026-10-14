# Table 4: employment-change regressions

The common sample uses valid employment changes and two valid wages, with the author's permanent-closure exception. The course data retain 357 stores (NJ 290; PA 67), including six permanent closures with follow-up FTE set to zero. Of the 384 paired employment stores, 27 are excluded by wage requirements. Temporary closures remain missing.

GAP = 0 in PA and max((5.05 - initial wage) / initial wage, 0) in NJ. An initial wage of 4.25 implies GAP = 0.188235. GAP coefficients are per unit proportional gap, not per dollar or per percentage point.

Models: (i) NJ; (ii) NJ with brand and ownership controls; (iii) GAP; (iv) GAP with brand and ownership controls; (v) GAP with brand, ownership and region controls, following the paper note. Wendy's and North NJ are reference categories. A full region set cannot be combined with NJ because of collinearity.

The replication uses conventional OLS coefficient SEs. The regression SE is residual SD, not the policy coefficient's SE. The controls p value is a joint test of the additional controls, not a policy p value. The displayed results come from the current numeric CSV.

The first four models match the published regression cells; 16/18 regression cells match overall. The paper-note fifth specification gives GAP 11.98 (7.42), while the paper prints 11.91 (7.39). Author check.sas omits ownership from that specification and gives 11.91 (7.39), residual SE 8.74 and controls p about 0.31, compared with the printed 8.75 and 0.40. Separate author-SAS outputs preserve this difference; values from the two models must not be spliced into one column.

The course sample's outcome mean -0.237535 rounds to -0.238 rather than the published -0.237. This descriptive difference is outside the 18-cell regression audit. Model (v) is not significant at the usual 5% level. Computational agreement does not validate parallel trends or overcome the two-state inference limitation.

## Current generated results

The tables below are generated from this run. Interpretation notes describe the assigned course dataset; consult the numeric files for full precision.

### Regression results

| estimate | se | regression_se | controls_p | n | residual_df | t | coefficient_p | ci95_low | ci95_high | model | variable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.32583 | 1.1916 | 8.79086 | - | 357 | 355 | 1.95186 | 0.0517406 | -0.0176441 | 4.66931 | i | nj |
| 2.30386 | 1.19553 | 8.78466 | 0.344251 | 357 | 351 | 1.92706 | 0.0547794 | -0.0474487 | 4.65517 | ii | nj |
| 15.6529 | 6.08024 | 8.75655 | - | 357 | 355 | 2.57439 | 0.0104464 | 3.69508 | 27.6107 | iii | gap |
| 14.9157 | 6.20533 | 8.75921 | 0.43736 | 357 | 351 | 2.40369 | 0.0167487 | 2.71136 | 27.12 | iv | gap |
| 11.9792 | 7.41912 | 8.75249 | 0.40457 | 357 | 347 | 1.61464 | 0.107297 | -2.61287 | 26.5713 | v | gap |

### Published-cell audit

| model | metric | replicated | published | match_at_precision |
| --- | --- | --- | --- | --- |
| i | estimate | 2.32583 | 2.33 | True |
| i | se | 1.1916 | 1.19 | True |
| i | regression_se | 8.79086 | 8.79 | True |
| ii | estimate | 2.30386 | 2.3 | True |
| ii | se | 1.19553 | 1.2 | True |
| ii | regression_se | 8.78466 | 8.78 | True |
| ii | controls_p | 0.344251 | 0.34 | True |
| iii | estimate | 15.6529 | 15.65 | True |
| iii | se | 6.08024 | 6.08 | True |
| iii | regression_se | 8.75655 | 8.76 | True |
| iv | estimate | 14.9157 | 14.92 | True |
| iv | se | 6.20533 | 6.21 | True |
| iv | regression_se | 8.75921 | 8.76 | True |
| iv | controls_p | 0.43736 | 0.44 | True |
| v | estimate | 11.9792 | 11.91 | False |
| v | se | 7.41912 | 7.39 | False |
| v | regression_se | 8.75249 | 8.75 | True |
| v | controls_p | 0.40457 | 0.4 | True |

### Author-SAS fifth model

| estimate | se | regression_se | controls_p | n | residual_df | t | coefficient_p | ci95_low | ci95_high | model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11.9131 | 7.39441 | 8.74016 | 0.307491 | 357 | 348 | 1.61109 | 0.108067 | -2.63029 | 26.4564 | v_author_sas_without_ownership |
