# Interpreting this replication

## Data and quantities

The input is the unchanged course Package 01 public.csv, 410 restaurants and 46 columns. Source SHEET is not globally unique; preserve both SHEET407 records, one in each state. The observed state/sheet pair is unique. The main workflow does not require the author's archive.

FTE = full-time workers + managers + 0.5 × part-time workers. Missing components remain missing. Six permanent closures have zero follow-up FTE. Four temporary/renovation closures stay missing in the baseline; Table 3 row 5 is a separate zero-closure sensitivity.

Samples are purpose-specific: variable-level available records for Table 2; nonmissing wages by state/wave for Figure 1; paired or unbalanced employment for Table 3; employment and wages with a permanent-closure exception for the common Table 4 sample. A standard input gives 384 paired employment stores, 388 with temporary closures zero, and 357 Table 4 stores. Read current counts from the actual outputs before reporting them.

GAP is zero in PA and max[(5.05 − initial starting wage)/initial starting wage, 0] in NJ. A4.25 initial wage implies GAP0.188235. A GAP coefficient is per unit proportional gap, not per dollar or per percentage point, and is not directly comparable to a binary NJ coefficient. NJ models cannot also include the full region dummy set because of collinearity.

## Known publication discrepancies

The established audit counts are Table 2 82/88, Table 3 66/80, Table 4 16/18. Read current audit files; these counts are not targets for adjusting data or algorithms.

- Table 2: six printed cells differ. NJ at exactly5.05 is283/331=85.5% versus85.2. A renovation-record diagnostic can match the mean and SE but not the printed t; it is not a verified original rule. Means and t alone were an incomplete earlier audit: the SE difference must also be disclosed.
- Figure 1:10-cent lower-inclusive bins and a final >=5.50 tail are documented reconstruction choices, not verified exact original edges. NJ's after-policy [5.00,5.10) bin is284/318=89.31%; its denominator and event differ from Table 2's exact-wage indicator. The two panels have different y scales.
- Table 3: unbalanced-row SE uses overlap-aware store influence scores with G/(G−1), independently checked against stacked OLS. The exact original algorithm is not confirmed. Current unbalanced DID2.753605783 rounds2.75, not the paper's2.76; do not attribute this discrepancy merely to rounding. Paired DID2.75 and temporary-zero DID2.51 match the paper at displayed precision.
- Table 4: the main fifth model follows the paper note and includes ownership, giving11.98(7.42), residual SE8.75 and joint controls p≈.40. Author check.sas omits ownership, giving11.91(7.39), residual SE8.74 and joint p≈.31. Matching the author's coefficient/SE does not reproduce the entire printed column. Never splice the two models. The sample outcome mean−.237535 rounds−.238 rather than printed−.237; this descriptive difference is outside the18-cell regression audit.

## Ownership extension

The primary model is employment change on NJ, company ownership, NJ×ownership, and three brand indicators, on the common357-store sample. The interaction is the company effect minus the non-company effect. The company effect is the NJ coefficient plus the interaction; its SE must include their covariance. The ownership main effect is the difference in employment changes within PA, not the difference in policy effects.

The existing primary estimate is about−0.942FTE, HC3 SE2.641,95% interval[−6.136,4.251], approximate p=.721. Treat these as historical cross-checks only; obtain current values from extension_ownership_effects.csv and filter model=NJ_brands_primary, contrast=company_minus_franchise.

GAP/brand, GAP/brand/region and the384-store NJ sample are supplementary checks, not alternatives selected to obtain significance. Failure to reject a zero interaction means insufficient evidence of a difference, not proof of equality. Comparing one group's significance with another group's significance is not a valid test of their difference.

## Limits

The extension uses store-level HC3 with approximate t(N−k) intervals. Only two states are observed, so HC3 cannot accommodate arbitrary common state shocks. Ownership is not randomized, brand controls do not remove every business difference, and one pre-policy wave cannot establish parallel pre-trends. Financing or decision authority are possible motivations, not measured mechanisms. The short survey cannot establish national, long-run employment or welfare effects.
