# AI-use log — living document

## 2026-10-04: selection, sources and initial setup

AI helped interpret the assignment, identify the author-hosted paper and public survey data, write the downloader and initial Python data-audit script, and draft project documentation.

Checks performed: confirmed dataset links on the author's website; used the original codebook to parse fixed-width fields; compared the employment formula with the original paper and author-provided SAS code; checked sample counts, unique store IDs, status codes, and missingness. Initial numerical output must still be reviewed by the student.

Correction: AI initially suggested comparing low-wage and high-wage New Jersey restaurants as an independent extension. The original paper already contains this comparison, so it was rejected as an independent extension by itself.

Technical correction: the first download attempt through PowerShell failed at the TLS authentication stage. Python's standard HTTPS downloader retrieved the author's archive successfully without disabling certificate verification.

No final causal conclusion or completed replication is claimed at this stage. Record subsequent AI errors, student checks, and rejected suggestions here as the project progresses.

Data-validation correction: AI initially enforced global uniqueness of SHEET based on the codebook. That check failed because SHEET 407 occurs in PA (chain 2) and NJ (chain 4). The records were inspected and retained, the observed `(state, sheet)` key was verified as unique, and a source-row identifier was added. No observation was deleted to make the check pass.

## Course input and Table 2

AI copied the course folder into the project, leaving the desktop source unchanged; compared all 410 × 46 numeric entries and missing positions against the author's fixed-width file; and wrote a Table 2 workflow. Source PDF page 5 was rendered and visually inspected to transcribe the published means and t statistics, since text extraction omitted multiple numeric columns.

The author's SAS program was used to document two non-obvious conventions: full-time percentage = EMPFT / FTE, and wage-equality indicators use all stores as the denominator, including stores with missing wages as non-reporters. A valid-wage-denominator sensitivity output was added so this choice is transparent. The full-time percentage label was clarified in the replication output.

The workflow identifies differences instead of forcing a match, including the NJ $5.05 wage indicator. Renovation store SHEET 65 explains one potential count difference, but the original paper's coding choice is not established. This is recorded as a hypothesis, not a verified cause. Student review of formulas, source table and interpretation remains required.

## 2026-10-05: complete Table 2 numeric audit

Compared all 40 published means, 29 printed standard errors and 19 printed t statistics. At the paper's precision 82/88 match. One mean, one SE and four t statistics differ. Tested pooled-variance and ddof=0 variants without replacing the baseline. A diagnostic change to the target-wage indicator for renovation store 65 matches the published 3e mean and SE but gives t=36.0, not the paper's 36.1. AI's first draft incorrectly anticipated that all three would match; the executed output revealed the mistake and the report was corrected before delivery. This scenario remains unverified as an explanation of the original authors' coding.

## 2026-10-05: Figure 1 reconstruction

AI wrote and ran a matplotlib workflow from the unchanged course CSV. Wage-bin edges (10 cents from 4.20) and pooling of values >=5.50 are transparent reconstruction choices inferred from the original axis, not verified original code. Missing wages are excluded within state/wave; all four distributions sum to 100%. Independent integer-cent interval counting verifies counts and boundary placement. Sample sizes are 314/76 before and 318/71 after (NJ/PA). The after-policy NJ [5.00,5.10) bin is 284/318 = 89.31%, distinct from Table 2's exact-wage indicator and all-store denominator.

Visual review identified overlapping legend/tick labels in the first image; margins and panel spacing were corrected. Exact original bar percentages are unavailable in the paper and have not been certified as matching. No data values were changed to mimic the image.

## 2026-10-05: Table 3

AI transcribed all 40 estimates and 40 SEs from a rendered view of Table 3, implemented its five sample definitions/rows and eight columns, and preserved wage-group missingness. Tests check the published group totals (101/140/73 in NJ), closure counts, unbalanced-change estimates against stacked OLS with store-level covariance, and balanced DID against OLS with HC2 SEs. At printed precision, 66/80 cells match; all 14 differences remain reported. Eight mismatches concern row-3 SEs. The paper and supplied SAS do not establish their exact algorithm; the implemented overlap-aware influence-function method is explicitly identified as a reconstruction choice, not the authors' verified method.

Correction to earlier teaching: AI previously explained 2.76 as a consequence of using unrounded values. The actual public CSV yields an unbalanced DID of 2.753605783, rounding to 2.75. That earlier explanation was unsupported and was corrected in the report and conversation. The reason for the original 2.76 remains unresolved. Balanced and temporary-closure DID estimates round to 2.75 and 2.51 as in the paper.

