# AI-use disclosure

**Course:** ECO6067 individual project  
**Student:** Liu Bojian (3036764602)  
**Project:** Card and Krueger minimum-wage replication and ownership extension

## Where and how AI was used

An OpenAI Codex assistant was used interactively to explain the assignment and paper, inspect the course data dictionary, obtain and parse the author-hosted archive, construct variables and samples, implement Python analyses, compare published results, propose extension options, generate plots, draft the report and documentation, and develop the reusable skill and local browser interface. This document does not assert a specific model version beyond the product used.

The student chose the minimum-wage topic, Python and the ownership extension; ran the staged scripts and unified workflow locally; requested explicit skill invocation; and supplied the report identity. AI assisted with implementation, calculation checks, writing and fresh-environment validation. The student remains responsible for understanding and reviewing the final methods, outputs and claims. This disclosure does not claim that the student independently wrote or checked every algorithm.

## How AI outputs were checked

| Area | Check and evidence |
|---|---|
| Data and samples | Course CSV compared with parsed author data: all 410 × 46 numeric values and missing positions matched. Identifiers, closure codes and sample counts were checked. See `docs/course_data_validation.json` and `docs/data_provenance.json`. |
| Core replication | Published means, SEs and other printed values were audited at their displayed precision. All remaining differences are preserved in `results/table2_audit_cells.csv`, `table3_audit_cells.csv` and `table4_audit_cells.csv`. |
| Independent calculations | Table 3 checked against alternative OLS representations; Table 4 OLS and joint tests checked through QR and Wald calculations; extension HC3 covariance and contrasts checked independently. See stage validation JSON files in `results/`. |
| Figures and writing | Generated figures and the prior Word rendering were visually inspected. The current Markdown report retains the reviewed scientific content; its image and internal file links are checked. |
| Reproducibility | Five stages regenerated 39 outputs. Fresh-directory and fresh-environment runs compared 22 CSVs within documented tolerances. Input, code and output hashes were verified. See `docs/clean_reproduction_validation.json` and `docs/teacher_download_validation.json`. |
| Skill and local page | Explicit skill invocation, result verification, browser execution and English result display were tested. Evidence is in the corresponding validation JSON files under `docs/`. |

The fresh-environment tests used the same Windows host, not a second computer or an actual GitHub clone. Calculation and integrity checks do not establish causal identification or perfect publication agreement.

## Important errors and suggestions corrected or rejected

1. **Extension already present in the paper.** The initial suggestion to compare low- and high-wage NJ restaurants was rejected as a standalone independent extension because the original paper already makes that comparison. Ownership-by-policy interaction was selected instead.
2. **Identifier uniqueness.** An initial global uniqueness check for SHEET failed because 407 appears once in each state. Both records were retained; `(STATE, SHEET)` was checked and a source-row identifier preserved row order.
3. **Incomplete Table 2 audit.** The initial comparison covered means and t statistics but omitted SE discrepancies. The expanded audit records six mismatches across 88 printed values.
4. **Unverified renovation-store explanation.** Changing one wage indicator could reproduce a published mean and SE, but not the t statistic. It was retained only as a diagnostic; the baseline data were not recoded to force agreement.
5. **Incorrect rounding explanation for Table 3.** AI initially attributed the paper's 2.76 to using unrounded values. The actual unbalanced estimate is 2.753605783 and rounds to 2.75. That explanation was rejected; the publication difference remains unresolved.
6. **Table 4 specification inconsistency.** The paper-note fifth model includes ownership, whereas the author SAS specification omits it. Both are reported separately. Matching coefficient and SE under the SAS version does not reproduce the entire column; values were not mixed across models.
7. **Overinterpretation avoided.** The imprecise ownership interaction is described as insufficient evidence of a difference, not proof of equal effects. The primary specification was not replaced to seek statistical significance.

## Current status and supporting records

The narrative report is [Markdown](report/ECO6067_Empirical_Report.md). The detailed chronological record is [AI_USE_LOG.md](docs/AI_USE_LOG.md); earlier pending statements in that historical log refer to those stages, not current completion status. Review [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) for current delivery tasks. No fabricated Git history, completed GitHub upload or verified teaching-team access is claimed.
