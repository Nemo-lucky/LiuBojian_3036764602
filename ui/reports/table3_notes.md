# Table 3: employment changes and difference-in-differences

DID = (NJ after - NJ before) - (PA after - PA before). NJ stores are also compared by initial starting wage: low, middle and high wage groups. Row 1 compares pre-policy levels, row 2 post-policy levels, row 3 changes using all available observations in each wave, row 4 paired-store changes, and row 5 paired changes with temporary closures assigned zero follow-up employment as a separate sensitivity check.

For the course data, the paired sample contains 384 stores: NJ 309 and PA 75. The temporary-zero sample contains 388 stores. The paired state DID is 2.75 FTE, SE 1.34, matching the paper at displayed precision. The temporary-zero DID is 2.51, SE 1.35.

The unbalanced-wave observations overlap. Row 3 uses overlap-aware store influence scores with G/(G-1) correction, independently checked using stacked OLS. Missing employment is not filled with zero. The original row 3 SE algorithm is unconfirmed, so this is a transparent reconstruction rather than a claim to reproduce the author's exact method.

The audit checks 80 published estimates and SEs; 66 match and 14 differ. Several differences are row 3 SEs. The current unbalanced DID is 2.753605783, which rounds to 2.75 rather than the published 2.76. The difference cannot simply be attributed to rounding; its original cause remains unverified. No baseline data are altered to force agreement.

Positive relative employment changes depend on comparison-group and trend assumptions. There is only one pre-policy wave and two states, limiting causal and policy-level inference.