## 2026-10-05 Table 4

AI constructed the common sample from valid employment changes and two valid wages, with the author-code permanent-closure exception: 357 stores (NJ290/PA67), six closed stores retained. Classical OLS and joint control F tests were independently checked via QR, mean contrasts, and Wald equivalence. All first-four-model regression cells match; 16/18 total match under paper-note controls. The fifth model includes ownership per the paper note (11.98/7.42), while check.sas omits it (11.91/7.39). Author-code residual SE8.74 differs from printed8.75. Both specifications exported separately; no selective mixing or raw data alteration. Outcome mean -.237535 rounds -.238, differing from printed -.237; explicitly recorded. No causal identification claim follows from computational checks.

## 2026-10-05 Ownership extension A

User selected ownership heterogeneity. AI implemented a model plan before inspecting extension outputs: primary NJ-by-ownership model with brand controls on the common357-store sample; unadjusted, GAP, GAP plus regions, and384-store sensitivity models fully exported. HC3 covariance independently checked through QR; unadjusted contrasts checked against group DIDs and balanced long-panel triple interaction. Primary difference -0.942367, SE2.640722, approximate p=.721412; no model interaction is significant at5%. No specification search for significance or raw changes. Plots visually checked. Report distinguishes company ownership indicator from unobserved franchise contract details, exploratory two-state inference from definitive policy inference, and insufficient evidence from equality. Student has run Table4 successfully; extension awaits student run and explanation.

## 2026-10-05 Empirical report draft

AI read the supplied assignment brief, assembled a12-page English report and Chinese reading guide, and generated tables from audited numeric outputs. Student has now run all core and extension stages. Report documents all remaining differences, approximate two-state inference, and insufficient ownership evidence without claiming equivalence. Further check recorded author-SAS fifth-model controls p=.307491 versus printed .40; coefficient/SE matching does not recreate the whole column. Default DOCX renderer failed because LibreOffice was absent. Installed Word exported the draft in an isolated hidden instance; Poppler rendered every page for visual inspection. Title border, Table2SE precision and an ambiguous Table3 sentence were corrected and the revised12 pages checked. Eight unchanged page images are byte-identical to the previously inspected version. No personal identity or completed GitHub history invented.

## 2026-10-05 Unified workflow and clean reproduction

User requested one-command execution and a clean-directory check. AI added run_all.py with dependency/input preflight, stop-on-failure, regenerated-file checks, input checksum preservation and local logs/manifests. A new directory with spaces and a newvenv contained only code and the course CSV, no pre-generated outputs or author archive. requirements.txt installed fresh dependencies; all four modules loaded from the newvenv and pip check passed. All5 stages regenerated39 analysis files. All22CSV files compared with prior audited outputs at rtol1e-9/atol1e-10; plots visually inspected. Missing input correctly returned failure and no stages ran. Installed versions frozen in requirements-lock.txt. This is clean environment testing on the same Windows host, not another machine or all platforms. No claim of exact publication agreement or automatic Word report regeneration. Report workflow paragraph awaits final revision.

## 2026-10-05 Reusable AI skill

At the student request, AI used the skill-creator instructions and current official Codex skill documentation to create minimum-wage-replication. It routes full-run versus explanation-only requests, resolves user paths, reuses existing code, verifies current recorded hashes and grounds explanations in generated estimates. A standard-library read-only helper verified all39 outputs of the student current run and detected deliberately changed output and source files in an isolated fixture. Skill structure validation passed; Chinese interface metadata encoding was corrected and checked. Natural-language automatic discovery/invocation by the student is still to be confirmed. No analysis rerun, raw changes, new causal claims, Git publication or automatic report regeneration was performed for this skill creation.

## 2026-10-05 Explicit AI skill invocation

Student explicitly invoked $minimum-wage-replication with Desktop project and course CSV paths. AI read the installed skill, README, dependencies and interpretation reference; checked the existing Python3.12.3 environment; executed run_all.py successfully for all5 stages and39 outputs; and ran the installed read-only helper to verify analytical-source, output and current-input hashes. Three generated figures were visually inspected. Current estimates and publication differences were explained from generated reports. Evidence: docs/ai_skill_invocation_validation.json and results/workflow_run.json. Raw input unchanged; narrative report and GitHub not updated by this invocation.

## 2026-10-05 Local operation page

