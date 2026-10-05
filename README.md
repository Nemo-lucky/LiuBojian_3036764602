# ECO6067 Minimum Wage Replication and Ownership Extension

This project reconstructs Tables 2–4 and Figure 1 of Card and Krueger (1994), then tests whether company-owned and non-company-owned restaurants respond differently. All five stages have been computed, validated and run by the student. The unified workflow also passed a fresh-directory, fresh-virtual-environment validation. The English report has been updated with completed workflow, skill, local-page and download-simulation evidence, and the supplied student details. Student review, real Git history, GitHub access and final submission checks are still pending.

## Review the submission

- [Empirical report (Markdown)](report/ECO6067_Empirical_Report.md)
- [AI-use disclosure](AI_USE_DISCLOSURE.md)
- [Data access and processed-data delivery](DATA_ACCESS.md)
- [Submission checklist](SUBMISSION_CHECKLIST.md)
- [English local-page guide](LOCAL_PAGE.md)

The report is now maintained in Markdown. Historical Word drafts are excluded from the public package. GitHub displays the report, tables and linked figures without Word.

## Reproduce all analytical results

From the project directory, using Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe run_all.py --data "01_DID\data\public.csv"
```

No activation or execution-policy change is required. `requirements-lock.txt` pins the exact versions tested in the clean validation. `requirements.txt` provides broader supported version ranges. Python 3.10 or later is required; the locked environment was tested on the specific Python and Windows versions in `docs/clean_reproduction_validation.json`, not on every platform.

For the student's current desktop layout, from `01_DID/Table2_Python`:

```powershell
python run_all.py --data "..\data\public.csv"
```

If dependencies are unavailable, first run `python -m pip install -r requirements.txt` with the same interpreter. The workflow checks the CSV and dependencies, runs five stages, verifies all 39 declared analytical files were regenerated, and confirms that the raw CSV checksum is unchanged. It stops at the first failure and records a failed status rather than reusing a prior success.

## Required input and access

Obtain the course Package 01 through authorized ECO6067 access and preserve its numbered folder and CSV filename. Within a portable project, the input layout is:

```text
project/
  run_all.py
  requirements.txt
  requirements-lock.txt
  src/
  01_DID/
    data/
      public.csv
