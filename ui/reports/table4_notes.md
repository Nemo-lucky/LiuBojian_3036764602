# Table 4: employment-change regressions

The common sample uses valid employment changes and two valid wages, with the author's permanent-closure exception. The course data retain 357 stores (NJ 290; PA 67), including six permanent closures with follow-up FTE set to zero. Of the 384 paired employment stores, 27 are excluded by wage requirements. Temporary closures remain missing.

GAP = 0 in PA and max((5.05 - initial wage) / initial wage, 0) in NJ. An initial wage of 4.25 implies GAP = 0.188235. GAP coefficients are per unit proportional gap, not per dollar or per percentage point.

Models: (i) NJ; (ii) NJ with brand and ownership controls; (iii) GAP; (iv) GAP with brand and ownership controls; (v) GAP with brand, ownership and region controls, following the paper note. Wendy's and North NJ are reference categories. A full region set cannot be combined with NJ because of collinearity.

The replication uses conventional OLS coefficient SEs. The regression SE is residual SD, not the policy coefficient's SE. The controls p value is a joint test of the additional controls, not a policy p value. The displayed results come from the current numeric CSV.

The first four models match the published regression cells; 16/18 regression cells match overall. The paper-note fifth specification gives GAP 11.98 (7.42), while the paper prints 11.91 (7.39). Author check.sas omits ownership from that specification and gives 11.91 (7.39), residual SE 8.74 and controls p about 0.31, compared with the printed 8.75 and 0.40. Separate author-SAS outputs preserve this difference; values from the two models must not be spliced into one column.

The course sample's outcome mean -0.237535 rounds to -0.238 rather than the published -0.237. This descriptive difference is outside the 18-cell regression audit. Model (v) is not significant at the usual 5% level. Computational agreement does not validate parallel trends or overcome the two-state inference limitation.