Student requested a clickable local interface. AI implemented a standard-library loopback HTTP server and Chinese browser page, reusing run_all.py and the existing skill integrity helper. No new analytical model or dependency was introduced. Browser clicks generated all39 outputs, and input/source/output hashes passed. Browser file selection copied the CSV locally under Git-ignored logs/ui_inputs; the copy matched the original. Read-only verification, output tabs and chart display were checked. API tests rejected missing paths, unauthorized mutations and private-data routes. An isolated malformed-CSV run failed before any stage and did not retain a verified result. Windows port reuse was corrected with exclusive binding; path separator comparisons were corrected. Evidence: docs/local_page_validation.json. This local UI testing does not replace the pending simulation of a teacher downloading the final GitHub project. Report and GitHub publication remain pending.

## 2026-10-05 English local interface

At the student request, AI translated all local-page labels, status messages, explanations and server errors into English, and added five English stage-note files without changing analytical outputs. Browser verification and HTTP checks confirmed English page text, notes and error messages, and integrity checks passed for the existing39 outputs. Local filesystem paths retain their actual spelling. Evidence: docs/local_page_english_validation.json.

## 2026-10-05 Download-package reviewer simulation

Student requested a simulation of teacher use after downloading. AI extracted the submitted ZIP into a new directory, set bundled results aside, created a new virtual environment and installed requirements-lock.txt. All analysis libraries loaded from that environment and pip check passed. The authorized course CSV was placed at the documented input location, automatically detected by the local page. Clicking Run all analyses generated all39 outputs; input/source/output integrity passed. All22 CSVs matched the reviewed Desktop run at rtol1e-9/atol1e-10. Three figures were visually checked; the English page showed Verified and correct result cards without console errors. README launch guidance was clarified to select .venv explicitly; an English reviewer guide was added. A test-reading encoding issue was corrected with explicit UTF-8; analysis code and data were unchanged. Evidence: docs/teacher_download_validation.json. This was the same Windows host with a fresh directory/environment, not another computer or an actual GitHub clone.


## Formal report update — 2026-10-05

AI updated the English report to reflect the completed unified runner, explicit skill invocation, English local page and fresh-directory download-package validation. The student supplied Liu Bojian and student ID 3036764602 for the cover. All 12 analytical tables and embedded figure bytes were preserved from the reviewed draft; DOCX and Markdown metadata were checked for consistency. The default document renderer lacked LibreOffice, so installed Microsoft Word exported a review PDF and Poppler generated page images. All 13 pages were individually inspected for readable text, intact tables, figures and formulas. No numerical analysis or raw data was changed. Student review, genuine Git history, GitHub publication/access and authorized teaching-team data access remain pending.


## Submission preparation and Markdown format — 2026-10-05

At the student request, AI made the existing reviewed Markdown report the primary deliverable, prepared an independent AI-use disclosure and documented restricted input access plus the four final processed datasets. Public packaging excludes local Word history, raw/store-level data, environments, logs and Git internals. Existing results were verified read-only before packaging; analyses and data were not modified. Markdown figure links and package inventory were checked. Git commits, GitHub publication and teaching-team access/transfer were not performed in this preparation step.


## GitHub publication and actual clone check — 2026-10-06

The student personally authorized Git Credential Manager. AI uploaded the verified public package to the student-owned repository using a GitHub noreply commit email. Git tracking starts with an explicit import of work completed before tracking; no prior history was invented. A subsequent real change preserves checksum bytes during checkout and documents reviewer use. Anonymous cloning succeeded with credentials and prompts disabled. A sandbox attempt could not launch the existing Microsoft Store-backed environment; running under the student account resolved it without code or data changes. The remote clone regenerated all39 outputs using the previously tested locked environment on the same Windows host; all22 CSVs matched reviewed outputs at rtol1e-9/atol1e-10 and the integrity helper passed. README, Markdown report, disclosure and checklist now reflect publication. No coursework submission message was sent and teaching-team restricted-data access is unverified.


## Final content closure — 2026-10-13

The student deferred submission-channel investigation and requested completion of project contents. The integrity helper detected a data-validation output replaced during the prior final file synchronization, making the saved run manifest stale. AI reran all five stages without altering code or input; all39 outputs and hashes passed, and all22 CSVs matched the earlier remote-clone run within the documented tolerances. Historical author-data comparison evidence was retained separately. Four final processed datasets were packaged locally for restricted teaching-team delivery, with row counts and SHA-256 checks; this archive was not uploaded publicly. Final content checks are recorded in docs/final_content_validation.json. Student final review and formal submission remain pending. Latest protected course notices have not been revalidated.