```

The input is 410 restaurants with 46 columns. No edits to data or code are needed. An explicit `--data` path can point to the course CSV elsewhere; relative arguments are interpreted from the terminal's current folder. Without `--data`, the runner first looks for `01_DID/data/public.csv` inside the project, then for `../data/public.csv` in the existing desktop layout.

The main workflow needs neither an author archive nor internet after package installation. The course CSV was independently compared with the author-hosted archive, and all numeric values and missing positions match. The optional author-source comparison runs if `data/raw/author/public.dat` and `codebook` are present; otherwise it is explicitly skipped.

## Output locations

- `results/`: Tables 2–4, Figure 1 PNG/SVG, ownership results and figures, complete numeric outputs, original-paper audits and validation files.
- `results/workflow_run.json`: current run environment, input/source/output SHA-256 hashes and stage status.
- `results/workflow_summary.md`: short current completion status.
- `logs/workflow.log`: detailed local execution output, ignored by Git.
- `data/processed/`: four generated store-level analysis CSVs, ignored by Git.
- `docs/clean_reproduction_validation.json`: independent clean-run evidence and comparisons.
- `docs/干净目录复现检查.md`: Chinese clean-validation explanation.
- `docs/REUSABLE_WORKFLOW.md`: reusable workflow contract, stage sequence and interpretation rules.
- `report/`: final English Markdown report and Chinese reading guide; prior Word files are local history.

`results/clean_workflow_run.json` and `clean_workflow_summary.md` are retained evidence from the isolated clean project, not a checksum certificate for the current directory's outputs. Runtime JSON/log files may include local paths and timestamps. Graphic bytes can differ across library versions while underlying counts and estimates remain the same.

## Validation results and limits

The clean run used only copied code and the unmodified course CSV, with no previous outputs, processed data or author archive. All four analysis libraries loaded from its new .venv, and pip reported no dependency conflicts. It generated 39 analytical files plus two workflow-state files. All 22 CSVs matched the audited project with numeric tolerance rtol1e-9/atol1e-10; the three charts were visually reviewed. Missing input produced a nonzero exit and a failed manifest. Full tested versions and source hashes are recorded in the validation JSON.

The original-paper cell audits remain Table 2 82/88, Table 3 66/80 and Table 4 16/18. Figure 1's exact original bar percentages are unverified. Table 3's unbalanced SE is a transparent reconstruction. Table 4's fifth paper-note model includes ownership, while the author SAS model omits it; both are reported separately. The ownership interaction is approximately −0.942 FTE (HC3 SE 2.641, approximate p=.721), providing insufficient evidence of different responses, not evidence of equality. Workflow success does not establish causal identification or perfect agreement with publication.

## Individual stages

```powershell
python run_table2.py --data "01_DID\data\public.csv"
python run_figure1.py --data "01_DID\data\public.csv"
python run_table3.py --data "01_DID\data\public.csv"
python run_table4.py --data "01_DID\data\public.csv"
python run_extension.py --data "01_DID\data\public.csv"
```

In the desktop copy replace the data argument with `..\data\public.csv`. Separate Chinese guides remain available. These entry points and `run_all.py` use the same stage implementations.

## Sources and data restrictions

Card, D., and Krueger, A. B. (1994), American Economic Review 84(4),772–793. Paper: https://davidcard.berkeley.edu/papers/njmin-aer.pdf

Independent author-source check: https://davidcard.berkeley.edu/data_sets.html and https://davidcard.berkeley.edu/data_sets/njmin.zip. `docs/data_provenance.json` records acquisition details. The supplied course input remains the actual analytical source.

Do not publish restricted course inputs, processed store-level data or course download links. Raw sources, `01_DID/`, processed files, virtual environments and local logs are excluded from Git. Processed datasets are generated automatically; arrange permitted teaching-team access or reproduction from their authorized course input. Aggregate tables, plots, audits, code and documentation are suitable repository contents.

## Remaining delivery work

Review [the Markdown report](report/ECO6067_Empirical_Report.md) and [AI-use disclosure](AI_USE_DISCLOSURE.md), establish real Git commits and an accessible GitHub repository, and verify the teaching team's input access. Do not fabricate earlier commit history. The unified runner generates analytical reports and figures; it does not automatically update the narrative report. The report now documents completed workflow checks; update it again only if methods or delivery status change.

Deadline:18 October 2026,23:59 Hong Kong time. Table 1 is not assigned.

## AI skill

The reusable AI instructions are in `skills/minimum-wage-replication/SKILL.md`. See [Chinese installation and usage guide](AI技能_中文使用说明.md) for natural-language invocation in a local AI environment. This companion skill runs or explains the existing Python workflow and verifies source/output/input hashes; it does not rewrite the report or publish to GitHub.

## Local browser interface

After the virtual-environment setup above, run `.\.venv\Scripts\python.exe local_app.py` from the project directory, or double-click `启动本地页面.bat` on Windows (the launcher automatically prefers the project .venv). Use `python local_app.py` only when that interpreter already has the required analysis dependencies. The loopback-only page lets users choose the course CSV, run all five stages, verify existing results, preview tables/figures and download aggregate outputs. It uses only the Python standard library for the interface and the existing analysis dependencies; no AI account is required. See the [English page guide](LOCAL_PAGE.md) or [Chinese page guide](本地页面_中文使用说明.md). Keep the server terminal open.

## Reviewer download simulation

The code archive passed extraction into a fresh directory with bundled results set aside, a new project virtual environment and only the authorized CSV in the documented location. The local browser regenerated all39 outputs; all22 CSVs matched the reviewed run within rtol1e-9/atol1e-10, and three figures were inspected. See docs/teacher_download_validation.json. This tested the same Windows host with a new directory/environment, not a second computer or an actual GitHub clone. Repository access and teaching-team data access remain final delivery checks.
