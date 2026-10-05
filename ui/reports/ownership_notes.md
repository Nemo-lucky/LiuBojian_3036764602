# Ownership extension: company-owned versus franchise / non-company stores

Research question: did employment respond differently to the minimum-wage increase by restaurant ownership? The primary model regresses employment change on NJ, company ownership, NJ x ownership and three brand indicators, using the common Table 4 sample. The interaction directly estimates the company-owned effect minus the franchise / non-company effect. Company-owned effects add the NJ and interaction coefficients; their SE includes the covariance.

Read the current interaction estimate, HC3 SE, 95% interval and approximate p value in the result cards and numeric CSV. The ownership main effect measures the difference in employment changes within PA; it is not the difference in policy effects. The co_owned indicator does not measure franchise contract details.

The unadjusted model, GAP with brands, GAP with brands and regions, and the employment-only 384-store sample are supplementary checks. All specifications are retained rather than selected for significance. GAP interactions have a different scale from binary NJ interactions.

Failure to reject a zero interaction means insufficient evidence of different responses, not proof of equal effects. Comparing one group's significance with another group's significance is not a valid test of their difference.

Inference uses store-level HC3 with approximate t(N-k) intervals. With only two states, HC3 cannot account for arbitrary common state shocks. Ownership is not randomized, brand controls cannot remove all business differences, and a single pre-policy wave cannot establish parallel pre-trends. Interpretation is exploratory and conditional on these limitations.

Checks compare QR estimates and HC3 covariance, unadjusted group DIDs, and the equivalent balanced long-panel triple interaction. These checks validate computations, not causal assumptions. Raw and store-level processed data remain local and excluded from public GitHub distribution.
